# RFC: scoped evidence reassessment alongside CASE/UCO graphs

Status: **proposed; draft discussion only**  
Author: Forest Savage  
Date: 2026-10-20

## Problem and proposed outcome

A human records a scoped decision using evidence available at a particular time.
Later, a source is corrected, an extraction changes, access becomes unknown, or a
new independent record appears in the same evidence pool. A structurally valid
graph and a historically reproducible review do not by themselves show whether
that decision has been reassessed against the changed pool.

Propose an optional, offline sidecar that records the decision's scope and exact
inputs, watches a declared bounded pool, and explains which recorded decisions
need human reassessment. Preserve the prior packet and review. Do not rewrite
the decision or promote an alert into a factual or legal conclusion.

This RFC adapts patterns explored in the author's local research prototypes. It
contributes an integration contract and evaluation plan, not their source code,
a released SDK API, or evidence of investigator benefit. Maintainers should
first decide whether an adapter to an existing system would meet this contract
with less maintenance. No claim of a novel or fully solved problem is made.

## Relationship to existing SDK capabilities

The SDK already has substantial review machinery. In particular,
[the critic rules](../docs/critic/RULES.md) describe artifact hashes, provenance
sidecar verification, rule execution ledgers, finding reconciliation, and
multi-pass sessions with hash-bound finalization. Extend or consume that
machinery where its contract fits.

| Existing capability | Reuse | Question this proposal adds |
| --- | --- | --- |
| CASE/UCO graph creation and serialization | Stable graph node identifiers and existing public runtime APIs | Which human decision depends on which versioned assertion or pool? |
| SHACL validation | Record validator, shapes, ontology versions and report digest | What changed after that validation and review? |
| Critic artifact and provenance checks | Bind a packet to the reviewed artifact set and report | Did an independent candidate enter or leave the registered pool? |
| Rule execution and finding ledgers | Preserve evaluated, skipped, failed and unevaluated distinctions | Which current reassessment obligations remain open? |
| Historical audit records | Reconstruct the recorded review without changing it | Can historical reconstruction succeed while current eligibility is unknown? |

The sidecar must not bypass or relax critic finalization. A successful sidecar
scan cannot clear a critic finding. A successful critic pass cannot clear an
unassessed change in the declared evidence pool. These are separate outputs.

## First increment and boundaries

Start with a local adapter and synthetic corpus for one declared decision type.
Store ordinary JSON records and retained bytes, with an explicit transactional
store for version order and publication state. No new ontology classes or
generated language bindings are proposed in this RFC.

Keep acquisition, original records, normalized assertions, enrichment, human
assessments and review decisions distinguishable. An enriched assertion must
identify its source version and producing transformation. It must not silently
replace the source's original statement.

The first implementation would issue review requests only. It would not rank
people, establish guilt, determine probable cause, authorize investigative
action, or claim evidence admissibility. Evidence truth, complete acquisition,
authentic identity, chain of custody and court defensibility require further
controls and human processes beyond this contract.

## Proposed records

Names below are illustrative sidecar fields, not new CASE/UCO vocabulary.

| Record | Required binding and meaning |
| --- | --- |
| Source capture | Stable source ID, immutable capture/version ID, content digest and retained-byte reference, capture method, availability observation and observation time. Claimed origin remains an assertion unless independently authenticated. |
| Extraction | Input capture digest, extractor/version/configuration digest, output digest, and exact field or text locator. A text span declares its encoding and coordinate unit; reject Boolean, fractional, negative and out-of-range coordinates. |
| Assertion | Immutable assertion revision, source/extraction references, typed value, graph-node link when present, and explicit supported, conflicting or unknown assessment. A local link is checked against the declared artifact set; external reference availability is separately observed. |
| Evidence pool | Pool ID, versioned selection policy, scope and exclusions, adapter revision, ordered scan revision, observed membership and failures. New independent candidates can be discovered without a dependency edge from the old decision. |
| Decision revision | Decision ID, scope, immutable revision, criteria/policy digest, explicit dependencies, pool subscription and declared exclusions. Retirement retains the identity; successor links cannot form cycles or rebind an old ID. |
| Review receipt | Decision revision, exact packet digest, policy revision, pool scan revision and reviewed impact-set digest; actor assertion, time and disposition. No identity-assurance claim follows from a name string. |
| Publication generation | One manifest for paired machine-readable and human-readable outputs, their digests, latest scan attempt, last successful scan and publication outcome. |

Digest comparison checks content integrity under the selected algorithm. It
does not establish authenticity, independence, lawful acquisition
or factual truth. Retaining a digest without the permitted bytes is insufficient
for full reconstruction.

Compare criteria and values with explicit type tags and a versioned canonical
representation. In particular, JSON true must differ from numeric 1, and false
from 0. Define distinctions for absent, null and unavailable before coding;
reject malformed or ambiguous inputs rather than silently coercing them.

## Current state and historical state

Report separate dimensions rather than a single green/red result:

| Dimension | Example values | Constraint |
| --- | --- | --- |
| Historical replay | verified, failed, unavailable | Applies only to the frozen packet and declared runtime/policy. |
| Scan execution | complete, partial, failed, not-run | A recent attempt is not necessarily a successful scan. |
| Availability | observed-available, observed-unavailable, unknown | Retained historical bytes do not prove present source access. |
| Impact review | no-open-impact, review-required, unresolved | A receipt does not remove changed inputs. |
| Publication | current-generation, failed, unknown | Old output can remain intact while a newer scan or publish attempt failed. |

"No open impact" means no unresolved change found under the declared pool,
policy and last successful scan. It must not be displayed as "all relevant
evidence checked" or as an assurance of currentness beyond that scope.

