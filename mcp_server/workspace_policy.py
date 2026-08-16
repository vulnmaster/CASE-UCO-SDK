"""Filesystem trust boundary for MCP tools that accept local paths.

``process_document_file``, the Apple package classifier/builder, and
``validate_graph`` accept caller-controlled paths. In an agent-connected
deployment the MCP server should not be an
arbitrary file read/write primitive, so deployments can configure a
workspace policy through environment variables:

- ``CASE_UCO_MCP_READ_ROOTS`` — path-separator-delimited directories that
  source/graph files must live under (evidence roots, read-only).
- ``CASE_UCO_MCP_WRITE_ROOTS`` — path-separator-delimited directories that
  output and progress files must live under (the case workspace).
- ``CASE_UCO_MCP_ALLOW_OVERWRITE`` — set to ``1``/``true`` to allow output
  paths to overwrite existing files. Under an active policy the default is
  non-overwrite.

Both variables accept ``os.pathsep`` (``:`` on POSIX, ``;`` on Windows) or
comma-separated lists. When neither variable is set, no policy is active and
behavior is unchanged (backward compatible); ``mcp_server/README.md``
documents the recommended secure deployment configuration.

Secure production mode (issue #57)
----------------------------------

``CASE_UCO_MCP_SECURE_MODE=1`` — or a production deployment profile in
``CASE_UCO_MCP_PROFILE`` — turns the opt-in policy into an enforced one:

- Server startup fails (``validate_security_configuration``) unless at least
  one read root **and** one write root are configured, every root is an
  existing absolute directory, and no root is dangerously broad (a
  filesystem/drive root or a home directory) unless
  ``CASE_UCO_MCP_ALLOW_BROAD_ROOTS=1`` explicitly acknowledges it.
- Evidence (read) roots must not be writable: a write root that equals or
  sits inside a read root is a configuration error.
- Partially configured policies no longer fall back to unrestricted
  behavior: with secure mode active, a missing read-roots or write-roots
  configuration is a typed refusal (``read_roots_unconfigured`` /
  ``write_roots_unconfigured``) instead of an implicit allow.

Deployment profiles (``CASE_UCO_MCP_PROFILE``):

- ``development`` (default) — backward-compatible local development; the
  policy is opt-in and knowledge promotion is unrestricted.
- ``offline-investigation`` — secure mode; knowledge promotion disabled
  (bounded case workspace, consume-only).
- ``production-authoring`` — secure mode; candidate knowledge may be
  created but not promoted.
- ``production-review`` — secure mode; promotion allowed and a reviewer
  identity is required (`knowledge_lifecycle` enforces it).

``security_profile()`` returns the machine-readable capability summary
(profile, active restrictions, root counts — never full paths).

Containment is decided on fully resolved paths (``Path.resolve()`` follows
symlinks), so ``..`` traversal and symlink escapes out of a configured root
are rejected with typed errors: ``source_outside_read_roots``,
``output_outside_write_roots``, ``progress_outside_write_roots``,
``output_exists``, ``source_output_conflict``. Error messages never echo the
offending path back to the caller.
"""

from __future__ import annotations

import os
from pathlib import Path

READ_ROOTS_ENV = "CASE_UCO_MCP_READ_ROOTS"
WRITE_ROOTS_ENV = "CASE_UCO_MCP_WRITE_ROOTS"
ALLOW_OVERWRITE_ENV = "CASE_UCO_MCP_ALLOW_OVERWRITE"
SECURE_MODE_ENV = "CASE_UCO_MCP_SECURE_MODE"
PROFILE_ENV = "CASE_UCO_MCP_PROFILE"
ALLOW_BROAD_ROOTS_ENV = "CASE_UCO_MCP_ALLOW_BROAD_ROOTS"

