# Compute and Platform Support

This document is the SDK source of truth for deployment sizing and CPU
architecture support. Downstream deployment catalogs should copy these values
rather than infer requirements from developer CI runners.

## Compute baseline

| Resource | Minimum | Recommended |
| --- | ---: | ---: |
| CPU | 4 cores | 8 or more cores for concurrent generation and validation |
| RAM | 8 GB | 16 GB; 32–64 GB for large in-memory graphs |
| GPU | Not required | Not required |
| Application/database disk | 20 GB | 40 GB or more for build caches and generated artifacts |
| Evidence storage | Not included | Size separately for retention and replication requirements |

The application/database figure covers the SDK, language toolchains, package
caches, temporary validation data, and generated artifacts. It does **not**
cover source evidence, forensic images, exports, backups, or replicas. Those
must use separately governed storage sized for the deployment's evidence
volume and retention policy.

Downstream deployment catalogs should keep their `case_uco_sdk` entry synchronized with this baseline during the same release cycle.

## CPU architecture matrix

| Package | Linux `x86_64` | Linux `aarch64` | Architecture-sensitive components |
| --- | --- | --- | --- |
| Python | Supported and CI-tested | Designed to be portable; native validation pending | The SDK wheel is pure Python. `rdflib`, `jinja2`, and SDK code are architecture-neutral; dependency wheels and `case-utils` availability must be verified on the target Python version. |
| C# | Supported and CI-tested on .NET 8 | Supported by the .NET 8 runtime; native validation pending | `CaseUco` is managed IL and ships no native library. Install the matching .NET `linux-arm64` runtime/SDK. |
| Java | Supported and CI-tested on JDK 11+ | Supported by a matching aarch64 JDK; native validation pending | The SDK JAR is architecture-neutral and contains no JNI library. |
| Rust | Supported and CI-tested | Source-compatible; native validation pending | Rust produces a native binary/library for the selected target. Build on aarch64 or use the `aarch64-unknown-linux-gnu` target with an appropriate linker. |

The repository does not currently publish container images and has no CUDA or
GPU runtime dependency. NVIDIA hardware does not accelerate ontology loading,
code generation, or SHACL validation unless a downstream application adds its
own GPU workload.

Native Linux `aarch64` testing on NVIDIA Spark remains pending. Record successful native validation in the deployment matrix before claiming support.

## Native validation checklist

Run from a recursive clone on the target host:

```bash
uname -m
python3 --version
dotnet --info
java -version
rustc -vV
make init
make generate
make test
make lint
make smoke
```

Record the host architecture, operating-system release, toolchain versions,
commands, test counts, failures, and any packages compiled from source. The
validation record must not contain case data or evidence; use only repository
T0 synthetic fixtures.
