<!-- Change Proposal: Relax required hierarchy and leadership cardinality on ChildExploitationEnterprise -->
<!-- Target repository: CAC-Ontology (cacontology-extremist-enterprises) -->
<!-- Target release: next backward-compatible CAC release -->
<!-- Drafted with the CASE/UCO SDK; auto-triage suggested UCO, corrected to CAC because the affected terms are CAC-only. -->

# Target release

**Target**: next backward-compatible CAC-Ontology release. Read the actual
number off the CAC `develop` branch rather than assuming one. This is a
constraint relaxation, so it is backward compatible: no graph that conforms
today becomes nonconformant.

# Background

`cacontology-extremist-enterprises:ChildExploitationEnterprise` declares four
required properties:

| Property | Current cardinality | Range | Declaring shape |
|---|---|---|---|
| `hasMember` | 2..* | `uco-identity:Person` | `GufoMembershipValidationShape` |
| `hasExploitationRelation` | 1..* | `gufo:Relator` | `GufoRelatorValidationShape` |
| `hasLeadershipRelation` | 1..* | `gufo:Relator` | `GufoRelatorValidationShape` |
| `hasHierarchy` | exactly 1 | `EnterpriseHierarchy` | `ChildExploitationEnterpriseShape` |

The class description cites 18 U.S.C. § 2252A(g). The last two requirements
overconstrain the class relative to that statute.

Section 2252A(g)(2) defines the offense as engaging in a child exploitation
enterprise, which a person does if they violate Chapter 110 "as part of a
series of felony violations constituting three or more separate incidents and
involving more than one victim, and commits those offenses in concert with
three or more other persons." The statutory elements are:

1. a series of predicate felony violations under Chapter 110,
2. three or more separate incidents,
3. more than one victim, and
4. acting in concert with three or more other persons.

There is no leadership element and no organizational-structure element. This
distinguishes § 2252A(g) from RICO: 18 U.S.C. § 1962 enterprise pleading turns
on an "enterprise" with structure, whereas § 2252A(g) turns only on a series of
violations committed in concert. A § 2252A(g) indictment can be legally
sufficient while alleging a wholly peer-structured group.

The practical consequence is that a modeler working from a real § 2252A(g)
charging instrument cannot type the charged enterprise as
`ChildExploitationEnterprise` without minting an `EnterpriseHierarchy` node and
at least one leadership `Relator` that the instrument does not allege.
Purchasing SHACL conformance with invented structure is exactly the failure
mode evidentiary graphs must avoid. Today the honest options are both bad:
fall back to `uco-identity:Organization` and lose the § 2252A(g) semantics, or
leave the graph nonconformant.

# Requirements

## Requirement 1

`hasHierarchy` on `ChildExploitationEnterprise` shall be optional
(`0..1`) rather than required (`exactly 1`). An enterprise whose charging
instrument pleads an organizational structure continues to assert the property
unchanged.

## Requirement 2

`hasLeadershipRelation` on `ChildExploitationEnterprise` shall be optional
(`0..*`) rather than required (`1..*`).

Both constraints live in SHACL only. `cacontology-extremist-enterprises.ttl`
declares all four properties as plain `owl:ObjectProperty` with
`rdfs:domain`/`rdfs:range` and carries no `owl:Restriction` or cardinality
axioms anywhere in the file, so no OWL edit is required.

## Requirement 3

`hasMember` and `hasExploitationRelation` shall remain required. They map
directly onto statutory elements: `hasMember` onto "in concert with three or
more other persons", and `hasExploitationRelation` onto "involving more than
one victim". Keeping them required preserves the class's discriminating power.

# Risk / Benefit analysis

## Benefits

- A § 2252A(g) enterprise pleaded without a hierarchy can be typed correctly
  instead of being flattened to `uco-identity:Organization`, so
  enterprise-level SPARQL (members, predicate violations, victim relations)
  works on real charging instruments.
- Removes a standing incentive to fabricate hierarchy and leadership nodes to
  satisfy SHACL, which is the more damaging outcome for an evidence graph than
  a missing property.
