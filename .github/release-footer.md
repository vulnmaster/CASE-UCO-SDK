
---

### Verification

All release artifacts include:

- **SHA256 checksums** (`SHA256SUMS.txt`)
- **SLSA build provenance** attestations via [actions/attest-build-provenance](https://github.com/actions/attest-build-provenance)
- **Python SBOM** (`sbom-python.cdx.json`) in CycloneDX format

```bash
sha256sum -c SHA256SUMS.txt
gh attestation verify <artifact> --repo vulnmaster/CASE-UCO-SDK
```

For full release notes including prior versions, see [CHANGELOG.md](https://github.com/vulnmaster/CASE-UCO-SDK/blob/main/CHANGELOG.md).
