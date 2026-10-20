# OCI Artifact Importer

OCI Artifact Importer handles the importing of OCI artifacts that were built outside of Konflux.

The tool handles three stages of the import pipeline:

1. **Verify** that a source image's cosign signature is valid against a known public key
2. **Mirror** the image and all its OCI referrers (signatures, attestations, SBOMs) to a destination registry
3. **Extract results** including image coordinates, SBOM, git provenance from SLSA attestations, and build index metadata

## Installation

OCI Artifact Importer requires Python 3.11+ and has no runtime dependencies beyond the standard library. It expects `cosign`, `oras`, `skopeo`, and `openssl` to be available on `PATH`.

```bash
pip install .
```

## Usage

Installs as both `oci-artifact-importer` and the shorter alias `oai` — the examples below use the full name, but either works interchangeably.

### Verify a source image

Verify the cosign signature on a digest-pinned source image and write the verification key fingerprint as a Tekton result.

```bash
oci-artifact-importer verify \
  --source-image registry.example.com/org/repo@sha256:abc123 \
  --key-file /path/to/cosign.pub \
  --results-dir /tekton/results \
  --ca-bundle /path/to/ca-bundle.crt  # optional
```

### Mirror an image

Copy the source image and all its OCI referrers to a destination registry.

```bash
oci-artifact-importer mirror \
  --source-image registry.example.com/org/repo@sha256:abc123 \
  --image dest-registry.example.com/org/repo:tag \
  --ca-bundle /path/to/ca-bundle.crt  # optional
```

### Extract results

Extract image metadata, SBOM, and git provenance from SLSA attestations, then write them as Tekton results.

```bash
oci-artifact-importer results \
  --source-image registry.example.com/org/repo@sha256:abc123 \
  --image dest-registry.example.com/org/repo:tag \
  --workdir /workspace/artifacts \
  --results-dir /tekton/results \
  --ca-bundle /path/to/ca-bundle.crt  # optional
```

Output results: `IMAGE_URL`, `IMAGE_DIGEST`, `IMAGE_REF`, `SBOM_BLOB_URL`, `CHAINS-GIT_URL`, `CHAINS-GIT_COMMIT`.

## Development

Install in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the full CI suite (tests, linting, security scan, dependency audit):

```bash
tox
```

Individual checks:

```bash
ruff check src/ tests/    # lint
ruff format src/ tests/   # format
bandit -r src/oci_artifact_importer/ -ll  # security
pip-audit                 # dependency audit
```