- Backward compatible. Relaxing a `minCount` never invalidates an existing
  conformant graph, so no republication of existing CAC graphs is needed.

## Risks

- **Weaker shape, weaker validation.** After the change, SHACL alone no longer
  distinguishes a well-populated enterprise from a bare stub with one member
  and one exploitation relation. Consumers that currently rely on
  `hasHierarchy` always being present would need a null check. This is the
  real cost of the proposal and the committee should weigh it deliberately.
- **Modeling drift.** Optional properties are under-populated in practice.
  Enterprises that *do* have pleaded leadership may stop asserting it. A
  `sh:Warning`-severity shape recommending `hasHierarchy` where a hierarchy is
  alleged would mitigate this without blocking honest graphs.
- **Alternative shape of the fix.** If the committee prefers to keep the
  current class as a structured-enterprise concept, an equivalent outcome is a
  superclass (e.g. `StatutoryChildExploitationEnterprise`) carrying only the
  statutory elements, with the existing class as a subclass adding hierarchy
  and leadership. That is a larger change and introduces a second term for the
  same statute; the cardinality relaxation is the smaller edit. Either
  resolves the underlying problem.

# Competencies demonstrated

## Competency 1

Retrieve child exploitation enterprises and their charged members where the
charging instrument alleges no leadership structure. Under the current shapes
this graph cannot exist, so the query has no answer set to run against.

## Competency 2

Confirm that an enterprise typed as `ChildExploitationEnterprise` still carries
its statutory elements — members and exploitation relations — even when
hierarchy and leadership are absent. This is the check that the relaxation does
not hollow out the class.

# Example instance data

`cac-enterprise-hierarchy-cardinality.jsonld` models the enterprise from
*United States v. Bermudez et al.*, No. 1:25-cr-00361-PKC (E.D.N.Y.), a public
PACER prosecution. Count One charges 18 U.S.C. §§ 2252A(g) and 3551 et seq.
against an Internet-based association-in-fact group that operated on a series
of Discord servers between 2019 and 2021. The indictment pleads the enterprise
in the statutory terms and then enumerates seventeen predicate violations
across six minor victims and four federal districts, together with the
enterprise's purposes and its means and methods.

What the instrument never alleges is a hierarchy or a leader. There is no chain
of command, no leadership tier, and no member identified as directing the
others; paragraph 7 describes members working "together and individually for
the benefit of the Enterprise", which is a peer structure.

The example graph therefore asserts `hasMember` for the charged defendants and
`hasExploitationRelation` for the victim relationships, and omits
`hasHierarchy` and `hasLeadershipRelation` because the source is silent on
both. Victims and defendants appear as label-only nodes; no identifying detail
is modeled.

`cac-enterprise-hierarchy-cardinality.ttl` and
`cac-enterprise-hierarchy-cardinality-shapes.ttl` carry the minimum term
declarations and the *proposed* (relaxed) shape, so the example can be
validated before the change lands upstream.

I am fine with my examples being transcribed and credited.

# Solution suggestion

The constraints are expressed only in SHACL. `cacontology-extremist-enterprises.ttl`
declares `hasHierarchy`, `hasLeadershipRelation`, `hasExploitationRelation` and
`hasMember` as plain `owl:ObjectProperty` with `rdfs:domain`/`rdfs:range` and no
OWL cardinality axioms, so this change touches
`cacontology-extremist-enterprises-shapes.ttl` alone. Line references below are
against that file on `main`.

* In `cacontology-enterprises:ChildExploitationEnterpriseShape`, drop
  `sh:minCount 1` from the `hasHierarchy` property shape and keep
  `sh:maxCount 1`. Update the message from "Enterprise must have exactly one
  hierarchy" to "Enterprise may have at most one hierarchy."
* In `cacontology-enterprises:GufoRelatorValidationShape`, drop `sh:minCount 1`
  from the `hasLeadershipRelation` property shape, keeping the
  `sh:class gufo:Relator` range check so any asserted value is still typed.
