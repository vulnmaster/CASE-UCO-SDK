# Cyber Threat Intelligence and APT Reporting

> See [Recipe Index](INDEX.md) for all recipes.

Model an open-source cyber threat intelligence (CTI) report — a vendor
analysis (Cisco Talos, Mandiant, Prevailion, etc.) of adversary activity,
malware families, post-compromise tooling, and tactics, techniques, and
procedures (TTPs). ATT&CK here names **hacker / attacker** tradecraft,
not a crimes-against-children **offender** who targets children or other
vulnerable people. Use CAC recipes for those investigations; emit ATT&CK
on a CAC graph only if the source describes that rare overlap.

This is fundamentally different from a single-incident
forensic case: the deliverable is *intelligence distilled from reporting*
(often many intrusions), not evidence acquired from one host or capture.
The distinctive modeling requirements are (1) **the report is the primary
artifact** — including graphics, tables, and inline code that routinely
carry IOCs, config dumps, and infection-chain detail absent from prose;
(2) **the actor abstraction follows source epistemology** — UCO has no
`ThreatActor` class; use a named `Organization`, an unattributed
`Grouping` activity cluster, or omit the actor entirely (see §2); and
(3) **malware families and variants** are tools with a lineage and an
activity timeline, distinct from the individual samples that carry hashes.