PROFILE_DEVELOPMENT = "development"
PROFILE_OFFLINE_INVESTIGATION = "offline-investigation"
PROFILE_PRODUCTION_AUTHORING = "production-authoring"
PROFILE_PRODUCTION_REVIEW = "production-review"
VALID_PROFILES = frozenset({
    PROFILE_DEVELOPMENT,
    PROFILE_OFFLINE_INVESTIGATION,
    PROFILE_PRODUCTION_AUTHORING,
    PROFILE_PRODUCTION_REVIEW,
})
# Profiles that imply secure (fail-closed) mode.
SECURE_PROFILES = frozenset({
    PROFILE_OFFLINE_INVESTIGATION,
    PROFILE_PRODUCTION_AUTHORING,
    PROFILE_PRODUCTION_REVIEW,
})


def _parse_roots(raw: str | None) -> tuple[Path, ...]:
    if not raw:
        return ()
    parts: list[str] = []
    for chunk in raw.split(os.pathsep):
        parts.extend(chunk.split(","))
    roots: list[Path] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        roots.append(Path(part).expanduser().resolve())
    return tuple(roots)


def read_roots() -> tuple[Path, ...]:
    return _parse_roots(os.environ.get(READ_ROOTS_ENV))


def write_roots() -> tuple[Path, ...]:
    return _parse_roots(os.environ.get(WRITE_ROOTS_ENV))


def overwrite_allowed() -> bool:
    return os.environ.get(ALLOW_OVERWRITE_ENV, "").strip().lower() in {"1", "true", "yes"}


def policy_active() -> bool:
    """True when a deployment has configured any filesystem restriction."""

    return bool(read_roots() or write_roots())


def _flag_set(env_name: str) -> bool:
    return os.environ.get(env_name, "").strip().lower() in {"1", "true", "yes"}


def deployment_profile() -> str:
    """Active deployment profile; unknown values are a typed error."""

    raw = os.environ.get(PROFILE_ENV, "").strip().lower()
    if not raw:
        return PROFILE_DEVELOPMENT
    if raw not in VALID_PROFILES:
        raise ValueError("unknown_deployment_profile")
    return raw


def secure_mode_active() -> bool:
    """Secure mode is explicit (env flag) or implied by a production profile.

    An unrecognized profile value counts as secure (fail closed): startup
    validation then refuses with ``unknown_deployment_profile`` rather than
    silently running in development mode.
    """

    if _flag_set(SECURE_MODE_ENV):
        return True
    try:
        return deployment_profile() in SECURE_PROFILES
    except ValueError:
        return True


def promotion_allowed() -> tuple[bool, str]:
    """Whether the active profile permits knowledge-lifecycle promotion.

    Returns ``(allowed, requirement)`` where ``requirement`` is
    ``"reviewer_identity"`` when promotion additionally requires a
    non-empty reviewer identity (production-review), or ``""``.
    """

    try:
        profile = deployment_profile()
    except ValueError:
        return False, ""  # unknown profile: fail closed
    if profile == PROFILE_DEVELOPMENT:
        return True, ""
    if profile == PROFILE_PRODUCTION_REVIEW:
        return True, "reviewer_identity"
    # offline-investigation and production-authoring consume or author
    # candidates; promotion authority lives with a review deployment.
    return False, ""


def _broad(root: Path) -> bool:
    """Filesystem/drive roots and the home directory itself are too broad."""

    if str(root) == root.anchor:  # "/" on POSIX, "C:\\" on Windows
        return True
    home = Path.home().resolve()
    return root == home