* Leave `hasExploitationRelation` at `sh:minCount 1` in that same
  `GufoRelatorValidationShape`, and leave `GufoMembershipValidationShape` at
  `sh:minCount 2` on `hasMember`. Note that `sh:minCount 2` already encodes a
  weaker requirement than § 2252A(g)'s "three or more other persons"; whether
  to raise it is a separate question this proposal does not reach.
* `LeadershipStructureRule` (the `sh:rule` requiring a formal leadership
  structure for enterprises whose `leadershipCount` is three or more) is
  already conditional and needs no change. It is the pattern this proposal
  generalizes: structure should be required when structure is alleged, not
  unconditionally.
* `GufoHierarchyComponentValidation` (the `sh:sparql` shape requiring an
  asserted hierarchy to be a `gufo:isComponentOf` component of the enterprise)
  also needs no change. Its `SELECT` matches only enterprises that assert
  `hasHierarchy`, so an enterprise with no hierarchy raises no violation.
* Related, and worth deciding alongside this: `ChildExploitationEnterpriseShape`
  constrains `leadershipCount` with `sh:minInclusive 1`, so a peer-structured
  enterprise cannot record `leadershipCount 0` — it can only omit the property.
  Allowing `0` would let a graph state positively that no leadership is
  alleged, rather than leaving it indistinguishable from "not yet modeled."
* Consider adding `sh:Warning`-severity shapes recommending `hasHierarchy` and
  `hasLeadershipRelation`, so under-population stays visible without blocking
  instruments that plead no structure.
* Add unit tests covering a hierarchy-bearing enterprise (still valid), a
  statute-only enterprise with neither property (newly valid), and an
  enterprise with fewer than two members (still invalid).

# Pre-submission testing

Run `make test-proposal PROPOSAL=cac-enterprise-hierarchy-cardinality`.

## SPARQL query testing

| Query | Tested | Expected results match | Notes |
|-------|--------|----------------------|-------|
| CQ 1.1 | Yes | Yes | 6 rows: the enterprise and its six charged members, with no leadership relation asserted. |
| CQ 2.1 | Yes | Yes | 1 row: `memberCount` 6, `exploitationCount` 2. The class retains its statutory elements. |
| CQ 2.2 | Yes | Yes | `ASK` returns false: no hierarchy and no leadership node was fabricated to satisfy validation. |
| CQ 3.1 | Yes | Yes | 1 row: the enterprise, `18 U.S.C. §§ 2252A(g) and 3551 et seq.`, and the 2019-2021 operating window. |

```
$ make test-proposal PROPOSAL=cac-enterprise-hierarchy-cardinality
Loaded 64 triples from change_proposals/cac-enterprise-hierarchy-cardinality.jsonld
  Query 1: 6 result(s) — OK
  Query 2: 1 result(s) — OK
  Query 3: 1 result(s) — OK
  Query 4: 1 result(s) — OK

SPARQL test summary: 4 passed, 0 failed
```

CQ 2.2 is written as `ASK` rather than `SELECT` because the correct answer is
an empty result, and the proposal test harness counts a zero-row `SELECT` as a
failure.

## Graph validation

```
$ make validate-proposal PROPOSAL=cac-enterprise-hierarchy-cardinality
Validation Report
Conforms: True
Results (12):
  ... 12 sh:Info results, all "UcoThings are suggested to end with a UUID"
```

The twelve informational results are the standard UUID-IRI suggestion against
the readable `kb:` identifiers used for legibility in this example. There are
no `sh:Violation` or `sh:Warning` results.

## Unresolved issues

- The committee should decide between the cardinality relaxation and the
  superclass alternative described under Risks. This proposal recommends the
  relaxation as the smaller and backward-compatible change.
- Several sibling classes in `cacontology-extremist-enterprises`
  (`EnterpriseHierarchy`, `MembershipTier`, `LeadershipStructure`) may carry
  the same assumption that an enterprise is necessarily structured. If the
  relaxation is accepted, those shapes are worth a consistency pass.