Validated against `examples/cti/lotus_blossom_2025/` (Cisco Talos, "Lotus
Blossom espionage group targets multiple industries with different
versions of Sagerunex and hacking tools," Joey Chen, 2025-02-27) and
`examples/cti/darkwatchman_2021/` (Prevailion PACT, "DarkWatchman: A new
evolution in fileless techniques," Matt Stafford and Sherman Smith,
2021-12-14 — fileless registry-buffered RAT + DGA C2).

**When to use this recipe**

- The source is a threat-intelligence report / threat spotlight / APT or
  malware writeup — either attributing activity to a named group (Lotus
  Blossom, APT41, etc.) **or** describing unattributed malware/activity
  clusters where attribution is explicitly impossible (DarkWatchman)
- The content describes malware families and variants, C2 infrastructure
  (including third-party cloud C2 such as Dropbox, Twitter/X, or webmail),
  a post-compromise toolkit, registry/service/task persistence, victimology
  by sector and region, and IOCs (hashes, IPs, domains, campaign codes,
  Snort/ClamAV/YARA signatures)
- The report embeds load-bearing source artifacts — graphics, tables,
  inline code blocks, configuration excerpts, and machine-readable IOC
  sections — that carry details absent from the surrounding prose
- For a single intrusion with acquired packet capture or host evidence,
  use [network-investigation.md](network-investigation.md); for a
  delivery-chain narrative from a phishing email, use
  [spear-phishing.md](spear-phishing.md); for the analysis/attribution
  layer mechanics, use [analysis.md](analysis.md)

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Report container; `focus` = attribution / malware / C2 / persistence |
| `uco-core:ContextualCompilation` | Thematic bundles under the Investigation (source, delivery, malware, infra, analytics, detection, ATT&CK mappings) |
| `uco-observable:ObservableObject` + `URLFacet` | The report itself (blog post) |
| `uco-identity:Person` / `Organization` | Report author and publisher (e.g., Joey Chen / Cisco Talos) |
| `uco-observable:ObservableObject` + `RasterPictureFacet` + `FileFacet` + `ContentDataFacet` | Each in-report graphic, captured by SHA-256 with a description of what it depicts |
| `uco-identity:Organization` **or** `uco-core:Grouping` | Named attributed actor **or** unattributed activity cluster (see §2); no `ThreatActor` class |
| `uco-core:Annotation` | Assessments, capabilities, contradictions, detection provenance, ATT&CK mapping notes |
| `uco-core:Event` | VT first-submission / first-seen style timestamps (not `FileFacet.observableCreatedTime`) |
| `uco-core:ConfidenceFacet` | Numeric confidence **only** when the source publishes a number or a project policy defines the scale; otherwise prefer verbal `confidence:*` tags |
| `uco-configuration:Configuration` + `ConfigurationEntry` | Code-derived malware parameter schemas (registry value-name templates, DGA seed sets) |
| `uco-tool:MaliciousTool` | Malware family (backdoor/RAT) and offensive tools; `toolType` |
| `uco-tool:Tool` | Dual-use / legitimate tooling (RAR, Impacket, VMProtect, HTran) |
| `uco-observable:ObservableObject` + `FileFacet` | Malware samples/variants and dropped DLLs (`observableCreatedTime` only for true creation times; see §3) |
| `uco-observable:WindowsRegistryKey` + `WindowsRegistryKeyFacet` + `WindowsRegistryValue` | Observed registry state only (`name` / `data` / `dataType` — no `description` on the value) |
| `uco-observable:WindowsTask` + `WindowsTaskFacet` | Scheduled-task persistence (`triggerList` / `actionList` when reported) |
| `uco-observable:WindowsService` + `WindowsServiceFacet` | The hijacked/created service (`startType`, `serviceType`) |
| `uco-pattern:LogicalPattern` | Machine-actionable detection expressions (`patternExpression` typed as `uco-pattern:PatternExpression` under CASE 1.4.0) |
| `uco-observable:IPv4AddressFacet` / `DomainNameFacet` | C2 servers, proxies, cloud-C2 endpoints, recon services |
| `uco-location:Location` + `SimpleAddressFacet` | Targeted regions (victimology map) |
| `uco-victim:VictimTargeting` | Targeted sectors (a `Victim` role subclass) |
| `uco-action:Action` | Observed/reported adversary (or victim) behaviors: persistence, discovery, lateral movement, collection/exfil — **not** capability bullets or vendor detection coverage |

## Modeling patterns

### 1. The report and its load-bearing source artifacts are first-class evidence

Model the blog post as an `ObservableObject` with a `URLFacet`, linked to
its author (`Person`) and publisher (`Organization`). Capture **every
load-bearing source artifact**: graphics, tables, inline code blocks,
configuration excerpts, and machine-readable IOC sections. Threat reports
put decisive detail into images and code — Gantt timelines, infection-chain
diagrams, DGA/registry handlers, and annotated config hexdumps with C2 IPs
and tokens. Download each graphic, hash it (SHA-256), and create an
`ObservableObject` with `FileFacet` + `RasterPictureFacet` +
`ContentDataFacet`, and — critically — a `uco-core:description` recording
*what the artifact shows*. Link graphics to the report with
`Contained_Within` tagged `graphic`. Prefer hashing inline code excerpts
the same way when they ground capability or contradiction Annotations.

### 2. Actor abstraction — three branches (do not collapse epistemology)

UCO has no dedicated ThreatActor/IntrusionSet class. Choose the branch that
matches the **source's epistemic state**, not a one-size-fits-all Organization:

| Source says… | Model as | Performer of observed Actions? |
|---|---|---|
| Named/attributed group (aliases, MITRE group page, exclusive malware) | `uco-identity:Organization` with reported aliases in `tag` | Yes — `uco-action:performer` |
| Unattributed activity / “attribution not possible” | `uco-core:Grouping` (activity cluster) + `uco-core:Annotation` claims with source locators | **No** — leave performer unset |
| No defensible actor abstraction | Omit actor node | Leave performer unknown |

Never invent aliases the report does not use. Never turn “appears criminal /
moderate confidence / ransomware hypothesis” into flat Organization facts.
Record those as `Annotation` statements with source provenance (report
section, figure, or code excerpt via `ExternalReference.definingContext`).
Prefer verbal confidence tags (`confidence:moderate-verbal`) over invented
numeric `ConfidenceFacet` values unless the source publishes a number or a
cited project normalization policy exists. The controlled vocabulary for
these tags (stance, verbal confidence, hash/bytes honesty, ATT&CK mapping
provenance) is published at
[`docs/vocabularies/epistemic-tags.md`](../vocabularies/epistemic-tags.md)
(JSON: [`epistemic-tags.json`](../vocabularies/epistemic-tags.json)).

Named-group exemplar: Lotus Blossom → Organization. Unattributed exemplar:
DarkWatchman → Grouping + analytic Annotations
(`examples/cti/darkwatchman_2021/`, `CASEGraph` public upsert APIs /
`serializer_mode=casegraph_raw` + `case_uco.validation.validate_graph_file`).
Keep builder/recipe hashes in a `build-manifest.json` sidecar — do not insert
implementation files into the CTI domain graph.

### 2b. Observed behavior vs capability vs enrichment

Do not represent every capability bullet as an observed `Action` with a
performer. Separate:

| Source meaning | Representation |
|---|---|
| Observed / repeatedly executed behavior | `uco-action:Action` (tag `epistemic:observed` or `reported`) |
| Code capability / conditional path | `Annotation` or capability-tagged `Grouping` on the tool; condition in description |
| Analyst hypothesis | `Annotation` tagged `epistemic:hypothesis` (+ verbal confidence tag or sourced numeric facet) |
| ATT&CK mapping | Technique punning on the Action **plus** mapping provenance Annotation (technique URL, mapping date/author, vendor-asserted vs modeler enrichment) |

Victim/user execution (“victim opens the attachment”) must not list the
adversary as `performer` — omit performer or use a redacted victim identity.

### 3. Malware families vs. variants vs. samples

Distinguish three levels:

- **Family** (`uco-tool:MaliciousTool`, e.g. Sagerunex): the named
  backdoor lineage, its `toolType`, injection method, and shared behaviors;
  link to its predecessor with `Related_To` ("assessed evolution of Evora").
- **Variant** (`ObservableObject` + `FileFacet`): each distinct version
  (Beta, original, Dropbox/Twitter, Zimbra), with its distinguishing C2
  mechanism in the description; `Related_To` the family.
- **Sample**: an individual binary carrying a hash — attach a
  `ContentDataFacet` when the report gives one.

**Timestamps:** use `observableCreatedTime` only for actual artifact creation
times. VirusTotal *submission*, first-seen, first-analyzed, and estimated
activity windows are `uco-core:Event` nodes (`eventType`, `startTime`,
`eventContext` → sample) — never silently rewrite submission times as file
creation.

When a named Organization is justified, record its `Used` relationship to the
family and to each variant. For unattributed clusters, classify samples via
`AnalyticResult` instead of inventing a Used edge from a fake Organization.

### 4. Registry-based persistence is fully covered by core UCO

`reg add` service-DLL persistence maps cleanly onto core UCO — **no
extension or change proposal is required**. For each key, create a
`uco-observable:WindowsRegistryKey` whose `WindowsRegistryKeyFacet` carries
the `key` path and one embedded `WindowsRegistryValue` per value. On each
`WindowsRegistryValue` set `uco-core:name` (the value name, e.g.
`ServiceDll` / `Start`), `uco-observable:data` (the data, e.g.
`c:\windows\tapisrv.dll` / `2`), and `uco-observable:dataType` using a
`RegistryDatatypeVocab` member (`reg_expand_sz`, `reg_dword`, `reg_sz`,
`reg_binary`, `reg_multi_sz`, `reg_qword`, …). Pair the key with a
`uco-observable:WindowsService` (`WindowsServiceFacet.serviceName`,
`startType` = `service_auto_start` when `Start=2`, `serviceType`), and
relate the `ServiceDll` value's key to the dropped DLL `ObservableObject`.
Wrap the whole thing in a single persistence `uco-action:Action`
(`performer` = named attributed Organization **only when justified**;
`object` = the keys, `result` = the services).

The same native coverage applies to **fileless registry-buffer** patterns
(DarkWatchman): configuration, encoded payloads, and IPC buffers live under
an application-looking hive (e.g. `HKCU\Software\Microsoft\Windows\DWM\`)
with host-derived value-name suffixes. Model the hive as one
`WindowsRegistryKey`. Use `WindowsRegistryValue` **only for observed state**
(`uco-core:name`, `uco-observable:data`, `uco-observable:dataType` — values
do **not** inherit `uco-core:description`). Put code-derived parameter
semantics (what `<uid>a` means) on
`uco-configuration:Configuration` / `ConfigurationEntry`, not as fake
registry snapshots. Do **not** instantiate values the source says are unset
(e.g. DGA salt never written). Pair with a `WindowsTask` observable
(`triggerList` / `actionList` when reported) and scheduled-task persistence
`Action` (T1053.005) when the report documents Task Scheduler rather than a
service DLL. Label analysis-sandbox accounts (ANY.RUN hostnames) as
analysis-environment identities, not victim accounts. Do not invent a
"fileless" extension class — registry + configuration + task + Action is enough.

Do not weaken `Contained_Within` merely because a contained file lacks a
published digest — name, size, and report provenance are enough. Tag the
artifact `hash-status:not-published` (or `source-bytes:not-acquired`) so the
critic emits a medium completeness note rather than a high defect.

<!-- recipe-lint: ignore-start anti-pattern -- The invalid predicate is shown explicitly so authors can recognize and replace it. -->
> **Note on the value name property.** `WindowsRegistryValue` is a
> `UcoInherentCharacterizationThing`, and its name is `uco-core:name` — not
> `uco-observable:name` (which does not exist and will fail strict concept
> coverage). This is the single most common validation slip when modeling
> registry values.
<!-- recipe-lint: ignore-end anti-pattern -->

### 5. MITRE ATT&CK techniques → the `uco-action:Technique` metaclass

`uco-action:Technique` is a **metaclass**, not an ordinary class, as defined
in [ucoProject/UCO PR #676](https://github.com/ucoProject/UCO/pull/676)
(resolving [issue #666](https://github.com/ucoProject/UCO/issues/666), UCO
1.5.0). Its exact wording: *"A technique is a class of actions joined by some
common characteristics. `uco-action:Technique` itself is a metaclass. A
Technique instance is an `owl:Class` that is a subclass of
`uco-action:Action`."* The PR also adds a top-level `uco-core:UcoType` (disjoint
from `uco-core:UcoThing`) to anchor the metaclass hierarchy, and one property,
`uco-action:techniqueID` (Literal-valued, used only on Techniques). It does
**not** add `techniqueFramework` / `techniqueTactic` / `techniquePlatform` —
those appeared only in the issue's early draft and are not in the merged model.

So model techniques with **punning**, in two layers:

- **The technique is a class.** Declare each ATT&CK technique as an
  `owl:Class` that is `a uco-action:Technique` and `rdfs:subClassOf
  uco-action:Action`, carrying `uco-action:techniqueID` (e.g. `T1543.003`).
  Keep these in an ontology/catalog graph, not the data graph — the local
  [`attack-technique`](../../extensions/attack-technique/) extension ships a
  partial MITRE ATT&CK catalog (`mitre-attack-catalog.ttl`) under the
  canonical `https://attack.mitre.org/techniques/<id>` IRIs. Tactic/platform
  context goes in each class's `rdfs:comment` (the merged UCO model keeps the
  general class minimal).
- **A concrete action exhibits the technique.** Type the behavior
  `uco-action:Action` instance *with the technique class* (add the technique
  IRI to its `@type`). Because the technique class is a subclass of
  `uco-action:Action`, the action instance is still a valid Action; the extra
  type asserts which technique it exhibits. Do **not** create a separate
  Technique instance per action or link with a custom technique relationship —
  the punning `rdf:type` edge *is* the association.

Sourcing matters: a report that lists no ATT&CK IDs in its prose (this Talos
post does not) is usually still mapped on the corresponding MITRE ATT&CK
**group** and **software** pages — for Lotus Blossom, group
[G0030](https://attack.mitre.org/groups/G0030/) and Sagerunex software S1156.
Enrich from those high-confidence mappings (e.g. T1543.003 Windows Service,
T1112 Modify Registry, T1055.001 DLL Injection, T1027.002 Software Packing,
T1090.001 Internal Proxy, T1102.002 Web Service, T1560.001 Archive via
Utility, T1041 Exfil over C2). Validate with the extension **and RDFS
inference** (the metaclass constraints resolve under inference):
`validate_graph(path, extensions=["attack-technique:full"])`. Reuse the
`attack-technique` catalog IRIs rather than minting your own technique class,
so the model matches the terms released in UCO 1.5.0.

### 6. Third-party cloud C2 is still C2

New variants tunnel C2 through legitimate services (Dropbox, Twitter/X,
Zimbra webmail) to blend with normal traffic. Model each channel as an
`ObservableObject` with a `DomainNameFacet`, and connect the variant to it
with a `Connected_To` relationship tagged `c2`. Keep legacy VPS C2 IPs
(`IPv4AddressFacet`) and hardcoded proxies distinct, tagged `c2` / `proxy`.
Model exfil artifacts (e.g. `mail_report.rar` saved to Zimbra draft/trash
folders) as observables `Created` by the variant and `Uploaded_To` the
cloud channel.

### 7. Victimology: regions and sectors

Model targeted regions (from the report's map graphic) as
`uco-location:Location` + `SimpleAddressFacet.country`, related to the actor
abstraction or activity cluster through a sourced targeting assertion
(`targeting`-tagged edge or Annotation). Model targeted sectors as a
`uco-victim:VictimTargeting` node (a `Victim` role subclass) — put the
sector list in the description and `tag`; there is no `targetSector`
property, so do not invent one.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Dropping graphics/code/tables because they are "just media" | Capture each load-bearing artifact (hash + description); link claims to section/figure/code locators |
| Forcing every CTI report into a named `Organization` actor | Choose Organization / unattributed `Grouping` / omit per §2; never use an unattributed cluster as `performer` |
| Modeling the threat actor as an `ObservableObject` or a `Tool` | Named actor → `Organization`; unattributed cluster → `Grouping`; behaviors → `Action` (performer only when attributed) |
| Claiming `serializer_mode=typed_sdk` while using only `upsert_node` | Use generated dataclasses + `graph.create()`, or label the builder `casegraph_raw` |
| Invented numeric `ConfidenceFacet` values | Preserve verbal confidence, or cite a normalization policy / source-published number |
| `uco-core:description` on `WindowsRegistryValue` | Values only expose `name` / `data` / `dataType`; put semantics on `ConfigurationEntry` |
| `uco-observable:name` on a `WindowsRegistryValue` | Use `uco-core:name`; the value's data/type are `uco-observable:data` / `uco-observable:dataType` |
| Free-text registry data type (`REG_EXPAND_SZ`) | Use `RegistryDatatypeVocab` members (`reg_expand_sz`, `reg_dword`, …) |
| Inventing a bespoke Technique/Malware/ThreatActor class | Actor abstraction per §2; malware → MaliciousTool; ATT&CK → `uco-action:Technique` metaclass via the `attack-technique` catalog |
| Modeling a technique as a plain instance node (`x a uco-action:Technique` with `techniqueTactic`/`techniquePlatform`) | `uco-action:Technique` is a **metaclass**: a technique is an `owl:Class` (`a uco-action:Technique`, `rdfs:subClassOf uco-action:Action`) with `uco-action:techniqueID`; the merged PR has no framework/tactic/platform properties |
| Linking an action to its technique with a custom relationship | Type the action instance *with the technique class* (`rdf:type`); the punning type edge is the association — no relationship node |
| Dropping ATT&CK techniques because the report's prose omits IDs | Enrich from MITRE group/software pages when available; always record mapping provenance |
| Embedding builder/recipe files in the Investigation graph | Put implementation provenance in a sidecar manifest; keep the domain graph about the report |
| Collapsing family, variant, and sample into one node | Family = `MaliciousTool`; variants/samples = `ObservableObject` + `FileFacet`/`ContentDataFacet`, `Related_To` the family |
| Treating cloud C2 (Dropbox/Twitter/Zimbra) as benign | It is a C2 channel — `Connected_To` tagged `c2`, with exfil artifacts `Uploaded_To` it |
| Putting ATT&CK IRIs on `solveit-core:usedTechnique` | ATT&CK describes **hacker / attacker** tradecraft, not examiner method and not CAC offender conduct. Examiner methods stay in SOLVE-IT. See [technique-evidence-outcome.md](technique-evidence-outcome.md) |

## Checklist

1. Fetch the report; capture the prose and **download every graphic**.
   View each image and write a description of what it depicts (timelines,
   maps, infection chains, decompiled code, config hexdumps with IOCs).
2. Create the `Investigation`; model the report `ObservableObject`
   (`URLFacet`), its author and publisher, and one hashed `RasterPicture`
   observable per graphic linked `Contained_Within` the report.
3. Model the actor abstraction per §2 (named `Organization`, unattributed
   `Grouping` + analytic `Annotation`s, or omit). Do not invent aliases or
   use an unattributed cluster as `performer`. Add predecessor tooling /
   lineage when the source supports it.
4. Model the malware family (`MaliciousTool`) and each variant
   (`ObservableObject` + `FileFacet`). Put VT submission / first-seen times
   on `Event` nodes (§3), not `observableCreatedTime`. Record `Used` only
   when a named Organization is justified; otherwise classify via
   `Annotation`. Add config-revealed artifacts (host paths, temp files).
5. Model the post-compromise toolkit (`MaliciousTool` / `Tool`) with
   `toolType` and hashes where given.
6. Model registry/service persistence with `WindowsRegistryKey` +
   `WindowsRegistryValue` (name via `uco-core:name`, `dataType` via
   `RegistryDatatypeVocab`) and `WindowsService`; wrap in a persistence
   `Action`.
7. Model C2 (legacy VPS IPs, proxies, and cloud channels) and exfil
   artifacts; model discovery / lateral-movement / exfil `Action`s. Keep
   pre-cloud VPS C2 scoped to the variants that used it — do not attach a
   variant's config-derived infrastructure to later variants that moved off
   it.
8. Add ATT&CK techniques with the `uco-action:Technique` metaclass (from the
   report and the MITRE group/software pages): declare each technique as an
   `owl:Class` (subclass of `uco-action:Action`, with `techniqueID`) in the
   `attack-technique` catalog, and type each exhibiting behavior `Action`
   *with* that technique class. Add IOCs (campaign codes, signatures) and
   vendor detection coverage.
9. Validate: `validate_graph(path, extensions=["attack-technique:full"])`
   (strict concept coverage) plus `case_validate --built-version case-1.4.0
   --ontology-graph extensions/attack-technique/attack-technique.ttl
   --ontology-graph extensions/attack-technique/attack-technique-shapes.ttl
   --ontology-graph extensions/attack-technique/mitre-attack-catalog.ttl
   --inference rdfs --allow-info`; `Conforms: True` before presenting.

## Validated exemplars

1. `examples/cti/lotus_blossom_2025/build_lotus_blossom_sagerunex.py` — the
   Cisco Talos Lotus Blossom / Sagerunex report: the blog post and its 24
   graphics captured by hash, Lotus Blossom as an `Organization` (aliases
   Spring Dragon / Billbug / Thrip), the Sagerunex `MaliciousTool` family with
   Beta/original/Dropbox-Twitter/Zimbra variants on their timeline windows, the
   post-compromise toolkit (Chrome cookie stealer, Venom proxy,
   adjust-privilege, archiver, mtrain/HTran port relay, RAR, Impacket),
   registry service-DLL persistence for `tapisrv`/`swprv`/`appmgmt` with
   `WindowsService` pairing, legacy VPS + Dropbox/Twitter/Zimbra cloud C2,
   victimology (Philippines/Vietnam/Hong Kong/Taiwan; government/manufacturing/
   telecom/media), campaign-code IOCs, Snort/ClamAV coverage, and twelve MITRE
   ATT&CK techniques (G0030/S1156 mappings) modeled with the
   `uco-action:Technique` metaclass — each technique an `owl:Class` in the
   `attack-technique` catalog and typed onto the behavior `Action` that exhibits
   it. Passes `case_validate` (with RDFS inference) and strict concept
   coverage — all registry data against core UCO (which covers it natively) and
   the technique metaclass/classes against the local `attack-technique` extension
   (the [UCO #676](https://github.com/ucoProject/UCO/pull/676)
   forward-implementation).

2. `examples/cti/darkwatchman_2021/build_darkwatchman.py` — the Prevailion
   PACT DarkWatchman report (2021-12-14), built with `CASEGraph` public upsert
   APIs (`serializer_mode=casegraph_raw`, not a typed-dataclass exemplar):
   unattributed `Grouping` activity cluster (no Organization performer);
   DarkWatchman as a `MaliciousTool`; spearphish → ZIP → WinRAR SFX delivery;
   VT submission `Event`s; capability Annotations (including conditional
   shadow-copy deletion — not a T1490 Action); observed vs candidate DGA via
   `Configuration` seed set; registry schema on `ConfigurationEntry` with
   observed install-flag value only; `WindowsTask` structure; `LogicalPattern`
   detection expressions; source-contradiction Annotations; ATT&CK mappings
   as modeler enrichment with provenance; builder/recipe hashes in
   `build-manifest.json`. Demonstrates the **fileless registry-buffer**
   pattern that complements Lotus Blossom service-DLL persistence. Validated
   with `case_uco.validation.validate_graph_file(...,
   extensions=["attack-technique:full"])` (`Conforms: True`).

## Related

- [network-investigation.md](network-investigation.md) — single-incident network forensics with acquired pcap (contrast: one capture, not adversary intelligence)
- [spear-phishing.md](spear-phishing.md) — delivery-chain attack narrative from a phishing email
- [analysis.md](analysis.md) — the attribution/analysis layer with confidence-scored classifications
- [network-artifacts.md](network-artifacts.md) — IPs, domains, and URLs as observables
- [forensic-tool.md](forensic-tool.md) — modeling tools and their configured runs
- [technique-evidence-outcome.md](technique-evidence-outcome.md) — examiner SOLVE-IT techniques stay separate from ATT&CK
