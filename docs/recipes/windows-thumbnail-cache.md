# Windows Thumbnail Cache (thumbcache_*.db)

> See [Recipe Index](INDEX.md) for all recipes.

Model thumbnails recovered from the Windows Explorer thumbnail cache
(`thumbcache_*.db`, stored under
`%LocalAppData%\Microsoft\Windows\Explorer\`). Each cache database is a
size-bucketed store (16 / 32 / 48 / 96 / 256 / 768 / 1280 / 1920 / 2560
pixels) of thumbnail images keyed by an 8-hex-character *ThumbnailCacheID*;
an accompanying `thumbcache_idx.db` maps each ThumbnailCacheID to its entry.
Because a thumbnail persists in the cache **after the original image file is
deleted**, the cache recovers visual evidence of images that no longer exist
on the volume — but the cache alone does **not** carry the original file
name (that resolves through the Windows Search index, `Windows.edb`, which is
frequently unavailable). This recipe models a cache database as a `File`, a
recovered thumbnail as an `ObservableObject` carrying picture, content, and
recovery facets, and the containment link between them. The derivation link
back to the now-deleted source image is a known ontology gap — see the
[change proposal](../../change_proposals/windows-thumbnail-cache-facet.md).

## When to use this recipe

- Evidence includes `thumbcache_*.db` / `thumbcache_idx.db` files, or a
  parser (Thumbcache Viewer, `thumbcache_parser`, tools that read the `CMMM`
  cache format) has extracted thumbnails from them.
- A recovered thumbnail depicts content whose **original file is no longer
  present** on the volume, and you need to record the image as evidence while
  being explicit that its name/origin could not be recovered.
- You have a ThumbnailCacheID and a size bucket but no resolved file name
  (no `Windows.edb`, no Shellbag/Recent-items correlation yet).
- Near-misses: for an EXIF-bearing image file still present on disk, use
  [exif-data.md](exif-data.md); for a thumbnail *embedded inside* a JPEG at a
  byte range (the JPEG's own APP1/thumbnail, not the OS cache), use
  [file-fragments.md](file-fragments.md); for generic carving/recovery status
  semantics, use [file-recovery.md](file-recovery.md).

## Classes and properties

| Class / property | Role |
|---|---|
| `uco-observable:File` + `uco-observable:FileFacet` | Each `thumbcache_*.db` cache database on disk (fileName, filePath, extension, sizeInBytes) |
| `uco-observable:ObservableObject` | The recovered thumbnail image; its `uco-core:name` carries the ThumbnailCacheID |
| `uco-observable:RasterPictureFacet` | Thumbnail dimensions and type (`pictureHeight`, `pictureWidth`, `pictureType`) |
| `uco-observable:ContentDataFacet` | Thumbnail bytes: `sizeInBytes`, `mimeType`, `hash` |
| `uco-observable:RecoveredObjectFacet` | `contentRecoveredStatus` / `nameRecoveredStatus` — records that the pixels were recovered but the name was not |
| `uco-types:Hash` | Integrity hash (`hashMethod` + `hashValue`) inside `ContentDataFacet` |
| `uco-observable:ObservableRelationship` | `Contained_Within` link from thumbnail to its cache database (`uco-core:kindOfRelationship`, `uco-core:source`, `uco-core:target`, `uco-core:isDirectional`) |

## Modeling pattern

Snippets below are copied verbatim from the validated exemplar
[`examples/windows-thumbnail-cache-example.jsonld`](../../examples/windows-thumbnail-cache-example.jsonld).

**1. The cache database as a `File`** (here the 256-pixel bucket, real size
7,340,032 bytes):

```json
{
  "@id": "kb:File-thumbcache-256-3b4ad986-0626-4b8b-89f7-672e7086a52d",
  "@type": "uco-observable:File",
  "uco-core:name": "thumbcache_256.db",
  "uco-core:description": [
    "Windows Thumbnail Cache database for the 256-pixel size bucket, from the Explorer cache of the user 'Alice'. Cache format signature 'CMMM', cache format version 32 (Windows 11)."
  ],
  "uco-core:hasFacet": [
    {
      "@id": "kb:FileFacet-bb22b6f7-2e2e-4d41-8311-15371f8fa298",
      "@type": "uco-observable:FileFacet",
      "uco-observable:fileName": "thumbcache_256.db",
      "uco-observable:filePath": "C:\\Users\\Alice\\AppData\\Local\\Microsoft\\Windows\\Explorer\\thumbcache_256.db",
      "uco-observable:extension": "db",
      "uco-observable:sizeInBytes": { "@type": "xsd:integer", "@value": "7340032" }
    }
  ]
}
```

**2. The recovered thumbnail** — an `ObservableObject` whose name is the
ThumbnailCacheID, carrying `RasterPictureFacet` (1280x721, `jpg`),
`ContentDataFacet` (real 110,625-byte thumbnail, `image/jpeg`, hash), and
`RecoveredObjectFacet` (pixels recovered, name not recovered):

```json
{
  "@id": "kb:ObservableObject-thumbnail-3869191d-8d2d-44de-b933-5d36cd7c612d",
  "@type": "uco-observable:ObservableObject",
  "uco-core:name": "2ba21a59792ff60a",
  "uco-core:description": [
    "Recovered thumbnail extracted from thumbcache_1280.db, keyed by ThumbnailCacheID '2ba21a59792ff60a'. The decoded image is a JPEG (1280x721) depicting Mont-Saint-Michel. The original source image file is no longer present on the volume; its filename cannot be recovered from the thumbcache alone (filenames resolve through the Windows.edb Search index, which is absent from this evidence)."
  ],
  "uco-core:hasFacet": [
    {
      "@id": "kb:RasterPictureFacet-1e779da4-ca97-4863-a262-3aa9102230b9",
      "@type": "uco-observable:RasterPictureFacet",
      "uco-observable:pictureHeight": { "@type": "xsd:integer", "@value": "721" },
      "uco-observable:pictureWidth": { "@type": "xsd:integer", "@value": "1280" },
      "uco-observable:pictureType": "jpg"
    },
    {
      "@id": "kb:ContentDataFacet-44097bec-6615-42e1-9b52-6f31f8c68419",
      "@type": "uco-observable:ContentDataFacet",
      "uco-observable:sizeInBytes": { "@type": "xsd:integer", "@value": "110625" },
      "uco-observable:mimeType": [ "image/jpeg" ],
      "uco-observable:hash": [
        {
          "@id": "kb:Hash-105d6f7b-4f98-4429-9001-350846f56f93",
          "@type": "uco-types:Hash",
          "uco-types:hashMethod": [ "SHA256" ],
          "uco-types:hashValue": {
            "@type": "xsd:hexBinary",
            "@value": "0000000000000000000000000000000000000000000000000000000000000000"
          }
        }
      ]
    },
    {
      "@id": "kb:RecoveredObjectFacet-8e2dcb2c-0408-4071-bf8a-fc4c7176266f",
      "@type": "uco-observable:RecoveredObjectFacet",
      "uco-observable:contentRecoveredStatus": "recovered",
      "uco-observable:nameRecoveredStatus": "Not Recovered"
    }
  ]
}
```

> The 64-zero `hashValue` above is a clearly-marked placeholder — replace it
> with the real SHA-256 of the extracted thumbnail bytes. Recovery-status
> values use the open `RecoveredObjectStatusVocab` (members: `recovered`,
> `partially recovered`, `overwritten`, `unknown`). `contentRecoveredStatus`
> here is the member `recovered`; `nameRecoveredStatus` uses the free-text
> "Not Recovered" because the vocabulary has no negative member, so
> `case_validate` emits a single `sh:Info` suggestion (not a warning or
> violation) for it.

**3. Containment** — the thumbnail is `Contained_Within` its cache database
(relationship properties are in `uco-core:`, since `ObservableRelationship`
subclasses `uco-core:Relationship`):

```json
{
  "@id": "kb:ObservableRelationship-42587d73-a925-4cef-9401-ab491773c350",
  "@type": "uco-observable:ObservableRelationship",
  "uco-core:kindOfRelationship": "Contained_Within",
  "uco-core:isDirectional": { "@type": "xsd:boolean", "@value": "true" },
  "uco-core:source": [
    { "@id": "kb:ObservableObject-thumbnail-3869191d-8d2d-44de-b933-5d36cd7c612d" }
  ],
  "uco-core:target": {
    "@id": "kb:File-thumbcache-1280-2b25936d-ed8a-467b-8897-a73665549e10"
  }
}
```

## Anti-patterns

- **Do not assert an original file name you cannot recover.** The thumbcache
  does not store file names. If `Windows.edb` (or a Shellbag/Recent-items
  correlation) has not resolved it, leave `nameRecoveredStatus` negative and
  do **not** invent a `FileFacet.fileName` on the thumbnail.
- **Do not type the thumbnail as the original image.** The recovered object is
  a *thumbnail* (a low-resolution derivative), not the source photo. Model it
  as its own `ObservableObject`; do not merge its identity with the deleted
  original or copy the original's presumed dimensions onto it.
- **Do not fabricate the source path or a wall-clock capture time.** Record
  only the cache file's own path/size and the thumbnail's own attributes.
- **Do not bury the ThumbnailCacheID / size bucket in free-text.** Put the
  ThumbnailCacheID in `uco-core:name` (and description) so it is queryable;
  the size bucket is carried by the specific `thumbcache_<N>.db` you link to.
  Note that structured, queryable fields for these (a dedicated thumbcache
  facet) are a pending ontology gap.
- **Do not invent a "generated-from" relationship term.** The evidentiary
  point — that this cached thumbnail was *generated from a now-deleted source
  image* — has **no adequate core relationship vocabulary term** today.
  `Contained_Within` (thumbnail-inside-db) is correct and sufficient for what
  the cache proves; the derivation link is deliberately left unmodeled here
  and is the subject of the
  [change proposal](../../change_proposals/windows-thumbnail-cache-facet.md).
  Do not substitute `Extracted_From`/`Created_By` to paper over the gap.

## Checklist

1. Enumerate the `thumbcache_*.db` files under
   `%LocalAppData%\Microsoft\Windows\Explorer\`; model each as a
   `uco-observable:File` + `FileFacet` (fileName, filePath, extension `db`,
   real `sizeInBytes`).
2. For each recovered thumbnail, create one `uco-observable:ObservableObject`
   and put its 8-hex ThumbnailCacheID in `uco-core:name`.
3. Add a `RasterPictureFacet` with the decoded `pictureWidth`,
   `pictureHeight`, and `pictureType` (e.g. `jpg`, `bmp`, `png`).
4. Add a `ContentDataFacet` with the thumbnail's `sizeInBytes`, `mimeType`,
   and a real `Hash` (SHA-256) of the extracted bytes.
5. Add a `RecoveredObjectFacet`: set `contentRecoveredStatus` to `recovered`;
   set `nameRecoveredStatus` negative unless the name was independently
   resolved.
6. Link each thumbnail to its cache database with an
   `ObservableRelationship`, `uco-core:kindOfRelationship` =
   `Contained_Within`, `source` = thumbnail, `target` = the `thumbcache_<N>.db`
   File, `isDirectional` = `true`.
7. Do **not** add a derivation relationship to the deleted source image;
   record that limitation in the description and cite the change proposal.
8. Validate: `case_validate --built-version case-1.4.0 --allow-info
   examples/windows-thumbnail-cache-example.jsonld` and confirm
   `Conforms: True`.

## Validated exemplar

[`examples/windows-thumbnail-cache-example.jsonld`](../../examples/windows-thumbnail-cache-example.jsonld)
— models `thumbcache_256.db` and `thumbcache_1280.db` as Files, the recovered
Mont-Saint-Michel thumbnail (ThumbnailCacheID `2ba21a59792ff60a`) with
`RasterPictureFacet` + `ContentDataFacet` + `RecoveredObjectFacet`, and the
`Contained_Within` relationship. `case_validate --built-version case-1.4.0
--allow-info` reports `Conforms: True` (1 `sh:Info` open-vocabulary
suggestion on `RecoveredObjectStatusVocab` for the free-text
`nameRecoveredStatus`; no warnings, no violations).

*Validated against the Windows 11 profile "Alice" Explorer cache exemplar
(thumbcache_96/256/768/1280.db; cache format `CMMM` version 32), DFRWS USA
2026 session — Team huh.*

## Related

- [file-fragments.md](file-fragments.md) — thumbnails embedded inside images at a byte range (distinct from the OS cache)
- [file-recovery.md](file-recovery.md) — `RecoveredObjectFacet` and carving/recovery status semantics
- [exif-data.md](exif-data.md) — image + camera metadata when the original file is still present
- [starter-filesystem-report.md](starter-filesystem-report.md) — the File + FileFacet + ContentDataFacet starter pattern
- [change-proposal.md](change-proposal.md) — the workflow behind the pending `WindowsThumbcacheFacet` / thumbnail-derivation ontology gap
