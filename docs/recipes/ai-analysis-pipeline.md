# AI/ML Analysis Pipelines

> See [Recipe Index](INDEX.md) for all recipes.

Model AI and machine-learning analysis workflows — image search, object detection, content classification, embedding-based retrieval, and multi-step inference pipelines — with explicit inputs, outputs, per-result scoring, and full provenance.

This recipe addresses seven areas that AI-generated CASE graphs commonly get wrong:

1. [Structured facts vs. JSON blobs](#anti-pattern-json-blobs-in-descriptions)
2. [Explicit input/output relationships](#explicit-inputoutput-relationships)
3. [Per-result ranking and scoring](#per-result-ranking-and-scoring)
4. [Multi-step pipeline modeling](#multi-step-pipelines)
5. [Correct use of ArtifactClassification](#artifact-classification-semantics)
6. [Rich file-level evidence metadata](#rich-evidence-metadata)
7. [RasterPicture for image files](#use-rasterpicture-for-images)

## Key classes

| Class | Role |
|---|---|
| `InvestigativeAction` | Each step in the analysis pipeline |
| `AnalyticTool` | The AI/ML tool or model used |
| `RasterPicture` | Image files (subclass of `File` — more precise than generic `File`) |
| `RasterPictureFacet` | Image dimensions, compression, picture type |
| `FileFacet` | Filename, path, size, timestamps |
| `ContentDataFacet` | Hash, MIME type, byte size |
| `ArtifactClassificationResultFacet` | True classification labels on artifacts |
| `ArtifactClassification` | A single label + confidence score |
| `Relationship` | Registered `Related_To` for selection/transformation provenance, `Contained_Within` for containment; action inputs/outputs use direct properties |
| `ProvenanceRecord` | Groups the pipeline and its artifacts |
| `ConfidenceFacet` | Numeric confidence on any assertion |

## Pattern

```
InvestigativeAction (step 1: preprocessing)
    ├── uco-action:instrument ──▶ AnalyticTool (e.g., age-gender model)
    ├── uco-action:object ──▶ [input RasterPicture files]
    ├── uco-action:result ──▶ [intermediate output objects]
    ├── uco-action:startTime / uco-action:endTime
    └── uco-action:actionStatus

InvestigativeAction (step 2: search/inference)
    ├── uco-action:instrument ──▶ AnalyticTool (e.g., CLIP search)
    ├── uco-action:object ──▶ [intermediate objects + query parameters]
    ├── uco-action:result ──▶ [ranked result objects with scores]
    ├── uco-action:startTime / uco-action:endTime
    └── uco-action:actionStatus

Each result RasterPicture:
    ├── uco-core:hasFacet ──▶ FileFacet + ContentDataFacet + RasterPictureFacet
    └── ConfidenceFacet (similarity score)

Relationship (source=result, target=input_dir, kind="Related_To", description="selected from target collection")

ProvenanceRecord ──▶ groups everything
```

## Anti-pattern: JSON blobs in descriptions

**Wrong** — hiding structured facts inside `uco-core:description` or custom extension properties as serialized JSON strings:

```python
# BAD: Structured data buried in a string
action = graph.create(InvestigativeAction,
    name="Image search",
    description=[
        '{"endpoint": "search_images", "model": "clip-vit-base", '
        '"top_k": 5, "min_similarity": 0.21, "query": "young girl"}'
    ],
)
```

**Right** — express each fact as a first-class property or facet:

```python
# GOOD: Structured data as explicit properties
action = graph.create(InvestigativeAction,
    name="Semantic image search",
    description=["CLIP-based semantic image search over input directory"],
    instrument=[search_tool],
    object=[input_dir],
    result=[result_1, result_2, result_3],
    start_time=datetime(...),
    end_time=datetime(...),
    action_status=["Success"],
)
```

Tool configuration details (model name, thresholds, query text) belong on a `ConfiguredTool` or as properties of the tool, not serialized into a description string. See the [Configured Tools](configured-tool.md) recipe.

## Explicit input/output relationships

Use `InvestigativeAction.object` for inputs and `InvestigativeAction.result` for outputs. For richer semantics, add explicit `Relationship` objects:

```python
from case_uco.uco.core import Relationship

# Link each result image back to the source directory
for result_image in result_images:
    graph.create(Relationship,
        source=[result_image],
        target=input_dir,
        kind_of_relationship="Related_To",
        description=["The source result was selected from the target collection."],
        is_directional=True,
    )
```

Relationship guidance for AI pipelines:
- Use registered `Related_To` plus a precise `description` for selection or transformation provenance not covered by a direct predicate.
- Use direct `uco-action:object` for process inputs and `uco-action:result` for outputs.
- Use registered `Contained_Within` for a file within a directory.

## Per-result ranking and scoring

Each result from a ranked search or inference should carry its own score. Use `ConfidenceFacet` for numeric confidence/similarity:

```python
from case_uco.uco.core import ConfidenceFacet

result_1 = graph.create(RasterPicture,
    name="COCO_test2014_000000581918.jpg",
    has_facet=[
        FileFacet(file_name="COCO_test2014_000000581918.jpg",
                  file_path="/path/to/inputs/COCO_test2014_000000581918.jpg",
                  size_in_bytes=245760),
        ContentDataFacet(
            hash=[Hash(hash_method="SHA256", hash_value="ab12cd34...")],
            mime_type=["image/jpeg"],
        ),
        RasterPictureFacet(
            picture_width=640, picture_height=480,
            picture_type="JPEG",
        ),
        ConfidenceFacet(confidence=0.87),  # similarity score from model
    ],
)
```

If ranking matters, model it in the `description` of each result or via an extension property. The `confidence` value on `ConfidenceFacet` carries the numeric score for queryability.

## Multi-step pipelines

When a workflow chains multiple models or processing steps, model each step as its own `InvestigativeAction` with its own instrument, inputs, outputs, and timestamps. Connect them via shared objects — step 1's `result` becomes step 2's `object`:

```python
# Step 1: Preprocessing (e.g., age-gender prediction)
preprocess_tool = graph.create(AnalyticTool,
    name="age-gender/predict",
    version="1.0",
    tool_type="Preprocessing Model",
)

step_1 = graph.create(InvestigativeAction,
    name="Age-gender preprocessing",
    description=["Run age-gender prediction on input images"],
    instrument=[preprocess_tool],
    object=input_images,          # input RasterPicture objects
    result=[intermediate_result],  # e.g., annotated embeddings
    start_time=datetime(...),
    end_time=datetime(...),
    action_status=["Success"],
)

# Step 2: Semantic search
search_tool = graph.create(AnalyticTool,
    name="image_embeddings/search_images",
    version="1.0",
    tool_type="Semantic Search Model",
)

step_2 = graph.create(InvestigativeAction,
    name="Semantic image search",
    description=["CLIP-based semantic search: query='young girl', top_k=5"],
    instrument=[search_tool],
    object=[intermediate_result],    # output of step 1
    result=ranked_result_images,     # RasterPicture objects with scores
    start_time=datetime(...),
    end_time=datetime(...),
    action_status=["Success"],
)
```

This lets a consumer trace the full dependency chain: which preprocessing fed into which search, with independent timestamps, tools, and statuses per step.

## Artifact classification semantics

`ArtifactClassification` should describe *what the artifact is*, not *which tool processed it*. Common correct uses:

- Content category: `"CSAM"`, `"benign"`, `"suspicious"`
- Object detection: `"person"`, `"vehicle"`, `"weapon"`
- Triage result: `"requires_review"`, `"cleared"`

**Wrong** — using classification to store a tool endpoint or processing method:

```python
# BAD: This is tool identity, not artifact classification
ArtifactClassification(class_=["image_embeddings/search_images"])
```

**Right** — classify the actual content or forensic status:

```python
# GOOD: Actual content classification
ArtifactClassification(
    class_=["potential_match"],
    classification_confidence=0.87,
)
```

Keep tool/endpoint identity on the `AnalyticTool` or `InvestigativeAction` side.

## Rich evidence metadata

For forensic use, observable objects need more than just filename and path. Always include:

```python
image = graph.create(RasterPicture,
    has_facet=[
        FileFacet(
            file_name="photo.jpg",
            file_path="/evidence/photos/photo.jpg",
            size_in_bytes=245760,
            # Include timestamps when available from source:
            # accessed_time=datetime(...),
            # modified_time=datetime(...),
            # created_time=datetime(...),
        ),
        ContentDataFacet(
            hash=[Hash(hash_method="SHA256", hash_value="ab12cd34...")],
            mime_type=["image/jpeg"],
            size_in_bytes=245760,
        ),
        RasterPictureFacet(
            picture_width=640,
            picture_height=480,
            picture_type="JPEG",
            image_compression_method="JPEG",
        ),
    ],
)
```

Without hashes and sizes, the graph is a workflow log but not an evidentiary record.

## Use RasterPicture for images

When modeling `.jpg`, `.png`, `.bmp`, or other raster image files, use `RasterPicture` (subclass of `File`) instead of generic `File` or `ObservableObject`. Attach `RasterPictureFacet` for image-specific metadata:

```python
from case_uco.uco.observable import RasterPicture, RasterPictureFacet, FileFacet, ContentDataFacet

# GOOD: RasterPicture with RasterPictureFacet
image = graph.create(RasterPicture,
    has_facet=[
        FileFacet(file_name="photo.jpg", file_path="...", size_in_bytes=...),
        ContentDataFacet(hash=[...], mime_type=["image/jpeg"]),
        RasterPictureFacet(picture_width=1920, picture_height=1080, picture_type="JPEG"),
    ],
)

# BAD: Generic File for a known image format
# image = graph.create(File, ...)       # too generic
# image = graph.create(ObservableObject, ...)  # even more generic
```

See also the [EXIF and Image Metadata](exif-data.md) recipe for camera and EXIF modeling.

## Complete example

A two-step pipeline: age-gender preprocessing, then CLIP semantic image search returning ranked results.

<details open><summary>Python</summary>

```python
from datetime import datetime, timezone
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
from case_uco.uco.tool import AnalyticTool
from case_uco.uco.core import Relationship, ConfidenceFacet
from case_uco.uco.observable import (
    RasterPicture, Directory,
    FileFacet, ContentDataFacet, RasterPictureFacet,
)
from case_uco.uco.types import Hash

graph = CASEGraph()

# --- Tools ---
parent_tool = graph.create(AnalyticTool,
    name="RescueBox",
    version="3.0.0",
    tool_type="AI Analysis Platform",
)

preprocess_tool = graph.create(AnalyticTool,
    name="age-gender/predict",
    version="1.0",
    tool_type="Preprocessing Model",
)

search_tool = graph.create(AnalyticTool,
    name="image_embeddings/search_images",
    version="1.0",
    tool_type="Semantic Search",
)

# --- Input directory ---
input_dir = graph.create(Directory,
    has_facet=[FileFacet(
        file_name="inputs_146_25_minutes",
        file_path="/home/tester/Documents/demo1/image-summary/inputs_146_25_minutes",
        is_directory=True,
    )],
)

# --- Step 1: Preprocessing ---
step_1 = graph.create(InvestigativeAction,
    name="Age-gender preprocessing",
    description=["Run age-gender prediction model on input image set"],
    instrument=[preprocess_tool],
    performer=parent_tool,
    object=[input_dir],
    start_time=datetime(2026, 4, 1, 19, 16, 15, tzinfo=timezone.utc),
    end_time=datetime(2026, 4, 1, 19, 16, 17, tzinfo=timezone.utc),
    action_status=["Success"],
)

# --- Step 2: Semantic search ---
# Result images with per-result scoring
results_data = [
    ("COCO_test2014_000000581918.jpg", "ab12cd34...", 0.87, 1),
    ("COCO_test2014_000000581645.jpg", "ef56gh78...", 0.82, 2),
    ("COCO_test2014_000000580044.jpg", "ij90kl12...", 0.76, 3),
    ("COCO_test2014_000000580531.jpg", "mn34op56...", 0.71, 4),
    ("COCO_test2014_000000580246.jpg", "qr78st90...", 0.68, 5),
]

result_images = []
for fname, hash_val, similarity, rank in results_data:
    img = graph.create(RasterPicture,
        name=fname,
        has_facet=[
            FileFacet(
                file_name=fname,
                file_path=f"/home/tester/Documents/demo1/image-summary/inputs_146_25_minutes/{fname}",
                extension="jpg",
            ),
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value=hash_val)],
                mime_type=["image/jpeg"],
            ),
            RasterPictureFacet(picture_type="JPEG"),
            ConfidenceFacet(confidence=similarity),
        ],
    )
    result_images.append(img)

    # Link each result back to the source directory
    graph.create(Relationship,
        source=[img], target=input_dir,
        kind_of_relationship="Related_To",
        description=["The source result was selected from the target collection."],
        is_directional=True,
    )

step_2 = graph.create(InvestigativeAction,
    name="Semantic image search: query='young girl', top_k=5, model=clip-vit-base-patch32",
    description=[
        "CLIP-based semantic image search over input directory. "
        "Query: 'young girl'. Model: openai/clip-vit-base-patch32. "
        "top_k=5, min_similarity=0.21."
    ],
    instrument=[search_tool],
    performer=parent_tool,
    object=[input_dir],
    result=result_images,
    start_time=datetime(2026, 4, 1, 19, 16, 17, tzinfo=timezone.utc),
    end_time=datetime(2026, 4, 1, 19, 16, 18, tzinfo=timezone.utc),
    action_status=["Success"],
)

# --- Provenance ---
provenance = graph.create(ProvenanceRecord,
    description=["Provenance bundle for RescueBox two-step image analysis pipeline"],
    object=[step_1, step_2, input_dir] + result_images,
)

graph.write("ai-analysis-pipeline.jsonld")
```

</details>

## Notes

- **One `InvestigativeAction` per pipeline step.** Each step gets its own tool, inputs, outputs, and timestamps. This makes the dependency chain traceable.
- **`ConfidenceFacet.confidence`** is `float` in range 0.0–1.0 (required field). Attach it as a facet on the result object to carry the model's similarity or confidence score.
- **Query text and model parameters** go in the action's `name` or `description` as human-readable text, or on a `ConfiguredTool`. They are search/configuration metadata, not artifact classifications.
- **`Relationship`** requires `is_directional` (boolean, required), `source` (list, required), and `target` (required). Use `kind_of_relationship` for the semantic label.
- For EXIF data on images, combine this recipe with the [EXIF and Image Metadata](exif-data.md) recipe.
- For tool configurations (model parameters, thresholds), see [Configured Tools](configured-tool.md).
- For more on classification, see [Forensic Analysis and Classification](analysis.md).
