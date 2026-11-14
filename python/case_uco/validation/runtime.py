"""Resolve CASE Utilities in the interpreter running the SDK."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
from dataclasses import dataclass

VALIDATOR_MODULE = "case_utils.case_validate"
_ENTRY_POINT = (
    "import sys; from case_utils.case_validate import main; "
    "sys.argv[0] = 'case_validate'; sys.exit(main())"
)


def validator_command() -> tuple[str, ...]:
    """Invoke the console entry point with the SDK interpreter, never PATH."""
    return (sys.executable, "-c", _ENTRY_POINT)


# Read the choices used by the validator's argparse parser in the child
# interpreter. A package version alone cannot establish ontology support.
_PROBE = """
import importlib.metadata
import json
import sys
try:
    import case_utils.case_validate as validator
except Exception:
    print(json.dumps({"error_code": "validator_unavailable"}))
    sys.exit(0)
print(json.dumps({
    "version": importlib.metadata.version("case-utils"),
    "built_versions": list(validator.built_version_choices_list),
}))
"""


@dataclass(frozen=True)
class ValidatorRuntime:
    command: tuple[str, ...]
    version: str


class ValidatorError(RuntimeError):
    def __init__(self, code: str, message: str, *, version: str | None = None):
        super().__init__(message)
        self.code = code
        self.version = version


def validator_available() -> bool:
    """Whether this interpreter can import the validator, ignoring PATH."""
    try:
        importlib.import_module(VALIDATOR_MODULE)
    except Exception:
        return False
    return True


def prepare_validator(built_version: str | None = None) -> ValidatorRuntime:
    """Check supported ontology versions without loading or validating a graph."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", _PROBE],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode != 0:
            raise ValueError("validator probe failed")
        info = json.loads(result.stdout)
        if info.get("error_code") == "validator_unavailable":
            raise ValidatorError(
                "validator_unavailable",
                "The CASE validator could not be imported in the SDK interpreter.",
            )
        version = info["version"]
        choices = info["built_versions"]
        if not isinstance(version, str) or not isinstance(choices, list):
            raise ValueError("invalid validator probe response")
    except (
        OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError, AttributeError
    ) as exc:
        raise ValidatorError(
            "validator_precheck_failed",
            "The CASE validator version precheck could not complete in the SDK interpreter.",
        ) from exc
    if built_version is not None and built_version not in choices:
        raise ValidatorError(
            "validator_version_mismatch",
            f"CASE validator {version} in the SDK interpreter does not support "
            f"--built-version {built_version}.",
            version=version,
        )
    return ValidatorRuntime(validator_command(), version)


def validator_error_code(returncode: int, stderr: str) -> str | None:
    """Separate argument/runtime failures from SHACL nonconformance."""
    diagnostic = stderr.lower()
    argparse_error = "invalid choice" in diagnostic or "usage:" in diagnostic
    if returncode == 2 or argparse_error:
        if "--built-version" in diagnostic and (
            "invalid choice" in diagnostic or "unrecognized arguments" in diagnostic
        ):
            return "validator_version_mismatch"
        return "validator_execution_failed"
    if returncode != 0 and any(
        marker in diagnostic
        for marker in ("no module named", "importerror:")
    ):
        return "validator_unavailable"
    return None


def validator_error_message(code: str, built_version: str | None) -> str:
    if code == "validator_version_mismatch":
        return f"The CASE validator rejected --built-version {built_version}; SHACL validation did not run."
    if code == "validator_unavailable":
        return "The CASE validator could not be imported in the SDK interpreter; SHACL validation did not run."
    return "The CASE validator could not run in the SDK interpreter; SHACL validation did not complete."


def main() -> int:
    """Forward CLI arguments through the same interpreter and version checks."""
    args = sys.argv[1:]
    built_version = None
    for index, arg in enumerate(args):
        if arg == "--built-version" and index + 1 < len(args):
            built_version = args[index + 1]
        elif arg.startswith("--built-version="):
            built_version = arg.partition("=")[2]
    try:
        runtime = prepare_validator(built_version)
        result = subprocess.run(
            [*runtime.command, *args], capture_output=True, text=True, check=False
        )
    except ValidatorError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 2
    except OSError:
        print("validator_execution_failed: CASE validator could not run", file=sys.stderr)
        return 2
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    code = validator_error_code(result.returncode, result.stderr)
    if code:
        print(f"{code}: {validator_error_message(code, built_version)}", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