For every impact, retain old and new revisions, the rule/policy version,
affected decision, reason, and whether that reason was evaluated successfully.
Missing or failed evaluation remains unresolved; absence of an alert after a
failed scan is not a clean result.

A human acknowledgment records a review action. It does not refresh source
captures, change a packet's inputs, dismiss another open impact, or turn an old
decision into a newly supported one. A revised decision is a new immutable
revision with its own receipt, while the old packet remains reconstructible.

## Synthetic example

Decision D1 selects one of two permitted leads under policy P1 after reviewing
records A1 and B1 from bounded pool E. The frozen packet and receipt bind those
revisions and E's scan revision 10.

1. Adapter scan 11 discovers new record C1 matching E's declared policy, with
   no dependency edge from D1. Emit a reassessment request and record why C1
   matches. Do not silently add C1 to the old packet.
2. A second item is a copy of C1. A content match alone does not establish an
   independent origin. Preserve both captures and the origin assessment;
   do not count them as two independent observations without justification.
3. A1 is replaced by corrected A2, leaving total corpus size unchanged.
   Record revision/membership change; equal counts cannot clear
   it. D1's historical A1 packet can still replay.
4. A reviewer acknowledges receipt of the alert. D1 still has an open impact
   until the scoped disposition is recorded against the exact current revisions.
5. Access to B becomes unknown. Report that fact even if B1's retained bytes
   remain available for historical reconstruction.

## Optional adapters

| Consumer | Proposed boundary | Access requirement |
| --- | --- | --- |
| SDK critic | Consume existing report/artifact hashes and rule-execution status through public interfaces; keep sidecar state separate | Review current report/schema compatibility before implementation |
| CAC Ontology | Pin ontology and SHACL versions; retain source-to-assertion links and validation reports | Use public schemas; propose vocabulary changes separately if actually needed |
| CaseLinker | Bind snapshot and extraction revisions plus declared corpus membership; distinguish historical cohorts from current corpus queries | Design a trustworthy corpus revision source; counts alone are insufficient |
| Case-management applications | Subscribe explicit decisions to permitted evidence pools; expose review reasons and frozen history | Application-specific identity, authorization and retention review |
| Licensed analysis/hash tools | Record versioned exported observations without altering their matching algorithms or copying their datasets | Documented export/API and permission to use it; no access assumed |

Adapters must preserve access markings. Do not put restricted evidence,
personal identifiers or licensed datasets in public examples, CI logs or model
prompts. The proposed reference harness would use invented identifiers and
records, operate offline and make no automatic calls to an external model. A production adapter
must enforce its own authorization before reads and exports.

## Acceptance plan before implementation is called complete

Use an independently specified oracle and preserve the original baseline. Freeze
the synthetic input records, expected transitions, policy and runtime versions
before evaluating an implementation. Distinguish test/specification consistency
from independent evidence that the specification is appropriate.

| Challenge | Required observable result |
| --- | --- |
| New in-scope candidate outside old dependency graph | Reopen the affected decision with a traceable pool-match reason |
| Out-of-scope candidate | No impact on that decision; report the bounded exclusion |
| Equal corpus count with corrected source or replaced membership | Detect changed revision/membership; do not declare currentness from count equality |
| Copy or unverified shared origin | Preserve source identities and uncertainty; do not manufacture independence |
| true/1 and false/0 policy changes, both directions | Distinct typed revisions and a new review obligation |
| Missing source link, unknown selected head, unavailable bytes | Visible unknown/unresolved state, including records without prior ordered history |
| Tampered capture/version/extraction, invalid span or malformed import | Reject or quarantine before publication, with a reason and no state promotion |
| Receipt replayed against another policy, packet or impact revision | Refuse to clear the current obligation |
| Decision retired and ID reused; cyclic successor | Reject identity reuse/cycle while preserving prior history |
| Write failure, concurrent publisher or interrupted publication | Readers see one complete old or new generation; health records the failed attempt |
| Historical replay after new evidence or access loss | Historical and current results remain separately visible |
| Rules skipped or failing; adapter scan failure | Do not convert unevaluated work into a clean result |

Add a separate relational/set-membership oracle for pool matching, including
seeded generated cases and adversarial exclusions. A SQL comparison that shares
the same specification can detect implementation disagreement but cannot prove
the specification correct. Use a fresh-process export/import replay; check
manifest and record bindings, rather than only round-tripping the same objects
in one process. Ordinary digest chains are not a signed external ledger against
an administrator who can rewrite the complete store.

For a permitted real-world pilot, predeclare scope, independent adjudicators,
comparison workflow and error categories. Measure missed changes, false review
requests, serious unsupported assertions, curation/setup effort and review time.
Do not infer operational benefit from synthetic tests. Stop or adopt an existing
extension if it meets the contract with less burden.

## Rollout and open decisions

1. Maintainers review scope, overlap and preferred host. Accepting this RFC would
   not itself accept a new runtime or vocabulary.
2. Agree on records, typed canonicalization, error behavior and oracle fixtures.
3. Build one opt-in offline adapter in a separate change, with fault injection,
   export/import replay and privacy review. Preserve current SDK behavior by
   default and do not mutate generated bindings.
4. Add consumers one at a time after their source and authorization contracts
   are understood. Qualify scale, recovery and operator workflow before a pilot.

Open questions include how to represent uncertain origin groups; how applications
provide reliable ordered corpus revisions; which existing audit/store component
to reuse; who adjudicates changes; and which review disposition vocabulary the
first consumer needs. Authentication, external attestations, real tool adapters
and measured investigator benefit are not delivered by this draft.
