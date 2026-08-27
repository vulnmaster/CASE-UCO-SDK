# Legal Process and Procedure Extension (`legalproc`)

Jurisdiction-neutral **criminal legal process** concepts — charges, charging
instruments, pleas, proceedings, verdicts, sentences, forfeiture, and
restitution — usable by **any** investigation domain (violent crime,
financial crime, CAC, terrorism, e-discovery hand-offs, ...).

## Provenance

This extension is the SDK-local implementation of the stub namespaces
proposed upstream to CASE:

| Upstream proposal | Terms tracked here |
|---|---|
| [CASE #192](https://github.com/casework/CASE/issues/192) — criminal process stubs | `CriminalCharge`, `Plea`, `CriminalProceeding`, `Sentence`, `ForfeitureOrder`, `RestitutionOrder`, `concernsCharge` |
| [CASE #191](https://github.com/casework/CASE/issues/191) — case identification | `caseIdentifier` (subproperty of `uco-core:externalIdentifier`) |
| This SDK (validated against U.S. v. Perry & O'Dell) | `ChargingInstrument`, `Verdict`, `offenseForm`, `objectOffense`, `assertedIn`, count/disposition/sentence detail properties |
| This SDK (press-release legal outcomes, #125) | `PleaAgreement`, `PotentialPenalty`, `PretrialReleaseCondition`, `StateCharge`, `FederalCharge`, `outcomeScope`, `sentenceKind`, `jurisdictionKind`, `victimFactStatus` |
| This SDK (discovery obligations, #132) | `DisclosureObligation`, `DiscoveryProduction`, `SuppressionMotion`, `disclosureKind`, `disclosureStatus`, `disclosureSourceCitation`, `concernsEvidence`, `chargedWith`, `appliesTo` |

When CASE adopts the proposed namespaces, these terms re-parent to the CASE
terms and this extension shrinks to a bridge file. Do **not** build new
domain-specific forks of these concepts (that is the duplication CASE #192
exists to end); subclass them instead. Plea and plea-agreement modeling
uses `legalproc:Plea` and `legalproc:PleaAgreement` (`recordsPlea`); do
not use `cryptoinv:PleaAgreement` or an undeclared CAC `PleaAgreement`.

## Namespace

The extension uses the namespace **proposed** to the CASE committee in
CASE #192, `https://ontology.caseontology.org/case/criminal/` (prefix
`legalproc` locally; the proposal suggests `criminal`). These are general
legal-process concepts, so per community-sandbox guidance they belong under
a CASE namespace rather than a vendor or application-domain namespace
(Project VIC namespaces are reserved for child-safeguarding concepts in the
CAC Ontology). The committee owns the final IRI; if it picks a different
one, only this extension's files need to change — graphs built through the
SDK re-serialize against the adopted namespace.

## Modeling inchoate and derivative offenses (conspiracy, attempt, § 924(c))

Conspiracy is **not** a separate class. It is a `CriminalCharge` whose
`offenseForm` is `"conspiracy"`, optionally linked by `objectOffense` to the
charge representing the object offense. The same pattern covers attempt,
solicitation, aiding-and-abetting, and predicate-linked (derivative) counts:

```turtle
kb:count-21 a legalproc:CriminalCharge ;
    legalproc:statuteCitation "18 U.S.C. §§ 924(c)(1)(A)(iii) & 2" ;
    legalproc:offenseForm "derivative" ;
    legalproc:objectOffense kb:count-4 .   # crime of violence charged in Count 4
```

The conspiracy *organization* (militia, trafficking ring, laundering crew) is
a separate concern: model it as `uco-identity:Organization` plus
`uco-core:Relationship` edges (and, in CAC-domain graphs, the existing
`cacontology:ConspiracyRole` role classes).

## Scope

In scope: the procedural skeleton of a criminal prosecution as recorded in
court filings (PACER dockets, indictments, plea agreements, sentencing
memoranda, judgments) and public press releases that report those stages.
`outcomeScope` distinguishes current-case outcomes from prior-conviction
history. `sentenceKind` keeps imposed sentences distinct from bail, bond,
and potential penalties (`PotentialPenalty`, `PretrialReleaseCondition`).

Out of scope: civil process (CASE #193), corporate/internal process
(CASE #194), evidence-law concepts, non-U.S. procedural detail. Statute
citations, offense forms, dispositions, and proceeding types are open
string vocabularies so any jurisdiction's terminology fits.

## Validation

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/legalproc/legalproc.ttl \
  --ontology-graph extensions/legalproc/legalproc-shapes.ttl \
  --inference rdfs --allow-info \
  extensions/legalproc/legalproc-exemplar.ttl
```

Full case exemplar: `examples/pacer/wdmo_2022_cr_04065/` (U.S. v. Perry &
O'Dell — 45-count conspiracy / attempted-murder / firearms prosecution).

Enable for the MCP server via `CASE_UCO_EXTENSIONS=cac,legalproc` and for
validation via `validate_graph(..., extensions=["legalproc"])`.
