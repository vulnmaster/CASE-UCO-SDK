# Weapons and Drug Evidence (Firearms, Ammunition, Controlled Substances)

Model physical weapon and drug evidence — firearms, ammunition, edged
weapons, and seized or charged quantities of controlled substances — with
queryable classes and properties using the `weapons` and `drugs`
extensions, instead of burying make, model, caliber, serial number,
substance, schedule, mass, and purity in `uco-core:description` strings.

**When to use this recipe**

- Firearms counts: 18 U.S.C. § 922(g) felon in possession, § 924(c)
  use/brandish/possess in furtherance, § 922(k) obliterated serial numbers
- Drug counts: 21 U.S.C. §§ 841/846 distribution and conspiracy charges
  with drug-quantity findings ("500 grams or more of a mixture…")
- Any case where weapons or drugs are seized, forfeited, brandished, or
  used as instruments of charged conduct

Charges, pleas, and sentences around this evidence follow
`docs/recipes/legal-process-modeling.md` (`legalproc` extension); document
ingestion mechanics are in `docs/recipes/cac-pacer-document-ingestion.md`.

## Why extensions (and which upper ontologies they anchor to)

Weapons and drugs are **never cyber**, so they are out of UCO's scope and
were previously modeled as bare `uco-core:UcoObject` items dual-typed
`gufo:FunctionalComplex`. That left no queryable structure ("all handguns
with obliterated serials", "all Schedule II seizures over 500 g"). The two
extensions keep instances inside the CASE/UCO graph (both classes subclass
`uco-core:UcoObject`) while anchoring to open external ontologies through
separate bridge files, per the
[CDO profile pattern](https://cyberdomainontology.org/ontology/development/#profiles):

- **`extensions/weapons/`** (`weap:`) — class tree mirrors the
  [Common Core Ontologies](https://github.com/CommonCoreOntology/CommonCoreOntologies)
  Artifact Ontology weapon hierarchy (BFO 2020 mid-level suite; DoD/IC
  ontology baseline; IEEE P3195.1). Bridges: `weapons-profile-cco.ttl`
  (subclass axioms into CCO) and `weapons-profile-gufo.ttl`
  (`weap:Weapon ⊑ gufo:FunctionalComplex`). Property names follow the NIEM
  justice-domain firearm representation while remaining declared in `weap:`.
- **`extensions/drugs/`** (`drug:`) — one class,
  `drug:ControlledSubstance`, representing the concrete **portion** of
  matter (the bag of meth, the charged quantity), not the chemical kind.
  Chemical identity is an IRI reference to
  [ChEBI](https://obofoundry.org/ontology/chebi.html) (OBO Foundry,
  BFO-compatible) via `drug:substance`. Bridge: `drugs-profile-gufo.ttl`
  (`drug:ControlledSubstance ⊑ gufo:Quantity` — an amount of matter, NOT
  `gufo:FunctionalComplex`).

## Weapons

```python
p365 = {
    "@id": uid("item-sig-p365"),
    "@type": "weap:Handgun",   # or Firearm/Rifle/Shotgun/LongGun/CuttingWeapon/Ammunition
    "uco-core:name": "SIG Sauer P365 9mm pistol (Serial Number 66F717834)",
    "weap:make": "SIG Sauer",
    "weap:model": "P365",
    "weap:caliber": "9mm",
    "weap:serialNumber": "66F717834",
    # "weap:serialNumberObliterated": True for § 922(k) facts
}
```

- Possession, brandishing, seizure, and forfeiture flow through the graph,
  not invented predicates: use `uco-action:instrument` for a weapon used in
  an Action. Otherwise use registered `Related_To` with the exact assertion
  (possessed, brandished, seized, or forfeited) in `uco-core:description`.
- Ammunition (including loaded magazines) is `weap:Ammunition` with
  `weap:caliber`.
- Record only what the document states; the shapes require nothing, so a
  weapon known only as "firearms" (plural, unspecified — common in
  brandishing counts) can stay a description-only `weap:Firearm` or be
  omitted in favor of the Action text.

## Controlled substances

```python
meth = {
    "@id": uid("item-meth-mixture"),
    "@type": "drug:ControlledSubstance",
    "uco-core:name": "Methamphetamine mixture charged in the Count 2 conspiracy",
    "drug:substanceName": "a mixture and substance containing a detectable amount of methamphetamine",
    "drug:csaSchedule": "II",
    "drug:mass": {"@type": "xsd:decimal", "@value": "500"},
    "drug:massUnit": "g",
    "drug:purityBasis": "mixture",   # vs "actual" (USSG § 2D1.1)
    "drug:quantityDescription": "500 grams or more of a mixture and substance containing methamphetamine",
}
```

- Use `drug:substanceName` unless the deployment explicitly vendors and
  validates a chemical ontology extension. Do not place unregistered ChEBI
  IRIs in an operational CASE/UCO graph merely because the identifier is
  externally resolvable.
  For diverted pharmaceutical products (NDC-coded tablets), reference the
  OBO Drug Ontology (DrOn) the same way.
- For threshold charges ("X grams or more"), set `drug:mass` to the
  threshold and keep the verbatim charging language in
  `drug:quantityDescription` — never fabricate a precise weight.
- The portion is **linked to, not typed by**, the ChEBI class: a bag of
  meth is not a molecule.

## Anti-patterns

- ❌ Typing a weapon or drug as `uco-observable:ObservableObject` — they
  are never cyber.
- ❌ Typing the seized portion directly with the ChEBI class
  (`@type: obo:CHEBI_6809`).
- ❌ Grounding drugs as `gufo:FunctionalComplex` — a quantity of a
  substance is a `gufo:Quantity`.
- ❌ Minting local classes for vehicles/electronics in these extensions —
  vehicles keep the `uco-core:UcoObject` + `gufo:FunctionalComplex`
  dual-typing until a dedicated extension exists.
- ❌ Multiple `uco-action:performer` values on one Action (max-1): primary
  actor is the performer; co-actors use `uco-action:participant`.

## Validation

```python
validate_graph(path, extensions=["legalproc", "weapons", "drugs"])
```

or with the CLI (bridges included so CCO/gUFO grounding is materialized
under RDFS inference):

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/weapons/weapons.ttl \
  --ontology-graph extensions/weapons/weapons-shapes.ttl \
  --ontology-graph extensions/weapons/weapons-profile-cco.ttl \
  --ontology-graph extensions/weapons/weapons-profile-gufo.ttl \
  --ontology-graph extensions/drugs/drugs.ttl \
  --ontology-graph extensions/drugs/drugs-shapes.ttl \
  --ontology-graph extensions/drugs/drugs-profile-gufo.ttl \
  --inference rdfs --allow-info graph.jsonld
```

## Validated exemplar

`examples/pacer/ndnd_2025_cr_00005/` — *U.S. v. Lindell et al.*
(D.N.D. 3:25-cr-00005): kidnapping of Victim A over a $6,000
methamphetamine debt. Exercises `weap:Handgun` (SIG Sauer P365, serial
66F717834), `weap:Ammunition` (seventeen 9mm rounds), and
`drug:ControlledSubstance` (500-gram meth-mixture quantity finding,
ChEBI-referenced), alongside `legalproc` charges, a guilty plea, and a
360-month sentence. Validates `Conforms: True` with all three extensions
and both bridge sets.
