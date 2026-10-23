# Vendor fixtures

Copies of acquisition summaries and reports published by
[Digital Corpora](https://digitalcorpora.org/) in its
[mobile datasets](https://digitalcorpora.s3.amazonaws.com/s3_browser.html#corpora/mobile/).
The devices are test phones populated for public research; the files are
used here only to test that the readers in `case_uco.vendors` cope with real
layouts across tool versions.

| Fixture | Source object | Notes |
|---|---|---|
| `cellebrite/android10_ufed_7.28_Pixel3_trimmed.ufd` | `corpora/mobile/android_10/Cellebrite Extraction/Google_G013A Pixel 3.ufd` | Trimmed to 2 of its 819 `[Dump/...]` sections |
| `cellebrite/ios15_premium_7.64_EXTRACTION_FFS.ufd` | `Cellebrite/EXTRACTION_FFS 01/EXTRACTION_FFS.ufd` from the iOS 15.3.1 image archives under `corpora/mobile/android_13/ios_15_3_1/` | Contains the test phone's passcode; the reader withholds it by default |
| `cellebrite/ios15_EvidenceCollection.ufdx` | `Cellebrite/EvidenceCollection.ufdx`, same archive | |
| `cellebrite/android14_inseyets_10.2_EXTRACTION_FFS.ufd` | `Android_14_Public_Image/UFED Google Pixel 7a 2024_07_28 (001)/EXTRACTION_FFS 01/EXTRACTION_FFS.ufd` inside `corpora/mobile/android_14/Android_14_Public_Image.tar.gz` | |
| `cellebrite/android14_EvidenceCollection.ufdx` | `EvidenceCollection.ufdx` in the same folder | |
| `cellebrite/android13_pa_7.58_report_trimmed.xml` | `report.xml` in `Android_13_Image.ufdr` inside `corpora/mobile/android_13/android_13_Celebrite_Reader.tar.gz` | Physical Analyzer 7.58.0.66, schema 7.48. Trimmed from 969 MB to the project header, 4 tagged files with their `RelatedNodes`, 4 decoded models, and their `extraInfo` entries; `NodeCount`/`ModelCount` rewritten to match. Elements are otherwise unchanged |
| `cellebrite/ios15_pa_7.62_report_trimmed.xml` | `report.xml` in `iPhone 8/iOS_15_Public_Image.ufdr` inside `corpora/mobile/android_13/ios_15_3_1/iOS_15_Public_Image_Reader.tar.gz` | Physical Analyzer 7.62.0.40, schema 7.48. Trimmed from 1.96 GB to the project header, 9 tagged files (two versions of `.GlobalPreferences.plist`, four lossily named `Zoom.app` files, `ThreemaData.sqlite` and two images decoded from it), 2 models, and their `extraInfo` entries. The four `Passcode`/`PasscodeLength` items are removed; `NodeCount`/`ModelCount` rewritten to match |
| `magnet/ios13_3_1/` | `corpora/mobile/ios_13_3_1/iOS 13.3.1 Extraction/Extraction Logs/` | `image_info.txt` and `activity_log.txt`, Magnet ACQUIRE 2.25.0.20236 |
| `magnet/ios13_4_1/` | `corpora/mobile/ios_13_4_1/iOS 13.4.1 Extraction/Extraction Logs/` | Same phone, after an OS update |

`.gitattributes` disables line-ending conversion here: the Magnet
`image_info.txt` records the MD5 of its CRLF-terminated activity log.