def validate_security_configuration() -> list[str]:
    """Validate the workspace policy for secure mode; return error codes.

    Empty list == configuration acceptable. Development mode (no secure
    flag, no production profile) never fails — the policy stays opt-in.
    Secure mode fails closed on: missing read or write roots, roots that do
    not exist or are not directories, dangerously broad roots (unless
    ``CASE_UCO_MCP_ALLOW_BROAD_ROOTS`` acknowledges them), and evidence
    (read) roots that are writable through a configured write root.
    """

    errors: list[str] = []
    try:
        profile = deployment_profile()
    except ValueError:
        return ["unknown_deployment_profile"]
    if not secure_mode_active():
        return errors

    reads = read_roots()
    writes = write_roots()
    if not reads:
        errors.append("read_roots_unconfigured")
    if not writes:
        errors.append("write_roots_unconfigured")

    allow_broad = _flag_set(ALLOW_BROAD_ROOTS_ENV)
    for kind, roots in (("read", reads), ("write", writes)):
        for root in roots:
            if not root.is_dir():
                errors.append(f"{kind}_root_not_directory")
                continue
            if not allow_broad and _broad(root):
                errors.append(f"{kind}_root_too_broad")

    # Evidence roots must not be writable by document-processing tools:
    # a write root inside (or equal to) a read root defeats read-only
    # evidence handling. Acknowledged broad read roots are exempt — every
    # path is inside "/", and the operator explicitly accepted that.
    for write_root in writes:
        for read_root in reads:
            if allow_broad and _broad(read_root):
                continue
            if write_root == read_root or read_root in write_root.parents:
                errors.append("write_root_inside_read_root")

    if profile == PROFILE_PRODUCTION_REVIEW and not reads:
        # Already covered by read_roots_unconfigured; nothing extra.
        pass
    return sorted(set(errors))


def security_profile() -> dict:
    """Bounded, machine-readable capability summary (no full paths)."""

    try:
        profile = deployment_profile()
        profile_error = ""
    except ValueError:
        profile = "invalid"
        profile_error = "unknown_deployment_profile"
    allowed, requirement = (False, "") if profile == "invalid" else promotion_allowed()
    payload = {
        "profile": profile,
        "secure_mode": False if profile == "invalid" else secure_mode_active(),
        "policy_active": policy_active(),
        "read_root_count": len(read_roots()),
        "write_root_count": len(write_roots()),
        "overwrite_allowed": overwrite_allowed(),
        "promotion_allowed": allowed,
        "promotion_requirement": requirement,
        "configuration_errors": validate_security_configuration() if not profile_error else [profile_error],
    }
    return payload


def _is_contained(path: Path, roots: tuple[Path, ...]) -> bool:
    for root in roots:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def check_read_path(path: str | Path, *, include_write_roots: bool = False) -> Path:
    """Resolve a caller-supplied read path and enforce the read policy.

    Returns the fully resolved path. Raises ``ValueError`` with a typed,
    non-sensitive message when the resolved path (after following symlinks)
    escapes every configured read root. With ``include_write_roots`` the
    write workspace also counts as readable — used by ``validate_graph``,
    which typically reads graphs the server itself just produced.
    """

    resolved = Path(path).expanduser().resolve()
    roots = read_roots()
    if not roots:
        if secure_mode_active():
            # Fail closed: secure mode never falls back to unrestricted reads.
            raise ValueError("read_roots_unconfigured")
        # Development mode: read containment is enforced only when read roots
        # are configured; a write-roots-only policy constrains writes only.
        return resolved
    if include_write_roots:
        roots = roots + write_roots()
    if not _is_contained(resolved, roots):
        raise ValueError("source_outside_read_roots")
    return resolved


def check_write_path(
    path: str | Path,
    *,
    error_code: str = "output_outside_write_roots",
    enforce_no_overwrite: bool = True,
) -> Path:
    """Resolve a caller-supplied write path and enforce the write policy.

    Under an active policy, the resolved path must be contained in a write
    root and (unless ``CASE_UCO_MCP_ALLOW_OVERWRITE`` is set) must not
    already exist. ``Path.resolve()`` on a not-yet-existing file resolves
    symlinks in every existing ancestor, so symlinked directories that point
    outside the workspace are rejected.
    """

    resolved = Path(path).expanduser().resolve()
    roots = write_roots()
    if not roots:
        if secure_mode_active():
            # Fail closed: secure mode never falls back to unrestricted writes.
            raise ValueError("write_roots_unconfigured")
        return resolved
    if not _is_contained(resolved, roots):
        raise ValueError(error_code)
    if enforce_no_overwrite and resolved.exists() and not overwrite_allowed():
        raise ValueError("output_exists")
    return resolved


def check_distinct(source: Path, output: Path) -> None:
    """Reject source and destination resolving to the same file."""

    if source == output:
        raise ValueError("source_output_conflict")
