# Forensic Analysis and Artifact Classification

> See [Recipe Index](INDEX.md) for all recipes.

Model forensic analysis workflows — malware reverse engineering, automated artifact classification, and their results with confidence scores. This covers both manual examination and automated tool-driven classification.

## Key classes

| Class | Role |
|---|---|
| `InvestigativeAction` | The analysis action performed |
| `AnalyticTool` | The analysis tool (e.g., IDA Pro, Hansken, YARA) |
| `ArtifactClassificationResultFacet` | Classification results with confidence |
| `ArtifactClassification` | A single class label + confidence score |
| `ProvenanceRecord` | Links the analysis to its inputs and outputs |
| `ObservableObject` | The artifact being analyzed |

## Two patterns

**Manual analysis** (e.g., malware reverse engineering):

```
InvestigativeAction
    ├── uco-action:performer ──▶ Identity (analyst)
    ├── uco-action:instrument ──▶ AnalyticTool (IDA Pro, Ghidra, etc.)
    ├── uco-action:object ──▶ ObservableObject (malware sample)
    └── uco-action:result ──▶ ObservableObject (analysis report/findings)
```

**Automated classification** (e.g., image categorization, malware detection):

```
InvestigativeAction
    ├── uco-action:instrument ──▶ AnalyticTool (classifier)
    ├── uco-action:object ──▶ ObservableObject (artifact to classify)
    └── uco-action:result ──▶ ObservableObject + ArtifactClassificationResultFacet
                        └── uco-analysis:classification ──▶ ArtifactClassification
                                                 ├── class_ = ["label"]
                                                 └── classification_confidence = 0.95
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.tool import AnalyticTool
from case_uco.uco.observable import ObservableObject, FileFacet, ContentDataFacet
from case_uco.uco.analysis import ArtifactClassificationResultFacet, ArtifactClassification
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# Analyst
analyst = graph.create(Identity, name="...")  # from source

# Analysis tool
tool = graph.create(AnalyticTool,
    name="...",       # e.g. "IDA Pro", "Hansken", "YARA" — from source
    version="...",    # from source
    tool_type="...",  # e.g. "Reverse Engineering", "Classifier"
)

# Artifact under analysis
artifact = graph.create(ObservableObject, name="...",
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"],
            hash_value="...",  # from source
        )]),
    ],
)

# --- Manual analysis pattern ---
manual_analysis = graph.create(InvestigativeAction,
    name="...",  # e.g. "Malware reverse engineering" — from source
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=analyst,
    instrument=[tool],
    object=[artifact],
)

# --- Automated classification pattern ---
classification_result = graph.create(ObservableObject, name="...",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[
            ArtifactClassification(
                class_=["..."],                  # label from classifier
                classification_confidence=...,   # 0.0-1.0 from source
            ),
        ],
    )],
)

auto_analysis = graph.create(InvestigativeAction,
    name="...",  # e.g. "Automated image classification" — from source
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    instrument=[tool],
    object=[artifact],
    result=[classification_result],
)

# Provenance
provenance = graph.create(ProvenanceRecord,
    name="...",
    description=["..."],
    object=[artifact, classification_result, manual_analysis, auto_analysis],
)

graph.write("analysis.jsonld")
```

</details>

## Anti-patterns

- **JSON blobs in description fields.** Do not serialize structured data (model parameters, endpoint names, result metadata) into `uco-core:description` as a JSON string. Express each fact as a first-class property or facet. If you need structured tool parameters, use `ConfiguredTool`.
- **Using ArtifactClassification for tool identity.** `ArtifactClassification.class_` should describe *what the artifact is* (content category, triage label, detection result), not *which tool or endpoint processed it*. Keep tool/endpoint identity on the `AnalyticTool` or `InvestigativeAction`.
- **Missing input/output links.** Always use `object` for inputs and `result` for outputs on `InvestigativeAction`. Without these, the provenance chain is broken.
- **Generic File for known media types.** Use `RasterPicture` for image files (`.jpg`, `.png`, `.bmp`) instead of `File` or `ObservableObject`. See the [EXIF and Image Metadata](exif-data.md) recipe.

## Notes

- `ArtifactClassification.class_` is `list[str]` (note the trailing underscore — `class` is a Python reserved word). It requires at least one value.
- `classification_confidence` is `Optional[float]` in the range 0.0 to 1.0.
- For multi-label classification, add multiple `ArtifactClassification` entries to the `classification` list.
- `AnalyticTool` (subclass of `Tool`) is used for analysis tools. Use `tool_type` to distinguish categories (e.g., "Reverse Engineering", "Classifier", "Malware Scanner").
- For tool configurations (specific command-line flags, rulesets, etc.), see the `ConfiguredTool` class in the SDK which wraps a base tool with configuration entries.
- For AI/ML inference pipelines with ranked results, multi-step processing, or semantic search, see the [AI/ML Analysis Pipelines](ai-analysis-pipeline.md) recipe.
