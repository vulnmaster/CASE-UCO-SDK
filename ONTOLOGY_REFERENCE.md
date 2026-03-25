# CASE/UCO Ontology Reference

Auto-generated reference for all classes, properties, and vocabulary types in the CASE/UCO ontology. Use this document to discover which classes model your domain and what properties they expose.

| Metric | Count |
|--------|-------|
| Classes | 428 |
| Direct properties | 923 |
| Modules | 15 |
| Vocabulary types | 54 |

## Table of Contents

- [case.investigation](#caseinvestigation) (10 classes)
- [ext.toolcap](#exttoolcap) (2 classes)
- [uco.action](#ucoaction) (7 classes)
- [uco.analysis](#ucoanalysis) (3 classes)
- [uco.configuration](#ucoconfiguration) (3 classes)
- [uco.core](#ucocore) (21 classes)
- [uco.identity](#ucoidentity) (20 classes)
- [uco.location](#ucolocation) (4 classes)
- [uco.marking](#ucomarking) (7 classes)
- [uco.observable](#ucoobservable) (323 classes)
- [uco.pattern](#ucopattern) (3 classes)
- [uco.role](#ucorole) (4 classes)
- [uco.tool](#ucotool) (10 classes)
- [uco.types](#ucotypes) (9 classes)
- [uco.victim](#ucovictim) (2 classes)
- [Vocabulary Types](#vocabulary-types) (54 types)

## case.investigation

### Attorney

*Attorney is a role involved in preparing, interpreting, and applying law.*

**Parents:** Role | **IRI:** `https://ontology.caseontology.org/case/investigation/Attorney`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### Authorization

*An authorization is a grouping of characteristics unique to some form of authoritative permission identified for investigative action.*

**Parents:** UcoObject | **IRI:** `https://ontology.caseontology.org/case/investigation/Authorization`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| authorizationIdentifier | string | zero_or_more | No | The identifier for a particular authorization (e.g. warrant number) |
| authorizationType | string | zero_or_one | No | A label categorizing a type of authorization (e.g. warrant) |
| endTime | dateTime | zero_or_one | No | The ending time of a time range. |
| startTime | dateTime | zero_or_one | No | The initial time of a time range. |

### Examiner

*Examiner is a role involved in providing scientific evaluations of evidence that are used to aid law enforcement investigations and court cases.*

**Parents:** Role | **IRI:** `https://ontology.caseontology.org/case/investigation/Examiner`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### Investigation

*An investigation is a grouping of characteristics unique to an exploration of the facts involved in a cyber-relevant set of suspicious activity.*

**Parents:** ContextualCompilation | **IRI:** `https://ontology.caseontology.org/case/investigation/Investigation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | zero_or_more | No | Specifies one or more UcoObjects. |
| focus | string | zero_or_more | No | Specifies the topical focus of an investigation. |
| investigationForm | string | zero_or_more | No | A label categorizing a type of investigation (case, incident, suspicious-activity, etc.) |
| investigationStatus | string | zero_or_one | No | A label characterizing the status of an investigation (open, closed, etc.). |
| relevantAuthorization | Authorization | zero_or_more | No | Specifies an authorization relevant to a particular investigation. |
| endTime | dateTime | zero_or_one | No | The ending time of a time range. |
| startTime | dateTime | zero_or_one | No | The initial time of a time range. |

### InvestigativeAction

*An investigative action is something that may be done or performed within the context of an investigation, typically to examine or analyze evidence or other data.*

**Parents:** Action | **IRI:** `https://ontology.caseontology.org/case/investigation/InvestigativeAction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_one | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_one | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_one | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |
| wasInformedBy | InvestigativeAction | zero_or_more | No | A re-implementation of the wasInformedBy property in W3C PROV-O, where an entity is exchanged by two activities, 'one... |

### Investigator

*Investigator is a role involved in coordinating an investigation.*

**Parents:** Role | **IRI:** `https://ontology.caseontology.org/case/investigation/Investigator`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### ProvenanceRecord

*A provenance record is a grouping of characteristics unique to the provenantial (chronology of the ownership, custody or location) connection between an investigative action and a set of observations (items and/or actions) or interpretations that result from it.*

**Parents:** ContextualCompilation | **IRI:** `https://ontology.caseontology.org/case/investigation/ProvenanceRecord`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | zero_or_more | No | Specifies one or more UcoObjects. |
| exhibitNumber | string | zero_or_one | No | The exhibit number specifies an identifier assigned to a set of objects, unique within the scope of an investigation. |
| rootExhibitNumber | string | zero_or_more | No | The root exhibit number specifies a unique identifier assigned to a set of objects at the start of their treatment as... |

### Subject

*Subject is a role whose conduct is within the scope of an investigation.*

**Parents:** Role | **IRI:** `https://ontology.caseontology.org/case/investigation/Subject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### SubjectActionLifecycle

*A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role whose conduct may be within the scope of an investigation.*

**Parents:** ActionLifecycle | **IRI:** `https://ontology.caseontology.org/case/investigation/SubjectActionLifecycle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_more | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_more | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_more | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |
| phase | ArrayOfAction | exactly_one | Yes | The ordered set of actions or sub action-lifecycles that represent the action lifecycle. |

### VictimActionLifecycle

*A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role characterized by its potential to be harmed as a result of a crime, accident, or other event or action.*

**Parents:** ActionLifecycle | **IRI:** `https://ontology.caseontology.org/case/investigation/VictimActionLifecycle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_more | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_more | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_more | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |
| phase | ArrayOfAction | exactly_one | Yes | The ordered set of actions or sub action-lifecycles that represent the action lifecycle. |

## ext.toolcap

### CapabilityMatrix

*A capability matrix is a named, versioned collection of ToolCapability assertions that together represent a comprehensive comparison of which digital forensic tools support which applications. A CapabilityMatrix serves as the top-level container for organizing and publishing capability data, enabling forensic labs and DFIR teams to compare tool coverage, identify gaps, plan acquisitions, and track changes over time. The matrix can be serialized as a CASE/UCO-compliant JSON-LD graph and shared across organizations for interoperability.*

**Parents:** ContextualCompilation | **IRI:** `http://example.org/ontology/toolcap/CapabilityMatrix`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | zero_or_more | No | Specifies one or more UcoObjects. |
| matrixName | string | zero_or_one | No | A human-readable name for this capability matrix, used to distinguish it from other matrices (e.g., 'ICAC Messaging A... |
| matrixVersion | string | zero_or_one | No | A version string for this capability matrix, allowing consumers to track updates and changes over time (e.g., '1.0', ... |

### ToolCapability

*A tool capability is a formal assertion that a specific digital forensic tool can successfully parse, extract, or decode data from a specific application on one or more device platforms. Each ToolCapability instance links exactly one forensic tool (uco-tool:Tool) to exactly one target application (uco-observable:ObservableObject with an ApplicationFacet), and may additionally specify the platforms supported, the types of observables the tool can extract, the tool version tested, whether the capability has been independently verified, and when it was last tested. ToolCapability instances are the building blocks of a capability comparison matrix used to evaluate forensic tool coverage across the application and platform landscape.*

**Parents:** UcoObject | **IRI:** `http://example.org/ontology/toolcap/ToolCapability`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| application | ObservableObject | exactly_one | Yes | Identifies the target application (an instance of uco-observable:ObservableObject, typically with an ApplicationFacet... |
| isVerified | boolean | zero_or_one | No | A boolean flag indicating whether this tool capability has been independently verified through controlled testing (e.... |
| lastTestedDate | dateTime | zero_or_one | No | The date and time when this capability was most recently tested or verified. This is important for tracking currency ... |
| parsedObservableType | string | zero_or_more | No | A category of observable data (e.g., 'messages', 'contacts', 'call logs', 'media files', 'calendar events', 'location... |
| supportedPlatform | string | zero_or_more | No | A device platform or operating system (e.g., 'Android', 'iOS', 'Windows', 'macOS', 'Linux') on which the forensic too... |
| tool | Tool | exactly_one | Yes | Identifies the digital forensic tool (an instance of uco-tool:Tool) that possesses this capability. For example, a To... |
| toolVersion | string | zero_or_one | No | The specific version string of the forensic tool that was tested or verified to support this capability. Because fore... |

## uco.action

### Action

*An action is something that may be done or performed.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/Action`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_one | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_one | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_one | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |

### ActionArgumentFacet

*An action argument facet is a grouping of characteristics unique to a single parameter of an action.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ActionArgumentFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| argumentName | string | exactly_one | Yes | The identifying label of an argument. |
| value | string | exactly_one | Yes | The value of an action parameter. |

### ActionEstimationFacet

*An action estimation facet is a grouping of characteristics unique to decision-focused approximation aspects for an action that may potentially be performed.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ActionEstimationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| estimatedCost | string | zero_or_one | No | An estimation of the cost if the action is performed. |
| estimatedEfficacy | string | zero_or_one | No | An estimation of the effectiveness of the action at achieving its objective if the action is performed. |
| estimatedImpact | string | zero_or_one | No | An estimation of the impact if the action is performed. |
| objective | string | zero_or_one | No | The intended purpose for performing the action. |

### ActionFrequencyFacet

*An action frequency facet is a grouping of characteristics unique to the frequency of occurrence for an action.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ActionFrequencyFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| rate | decimal | exactly_one | Yes | The frequency rate for the occurence of an action. |
| scale | string | exactly_one | Yes | The time scale utilized for the frequency rate count for the occurence of an action. |
| trend | string | zero_or_more | No | A characterization of the frequency trend for the occurence of an action. |
| units | string | exactly_one | Yes | The units of measure utilized for the frequency rate count for the occurence of an action. |

### ActionLifecycle

*An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action lifecycles.*

**Parents:** Action | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ActionLifecycle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_more | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_more | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_more | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |
| phase | ArrayOfAction | exactly_one | Yes | The ordered set of actions or sub action-lifecycles that represent the action lifecycle. |

### ActionPattern

*An action pattern is a grouping of characteristics unique to a combination of actions forming a consistent or characteristic arrangement.*

**Parents:** Action, Pattern | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ActionPattern`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_one | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_one | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_one | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |

### ArrayOfAction

*An array of action is an ordered list of references to things that may be done or performed.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| action | Action | one_or_more | Yes | A characterization of a single action. |

## uco.analysis

### AnalyticResultFacet

*An analytic result facet is a grouping of characteristics unique to the results of an analysis action.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/analysis/AnalyticResultFacet`

*No direct or inherited properties.*

### ArtifactClassification

*An artifact classification is a single specific assertion that a particular class of a classification taxonomy applies to something.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassification`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| class | string | one_or_more | Yes | A specific classification class. |
| classificationConfidence | decimal | zero_or_one | No | The level of confidence that a classification assertion is correct. |

### ArtifactClassificationResultFacet

*An artifact classification result facet is a grouping of characteristics unique to the results of an artifact classification analysis action.*

**Parents:** AnalyticResultFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassificationResultFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| classification | ArtifactClassification | zero_or_more | No | An asserted classification of an analyzed artifact resulting from the analysis. |

## uco.configuration

### Configuration

*A configuration is a grouping of characteristics unique to a set of parameters or initial settings for the use of a tool, application, software, or other cyber object.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/configuration/Configuration`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| configurationEntry | ConfigurationEntry | zero_or_more | No | A single configuration setting entry item for a tool or other software. |
| dependencies | Dependency | zero_or_more | No | The relevant configuration dependencies for a tool, application, software, or other cyber object. |
| usageContextAssumptions | string | zero_or_more | No | Description of the various relevant usage context assumptions for a tool or other software . |

### ConfigurationEntry

*A configuration entry is a grouping of characteristics unique to a particular parameter or initial setting for the use of a tool, application, software, or other cyber object.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/configuration/ConfigurationEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| itemDescription | string | zero_or_one | No | A description of a configuration setting entry item. |
| itemName | string | zero_or_one | No | The name of a configuration setting entry item. |
| itemObject | UcoObject | zero_or_more | No | The structured value of a configuration setting entry instance. |
| itemType | string | zero_or_one | No | The type of a configuration setting entry item. |
| itemValue | string | zero_or_more | No | The value of a configuration setting entry instance. |

### Dependency

*A dependency is a grouping of characteristics unique to something that a tool or other software relies on to function as intended.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/configuration/Dependency`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| dependencyDescription | string | zero_or_one | No | A description of a tool or other software dependency. |
| dependencyType | string | zero_or_one | No | The type of a tool or other software dependency. |

## uco.core

### Annotation

*An annotation is an assertion made in relation to one or more objects.*

**Parents:** Assertion | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Annotation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| statement | string | zero_or_more | No | A textual statement of an assertion. |
| object | UcoObject | one_or_more | Yes | Specifies one or more UcoObjects. |

### Assertion

*An assertion is a statement declared to be true.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Assertion`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| statement | string | zero_or_more | No | A textual statement of an assertion. |

### AttributedName

*An attributed name is a name of an entity issued by some attributed naming authority.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/AttributedName`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| namingAuthority | string | zero_or_one | No | Specifies the naming authority that issued the name of the entity. |

### Bundle

*A bundle is a container for a grouping of UCO content with no presumption of shared context.*

**Parents:** EnclosingCompilation | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Bundle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | one_or_more | Yes | Specifies one or more UcoObjects. |

### Compilation

*A compilation is a grouping of things.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Compilation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### ConfidenceFacet

*A confidence is a grouping of characteristics unique to an asserted level of certainty in the accuracy of some information.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ConfidenceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| confidence | nonNegativeInteger | exactly_one | Yes | An asserted level of certainty in the accuracy of some information. |

### ContextualCompilation

*A contextual compilation is a grouping of things sharing some context (e.g., a set of network connections observed on a given day, all accounts associated with a given person).*

**Parents:** Compilation | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ContextualCompilation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | zero_or_more | No | Specifies one or more UcoObjects. |

### ControlledVocabulary

*A controlled vocabulary is an explicitly constrained set of string values.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ControlledVocabulary`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| constrainingVocabularyName | string | zero_or_one | No | The name of an explicitly constrained set of string values. |
| constrainingVocabularyReference | anyURI | zero_or_one | No | A reference to a specification for an explicitly constrained set of string values. The specification may be unstructu... |
| value | string | exactly_one | Yes | A string value. |

### EnclosingCompilation

*An enclosing compilation is a container for a grouping of things.*

**Parents:** Compilation | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/EnclosingCompilation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | one_or_more | Yes | Specifies one or more UcoObjects. |

### Event

*An Event is a noteworthy occurrence (something that happens or might happen).*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Event`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| endTime | dateTime | zero_or_more | No | The ending time of a time range. |
| eventAttribute | Dictionary | zero_or_more | No | An event attribute specifies an ad-hoc attribute/value for an event. |
| eventContext | UcoObject | zero_or_more | No | An event context describes the association of actions and objects relating to an event. |
| eventType | string | zero_or_more | No | An event type specifies a classification type for the event. |
| startTime | dateTime | zero_or_more | No | The initial time of a time range. |

### ExternalReference

*Characteristics of a reference to a resource outside of the UCO.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ExternalReference`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| definingContext | string | zero_or_one | No | A description of the context relevant to the definition of a particular external reference identifier. |
| externalIdentifier | string | zero_or_one | No | An identifier for some information defined external to the UCO context. |
| referenceURL | anyURI | zero_or_one | No | A URL for some information defined external to the UCO context. |

### Facet

*A facet is a grouping of characteristics singularly unique to a particular inherent aspect of a UCO domain object.*

**Parents:** UcoInherentCharacterizationThing | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Facet`

*No direct or inherited properties.*

### Grouping

*A grouping is a compilation of referenced UCO content with a shared context.*

**Parents:** ContextualCompilation | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Grouping`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| object | UcoObject | zero_or_more | No | Specifies one or more UcoObjects. |
| context | string | zero_or_more | No | A description of particular contextual affinity. |

### IdentityAbstraction

*An identity abstraction is a grouping of identifying characteristics unique to an individual or organization. This class is an ontological structural abstraction for this concept. Implementations of this concept should utilize the identity:Identity class.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/IdentityAbstraction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### Item

*An item is a distinct article or unit.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Item`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### MarkingDefinitionAbstraction

*A marking definition abstraction is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and shared. This class is an ontological structural abstraction for this concept. Implementations of this concept should utilize the marking:MarkingDefinition class.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/MarkingDefinitionAbstraction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### ModusOperandi

*A modus operandi is a particular method of operation (how a particular entity behaves or the resources they use).*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ModusOperandi`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### Relationship

*A relationship is a grouping of characteristics unique to an assertion that one or more objects are related to another object in some way.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/Relationship`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| endTime | dateTime | zero_or_more | No | The ending time of a time range. |
| isDirectional | boolean | exactly_one | Yes | A specification whether or not a relationship assertion is limited to the context FROM a source object(s) TO a target... |
| kindOfRelationship | string | zero_or_one | No | A characterization of the nature of a relationship between objects. |
| source | UcoObject | one_or_more | Yes | The originating node of a specified relationship. |
| startTime | dateTime | zero_or_more | No | The initial time of a time range. |
| target | UcoObject | exactly_one | Yes | The terminating node of a specified relationship. |

### UcoInherentCharacterizationThing

*A UCO inherent characterization thing is a grouping of characteristics unique to a particular inherent aspect of a UCO domain object.*

**Parents:** UcoThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/UcoInherentCharacterizationThing`

*No direct or inherited properties.*

### UcoObject

*A UCO object is a representation of a fundamental concept either directly inherent to the cyber domain or indirectly related to the cyber domain and necessary for contextually characterizing cyber domain concepts and relationships. Within the Unified Cyber Ontology (UCO) structure this is the base class acting as a consistent, unifying and interoperable foundation for all explicit and inter-relatable content objects.*

**Parents:** UcoThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/core/UcoObject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### UcoThing

*UcoThing is the top-level class within UCO.*

**IRI:** `https://ontology.unifiedcyberontology.org/uco/core/UcoThing`

*No direct or inherited properties.*

## uco.identity

### AddressFacet

*An address facet is a grouping of characteristics unique to an administrative identifier for a geolocation associated with a specific identity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/AddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| address | Location | zero_or_one | No |  |

### AffiliationFacet

*An affiliation is a grouping of characteristics unique to the established affiliations of an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/AffiliationFacet`

*No direct or inherited properties.*

### BirthInformationFacet

*Birth information is a grouping of characteristics unique to information pertaining to the birth of an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/BirthInformationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| birthdate | dateTime | zero_or_one | No |  |

### CountryOfResidenceFacet

*Country of residence is a grouping of characteristics unique to information related to the country, or countries, where an entity resides.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/CountryOfResidenceFacet`

*No direct or inherited properties.*

### EventsFacet

*Events is a grouping of characteristics unique to information related to specific relevant things that happen in the lifetime of an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/EventsFacet`

*No direct or inherited properties.*

### IdentifierFacet

*Identifier is a grouping of characteristics unique to information that uniquely and specifically identities an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/IdentifierFacet`

*No direct or inherited properties.*

### Identity

*An identity is a grouping of identifying characteristics unique to an individual or organization.*

**Parents:** IdentityAbstraction | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/Identity`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### IdentityFacet

*An identity facet is a grouping of characteristics unique to a particular aspect of an identity.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/IdentityFacet`

*No direct or inherited properties.*

### LanguagesFacet

*Languages is a grouping of characteristics unique to specific syntactically and grammatically standardized forms of communication (human or computer) in which an entity has proficiency (comprehends, speaks, reads, or writes).*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/LanguagesFacet`

*No direct or inherited properties.*

### NationalityFacet

*Nationality is a grouping of characteristics unique to the condition of an entity belonging to a particular nation.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/NationalityFacet`

*No direct or inherited properties.*

### OccupationFacet

*Occupation is a grouping of characteristics unique to the job or profession of an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/OccupationFacet`

*No direct or inherited properties.*

### Organization

*An organization is a grouping of identifying characteristics unique to a group of people who work together in an organized way for a shared purpose. [based on https://dictionary.cambridge.org/us/dictionary/english/organization]*

**Parents:** Identity | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/Organization`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### OrganizationDetailsFacet

*Organization details is a grouping of characteristics unique to an identity representing an administrative and functional structure.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/OrganizationDetailsFacet`

*No direct or inherited properties.*

### Person

*A person is a grouping of identifying characteristics unique to a human being regarded as an individual. [based on https://www.lexico.com/en/definition/person]*

**Parents:** Identity | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/Person`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### PersonalDetailsFacet

*Personal details is a grouping of characteristics unique to an identity representing an individual person.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/PersonalDetailsFacet`

*No direct or inherited properties.*

### PhysicalInfoFacet

*Physical info is a grouping of characteristics unique to the outwardly observable nature of an individual person.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/PhysicalInfoFacet`

*No direct or inherited properties.*

### QualificationFacet

*Qualification is a grouping of characteristics unique to particular skills, capabilities or their related achievements (educational, professional, etc.) of an entity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/QualificationFacet`

*No direct or inherited properties.*

### RelatedIdentityFacet

*<Needs fleshed out from CIQ>*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/RelatedIdentityFacet`

*No direct or inherited properties.*

### SimpleNameFacet

*A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John Smith Jr.) held by an identity.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/SimpleNameFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| familyName | string | zero_or_more | No |  |
| givenName | string | zero_or_more | No |  |
| honorificPrefix | string | zero_or_more | No |  |
| honorificSuffix | string | zero_or_more | No |  |

### VisaFacet

*Visa is a grouping of characteristics unique to information related to a person's ability to enter, leave, or stay for a specified period of time in a country.*

**Parents:** IdentityFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/identity/VisaFacet`

*No direct or inherited properties.*

## uco.location

### GPSCoordinatesFacet

*A GPS coordinates facet is a grouping of characteristics unique to the expression of quantified dilution of precision (DOP) for an asserted set of geolocation coordinates typically associated with satellite navigation such as the Global Positioning System (GPS).*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/location/GPSCoordinatesFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| hdop | decimal | zero_or_one | No | The horizontal dilution of precision of the GPS location. |
| pdop | decimal | zero_or_one | No | The positional (3D) dilution of precision of the GPS location. |
| tdop | decimal | zero_or_one | No | The temporal dilution of precision of the GPS location. |
| vdop | decimal | zero_or_one | No | The vertical dilution of precision of the GPS location. |

### LatLongCoordinatesFacet

*A lat long coordinates facet is a grouping of characteristics unique to the expression of a geolocation as the intersection of specific latitude, longitude, and altitude values.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/location/LatLongCoordinatesFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| altitude | decimal | zero_or_one | No | The altitude coordinate of a geolocation. |
| latitude | decimal | zero_or_one | No | The latitude coordinate of a geolocation. |
| longitude | decimal | zero_or_one | No | The longitude coordinate of a geolocation. |

### Location

*A location is a geospatial place, site, or position.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/location/Location`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### SimpleAddressFacet

*A simple address facet is a grouping of characteristics unique to a geolocation expressed as an administrative address.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/location/SimpleAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressType | string | zero_or_one | No | The type of the address, for instance home or work. |
| country | string | zero_or_one | No | The name of the geolocation country. |
| locality | string | zero_or_one | No | The name of the geolocation locality (e.g., city). |
| postalCode | string | zero_or_one | No | The zip-code. |
| region | string | zero_or_one | No | The name of the geolocation region (e.g., state). |
| street | string | zero_or_one | No | The name of the street. |

## uco.marking

### GranularMarking

*A granular marking is a grouping of characteristics unique to specification of marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) that apply to particular portions of a particular UCO object.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/GranularMarking`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contentSelectors | string | zero_or_more | No | Explicit specification of exactly which portions of a UCO object to apply marking definitions to.   Specific syntax f... |
| marking | MarkingDefinition | zero_or_more | No | Represents specific marking definitions to be applied to UCO data. |

### LicenseMarking

*A license marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey details of license restrictions that apply to the data.*

**Parents:** MarkingModel | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/LicenseMarking`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| definitionType | string | zero_or_more | No | Specifies the Marking Model for a Marking Definition. |
| license | string | exactly_one | Yes | Specifies the identifier for the type of license |

### MarkingDefinition

*A marking definition is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and shared.*

**Parents:** MarkingDefinitionAbstraction | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| definition | MarkingModel | zero_or_more | No | Explicit specification of a data marking instance. |
| definitionType | string | exactly_one | Yes | Specifies the Marking Model for a Marking Definition. |

### MarkingModel

*A marking model is a grouping of characteristics unique to the expression of a particular form of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared).*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/MarkingModel`

*No direct or inherited properties.*

### ReleaseToMarking

*A release-to marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey details of authorized persons and/or organizations to which to the associated content may be released. The existence of the Release-To marking restricts access to ONLY those identities explicitly listed, regardless of whether another data marking exists that allows sharing with other members of the community.*

**Parents:** MarkingModel | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/ReleaseToMarking`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| authorizedIdentities | string | one_or_more | Yes | Specifies the identities that are authorized to access the data to which the data marking is associated.  The list of... |
| definitionType | string | zero_or_more | No | Specifies the Marking Model for a Marking Definition. |

### StatementMarking

*A statement marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey details of a textual marking statement, (e.g., copyright) whose semantic meaning should apply to the associated content. Statement markings are generally not machine-readable. An example of this would be a simple marking to apply copyright information, such as 'Copyright 2014 Acme Inc.'.*

**Parents:** MarkingModel | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/StatementMarking`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| definitionType | string | zero_or_more | No | Specifies the Marking Model for a Marking Definition. |
| statement | string | exactly_one | Yes | Specifies the statement to apply to the structure for which the Marking is to be applied. |

### TermsOfUseMarking

*A terms of use marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey details of a textual statement specifying the Terms of Use (that is, the conditions under which the content may be shared, applied, or otherwise used) of the marked content. An example of this would be used to communicate a simple statement, such as 'Acme Inc. is not responsible for the content of this file'.*

**Parents:** MarkingModel | **IRI:** `https://ontology.unifiedcyberontology.org/uco/marking/TermsOfUseMarking`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| definitionType | string | zero_or_more | No | Specifies the Marking Model for a Marking Definition. |
| termsOfUse | string | exactly_one | Yes | Specifies the terms of use that apply to the structure for which the Marking is to be applied. |

## uco.observable

### API

*An API (application programming interface) is a computing interface that defines interactions between multiple software or mixed hardware-software intermediaries. It defines the kinds of calls or requests that can be made, how to make them, the data formats that should be used, the conventions to follow, etc. [based on https://en.wikipedia.org/wiki/API]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/API`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ARPCache

*An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that are created when an IP address is resolved to a MAC address (so the computer can effectively communicate with the IP address). [based on https://en.wikipedia.org/wiki/ARP_cache]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ARPCache`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ARPCacheEntry

*An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created when an IP address is resolved to a MAC address (so the computer can effectively communicate with the IP address). [based on https://en.wikipedia.org/wiki/ARP_cache]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ARPCacheEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Account

*An account is an arrangement with an entity to enable and control the provision of some capability or service.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Account`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AccountAuthenticationFacet

*An account authentication facet is a grouping of characteristics unique to the mechanism of accessing an account.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AccountAuthenticationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| password | string | zero_or_one | No | Specifies an authentication password. |
| passwordLastChanged | dateTime | zero_or_one | No | The date and time that the password was last changed. |
| passwordType | string | zero_or_one | No | The type of password, for instance plain-text or encrypted. |

### AccountFacet

*An account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accountIdentifier | string | zero_or_one | No | The unique identifier for the account. |
| accountIssuer | UcoObject | zero_or_one | No | The issuer of this account. |
| accountType | string | zero_or_more | No | The type of account, for instance bank, phone, application, service, etc. |
| expirationTime | dateTime | zero_or_one | No | The date and time at which the validity of the object expires. |
| isActive | boolean | zero_or_one | No | Indicates whether the network connection is still active. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| owner | UcoObject | zero_or_one | No | Specifies the owner of an Observable Object. |

### Adaptor

*An adaptor is a device that physically converts the pin outputs but does not alter the underlying protocol (e.g. uSD to SD, CF to ATA, etc.)*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Adaptor`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Address

*An address is an identifier assigned to enable routing and management of information.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Address`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AlternateDataStream

*An alternate data stream is data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from access by default NTFS file viewing mechanisms.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStream`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AlternateDataStreamFacet

*An alternate data stream facet is a grouping of characteristics unique to data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from access by default NTFS file viewing mechanisms.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStreamFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| hashes | Hash | zero_or_one | No | Specifies any hashes computed over the section. |
| size | integer | zero_or_one | No | Specifies the size of the section, in bytes. |

### AndroidDevice

*An Android device is a device running the Android operating system. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AndroidDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AndroidDeviceFacet

*An Android device facet is a grouping of characteristics unique to an Android device. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AndroidDeviceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| androidFingerprint | string | zero_or_one | No | A string that uniquely identifies a build of the Android operating system. [based on https://developer.android.com/re... |
| androidID | hexBinary | zero_or_one | No | A 64-bit number (expressed as a hexadecimal string), unique to each combination of app-signing key, user, and device.... |
| androidVersion | string | zero_or_one | No | The user-visible version string. E.g., '1.0' or '3.4b5' or 'bananas'. This field is an opaque string. Do not assume t... |
| isADBRootEnabled | boolean | zero_or_one | No | Root access through the Android Debug Bridge (ADB) daemon observed to be enabled. [based on https://developer.android... |
| isSURootEnabled | boolean | zero_or_one | No | Root access through Linux SU binary observed to be enabled. [based on https://en.wikipedia.org/wiki/Rooting_(Android)] |

### AndroidPhone

*An android phone is a smart phone that applies the Android mobile operating system.*

**Parents:** AndroidDevice, SmartPhone | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AndroidPhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AntennaFacet

*An antenna alignment facet contains the metadata surrounding the cell tower's antenna position.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AntennaFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| antennaHeight | decimal | zero_or_one | No | The height (in meters) of the antenna from the ground. |
| azimuth | decimal | zero_or_one | No | The median rotation in degrees around a vertical axis of the cell antenna sector accessed. |
| elevation | decimal | zero_or_one | No | The angle in degrees of the antenna from the local horizontal plane. |
| horizontalBeamWidth | decimal | zero_or_one | No | The width of the antenna beam in degrees. |
| signalStrength | decimal | zero_or_one | No | The strength of the antenna signal. |
| skew | decimal | zero_or_one | No | The angle in degrees of the radial rotation around its main beam direction. |

### AppleDevice

*An apple device is a smart device that applies either the MacOS or iOS operating system.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AppleDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Appliance

*An appliance is a purpose-built computer with software or firmware that is designed to provide a specific computing capability or resource. [based on https://en.wikipedia.org/wiki/Computer_appliance]*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Appliance`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Application

*An application is a particular software program designed for end users.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Application`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ApplicationAccount

*An application account is an account within a particular software program designed for end users.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ApplicationAccountFacet

*An application account facet is a grouping of characteristics unique to an account within a particular software program designed for end users.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |

### ApplicationFacet

*An application facet is a grouping of characteristics unique to a particular software program designed for end users.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ApplicationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| applicationIdentifier | string | zero_or_one | No |  |
| installedVersionHistory | ApplicationVersion | zero_or_more | No | Specifies the history of installed application version(s). |
| numberOfLaunches | integer | zero_or_one | No |  |
| operatingSystem | ObservableObject | zero_or_one | No |  |
| version | string | zero_or_one | No |  |

### ApplicationVersion

*An application version is a grouping of characteristics unique to a particular software program version.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ApplicationVersion`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| installDate | dateTime | zero_or_one | No | Specifies the date the operating system or application was installed. |
| uninstallDate | dateTime | zero_or_one | No | Specifies the date the operating system or application was uninstalled. |
| version | string | zero_or_one | No |  |

### ArchiveFile

*An archive file is a file that is composed of one or more computer files along with metadata.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ArchiveFileFacet

*An archive file facet is a grouping of characteristics unique to a file that is composed of one or more computer files along with metadata.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| archiveType | string | zero_or_one | No | The type of a file archive, e.g. ZIP, GZIP or RAR. |
| comment | string | zero_or_one | No |  |
| version | string | zero_or_one | No |  |

### Audio

*Audio is a digital representation of sound.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Audio`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AudioFacet

*An audio facet is a grouping of characteristics unique to a digital representation of sound.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AudioFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| audioType | string | zero_or_one | No | The type of a audio. For example: music or speech. |
| bitRate | integer | zero_or_one | No | The bitrate of the audio in bits per second. |
| duration | integer | zero_or_one | No | The duration of the phone call in seconds. |
| format | string | zero_or_one | No | The format of the audio. For example: mp3 or flac. |

### AutonomousSystem

*An autonomous system is a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain that presents a common, clearly defined routing policy to the Internet. [based on https://en.wikipedia.org/wiki/Autonomous_system_(Internet)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystem`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### AutonomousSystemFacet

*An autonomous system facet is a grouping of characteristics unique to a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain that presents a common, clearly defined routing policy to the Internet. [based on https://en.wikipedia.org/wiki/Autonomous_system_(Internet)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystemFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| asHandle | string | zero_or_one | No |  |
| number | integer | zero_or_one | No |  |
| regionalInternetRegistry | string | zero_or_more | No | specifies the name of the Regional Internet Registry (RIR) which allocated the IP address contained in a WHOIS entry. |

### BlackberryPhone

*A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blackberry 10 re-introduces Blackberry OS, prior to that the OS was Android.)*

**Parents:** SmartPhone | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BlackberryPhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BlockDeviceNode

*A block device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing buffered randomly accesible input and output. Block device nodes are used to apply access rights to the devices and to direct operations on the files to the appropriate device drivers. [based on https://en.wikipedia.org/wiki/Unix_file_types]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BlockDeviceNode`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BluetoothAddress

*A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards conformant communication to or from that device.*

**Parents:** MACAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BluetoothAddressFacet

*A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards conformant communication to or from that device.*

**Parents:** MACAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### BotConfiguration

*A bot configuration is a set of contextual settings for a software application that runs automated tasks (scripts) over the Internet at a much higher rate than would be possible for a human alone.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BotConfiguration`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BrowserBookmark

*A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on https://techterms.com/definition/bookmark]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmark`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BrowserBookmarkFacet

*A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on https://techterms.com/definition/bookmark]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmarkFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accessedTime | dateTime | zero_or_one | No | The date and time at which the Object was accessed. |
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| bookmarkPath | string | zero_or_one | No | The folder containing the bookmark. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| urlTargeted | anyURI | zero_or_more | No | The target of the bookmark. |
| visitCount | integer | zero_or_one | No | Specifies the number of times a URL has been visited by a particular web browser. |

### BrowserCookie

*A browser cookie is a piece of of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on https://en.wikipedia.org/wiki/HTTP_cookie]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookie`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### BrowserCookieFacet

*A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on https://en.wikipedia.org/wiki/HTTP_cookie]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookieFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accessedTime | dateTime | zero_or_one | No | The date and time at which the Object was accessed. |
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| cookieDomain | ObservableObject | zero_or_one | No | The domain for which the cookie is stored, for example nfi.minjus.nl. |
| cookieName | string | zero_or_one | No | The name of the cookie. |
| cookiePath | string | zero_or_one | No | String representation of the path of the cookie. |
| expirationTime | dateTime | zero_or_one | No | The date and time at which the validity of the object expires. |
| isSecure | boolean | zero_or_one | No | Is the cookie secure? If the cookie is secure it cannot be delivered over an unencrypted session such as http. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |

### Calendar

*A calendar is a collection of appointments, meetings, and events.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Calendar`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CalendarEntry

*A calendar entry is an appointment, meeting or event within a collection of appointments, meetings and events.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CalendarEntryFacet

*A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or event within a collection of appointments, meetings, and events.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntryFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| attendant | Identity | zero_or_more | No | The attendants of the event. |
| duration | integer | zero_or_one | No | The duration of the phone call in seconds. |
| endTime | dateTime | zero_or_one | No |  |
| eventStatus | string | zero_or_one | No | The status of the event, for instance accepted, pending or cancelled. |
| eventType | string | zero_or_one | No | The type of the event, for example 'information', 'warning' or 'error'. |
| isPrivate | boolean | zero_or_one | No | Is the event marked as private? |
| location | Location | zero_or_one | No | An associated location. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| owner | UcoObject | zero_or_one | No | Specifies the owner of an Observable Object. |
| recurrence | string | zero_or_one | No | Recurrence of the event. |
| remindTime | dateTime | zero_or_one | No |  |
| startTime | dateTime | zero_or_one | No |  |
| subject | string | zero_or_one | No | The subject of the email. |

### CalendarFacet

*A calendar facet is a grouping of characteristics unique to a collection of appointments, meetings, and events.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CalendarFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| owner | UcoObject | zero_or_one | No | Specifies the owner of an Observable Object. |

### Call

*A call is a connection as part of a realtime cyber communication between one or more parties.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Call`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CallFacet

*A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber communication between one or more parties.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CallFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| callType | string | zero_or_one | No | The type of a phone call,for example incoming, outgoing, missed. |
| duration | integer | zero_or_one | No | The duration of the phone call in seconds. |
| endTime | dateTime | zero_or_one | No |  |
| from | ObservableObject | zero_or_one | No | The phone number of the initiating party. |
| participant | ObservableObject | zero_or_more | No |  |
| startTime | dateTime | zero_or_one | No |  |
| to | ObservableObject | zero_or_more | No | The receiver's phone number. |

### CapturedTelecommunicationsInformation

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CapturedTelecommunicationsInformationFacet

*A captured telecommunications information facet represents certain information within captured or intercepted telecommunications data.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| captureCellSite | CellSite | exactly_one | Yes | Specifies the cell site accessed. |
| endTime | dateTime | zero_or_one | No |  |
| interceptedCallState | string | zero_or_one | No | State of the call in a Call Detail Record (e.g. idle). |
| startTime | dateTime | zero_or_one | No |  |

### CellSite

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CellSite`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CellSiteFacet

*A cell site facet contains the metadata surrounding the cell site.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CellSiteFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| cellSiteCountryCode | string | zero_or_one | No | The country code represents the country of the cell site. For GSM, this is the Mobile Country Code (MCC). |
| cellSiteIdentifier | string | zero_or_one | No | Specifies the unique number used to identify each Cell Site within a location area code. |
| cellSiteLocationAreaCode | string | zero_or_one | No | The location area code is a unique number of current location area of the cell site. A location area is a set of cell... |
| cellSiteNetworkCode | string | zero_or_one | No | This code identifies the mobile operator of the cell site. For GSM, this is the Mobile Network Code (MNC) and for CMD... |
| cellSiteType | string | zero_or_one | No | Specifies the technology used by the Cell Site (e.g., GSM, CDMA, or LTE). |

### CharacterDeviceNode

*A character device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing only a serial stream of input or accepting a serial stream of output. Character device nodes are used to apply access rights to the devices and to direct operations on the files to the appropriate device drivers. [based on https://en.wikipedia.org/wiki/Unix_file_types]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CharacterDeviceNode`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Code

*Code is a direct representation (source, byte or binary) of a collection of computer instructions that form software which tell a computer how to work. [based on https://en.wikipedia.org/wiki/Software]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Code`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CompressedStreamFacet

*A compressed stream facet is a grouping of characteristics unique to the application of a size-reduction process to a body of data content.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CompressedStreamFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| compressionMethod | string | zero_or_one | No | The algorithm used to compress the data. |
| compressionRatio | decimal | zero_or_one | No | The compression ratio of the compressed data. |

### Computer

*A computer is an electronic device for storing and processing data, typically in binary, according to instructions given to it in a variable program. [based on 'Computer.' Oxford English Dictionary, Oxford University Press, 2022.]*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Computer`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ComputerSpecification

*A computer specification is the hardware and software of a programmable electronic device that can store, retrieve, and process data. {based on merriam-webster.com/dictionary/computer]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecification`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ComputerSpecificationFacet

*A computer specificaiton facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data. [based on merriam-webster.com/dictionary/computer]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecificationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| availableRam | integer | zero_or_one | No | Specifies the amount of physical memory available on the system, in bytes. |
| biosDate | dateTime | zero_or_one | No | Specifies the date of the BIOS (e.g. the datestamp of the BIOS revision). |
| biosManufacturer | string | zero_or_one | No | Specifies the manufacturer of the BIOS. |
| biosReleaseDate | dateTime | zero_or_one | No | Specifies the date the BIOS was released. |
| biosSerialNumber | string | zero_or_one | No | Specifies the serial number of the BIOS. |
| biosVersion | string | zero_or_one | No | Specifies the version of the BIOS. |
| cpu | string | zero_or_one | No | Specifies the name of the CPU used by the system. |
| cpuFamily | string | zero_or_one | No | Specifies the name of the CPU family used by the system. |
| currentSystemDate | dateTime | zero_or_one | No | Specifies the current date on the system. |
| gpu | string | zero_or_one | No | Specifies the name of the GPU used by the system. |
| gpuFamily | string | zero_or_one | No | Specifies the name of the GPU family used by the system. |
| hostname | string | zero_or_one | No | Specifies the hostname of the system. |
| localTime | dateTime | zero_or_one | No | Specifies the local time on the system. |
| networkInterface | ObservableObject | zero_or_more | No | Specifies the list of network interfaces present on the system. |
| processorArchitecture | string | zero_or_one | No | Specifies the specific architecture (e.g. x86) used by the CPU of the system. |
| systemTime | dateTime | zero_or_one | No |  |
| timezoneDST | string | zero_or_one | No | Specifies the time zone used by the system, taking daylight savings time (DST) into account. |
| timezoneStandard | string | zero_or_one | No | Specifies the time zone used by the system, without taking daylight savings time (DST) into account. |
| totalRam | integer | zero_or_one | No | Specifies the total amount of physical memory present on the system, in bytes. |
| uptime | string | zero_or_one | No | Specifies the duration that represents the current amount of time that the system has been up. |

### ConfiguredSoftware

*A ConfiguredSoftware is a Software that is known to be configured to run in a more specified manner than some unconfigured or less-configured Software.*

**Parents:** Software | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ConfiguredSoftware`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |
| isConfigurationOf | Software | zero_or_one | No | The object which has been configured to run in a more specified manner than another object.  This property is expecte... |
| usesConfiguration | Configuration | zero_or_one | No | A configuration used by an object. |

### Contact

*A contact is a set of identification and communication related details for a single entity.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Contact`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ContactAddress

*A contact address is a grouping of characteristics unique to a geolocation address of a contact entity.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactAddressScope | string | zero_or_more | No | Contact address scope specifies the relevant scope (home, work, school, etc) for a geolocation address of a contact e... |
| geolocationAddress | Location | zero_or_one | No | An administrative address for a particular geolocation. |

### ContactAffiliation

*A contact affiliation is a grouping of characteristics unique to details of an organizational affiliation for a single contact entity.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactAffiliation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactEmail | ContactEmail | zero_or_more | No | Contact email specifies information characterizing details for contacting a contact entity by email. |
| contactMessaging | ContactMessaging | zero_or_more | No | Contact messaging specifies information characterizing details for contacting a contact entity by digital messaging. |
| contactOrganization | Organization | zero_or_one | No | The name of the organization a contact works for or is assocciated with. |
| contactPhone | ContactPhone | zero_or_more | No | Contact phone specifies information characterizing details for contacting a contact entity by telephone. |
| contactProfile | ContactProfile | zero_or_more | No | Contact profile specifies information characterizing details for contacting a contact entity by online service. |
| contactURL | ContactURL | zero_or_more | No | Contact URL specifies information characterizing details for contacting a contact entity by Uniform Resource Locator ... |
| organizationDepartment | string | zero_or_one | No | Specifies a particular suborganization (division, branch, office, etc.) that exists within a larger organization. |
| organizationLocation | ContactAddress | zero_or_more | No | Specifies a geolocation address of an organization. |
| organizationPosition | string | zero_or_one | No | Specifies the title or role that a person plays within an organization. |

### ContactEmail

*A contact email is a grouping of characteristics unique to details for contacting a contact entity by email.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactEmailScope | string | zero_or_more | No | Contact email scope specifies the relevant scope (home, work, school, etc) of details for contacting a contact entity... |
| emailAddress | ObservableObject | zero_or_one | No | An email address. |

### ContactFacet

*A contact facet is a grouping of characteristics unique to a set of identification and communication related details for a single entity.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| birthdate | dateTime | zero_or_one | No |  |
| contactAddress | ContactAddress | zero_or_more | No | Contact address specifies information characterizing a geolocation address of a contact entity. |
| contactAffiliation | ContactAffiliation | zero_or_more | No | Contact affiliation specifies information characterizing details of an organizational affiliation for a single contac... |
| contactEmail | ContactEmail | zero_or_more | No | Contact email specifies information characterizing details for contacting a contact entity by email. |
| contactGroup | string | zero_or_more | No | Contact group specifies the name/tag of a particular named/tagged grouping of contacts. |
| contactID | string | zero_or_one | No | Specifies an ID for the contact. |
| contactMessaging | ContactMessaging | zero_or_more | No | Contact messaging specifies information characterizing details for contacting a contact entity by digital messaging. |
| contactNote | string | zero_or_more | No | Contact note specifies a comment/note associated with a given contact. |
| contactPhone | ContactPhone | zero_or_more | No | Contact phone specifies information characterizing details for contacting a contact entity by telephone. |
| contactProfile | ContactProfile | zero_or_more | No | Contact profile specifies information characterizing details for contacting a contact entity by online service. |
| contactSIP | ContactSIP | zero_or_more | No | Contact SIP specifies information characterizing details for contacting a contact entity by Session Initiation Protoc... |
| contactURL | ContactURL | zero_or_more | No | Contact URL specifies information characterizing details for contacting a contact entity by Uniform Resource Locator ... |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |
| firstName | string | zero_or_one | No | The first name of a person. |
| lastName | string | zero_or_one | No | The last name of a person. |
| lastTimeContacted | dateTime | zero_or_one | No | Last time contacted specifies the date and time that a particular contact was last contacted. |
| middleName | string | zero_or_one | No | The middle name of a person. |
| namePhonetic | string | zero_or_one | No | Name phonetic specifies the phonetic pronunciation of the name of a person. |
| namePrefix | string | zero_or_one | No | Name prefix specifies an honorific prefix (coming ordinally before first/given name) for the name of a person. |
| nameSuffix | string | zero_or_one | No | Name suffix specifies an suffix (coming ordinally after last/family name) for the name of a person. |
| nickname | string | zero_or_more | No | Nickname specifies an alternate, unofficial and typically informal name for a person independent of their official name. |
| numberTimesContacted | integer | zero_or_one | No | Number times contacted specifies the number of times a particular contact has been contacted. |
| sourceApplication | ObservableObject | zero_or_one | No | Source application specifies the software application that a particular contact or contact list is associated with. |

### ContactList

*A contact list is a set of multiple individual contacts such as that found in a digital address book.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactList`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ContactListFacet

*A contact list facet is a grouping of characteristics unique to a set of multiple individual contacts such as that found in a digital address book.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactListFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contact | ObservableObject | zero_or_more | No | Contact specifies information characterizing contact details for a single entity. |
| sourceApplication | ObservableObject | zero_or_one | No | Source application specifies the software application that a particular contact or contact list is associated with. |

### ContactMessaging

*A contact messaging is a grouping of characteristics unique to details for contacting a contact entity by digital messaging.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactMessagingPlatform | ObservableObject | zero_or_one | No | A contact messaging platform specifies a digital messaging platform associated with a contact. |
| messagingAddress | ObservableObject | zero_or_one | No | A messaging address specifies details of an identifier for digital messsaging communication. |

### ContactPhone

*A contact phone is a grouping of characteristics unique to details for contacting a contact entity by telephone.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactPhoneNumber | ObservableObject | zero_or_one | No | Contact phone number specifies a telephone service account number for contacting a contact entity by telephone. |
| contactPhoneScope | string | zero_or_more | No | Contact phone scope specifies the relevant scope (home, work, school, etc) of details for contacting a contact entity... |

### ContactProfile

*A contact profile is a grouping of characteristics unique to details for contacting a contact entity by online service.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactProfilePlatform | ObservableObject | zero_or_one | No | A contact profile platform specifies an online service platform associated with a contact. |
| profile | ObservableObject | zero_or_one | No | A profile specifies a particular online service profile. |

### ContactSIP

*A contact SIP is a grouping of characteristics unique to details for contacting a contact entity by Session Initiation Protocol (SIP).*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactSIP`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactSIPScope | string | zero_or_more | No | Contact SIP scope specifies the relevant scope (home, work, school, etc) of details for contacting a contact entity b... |
| sipAddress | ObservableObject | zero_or_one | No | A SIP address specifies Session Initiation Protocol (SIP) identifier. |

### ContactURL

*A contact URL is a grouping of characteristics unique to details for contacting a contact entity by Uniform Resource Locator (URL).*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContactURL`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactURLScope | string | zero_or_more | No | Contact url scope specifies the relevant scope (homepage, home, work, school, etc) of details for contacting a contac... |
| url | ObservableObject | zero_or_one | No | Specifies a URL associated with a particular observable object or facet. |

### ContentData

*Content data is a block of digital data.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContentData`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ContentDataFacet

*A content data facet is a grouping of characteristics unique to a block of digital data.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ContentDataFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| byteOrder | string | zero_or_more | No |  |
| dataPayload | string | zero_or_one | No |  |
| dataPayloadReferenceURL | ObservableObject | zero_or_one | No |  |
| entropy | decimal | zero_or_one | No | Shannon entropy (a measure of randomness) of the data. |
| hash | Hash | zero_or_more | No | Hash values of the data. |
| isEncrypted | boolean | zero_or_one | No |  |
| magicNumber | string | zero_or_one | No |  |
| mimeClass | string | zero_or_one | No |  |
| mimeType | string | zero_or_more | No | MIME type of the data. For example 'text/html' or 'audio/mp3'. |
| sizeInBytes | integer | zero_or_one | No | The size of the data in bytes. |

### CookieHistory

*A cookie history is the stored web cookie history for a particular web browser.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CookieHistory`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Credential

*A credential is a single specific login and password combination for authorization of access to a digital account or system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Credential`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### CredentialDump

*A credential dump is a collection (typically forcibly extracted from a system) of specific login and password combinations for authorization of access to a digital account or system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/CredentialDump`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DNSCache

*An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query results (created when an domain name is resolved to a IP address) for a particular computer.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DNSCache`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DNSRecord

*A DNS record is a single Domain Name System (DNS) artifact specifying information of a particular type (routing, authority, responsibility, security, etc.) for a specific Internet domain name.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DNSRecord`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DataRangeFacet

*A data range facet is a grouping of characteristics unique to a particular contiguous scope within a block of digital data.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DataRangeFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| rangeOffset | integer | zero_or_one | No | The offset at which the start of data can be found, relative to the rangeOffsetType defined. |
| rangeOffsetType | string | zero_or_one | No | The type of offset defined for the range (e.g., image, file, address). |
| rangeSize | integer | zero_or_one | No | The size of the data in bytes. |

### DefinedEffectFacet

*A defined effect facet is a grouping of characteristics unique to the effect of an observable action in relation to one or more observable objects.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DefinedEffectFacet`

*No direct or inherited properties.*

### Device

*A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.com/dictionary/device]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Device`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DeviceFacet

*A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.com/dictionary/device]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DeviceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| cpeid | string | zero_or_one | No | Specifies the Common Platform Enumeration identifier for the software. |
| deviceType | string | zero_or_one | No |  |
| manufacturer | Identity | zero_or_one | No |  |
| model | string | zero_or_one | No |  |
| serialNumber | string | zero_or_one | No |  |

### DigitalAccount

*A digital account is an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.*

**Parents:** Account | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DigitalAccountFacet

*A digital account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accountLogin | string | zero_or_more | No | The login identifier for the digital account. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |
| firstLoginTime | dateTime | zero_or_one | No | The date and time of the first login of the account. |
| isDisabled | boolean | zero_or_one | No | Is the digital account disabled? |
| lastLoginTime | dateTime | zero_or_one | No | The date and time of the last login of the account. |

### DigitalAddress

*A digital address is an identifier assigned to enable routing and management of digital communication.*

**Parents:** Address | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DigitalAddressFacet

*A digital address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of digital communication.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### DigitalCamera

*A digital camera is a camera that captures photographs in digital memory as opposed to capturing images on photographic film.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalCamera`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DigitalSignatureInfo

*A digital signature info is a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfo`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DigitalSignatureInfoFacet

*A digital signature info facet is a grouping of characteristics unique to a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfoFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| certificateIssuer | Identity | zero_or_one | No |  |
| certificateSubject | UcoObject | zero_or_one | No |  |
| signatureDescription | string | zero_or_one | No |  |
| signatureExists | boolean | zero_or_one | No |  |
| signatureVerified | boolean | zero_or_one | No |  |

### Directory

*A directory is a file system cataloging structure which contains references to other computer files, and possibly other directories. On many computers, directories are known as folders, or drawers, analogous to a workbench or the traditional office filing cabinet. In UNIX a directory is implemented as a special file. [based on https://en.wikipedia.org/wiki/Directory_(computing)]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Directory`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Disk

*A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Disk`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DiskFacet

*A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DiskFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| diskSize | integer | zero_or_one | No | The size of the disk, in bytes. |
| diskType | string | zero_or_one | No | The type of disk being characterized, e.g., removable. |
| freeSpace | integer | zero_or_one | No | The amount of free space on the disk, in bytes. |
| partition | ObservableObject | zero_or_more | No | The partitions that reside on the disk. |

### DiskPartition

*A disk partition is a particular managed region on a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks. [based on https://en.wikipedia.org/wiki/Disk_storage]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DiskPartition`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DiskPartitionFacet

*A disk partition facet is a grouping of characteristics unique to a particular managed region on a storage mechanism.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DiskPartitionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| diskPartitionType | string | zero_or_one | No | Specifies the type of partition being characterized. |
| mountPoint | string | zero_or_one | No | Specifies the mount point of the partition. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| partitionID | string | zero_or_one | No | Specifies the identifier of the partition, as provided by the containing partition table.  This identifier is the ind... |
| partitionLength | integer | zero_or_one | No | Specifies the length of the partition, in bytes. |
| partitionOffset | integer | zero_or_one | No | Specifies the starting offset of the partition, in bytes. |
| spaceLeft | integer | zero_or_one | No | Specifies the amount of space left on the partition, in bytes. |
| spaceUsed | integer | zero_or_one | No | Specifies the amount of space used on the partition, in bytes. |
| totalSpace | integer | zero_or_one | No | Specifies the total amount of space available on the partition, in bytes. |

### DomainName

*A domain name is an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.wikipedia.org/wiki/Domain_name]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DomainName`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### DomainNameFacet

*A domain name facet is a grouping of characteristics unique to an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.wikipedia.org/wiki/Domain_name]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/DomainNameFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| isTLD | boolean | zero_or_one | No |  |
| value | string | zero_or_one | No |  |

### Drone

*A drone, unmanned aerial vehicle (UAV), is an aircraft without a human pilot, crew, or passengers that typically involve a ground-based controller and a system for communications with the UAV.*

**Parents:** MobileDevice | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Drone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EXIFFacet

*An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners and other systems handling image and sound files recorded by digital cameras conformant to JEIDA/JEITA/CIPA specifications. [based on https://en.wikipedia.org/wiki/Exif]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EXIFFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| exifData | ControlledDictionary | zero_or_more | No |  |

### EmailAccount

*An email account is an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EmailAccountFacet

*An email account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| emailAddress | ObservableObject | zero_or_one | No | An email address. |

### EmailAddress

*An email address is an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are sent from and delivered to.*

**Parents:** DigitalAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EmailAddressFacet

*An email address facet is a grouping of characteristics unique to an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are sent from and delivered to.*

**Parents:** DigitalAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### EmailMessage

*An email message is a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and related RFCs.*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailMessage`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EmailMessageFacet

*An email message facet is a grouping of characteristics unique to a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and related RFCs.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmailMessageFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| bcc | ObservableObject | zero_or_more | No |  |
| body | string | zero_or_one | No |  |
| bodyMultipart | MimePartType | zero_or_more | No | A list of the MIME parts that make up the email body. This field MAY only be used if isMultipart is true. |
| bodyRaw | ObservableObject | zero_or_one | No |  |
| categories | string | zero_or_more | No | Categories applied to the object. |
| cc | ObservableObject | zero_or_more | No |  |
| contentDisposition | string | zero_or_one | No |  |
| contentType | string | zero_or_one | No |  |
| from | ObservableObject | zero_or_one | No | The phone number of the initiating party. |
| headerRaw | ObservableObject | zero_or_one | No |  |
| inReplyTo | string | zero_or_one | No | One of more unique identifiers for identifying the email(s) this email is a reply to. |
| isMimeEncoded | boolean | zero_or_one | No |  |
| isMultipart | boolean | zero_or_one | No |  |
| isRead | boolean | zero_or_one | No |  |
| labels | string | zero_or_more | No | Named and colored label. |
| messageID | string | zero_or_one | No | An unique identifier for the message. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| otherHeaders | Dictionary | zero_or_one | No |  |
| priority | string | zero_or_one | No | The priority of the email. |
| receivedLines | string | zero_or_more | No |  |
| receivedTime | dateTime | zero_or_one | No | The date and time at which the message received.  |
| references | ObservableObject | zero_or_more | No | A list of email message identifiers this email relates to. |
| sender | ObservableObject | zero_or_one | No |  |
| sentTime | dateTime | zero_or_one | No | The date and time at which the message sent. |
| subject | string | zero_or_one | No | The subject of the email. |
| to | ObservableObject | zero_or_more | No | The receiver's phone number. |
| xMailer | string | zero_or_one | No |  |
| xOriginatingIP | ObservableObject | zero_or_one | No |  |

### EmbeddedDevice

*An embedded device is a highly specialized microprocessor device meant for one or very few specific purposes and is usually embedded or included within another object or as part of a larger system. Examples include answer machine, door access logger, card scanner, etc.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EmbeddedDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EncodedStreamFacet

*An encoded stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another form.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EncodedStreamFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| encodingMethod | string | zero_or_one | No |  |

### EncryptedStreamFacet

*An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another obfuscated form in such a way that reversing the conversion to obtain the original data form can only be accomplished through possession and use of a specific key.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EncryptedStreamFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| encryptionIV | string | zero_or_more | No |  |
| encryptionKey | string | zero_or_more | No |  |
| encryptionMethod | string | zero_or_one | No |  |
| encryptionMode | string | zero_or_one | No |  |

### EnvironmentVariable

*An environment variable is a grouping of characteristics unique to a dynamic-named value that can affect the way running processes will behave on a computer. [based on https://en.wikipedia.org/wiki/Environment_variable]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EnvironmentVariable`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| value | string | zero_or_one | No |  |

### EventLog

*An event log is a collection of event records.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EventLog`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EventRecord

*An event record is something that happens in a digital context (e.g., operating system events).*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EventRecord`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### EventRecordFacet

*An event record facet is a grouping of characteristics unique to something that happens in a digital context (e.g., operating system events).*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/EventRecordFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| account | ObservableObject | zero_or_one | No | Specifies the account referenced in an event log entry or used to run the scheduled task. See also: http://msdn.micro... |
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| cyberAction | ObservableAction | zero_or_one | No | The action taken in response to the event. |
| endTime | dateTime | zero_or_one | No |  |
| eventID | string | zero_or_one | No |  |
| eventRecordDevice | ObservableObject | zero_or_one | No | The device on which the log entry was generated. |
| eventRecordID | string | zero_or_one | No | The identifier of the event record. |
| eventRecordRaw | string | zero_or_one | No | The complete raw content of the event record. |
| eventRecordServiceName | string | zero_or_one | No | The service that generated the event record. A single application can have multiple services generating event records. |
| eventRecordText | string | zero_or_one | No | The textual representation of the event. |
| eventType | string | zero_or_one | No | The type of the event, for example 'information', 'warning' or 'error'. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| startTime | dateTime | zero_or_one | No |  |

### ExtInodeFacet

*An extInode facet is a grouping of characteristics unique to a file system object (file, directory, etc.) conformant to the extended file system (EXT or related derivations) specification.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ExtInodeFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| extDeletionTime | dateTime | zero_or_one | No | Specifies the time at which the file represented by an Inode was 'deleted'. |
| extFileType | integer | zero_or_one | No | Specifies the EXT file type (FIFO, Directory, Regular file, Symbolic link, etc) for the Inode. |
| extFlags | integer | zero_or_one | No | Specifies user flags to further protect (limit its use and modification) the file represented by an Inode. |
| extHardLinkCount | integer | zero_or_one | No | Specifies a count of how many hard links point to an Inode. |
| extInodeChangeTime | dateTime | zero_or_one | No | The date and time at which the file Inode metadata was last modified. |
| extInodeID | integer | zero_or_one | No | Specifies a single Inode identifier. |
| extPermissions | integer | zero_or_one | No | Specifies the read/write/execute permissions for the file represented by an EXT Inode. |
| extSGID | integer | zero_or_one | No | Specifies the group ID for the file represented by an Inode. |
| extSUID | integer | zero_or_one | No | Specifies the user ID that 'owns' the file represented by an Inode. |

### ExtractedString

*An extracted string is a grouping of characteristics unique to a series of characters pulled from an observable object.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ExtractedString`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| byteStringValue | base64Binary | zero_or_one | No | Specifies the raw, byte-string representation of the extracted string. |
| encoding | string | zero_or_one | No | The encoding method used for the extracted string. |
| englishTranslation | string | zero_or_one | No | Specifies the English translation of the string, if it is not written in English. |
| language | string | zero_or_one | No | Specifies the language the string is written in, e.g. English.           For consistency, it is strongly recommended ... |
| length | integer | zero_or_one | No | Specifies the length, in characters, of the extracted string. |
| stringValue | string | zero_or_one | No | Specifies the actual value of the extracted string. |

### ExtractedStringsFacet

*An extracted strings facet is a grouping of characteristics unique to one or more sequences of characters pulled from an observable object.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ExtractedStringsFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| strings | ExtractedString | zero_or_more | No |  |

### File

*A file is a computer resource for recording data discretely on a computer storage device.*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/File`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### FileFacet

*A file facet is a grouping of characteristics unique to the storage of a file (computer resource for recording data discretely in a computer storage device) on a file system (process that manages how and where data on a storage device is stored, accessed and managed). [based on https://en.wikipedia.org/Computer_file and https://www.techopedia.com/definition/5510/file-system]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accessedTime | dateTime | zero_or_one | No | The date and time at which the Object was accessed. |
| allocationStatus | string | zero_or_one | No | The allocation status of a file. |
| extension | string | zero_or_one | No | The file name extension: everything after the last dot. Not present if the file has no dot in its name. |
| fileName | string | zero_or_more | No | Specifies the name associated with a file in a file system. |
| filePath | string | zero_or_more | No | Specifies the file path for the location of a file within a filesystem. |
| isDirectory | boolean | zero_or_more | No | Specifies whether a file entry represents a directory. |
| metadataChangeTime | dateTime | zero_or_one | No | The date and time at which the file metadata was last modified. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| sizeInBytes | integer | zero_or_one | No | The size of the data in bytes. |

### FilePermissionsFacet

*A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a file system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FilePermissionsFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| owner | UcoObject | zero_or_one | No | Specifies the owner of an Observable Object. |

### FileSystem

*A file system is the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/definition/5510/file-system]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FileSystem`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### FileSystemFacet

*A file system facet is a grouping of characteristics unique to the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/definition/5510/file-system]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FileSystemFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| clusterSize | integer | zero_or_one | No | The size of cluster allocation units in a file system. |
| fileSystemType | string | zero_or_one | No | The specific type of a file system. |

### FileSystemObject

*A file system object is an informational object represented and managed within a file system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FileSystemObject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ForumPost

*A forum post is message submitted by a user account to an online forum where the message content (and typically metadata including who posted it and when) is viewable by any party with viewing permissions on the forum.*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ForumPost`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ForumPrivateMessage

*A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific user account to another specific user account on an online form where transmission is managed by the online forum platform and the message is only viewable by the parties directly involved.*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ForumPrivateMessage`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### FragmentFacet

*A fragment facet is a grouping of characteristics unique to an individual piece of the content of a file.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/FragmentFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| fragmentIndex | integer | zero_or_more | No |  |
| totalFragments | integer | zero_or_more | No |  |

### GUI

*A GUI is a graphical user interface that allows users to interact with electronic devices through graphical icons and audio indicators such as primary notation, instead of text-based user interfaces, typed command labels or text navigation. [based on https://en.wikipedia.org/wiki/Graphical_user_interface]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GUI`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GamingConsole

*A gaming console (video game console or game console) is an electronic system that connects to a display, typically a TV or computer monitor, for the primary purpose of playing video games.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GamingConsole`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GenericObservableObject

*A generic observable object is an article or unit within the digital domain.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GenericObservableObject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GeoLocationEntry

*A geolocation entry is a single application-specific geolocation entry.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GeoLocationEntryFacet

*A geolocation entry facet is a grouping of characteristics unique to a single application-specific geolocation entry.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntryFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| location | Location | zero_or_one | No | An associated location. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |

### GeoLocationLog

*A geolocation log is a record containing geolocation tracks and/or geolocation entries.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLog`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GeoLocationLogFacet

*A geolocation log facet is a grouping of characteristics unique to a record containing geolocation tracks and/or geolocation entries.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLogFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |

### GeoLocationTrack

*A geolocation track is a set of contiguous geolocation entries representing a path/track taken.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrack`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### GeoLocationTrackFacet

*A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocation entries representing a path/track taken.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrackFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| endTime | dateTime | zero_or_one | No |  |
| geoLocationEntry | ObservableObject | zero_or_more | No |  |
| startTime | dateTime | zero_or_one | No |  |

### GlobalFlagType

*A global flag type is a grouping of characteristics unique to the Windows systemwide global variable named NtGlobalFlag that enables various internal debugging, tracing, and validation support in the operating system. [based on "Windows Global Flags, Chapter 3: System Mechanisms of Windows Internals by Solomon, Russinovich, and Ionescu]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/GlobalFlagType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| abbreviation | string | zero_or_one | No | The abbreviation of a global flag. See also: http://msdn.microsoft.com/en-us/library/windows/hardware/ff549646(v=vs.8... |
| destination | string | zero_or_one | No | The destination of a global flag. See also: http://msdn.microsoft.com/en-us/library/windows/hardware/ff549646(v=vs.85... |
| hexadecimalValue | hexBinary | zero_or_more | No | The hexadecimal value of a global flag. See also: http://msdn.microsoft.com/en-us/library/windows/hardware/ff549646(v... |
| symbolicName | string | zero_or_one | No | The symbolic name of a global flag. See also: http://msdn.microsoft.com/en-us/library/windows/hardware/ff549646(v=vs.... |

### HTTPConnection

*An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (HTTP) standard.*

**Parents:** NetworkConnection | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### HTTPConnectionFacet

*An HTTP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Hypertext Transfer Protocol (HTTP) standard.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnectionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| httpMesageBodyLength | integer | zero_or_one | No | Specifies the length of an HTTP message body in bytes. |
| httpMessageBodyData | ObservableObject | zero_or_one | No | Specifies the data contained in an HTTP message body. |
| httpRequestHeader | Dictionary | zero_or_one | No | Specifies all of the HTTP header fields that may be found in the HTTP client request |
| requestMethod | string | zero_or_one | No | Specifies the HTTP method portion of the HTTP request line, as a lowercase string.            |
| requestValue | string | zero_or_one | No | Specifies the value (typically a resource path) portion of the HTTP request line. |
| requestVersion | string | zero_or_one | No | Specifies the HTTP version portion of the HTTP request line, as a lowercase string. |

### Hostname

*A hostname is a label that is assigned to a device connected to a computer network and that is used to identify the device in various forms of electronic communication, such as the World Wide Web. A hostname may be a domain name, if it is properly organized into the domain name system. A domain name may be a hostname if it has been assigned to an Internet host and associated with the host's IP address. [based on https://en.wikipedia.org/wiki/Hostname]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Hostname`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ICMPConnection

*An ICMP connection is a network connection that is conformant to the Internet Control Message Protocol (ICMP) standard.*

**Parents:** NetworkConnection | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ICMPConnectionFacet

*An ICMP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Internet Control Message Protocol (ICMP) standard.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnectionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| icmpCode | hexBinary | zero_or_more | No | Specifies the ICMP code byte. |
| icmpType | hexBinary | zero_or_more | No | Specifies the ICMP type byte. |

### IComHandlerActionType

*An IComHandler action type is a grouping of characteristics unique to a Windows Task-related action that fires a Windows COM handler (smart code in the client address space that can optimize calls between a client and server). [based on https://docs.microsoft.com/en-us/windows/win32/taskschd/comhandleraction]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IComHandlerActionType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| comClassID | string | zero_or_one | No | Specifies the ID of the COM action. See also: http://msdn.microsoft.com/en-us/library/windows/desktop/aa380613(v=vs.8... |
| comData | string | zero_or_one | No | Specifies the data associated with the COM handler. See also: http://msdn.microsoft.com/en-us/library/windows/desktop... |

### IExecActionType

*An IExec action type is a grouping of characteristics unique to an action that executes a command-line operation on a Windows operating system. [based on https://docs.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iexecaction?redirectedfrom=MSDN]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IExecActionType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| execArguments | string | zero_or_one | No | Specifies the arguments associated with the command-line operation launched by the action. See also: http://msdn.micr... |
| execProgramHashes | Hash | zero_or_more | No | Specifies the hashes of the executable file launched by the action. |
| execProgramPath | string | zero_or_one | No | Specifies the path to the executable file launched by the action. See also: http://msdn.microsoft.com/en-us/library/w... |
| execWorkingDirectory | string | zero_or_one | No | Specifies the directory that contains either the executable file or the files that are used by the executable file la... |

### IPAddress

*An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conformant communication to or from that device.*

**Parents:** DigitalAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### IPAddressFacet

*An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conformant communication to or from that device.*

**Parents:** DigitalAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### IPNetmask

*An IP netmask is a 32-bit 'mask' used to divide an IP address into subnets and specify the network's available hosts.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPNetmask`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### IPhone

*An iPhone is a smart phone that applies the iOS mobile operating system.*

**Parents:** AppleDevice, SmartPhone | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### IPv4Address

*An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 standards conformant communication to or from that device.*

**Parents:** IPAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPv4Address`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### IPv4AddressFacet

*An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 standards conformant communication to or from that device.*

**Parents:** IPAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPv4AddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### IPv6Address

*An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 standards conformant communication to or from that device.*

**Parents:** IPAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPv6Address`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### IPv6AddressFacet

*An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 standards conformant communication to or from that device.*

**Parents:** IPAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IPv6AddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### IShowMessageActionType

*An IShow message action type is a grouping of characteristics unique to an action that shows a message box when a task is activate. [based on https://docs.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-ishowmessageaction?redirectedfrom=MSDN]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/IShowMessageActionType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| showMessageBody | string | zero_or_one | No | Specifies the message text that is displayed in the body of the message box by the action. See also: http://msdn.micr... |
| showMessageTitle | string | zero_or_one | No | Specifies the title of the message box shown by the action. See also: http://msdn.microsoft.com/en-us/library/windows... |

### Image

*An image is a complete copy of a hard disk, memory, or other digital media.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Image`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ImageFacet

*An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory, or other digital media.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ImageFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| imageType | string | zero_or_one | No | The type of the image, e.g. EnCase, RAW or LocalFolder. |

### InstantMessagingAddress

**Parents:** DigitalAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### InstantMessagingAddressFacet

*An instant messaging address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of instant messaging digital communication.*

**Parents:** DigitalAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### Junction

*A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory access to another directory which can be on the same volume or another volume. A junction is similar to a directory symbolic link but may differ on whether they are processed on the local system or on the remote file server. [based on https://jp-andre.pagesperso-orange.fr/junctions.html]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Junction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Laptop

*A laptop, laptop computer, or notebook computer is a small, portable personal computer with a screen and alphanumeric keyboard. These typically have a clam shell form factor with the screen mounted on the inside of the upper lid and the keyboard on the inside of the lower lid, although 2-in-1 PCs with a detachable keyboard are often marketed as laptops or as having a laptop mode. (Devices categorized by their manufacturer as a Laptop)*

**Parents:** Computer | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Laptop`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Library

*A library is a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definition/3828/software-library]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Library`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### LibraryFacet

*A library facet is a grouping of characteristics unique to a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definition/3828/software-library]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/LibraryFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| libraryType | string | zero_or_one | No | Specifies the type of library being characterized. |

### MACAddress

*A MAC address is a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications at the data link layer of a network segment.*

**Parents:** DigitalAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MACAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MACAddressFacet

*A MAC address facet is a grouping of characteristics unique to a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications at the data link layer of a network segment.*

**Parents:** DigitalAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MACAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### Memory

*Memory is a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Memory`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MemoryFacet

*A memory facet is a grouping of characteristics unique to a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MemoryFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| blockType | string | zero_or_more | No | The blockType property specifies the block type of a particular memory object. |
| isInjected | boolean | zero_or_one | No | The isInjected property specifies whether or not the particular memory object has had data/code injected into it by a... |
| isMapped | boolean | zero_or_one | No | The isMapped property specifies whether or not the particular memory object has been assigned a byte-for-byte correla... |
| isProtected | boolean | zero_or_one | No | The isProtected property specifies whether or not the particular memory object is protected (read/write only from the... |
| isVolatile | boolean | zero_or_one | No | The isVolatile property specifies whether or not the particular memory object is volatile. |
| regionEndAddress | hexBinary | zero_or_more | No | The regionEndAddress property specifies the ending address of the particular memory region. |
| regionSize | integer | zero_or_one | No | The regionSize property specifies the size of the particular memory region, in bytes. |
| regionStartAddress | hexBinary | zero_or_more | No | The regionStartAddress property specifies the starting address of the particular memory region.            |

### Message

*A message is a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https://en.wikipedia.org/wiki/Message]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Message`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MessageFacet

*A message facet is a grouping of characteristics unique to a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https://en.wikipedia.org/wiki/Message]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MessageFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| from | ObservableObject | zero_or_one | No | The phone number of the initiating party. |
| messageID | string | zero_or_one | No | An unique identifier for the message. |
| messageText | string | zero_or_one | No | The contents of the message. |
| messageType | string | zero_or_one | No | Message type specifies what sort of message (email, chat, SMS, etc) a Message is. |
| sentTime | dateTime | zero_or_one | No | The date and time at which the message sent. |
| sessionID | string | zero_or_one | No | An identifier for the session from which the message originates. |
| to | ObservableObject | zero_or_more | No | The receiver's phone number. |

### MessageThread

*A message thread is a running commentary of electronic messages pertaining to one topic or question.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MessageThread`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MessageThreadFacet

*A message thread facet is a grouping of characteristics unique to a running commentary of electronic messages pertaining to one topic or question.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MessageThreadFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| messageThread | Thread | zero_or_one | No |  |
| participant | ObservableObject | zero_or_more | No |  |
| visibility | boolean | zero_or_one | No |  |

### MftRecordFacet

*An MFT record facet is a grouping of characteristics unique to the details of a single file as managed in an NTFS (new technology filesystem) master file table (which is a collection of information about all files on an NTFS filesystem). [based on https://docs.microsoft.com/en-us/windows/win32/devnotes/master-file-table]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MftRecordFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| mftFileID | integer | zero_or_one | No | Specifies the record number for the file within an NTFS Master File Table. |
| mftFileNameAccessedTime | dateTime | zero_or_one | No | The access date and time recorded in an MFT entry $File_Name attribute. |
| mftFileNameCreatedTime | dateTime | zero_or_one | No | The creation date and time recorded in an MFT entry $File_Name attribute. |
| mftFileNameLength | integer | zero_or_one | No |  Specifies the length of an NTFS file name, in unicode characters. |
| mftFileNameModifiedTime | dateTime | zero_or_one | No | The modification date and time recorded in an MFT entry $File_Name attribute. |
| mftFileNameRecordChangeTime | dateTime | zero_or_one | No | The metadata modification date and time recorded in an MFT entry $File_Name attribute. |
| mftFlags | integer | zero_or_one | No | Specifies basic permissions for the file (Read-Only, Hidden, Archive, Compressed, etc.). |
| mftParentID | integer | zero_or_one | No | Specifies the record number within an NTFS Master File Table for parent directory of the file. |
| mftRecordChangeTime | dateTime | zero_or_one | No | The date and time at which an NTFS file metadata was last modified. |
| ntfsHardLinkCount | integer | zero_or_one | No | Specifies the number of directory entries that reference an NTFS file record. |
| ntfsOwnerID | string | zero_or_one | No | Specifies the identifier of the file owner, from the security index. |
| ntfsOwnerSID | string | zero_or_one | No | Specifies the security ID (key in the $SII Index and $SDS DataStream in the file $Secure) for an NTFS file. |

### MimePartType

*A mime part type is a grouping of characteristics unique to a component of a multi-part email body.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MimePartType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| body | string | zero_or_one | No |  |
| bodyRaw | ObservableObject | zero_or_one | No |  |
| contentDisposition | string | zero_or_one | No |  |
| contentType | string | zero_or_one | No |  |

### MobileAccount

*A mobile account is an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based on https://www.lexico.com/definition/mobile_device]*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MobileAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MobileAccountFacet

*A mobile account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based on https://www.lexico.com/definition/mobile_device]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MobileAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| IMSI | string | zero_or_one | No | An International Mobile Subscriber Identity (IMSI) is a unique identification associated with all GSM and UMTS networ... |
| MSISDN | string | zero_or_one | No | Mobile Station International Subscriber Directory Number (MSISDN) is a number used to identify a mobile phone number ... |
| MSISDNType | string | zero_or_one | No | ???. |

### MobileDevice

*A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobile_device]*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MobileDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MobileDeviceFacet

*A mobile device facet is a grouping of characteristics unique to a portable computing device. [based on https://www.lexico.com/definition/mobile_device]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MobileDeviceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| ESN | string | zero_or_one | No | Electronic Serial Number . |
| IMEI | string | zero_or_more | No | International Mobile Equipment Identity (IMEI). |
| bluetoothDeviceName | string | zero_or_one | No | Name configured withing Bluetooth settings on a device. |
| clockSetting | dateTime | zero_or_one | No | The generalizedTime value on the mobile device when it was processed. |
| keypadUnlockCode | string | zero_or_one | No | A code or password set on a device for security that must be entered to gain access to the device. |
| mockLocationsAllowed | boolean | zero_or_one | No | ???. |
| network | string | zero_or_one | No | ???. |
| phoneActivationTime | dateTime | zero_or_one | No | The date and time that a device was activated. |
| storageCapacityInBytes | integer | zero_or_one | No | The number of bytes that can be stored on a SIM card. |

### MobilePhone

*A mobile phone is a portable telephone that at least can make and receive calls over a radio frequency link while the user is moving within a telephone service area. This category encompasses all types of mobiles, simple and smart and satellite ones all together.*

**Parents:** MobileDevice | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MobilePhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Mutex

*A mutex is a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual exclusion concurrency control policy, and with a variety of possible methods there exists multiple unique implementations for different applications. [based on https://en.wikipedia.org/wiki/Lock_(computer_science)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Mutex`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### MutexFacet

*A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual exclusion concurrency control policy, and with a variety of possible methods there exists multiple unique implementations for different applications. [based on https://en.wikipedia.org/wiki/Lock_(computer_science)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/MutexFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| isNamed | boolean | zero_or_one | No |  |
| mutexName | string | zero_or_one | No | Specifies the name identifier for a specific instance of a mechanism that enforces limits on access to a resource whe... |

### NTFSFile

*An NTFS file is a New Technology File System (NTFS) file.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NTFSFile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NTFSFileFacet

*An NTFS file facet is a grouping of characteristics unique to a file on an NTFS (new technology filesystem) file system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NTFSFileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| alternateDataStreams | AlternateDataStream | zero_or_more | No |  |
| entryID | integer | zero_or_one | No | A unique identifier for the file within the filesystem. |
| sid | string | zero_or_one | No |  |

### NTFSFilePermissionsFacet

*An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on an NTFS (new technology filesystem) file system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NTFSFilePermissionsFacet`

*No direct or inherited properties.*

### NamedPipe

*A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is persisted as a filesystem object (that can be deleted like any other file), can be written to or read from by any process and exists beyond the lifespan of any process interacting with it (unlike simple anonymous pipes). [based on https://en.wikipedia.org/wiki/Named_pipe]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NamedPipe`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkAppliance

*A network appliance is a purpose-built computer with software or firmware that is designed to provide a specific network management function.*

**Parents:** Appliance | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkAppliance`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkConnection

*A network connection is a connection (completed or attempted) across a digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkConnectionFacet

*A network connection facet is a grouping of characteristics unique to a connection (complete or attempted) accross a digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnectionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| destinationPort | integer | zero_or_one | No | Specifies the destination port used in the connection, as an integer in the range of 0 - 65535. |
| dst | ObservableObject | zero_or_more | No | Specifies the destination(s) of the network connection. |
| endTime | dateTime | zero_or_one | No |  |
| isActive | boolean | zero_or_one | No | Indicates whether the network connection is still active. |
| protocols | ControlledDictionary | zero_or_one | No | Specifies the protocols involved in the network connection, along with their corresponding state.  |
| sourcePort | integer | zero_or_one | No | Specifies the source port used in the connection, as an integer in the range of 0 - 65535.            |
| src | UcoObject | zero_or_more | No | Specifies the source(s) of the network connection. |
| startTime | dateTime | zero_or_one | No |  |

### NetworkFlow

*A network flow is a sequence of data transiting one or more digital network (a group or two or more computer systems linked together) connections. [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlow`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkFlowFacet

*A network flow facet is a grouping of characteristics unique to a sequence of data transiting one or more digital network (a group of two or more computer systems linked together) connections. [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlowFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| dstBytes | integer | zero_or_one | No |  |
| dstPackets | integer | zero_or_one | No |  |
| dstPayload | ObservableObject | zero_or_one | No |  |
| ipfix | Dictionary | zero_or_one | No | Specifies any IP Flow Information Export (IPFIX) data for the network traffic flow. |
| srcBytes | integer | zero_or_one | No |  |
| srcPackets | integer | zero_or_one | No |  |
| srcPayload | ObservableObject | zero_or_one | No |  |

### NetworkInterface

*A network interface is a software or hardware interface between two pieces of equipment or protocol layers in a computer network.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterface`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkInterfaceFacet

*A network interface facet is a grouping of characteristics unique to a software or hardware interface between two pieces of equipment or protocol layers in a computer network.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterfaceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| adapterName | string | zero_or_one | No | Specifies the name of the network adapter used by the network interface. |
| dhcpLeaseExpires | dateTime | zero_or_one | No | Specifies the date/time that the DHCP lease obtained on the network interface expires. |
| dhcpLeaseObtained | dateTime | zero_or_one | No | Specifies the date/time that the DHCP lease was obtained on the network interface. |
| dhcpServer | ObservableObject | zero_or_more | No | Specifies the list of DHCP server IP Addresses used by the network interface. |
| ip | ObservableObject | zero_or_more | No | Specifies the list of IP addresses used by the network interface. |
| ipGateway | ObservableObject | zero_or_more | No | Specifies the list of IP Gateway IP Addresses used by the network interface. |
| macAddress | ObservableObject | zero_or_one | No | Specifies the MAC or hardware address of the physical network card.  |

### NetworkProtocol

*A network protocol is an established set of structured rules that determine how data is transmitted between different devices in the same network. Essentially, it allows connected devices to communicate with each other, regardless of any differences in their internal processes, structure or design. [based on https://www.comptia.org/content/guides/what-is-a-network-protocol]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkProtocol`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkRoute

*A network route is a specific path (of specific network nodes, connections and protocols) for traffic in a network or between or across multiple networks.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkRoute`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NetworkSubnet

*A network subnet is a logical subdivision of an IP network. [based on https://en.wikipedia.org/wiki/Subnetwork]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkSubnet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Note

*A note is a brief textual record.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Note`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### NoteFacet

*A note facet is a grouping of characteristics unique to a brief textual record.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NoteFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| text | string | zero_or_one | No |  |

### Observable

*An observable is a characterizable item or action within the digital domain.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Observable`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### ObservableAction

*An observable action is a grouping of characteristics unique to something that may be done or performed within the digital domain.*

**Parents:** Action, Observable | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ObservableAction`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_one | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_one | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_one | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |

### ObservableObject

*An observable object is a grouping of characteristics unique to a distinct article or unit within the digital domain.*

**Parents:** Item, Observable | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ObservablePattern

*An observable pattern is a grouping of characteristics unique to a logical pattern composed of observable object and observable action properties.*

**Parents:** Observable | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ObservablePattern`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### ObservableRelationship

*An observable relationship is a grouping of characteristics unique to an assertion of an association between two observable objects.*

**Parents:** Relationship, Observable | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ObservableRelationship`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| endTime | dateTime | zero_or_more | No | The ending time of a time range. |
| isDirectional | boolean | exactly_one | Yes | A specification whether or not a relationship assertion is limited to the context FROM a source object(s) TO a target... |
| kindOfRelationship | string | zero_or_one | No | A characterization of the nature of a relationship between objects. |
| source | Observable | zero_or_more | No | The originating node of a specified relationship. |
| startTime | dateTime | zero_or_more | No | The initial time of a time range. |
| target | Observable | zero_or_more | No | The terminating node of a specified relationship. |

### Observation

*An observation is a temporal perception of an observable.*

**Parents:** Action | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Observation`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | exactly_one | Yes | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| actionCount | nonNegativeInteger | zero_or_one | No | The number of times that the action was performed. |
| actionStatus | string | zero_or_more | No | The current state of the action. |
| endTime | dateTime | zero_or_one | No | The time at which performance of the action ended. |
| environment | UcoObject | zero_or_one | No | The environment wherein an action occurs. |
| error | UcoObject | zero_or_more | No | A characterization of the differences between the expected and the actual performance of the action. |
| instrument | UcoObject | zero_or_more | No | The things used to perform an action. |
| location | Location | zero_or_more | No | The locations where an action occurs. |
| object | UcoObject | zero_or_more | No | The things that the action is performed on/against. |
| participant | UcoObject | zero_or_more | No | The supporting (non-primary) performers of an action. |
| performer | UcoObject | zero_or_one | No | The primary performer of an action. |
| result | UcoObject | zero_or_more | No | The things resulting from performing an action. |
| startTime | dateTime | zero_or_one | No | The time at which performance of the action began. |
| subaction | Action | zero_or_more | No | References to other actions that make up part of a larger more complex action. |

### OnlineService

*An online service is a particular provision mechanism of information access, distribution or manipulation over the Internet.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/OnlineService`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### OnlineServiceFacet

*An online service facet is a grouping of characteristics unique to a particular provision mechanism of information access, distribution or manipulation over the Internet.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/OnlineServiceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| inetLocation | ObservableObject | zero_or_more | No | Specifies a location on the Internet. |
| location | Location | zero_or_more | No | An associated location. |

### OperatingSystem

*An operating system is the software that manages computer hardware, software resources, and provides common services for computer programs. [based on https://en.wikipedia.org/wiki/Operating_system]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystem`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### OperatingSystemFacet

*An operating system facet is a grouping of characteristics unique to the software that manages computer hardware, software resources, and provides common services for computer programs. [based on https://en.wikipedia.org/wiki/Operating_system]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystemFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| advertisingID | string | zero_or_more | No | Advertising ID as a UUID. [based on https://developer.android.com/reference/androidx/ads/identifier/AdvertisingIdInfo] |
| bitness | string | zero_or_one | No | Specifies the bitness of the operating system (i.e. 32 or 64). Note that this is potentially different from the word ... |
| environmentVariables | Dictionary | zero_or_one | No | A list of environment variables associated with the process.  |
| installDate | dateTime | zero_or_one | No | Specifies the date the operating system or application was installed. |
| isLimitAdTrackingEnabled | boolean | zero_or_one | No | Limits advertising tracking if enabled. [based on https://developer.android.com/reference/androidx/ads/identifier/Adv... |
| manufacturer | Identity | zero_or_one | No |  |
| version | string | zero_or_one | No |  |

### PDFFile

*A PDF file is a Portable Document Format (PDF) file.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PDFFile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### PDFFileFacet

*A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PDFFileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| documentInformationDictionary | ControlledDictionary | zero_or_one | No |  |
| isOptimized | boolean | zero_or_one | No |  |
| pdfCreationDate | dateTime | zero_or_one | No | The PDF CreationDate property is defined in ISO 32000-1:2008 as 'The date and time the document was created, in human... |
| pdfId0 | string | zero_or_more | No |  |
| pdfId1 | string | zero_or_one | No |  |
| pdfModDate | dateTime | zero_or_one | No | The PDF ModDate property is defined in ISO 32000-1:2008 as 'The date and time the document was most recently modified... |
| version | string | zero_or_one | No |  |

### PathRelationFacet

*A path relation facet is a grouping of characteristics unique to the location of one object within another containing object.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PathRelationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| path | string | zero_or_more | No | Specifies the location of one object within another containing object. |

### PaymentCard

*A payment card is a physical token that is part of a payment system issued by financial institutions, such as a bank, to a customer that enables its owner (the cardholder) to access the funds in the customer's designated bank accounts, or through a credit account and make payments by electronic funds transfer and access automated teller machines (ATMs). [based on https://en.wikipedia.org/wiki/Payment_card]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PaymentCard`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### PhoneAccount

*A phone account is an arrangement with an entity to enable and control the provision of a telephony capability or service.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### PhoneAccountFacet

*A phone account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of a telephony capability or service.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| phoneNumber | string | zero_or_one | No | A phone number(account). |

### Pipe

*A pipe is a mechanism for one-way inter-process communication using message passing where data written by one process is buffered by the operating system until it is read by the next process, and this uni-directional channel disappears when the processes are completed. [based on https://en.wikipedia.org/wiki/Pipeline_(Unix) ; https://en.wikipedia.org/wiki/Anonymous_pipe]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Pipe`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Post

*A post is message submitted to an online discussion/publishing site (forum, blog, etc.).*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Post`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Process

*A process is an instance of a computer program executed on an operating system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Process`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ProcessFacet

*A process facet is a grouping of characteristics unique to an instance of a computer program executed on an operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ProcessFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| arguments | string | zero_or_more | No | A list of arguments utilized in initiating the process. |
| binary | ObservableObject | zero_or_one | No |  |
| creatorUser | ObservableObject | zero_or_one | No | The user that created/owns the process. |
| currentWorkingDirectory | string | zero_or_one | No |  |
| environmentVariables | Dictionary | zero_or_one | No | A list of environment variables associated with the process.  |
| exitStatus | integer | zero_or_one | No | A small number passed from the process to the parent process when it has finished executing. In general, 0 indicates ... |
| exitTime | dateTime | zero_or_one | No | The time at which the process exited. |
| isHidden | boolean | zero_or_one | No | The isHidden property specifies whether the process is hidden or not.            |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| parent | ObservableObject | zero_or_one | No | The process that created this process. |
| pid | integer | zero_or_one | No | The Process ID, or PID, of the process. |
| status | string | zero_or_one | No | Specifies a list of statuses for a given Whois entry. |

### ProcessThread

*A process thread is the smallest sequence of programmed instructions that can be managed independently by a scheduler on a computer, which is typically a part of the operating system. It is a component of a process. Multiple threads can exist within one process, executing concurrently and sharing resources such as memory, while different processes do not share these resources. In particular, the threads of a process share its executable code and the values of its dynamically allocated variables and non-thread-local global variables at any given time. [based on https://en.wikipedia.org/wiki/Thread_(computing)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ProcessThread`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Profile

*A profile is an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or application. [based on https://en.wikipedia.org/wiki/User_profile]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Profile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ProfileFacet

*A profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or application. [based on https://en.wikipedia.org/wiki/User_profile]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ProfileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| contactAddress | ContactAddress | zero_or_one | No | Contact address specifies information characterizing a geolocation address of a contact entity. |
| contactEmail | ContactEmail | zero_or_one | No | Contact email specifies information characterizing details for contacting a contact entity by email. |
| contactMessaging | ContactMessaging | zero_or_one | No | Contact messaging specifies information characterizing details for contacting a contact entity by digital messaging. |
| contactPhone | ContactPhone | zero_or_one | No | Contact phone specifies information characterizing details for contacting a contact entity by telephone. |
| contactURL | ContactURL | zero_or_one | No | Contact URL specifies information characterizing details for contacting a contact entity by Uniform Resource Locator ... |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |
| profileAccount | ObservableObject | zero_or_one | No | Specifies the online service account associated with the profile. |
| profileCreated | dateTime | zero_or_one | No | Specifies the date and time the profile was created. |
| profileIdentity | Identity | zero_or_one | No | Specifies the identity associated with the profile. |
| profileLanguage | string | zero_or_more | No | Specifies the language associated with the profile. When present, it MUST be a language code conformant to RFC 5646/B... |
| profileService | ObservableObject | zero_or_one | No | Specifies the online service associated with the profile. |
| profileWebsite | ObservableObject | zero_or_one | No | Specifies the website URL associated with the profile. |

### PropertiesEnumeratedEffectFacet

*A properties enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic of the observable object is enumerated. An example of this would be startup parameters for a process.*

**Parents:** Facet, DefinedEffectFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PropertiesEnumeratedEffectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| properties | string | zero_or_one | No | Specifies the properties that were enumerated as a result of the action on the observable object. |

### PropertyReadEffectFacet

*A properties read effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic is read from an observable object. An example of this would be the current running state of a process.*

**Parents:** DefinedEffectFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/PropertyReadEffectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| propertyName | string | zero_or_one | No | Specifies the Name of the property being read. |
| value | string | zero_or_one | No |  |

### ProtocolConverter

*A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA to USB, etc.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ProtocolConverter`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### RasterPicture

*A raster picture is a raster (or bitmap) image.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/RasterPicture`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### RasterPictureFacet

*A raster picture facet is a grouping of characteristics unique to a raster (or bitmap) image.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/RasterPictureFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| bitsPerPixel | integer | zero_or_one | No |  |
| camera | ObservableObject | zero_or_one | No | The name/make of the camera that was used for taking the picture. |
| imageCompressionMethod | string | zero_or_one | No |  |
| pictureHeight | integer | zero_or_one | No |  |
| pictureType | string | zero_or_one | No | The type of a picture, for example a thumbnail. |
| pictureWidth | integer | zero_or_one | No | The width of the picture in pixels. |

### RecoveredObject

*An observable object that was the result of a recovery operation.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObject`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### RecoveredObjectFacet

*Recoverability status of name, metadata, and content.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObjectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contentRecoveredStatus | string | zero_or_more | No | Specifies the recoverability status of the content of an object. |
| metadataRecoveredStatus | string | zero_or_more | No | Specifies the recoverability status of the metadata of an object. |
| nameRecoveredStatus | string | zero_or_more | No | Specifies the recoverability status of the name of an object. |

### ReparsePoint

*A reparse point is a type of NTFS (New Technology File System) object which is an optional attribute of files and directories meant to define some sort of preprocessing before accessing the said file or directory. For instance reparse points can be used to redirect access to files which have been moved to long term storage so that some application would retrieve them and make them directly accessible. A reparse point contains a reparse tag and data that are interpreted by a filesystem filter identified by the tag. [based on https://jp-andre.pagesperso-orange.fr/junctions.html ; https://en.wikipedia.org/wiki/NTFS_reparse_point]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ReparsePoint`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SIMCard

*A SIM card is a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its related key, which are used to identify and authenticate subscribers on mobile telephony. [based on https://en.wikipedia.org/wiki/SIM_card]*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SIMCard`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SIMCardFacet

*A SIM card facet is a grouping of characteristics unique to a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its related key, which are used to identify and authenticate subscribers on mobile telephony devices (such as mobile phones and computers). [based on https://en.wikipedia.org/wiki/SIM_card]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SIMCardFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| ICCID | string | zero_or_one | No | Integrated circuit card identifier (http://www.itu.int/). |
| IMSI | string | zero_or_one | No | An International Mobile Subscriber Identity (IMSI) is a unique identification associated with all GSM and UMTS networ... |
| PIN | string | zero_or_one | No | Personal Identification Number (PIN). |
| PUK | string | zero_or_one | No | Personal Unlocking Key (PUK) to unlock the SIM card. |
| SIMForm | string | zero_or_one | No | The form of SIM card such as SIM, Micro SIM, Nano SIM. |
| SIMType | string | zero_or_one | No | The type of SIM card such as SIM, USIM, UICC. |
| carrier | Identity | zero_or_one | No | Telecommunications service provider that sold the SIM card. |
| storageCapacityInBytes | integer | zero_or_one | No | The number of bytes that can be stored on a SIM card. |

### SIPAddress

*A SIP address is an identifier for Session Initiation Protocol (SIP) communication.*

**Parents:** DigitalAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SIPAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SIPAddressFacet

*A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP) standards conformant identifier assigned to a user to enable routing and management of SIP standards conformant communication to or from that user loosely coupled from any particular devices.*

**Parents:** DigitalAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SIPAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### SMSMessage

*An SMS message is a message conformant to the short message service (SMS) communication protocol standards.*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SMSMessage`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SMSMessageFacet

*A SMS message facet is a grouping of characteristics unique to a message conformant to the short message service (SMS) communication protocol standards.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SMSMessageFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| isRead | boolean | zero_or_one | No |  |

### SQLiteBlob

*An SQLite blob is a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlob`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SQLiteBlobFacet

*An SQLite blob facet is a grouping of characteristics unique to a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlobFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| columnName | string | zero_or_one | No |  |
| rowCondition | string | zero_or_one | No |  |
| rowIndex | positiveInteger | zero_or_more | No |  |
| tableName | string | zero_or_one | No | The table containing a specified database record. |

### SecurityAppliance

*A security appliance is a purpose-built computer with software or firmware that is designed to provide a specific security function to protect computer networks.*

**Parents:** Appliance | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SecurityAppliance`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Semaphore

*A semaphore is a variable or abstract data type used to control access to a common resource by multiple processes and avoid critical section problems in a concurrent system such as a multitasking operating system. [based on https://en.wikipedia.org/wiki/Semaphore_(programming)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Semaphore`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SendControlCodeEffectFacet

*A send control code effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a control code, or other control-oriented communication signal, is sent to the observable object. An example of this would be an action sending a control code changing the running state of a process.*

**Parents:** DefinedEffectFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SendControlCodeEffectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| controlCode | string | zero_or_one | No | Specifies the actual control code that was sent to the observable object. |

### Server

*A server is a server rack-mount based computer, minicomputer, supercomputer, etc.*

**Parents:** Computer | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Server`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### ShopListing

*A shop listing is a listing of offered products on an online marketplace/shop.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ShopListing`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SmartDevice

*A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-based networks or via smartphone*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SmartDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SmartPhone

*A smartphone is a portable device that combines mobile telephone and computing functions into one unit.  Examples include iPhone, Samsung Galaxy, Huawei, Blackberry. (Inferred by model and OperatingSystemFacet)*

**Parents:** Computer, MobilePhone, SmartDevice | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SmartPhone`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Snapshot

*A snapshot is a file system object representing a snapshot of the contents of a part of a file system at a point in time.*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Snapshot`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Socket

*A socket is a special file used for inter-process communication, which enables communication between two processes. In addition to sending data, processes can send file descriptors across a Unix domain socket connection using the sendmsg() and recvmsg() system calls. Unlike named pipes which allow only unidirectional data flow, sockets are fully duplex-capable. [based on https://en.wikipedia.org/wiki/Unix_file_types]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Socket`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SocketAddress

*A socket address (combining and IP address and a port number) is a composite identifier for a network socket endpoint supporting internet protocol communications.*

**Parents:** Address | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SocketAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### Software

*Software is a definitely scoped instance of a collection of data or computer instructions that tell the computer how to work. [based on https://en.wikipedia.org/wiki/Software]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Software`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SoftwareFacet

*A software facet is a grouping of characteristics unique to a software program (a definitively scoped instance of a collection of data or computer instructions that tell the computer how to work). [based on https://en.wikipedia.org/wiki/Software]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SoftwareFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| cpeid | string | zero_or_one | No | Specifies the Common Platform Enumeration identifier for the software. |
| language | string | zero_or_one | No | Specifies the language the string is written in, e.g. English.           For consistency, it is strongly recommended ... |
| manufacturer | Identity | zero_or_one | No |  |
| swid | string | zero_or_one | No | Specifies the SWID tag for the software. |
| version | string | zero_or_one | No |  |

### StateChangeEffectFacet

*A state change effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a state of the observable object is changed.*

**Parents:** DefinedEffectFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/StateChangeEffectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| newObject | ObservableObject | zero_or_one | No | Specifies the observable object and its properties as they are after the state change effect occurred. |
| oldObject | ObservableObject | zero_or_one | No | Specifies the observable object and its properties as they were before the state change effect occurred. |

### StorageMedium

*A storage medium is any digital storage device that applies electromagnetic or optical surfaces, or depends solely on electronic circuits as solid state storage, for storing digital data. Examples include HDD (PATA), SATA, SSD, Optical, Memory_Card, Tape, etc*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/StorageMedium`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### StorageMediumFacet

*A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a piece of equipment or a mechanism designed to serve a special purpose or perform a special function.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/StorageMediumFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| totalStorageCapacityInBytes | integer | zero_or_one | No | The maximum number of bytes that can be stored on a storage device. |

### SymbolicLink

*A symbolic link is a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname resolution. [based on https://en.wikipedia.org/wiki/Symbolic_link]*

**Parents:** FileSystemObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLink`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### SymbolicLinkFacet

*A symbolic link facet is a grouping of characteristics unique to a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname resolution. [based on https://en.wikipedia.org/wiki/Symbolic_link]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLinkFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| targetFile | ObservableObject | zero_or_one | No | Specifies the file targeted by a symbolic link. |

### TCPConnection

*A TCP connection is a network connection that is conformant to the Transfer *

**Parents:** NetworkConnection | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TCPConnection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### TCPConnectionFacet

*A TCP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Transmission Control Protocl (TCP) standard.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TCPConnectionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| destinationFlags | hexBinary | zero_or_more | No | Specifies the destination TCP flags. |
| sourceFlags | hexBinary | zero_or_more | No | Specifies the source TCP flags. |

### TableField

*A database table field and its associated value contained within a relational database.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TableField`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### TableFieldFacet

*A database record facet contains properties associated with a specific table record value from a database.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TableFieldFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| recordFieldIsNull | boolean | zero_or_one | No | Whether the specified database record field is null. |
| recordFieldName | string | zero_or_one | No | A field name of a database record value being identified. |
| recordFieldValue | base64Binary | zero_or_one | No | The field value of a specified database record. |
| recordRowID | integer | zero_or_one | No | The unique ID that identifies a database record, supplied by the originating database engine. |
| tableName | string | zero_or_one | No | The table containing a specified database record. |
| tableSchema | string | zero_or_one | No | The schema that contains the identified database record. |

### Tablet

*A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categorized by their manufacturer as a Tablet)*

**Parents:** Computer, MobileDevice, SmartDevice | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Tablet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### TaskActionType

*A task action type is a grouping of characteristics for a scheduled action to be completed.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TaskActionType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| actionID | string | zero_or_one | No | Specifies the user-defined identifier for the action. This identifier is used by the Task Scheduler for logging purpo... |
| actionType | string | zero_or_more | No | Specifies the type of the action. See also: http://msdn.microsoft.com/en-us/library/windows/desktop/aa380596(v=vs.85)... |
| iComHandlerAction | IComHandlerActionType | zero_or_one | No | Specifies the data associated with the task action-fired COM handler. |
| iEmailAction | ObservableObject | zero_or_one | No | Specifies an action that sends an e-mail, which in this context refers to actual email message sent. See also: http:/... |
| iExecAction | IExecActionType | zero_or_one | No | Specifies an action that executes a command-line operation. See also: http://msdn.microsoft.com/en-us/library/windows... |
| iShowMessageAction | IShowMessageActionType | zero_or_one | No | Specifies an action that shows a message box when a task is activated. See also: http://msdn.microsoft.com/en-us/libr... |

### TriggerType

*A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts the execution of a task within a Windows operating system. [based on https://docs.microsoft.com/en-us/windows/win32/taskschd/task-triggers]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TriggerType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| isEnabled | boolean | zero_or_one | No | Specifies whether the trigger is enabled. |
| triggerBeginTime | dateTime | zero_or_one | No | Specifies the date/time that the trigger is activated. |
| triggerDelay | string | zero_or_one | No | Specifies the delay that takes place between when the task is registered and when the task is started. |
| triggerEndTime | dateTime | zero_or_one | No | Specifies the date/time that the trigger is deactivated. |
| triggerFrequency | string | zero_or_more | No | Specifies the frequency at which the trigger repeats. |
| triggerMaxRunTime | string | zero_or_one | No | The maximum amount of time that the task launched by the trigger is allowed to run. See also: http://msdn.microsoft.c... |
| triggerSessionChangeType | string | zero_or_one | No | Specifies the type of Terminal Server session change that would trigger a task launch. See also: http://msdn.microsof... |
| triggerType | string | zero_or_more | No | Specifies the type of the task trigger. |

### Tweet

*A tweet is message submitted by a Twitter user account to the Twitter microblogging platform.*

**Parents:** Message | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Tweet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### TwitterProfileFacet

*A twitter profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single Twitter user account. [based on https://en.wikipedia.org/wiki/User_profile]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/TwitterProfileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| favoritesCount | nonNegativeInteger | zero_or_one | No | Specifies the number of times that this profile has favorited a tweet. |
| followersCount | nonNegativeInteger | zero_or_one | No | Specifies the followers count associated with the twitter profile. |
| friendsCount | nonNegativeInteger | zero_or_one | No | Specifies the friends count associated with the twitter profile. |
| listedCount | integer | zero_or_one | No | Specifies the number of public lists that this profile is associated with. |
| profileBackgroundHash | Hash | zero_or_more | No | Specifies hashes of the background associated with the profile. |
| profileBackgroundLocation | ObservableObject | zero_or_one | No | Specifies the network location of the background associated with the profile. |
| profileBannerHash | Hash | zero_or_more | No | Specifies hashes of the banner associated with the profile. |
| profileBannerLocation | ObservableObject | zero_or_one | No | Specifies the network location of the banner associated with the profile. |
| profileImageHash | Hash | zero_or_more | No | Specifies hashes of the profile image associated with the profile. |
| profileImageLocation | ObservableObject | zero_or_one | No | Specifies the network location of the profile image associated with the profile. |
| profileIsProtected | boolean | zero_or_one | No | Specifies whether the twitter profile is protected. |
| profileIsVerified | boolean | zero_or_one | No | Specifies whether the twitter profile is verified. |
| statusesCount | nonNegativeInteger | zero_or_one | No | Specifies the number of tweets that this profile has issued. |
| twitterHandle | string | zero_or_one | No | Specifies the twitter handle associated with the profile. |
| twitterId | string | zero_or_one | No | Specifies the twitter id associated with the profile. |
| userLocationString | string | zero_or_one | No | Specifies the user-provided location string associated with the profile. |

### UNIXAccount

*A UNIX account is an account on a UNIX operating system.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### UNIXAccountFacet

*A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| gid | integer | zero_or_one | No |  |
| shell | string | zero_or_one | No |  |

### UNIXFile

*A UNIX file is a file pertaining to the UNIX operating system.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXFile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### UNIXFilePermissionsFacet

*A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a UNIX file system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXFilePermissionsFacet`

*No direct or inherited properties.*

### UNIXProcess

*A UNIX process is an instance of a computer program executed on a UNIX operating system.*

**Parents:** Process | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcess`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### UNIXProcessFacet

*A UNIX process facet is a grouping of characteristics unique to an instance of a computer program executed on a UNIX operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcessFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| openFileDescriptor | integer | zero_or_more | No | Specifies a listing of the current file descriptors used by the Unix process. |
| ruid | nonNegativeInteger | zero_or_more | No | Specifies the real user ID, which represents the Unix user who created the process. |

### UNIXVolumeFacet

*A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single UNIX file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UNIXVolumeFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| mountPoint | string | zero_or_one | No | Specifies the mount point of the partition. |
| options | string | zero_or_one | No | Specifies any options used when mounting the volume. |

### URL

*A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URL`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### URLFacet

*A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| fragment | string | zero_or_one | No | Fragment pointing to a specific part in the resource. |
| fullValue | string | zero_or_one | No | The full string value of the URL. |
| host | ObservableObject | zero_or_one | No | Domain name or IP address where the resource is located. |
| password | string | zero_or_one | No | Specifies an authentication password. |
| path | string | zero_or_one | No | Specifies the location of one object within another containing object. |
| port | integer | zero_or_one | No | Port on which communication takes place. |
| query | string | zero_or_one | No | Query passed to the resource. |
| scheme | string | zero_or_one | No | Identifies the type of URL. |
| userName | string | zero_or_one | No | Username used to authenticate to this resource. |

### URLHistory

*A URL history characterizes the stored URL history for a particular web browser*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLHistory`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### URLHistoryEntry

*A URL history entry is a grouping of characteristics unique to the properties of a single URL history entry for a particular browser.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| browserUserProfile | string | zero_or_one | No | Specifies the web browser user profile for which the URL history entry was created. |
| expirationTime | dateTime | zero_or_one | No | The date and time at which the validity of the object expires. |
| firstVisit | dateTime | zero_or_one | No | Specifies the date/time that the URL referred to by the URL field was first visited. |
| hostname | string | zero_or_one | No | Specifies the hostname of the system. |
| keywordSearchTerm | string | zero_or_more | No | Specifies a string representing a keyword search term contained within the URL field. |
| lastVisit | dateTime | zero_or_one | No | Specifies the date/time that the URL referred to by the URL field was last visited. |
| manuallyEnteredCount | nonNegativeInteger | zero_or_one | No | Specifies the number of times the URL referred to by the URL field was manually entered into the browser's address fi... |
| pageTitle | string | zero_or_one | No | Specifies the title of a web page. |
| referrerUrl | ObservableObject | zero_or_more | No | Specifies the origination point (i.e., URL) of a URL request. |
| url | ObservableObject | zero_or_one | No | Specifies a URL associated with a particular observable object or facet. |
| visitCount | integer | zero_or_one | No | Specifies the number of times a URL has been visited by a particular web browser. |

### URLHistoryFacet

*A URL history facet is a grouping of characteristics unique to the stored URL history for a particular web browser*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| browserInformation | ObservableObject | zero_or_one | No | Specifies information about the particular Web Browser. |
| urlHistoryEntry | URLHistoryEntry | zero_or_more | No | Specifies a URL history record stored in the browser's history. |

### URLVisit

*A URL visit characterizes the properties of a visit of a URL within a particular browser.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLVisit`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### URLVisitFacet

*A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL within a particular browser.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/URLVisitFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| browserInformation | ObservableObject | zero_or_one | No | Specifies information about the particular Web Browser. |
| fromURLVisit | ObservableObject | zero_or_one | No | Specifies the URL visit origination point (i.e., URL) of the URL captured in the URL history entry, if applicable. |
| url | ObservableObject | zero_or_one | No | Specifies a URL associated with a particular observable object or facet. |
| urlTransitionType | string | zero_or_more | No | Specifies how a browser navigated to a particular URL on a particular visit. |
| visitDuration | duration | zero_or_one | No | Specifies the duration of a specific visit of a URL within a particular browser. |
| visitTime | dateTime | zero_or_one | No | Specifies the date/time of a specific visit of a URL within a particular browser. |

### UserAccount

*A user account is an account controlling a user's access to a network, system or platform.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UserAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### UserAccountFacet

*A user account facet is a grouping of characteristics unique to an account controlling a user's access to a network, system, or platform.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UserAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| canEscalatePrivs | boolean | zero_or_one | No |  |
| homeDirectory | string | zero_or_one | No |  |
| isPrivileged | boolean | zero_or_one | No |  |
| isServiceAccount | boolean | zero_or_one | No |  |

### UserSession

*A user session is a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user. [based on https://en.wikipedia.org/wiki/Session_(computer_science)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UserSession`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### UserSessionFacet

*A user session facet is a grouping of characteristics unique to a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user. [based on https://en.wikipedia.org/wiki/Session_(computer_science)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/UserSessionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| effectiveGroup | string | zero_or_one | No | Specifies the name of the effective group used in the user session. |
| effectiveGroupID | string | zero_or_one | No | Specifies the effective group ID of the group used in the user session. |
| effectiveUser | ObservableObject | zero_or_one | No | Specifies the effective user details used in the user session. |
| loginTime | dateTime | zero_or_one | No | Specifies the date/time of the login for the user session. |
| logoutTime | dateTime | zero_or_one | No | Specifies the date/time of the logout for the user session. |

### ValuesEnumeratedEffectFacet

*A values enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a value of the observable object is enumerated. An example of this would be the values of a registry key.*

**Parents:** DefinedEffectFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/ValuesEnumeratedEffectFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| values | string | zero_or_one | No | The values that were enumerated as a result of the action on the object. |

### Volume

*A volume is a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Volume`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### VolumeFacet

*A volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/VolumeFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| sectorSize | integer | zero_or_one | No | The sector size of the volume in bytes. |
| volumeID | string | zero_or_one | No | The unique identifier of the volume. |

### WearableDevice

*A wearable device is an electronic device that is designed to be worn on a person's body.*

**Parents:** SmartDevice | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WearableDevice`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WebPage

*A web page is a specific collection of information provided by a website and displayed to a user in a web browser. A website typically consists of many web pages linked together in a coherent fashion. [based on https://en.wikipedia.org/wiki/Web_page]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WebPage`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WhoIs

*WhoIs is a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WhoIs`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WhoIsFacet

*A whois facet is a grouping of characteristics unique to a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WhoIsFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| creationDate | dateTime | zero_or_one | No | Specifies the date in which the registered domain was created. |
| dnssec | WhoisDNSSECTypeVocab | zero_or_one | No | Specifies the DNSSEC property associated with a Whois entry. Acceptable values are: 'Signed' or 'Unsigned'. |
| domainID | string | zero_or_one | No | Specifies the domain id for the domain associated with a Whois entry. |
| domainName | ObservableObject | zero_or_one | No | Specifies the corresponding domain name for a whois entry. |
| expirationDate | dateTime | zero_or_one | No | Specifies the date in which the registered domain will expire. |
| ipAddress | ObservableObject | zero_or_one | No | Specifies the corresponding ip address for a whois entry. Usually corresponds to a name server lookup. |
| lookupDate | dateTime | zero_or_one | No | Specifies the date and time that the Whois record was queried. |
| nameServer | ObservableObject | zero_or_more | No | Specifies a list of name server entries for a Whois entry. |
| regionalInternetRegistry | string | zero_or_more | No | specifies the name of the Regional Internet Registry (RIR) which allocated the IP address contained in a WHOIS entry. |
| registrantContactInfo | ObservableObject | zero_or_one | No | Specifies contact info for the registrant of a domain within a WHOIS entity. |
| registrantIDs | string | zero_or_more | No | Specifies the registrant IDs associated with a domain lookup. |
| registrarInfo | WhoisRegistrarInfoType | zero_or_one | No | Specifies registrar info that would be returned from a registrar lookup. |
| remarks | string | zero_or_one | No | Specifies any remarks associated with this Whois entry. |
| serverName | ObservableObject | zero_or_one | No | Specifies the corresponding server name for a whois entry. This usually corresponds to a name server lookup. |
| sponsoringRegistrar | string | zero_or_one | No | Specifies the name of the sponsoring registrar for a domain. |
| status | string | zero_or_more | No | Specifies a list of statuses for a given Whois entry. |
| updatedDate | dateTime | zero_or_one | No | Specifies the date in which the registered domain information was last updated. |

### WhoisContactFacet

*A Whois contact type is a grouping of characteristics unique to contact-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]*

**Parents:** ContactFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WhoisContactFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| birthdate | dateTime | zero_or_one | No |  |
| contactAddress | ContactAddress | zero_or_more | No | Contact address specifies information characterizing a geolocation address of a contact entity. |
| contactAffiliation | ContactAffiliation | zero_or_more | No | Contact affiliation specifies information characterizing details of an organizational affiliation for a single contac... |
| contactEmail | ContactEmail | zero_or_more | No | Contact email specifies information characterizing details for contacting a contact entity by email. |
| contactGroup | string | zero_or_more | No | Contact group specifies the name/tag of a particular named/tagged grouping of contacts. |
| contactID | string | zero_or_one | No | Specifies an ID for the contact. |
| contactMessaging | ContactMessaging | zero_or_more | No | Contact messaging specifies information characterizing details for contacting a contact entity by digital messaging. |
| contactNote | string | zero_or_more | No | Contact note specifies a comment/note associated with a given contact. |
| contactPhone | ContactPhone | zero_or_more | No | Contact phone specifies information characterizing details for contacting a contact entity by telephone. |
| contactProfile | ContactProfile | zero_or_more | No | Contact profile specifies information characterizing details for contacting a contact entity by online service. |
| contactSIP | ContactSIP | zero_or_more | No | Contact SIP specifies information characterizing details for contacting a contact entity by Session Initiation Protoc... |
| contactURL | ContactURL | zero_or_more | No | Contact URL specifies information characterizing details for contacting a contact entity by Uniform Resource Locator ... |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |
| firstName | string | zero_or_one | No | The first name of a person. |
| lastName | string | zero_or_one | No | The last name of a person. |
| lastTimeContacted | dateTime | zero_or_one | No | Last time contacted specifies the date and time that a particular contact was last contacted. |
| middleName | string | zero_or_one | No | The middle name of a person. |
| namePhonetic | string | zero_or_one | No | Name phonetic specifies the phonetic pronunciation of the name of a person. |
| namePrefix | string | zero_or_one | No | Name prefix specifies an honorific prefix (coming ordinally before first/given name) for the name of a person. |
| nameSuffix | string | zero_or_one | No | Name suffix specifies an suffix (coming ordinally after last/family name) for the name of a person. |
| nickname | string | zero_or_more | No | Nickname specifies an alternate, unofficial and typically informal name for a person independent of their official name. |
| numberTimesContacted | integer | zero_or_one | No | Number times contacted specifies the number of times a particular contact has been contacted. |
| sourceApplication | ObservableObject | zero_or_one | No | Source application specifies the software application that a particular contact or contact list is associated with. |
| whoisContactType | string | zero_or_more | No | Specifies what type of WHOIS contact this is. |

### WhoisRegistrarInfoType

*A Whois registrar info type is a grouping of characteristics unique to registrar-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WhoisRegistrarInfoType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| contactPhoneNumber | ObservableObject | zero_or_one | No | Contact phone number specifies a telephone service account number for contacting a contact entity by telephone. |
| emailAddress | ObservableObject | zero_or_one | No | An email address. |
| geolocationAddress | Location | zero_or_one | No | An administrative address for a particular geolocation. |
| referralURL | ObservableObject | zero_or_one | No | Specifies the corresponding referral URL for a registrar. |
| registrarGUID | string | zero_or_one | No | Specifies the Registrar GUID field of a Whois entry. |
| registrarID | string | zero_or_one | No | Specifies the Registrar ID field of a Whois entry. |
| registrarName | string | zero_or_one | No | The name of the registrar organization. |
| whoisServer | ObservableObject | zero_or_one | No | Specifies the corresponding whois server for a registrar. |

### WifiAddress

*A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a device network interface to enable routing and management of IEEE 802.11 standards-conformant communications to and from that device.*

**Parents:** MACAddress | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WifiAddress`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WifiAddressFacet

*A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) standards conformant identifier assigned to a device network interface to enable routing and management of IEEE 802.11 standards-conformant communications to and from that device.*

**Parents:** MACAddressFacet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WifiAddressFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressValue | string | zero_or_one | No | The value of an address. |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |

### Wiki

*A wiki is an online hypertext publication collaboratively edited and managed by its own audience directly using a web browser. A typical wiki contains multiple pages/articles for the subjects or scope of the project and could be either open to the public or limited to use within an organization for maintaining its internal knowledge base. [based on https://en.wikipedia.org/wiki/Wiki]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/Wiki`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WikiArticle

*A wiki article is one or more pages in a wiki focused on characterizing a particular topic.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WikiArticle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsAccount

*A Windows account is a user account on a Windows operating system.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsAccountFacet

*A Windows account facet is a grouping of characteristics unique to a user account on a Windows operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| groups | string | zero_or_more | No |  |

### WindowsActiveDirectoryAccount

*A Windows Active Directory account is an account managed by directory-based identity-related services of a Windows operating system.*

**Parents:** DigitalAccount | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccount`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsActiveDirectoryAccountFacet

*A Windows Active Directory account facet is a grouping of characteristics unique to an account managed by directory-based identity-related services of a Windows operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccountFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| activeDirectoryGroups | string | zero_or_more | No |  |
| objectGUID | string | zero_or_one | No |  |

### WindowsComputerSpecification

*A Windows computer specification is the hardware ans software of a programmable electronic device that can store, retrieve, and process data running a Microsoft Windows operating system. [based on merriam-webster.com/dictionary/computer]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecification`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsComputerSpecificationFacet

*A Windows computer specification facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data running a Microsoft Windows operating system. [based on merriam-webster.com/dictionary/computer]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecificationFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| domain | string | zero_or_more | No | The domain(s) that the system belongs to. |
| globalFlagList | GlobalFlagType | zero_or_more | No | A list of global flags. See also: http://msdn.microsoft.com/en-us/library/windows/hardware/ff549557(v=vs.85).aspx. |
| lastShutdownDate | dateTime | zero_or_one | No | Specifies the date on which the device was last shutdown. |
| msProductID | string | zero_or_one | No | The Microsoft Product ID. See also: http://support.microsoft.com/gp/pidwin. |
| msProductName | string | zero_or_one | No | The Microsoft ProductName of the current installation of Windows. This is typically found in HKEY_LOCAL_MACHINE\Softw... |
| netBIOSName | string | zero_or_one | No | Specifies the NetBIOS (Network Basic Input/Output System) name of the Windows system. This is not the same as the hos... |
| osInstallDate | dateTime | zero_or_one | No | Specifies the date on which the operating system (OS) was installed. |
| osLastUpgradeDate | dateTime | zero_or_one | No | Specifies the date on which the operating system (OS) was last upgraded. |
| registeredOrganization | Identity | zero_or_one | No | The organization that this copy of Windows is registered to. |
| registeredOwner | Identity | zero_or_one | No | The person or organization that is the registered owner of this copy of Windows. |
| windowsDirectory | ObservableObject | zero_or_one | No | The Windows_Directory field specifies the fully-qualified path to the Windows install directory. |
| windowsSystemDirectory | ObservableObject | zero_or_one | No | The Windows_System_Directory field specifies the fully-qualified path to the Windows system directory. |
| windowsTempDirectory | ObservableObject | zero_or_one | No | The Windows_Temp_Directory field specifies the fully-qualified path to the Windows temporary files directory. |

### WindowsCriticalSection

*A Windows critical section is a Windows object that provides synchronization similar to that provided by a mutex object, except that a critical section can be used only by the threads of a single process. Critical section objects cannot be shared across processes. Event, mutex, and semaphore objects can also be used in a single-process application, but critical section objects provide a slightly faster, more efficient mechanism for mutual-exclusion synchronization (a processor-specific test and set instruction). Like a mutex object, a critical section object can be owned by only one thread at a time, which makes it useful for protecting a shared resource from simultaneous access. Unlike a mutex object, there is no way to tell whether a critical section has been abandoned. [based on https://docs.microsoft.com/en-us/windows/win32/sync/critical-section-objects]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsCriticalSection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsEvent

*A Windows event is a notification record of an occurance of interest (system, security, application, etc.) on a Windows operating system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsEvent`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsFilemapping

*A Windows file mapping is the association of a file's contents with a portion of the virtual address space of a process within a Windows operating system. The system creates a file mapping object (also known as a section object) to maintain this association. A file view is the portion of virtual address space that a process uses to access the file's contents. File mapping allows the process to use both random input and output (I/O) and sequential I/O. It also allows the process to work efficiently with a large data file, such as a database, without having to map the whole file into memory. Multiple processes can also use memory-mapped files to share data. Processes read from and write to the file view using pointers, just as they would with dynamically allocated memory. The use of file mapping improves efficiency because the file resides on disk, but the file view resides in memory.[based on https://docs.microsoft.com/en-us/windows/win32/memory/file-mapping]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsFilemapping`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsHandle

*A Windows handle is an abstract reference to a resource within the Windows operating system, such as a window, memory, an open file or a pipe. It is the mechanism by which applications interact with such resources in the Windows operating system.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsHandle`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsHook

*A Windows hook is a mechanism by which an application can intercept events, such as messages, mouse actions, and keystrokes within the Windows operating system. A function that intercepts a particular type of event is known as a hook procedure. A hook procedure can act on each event it receives, and then modify or discard the event. [based on https://docs.microsoft.com/en-us/windows/win32/winmsg/about-hooks]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsHook`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsMailslot

*A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard file functions. The data in a mailslot message can be in any form, but cannot be larger than 424 bytes when sent between computers. Unlike disk files, mailslots are temporary. When all handles to a mailslot are closed, the mailslot and all the data it contains are deleted. [based on https://docs.microsoft.com/en-us/windows/win32/ipc/about-mailslots]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsMailslot`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsNetworkShare

*A Windows network share is a Windows computer resource made available from one host to other hosts on a computer network. It is a device or piece of information on a computer that can be remotely accessed from another computer transparently as if it were a resource in the local machine. Network sharing is made possible by inter-process communication over the network. [based on https://en.wikipedia.org/wiki/Shared_resource]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsNetworkShare`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsPEBinaryFile

*A Windows PE binary file is a Windows portable executable (PE) file.*

**Parents:** File | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFile`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsPEBinaryFileFacet

*A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable executable (PE) file.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFileFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| characteristics | unsignedShort | zero_or_more | No | Specifies the flags that indicate the fileâ€™s characteristics. |
| fileHeaderHashes | Hash | zero_or_more | No | Specifies any hashes that were computed for the file header. |
| impHash | string | zero_or_one | No | Specifies the special import hash, or â€˜imphashâ€™, calculated for the PE Binary based on its imported libraries and... |
| machine | string | zero_or_more | No | Specifies the type of target machine. |
| numberOfSections | integer | zero_or_one | No | Specifies the number of sections in the PE binary, as a non-negative integer. |
| numberOfSymbols | integer | zero_or_one | No | Specifies the number of entries in the symbol table of the PE binary, as a non-negative integer. |
| optionalHeader | WindowsPEOptionalHeader | zero_or_one | No | Specifies the PE optional header of the PE binary. |
| peType | string | zero_or_one | No | Specifies the type of the PE binary. |
| pointerToSymbolTable | hexBinary | zero_or_more | No | Specifies the file offset of the COFF symbol table. |
| sections | WindowsPESection | zero_or_more | No | Specifies metadata about the sections in the PE file. |
| sizeOfOptionalHeader | integer | zero_or_one | No | Specifies the size of the optional header of the PE binary.  |
| timeDateStamp | dateTime | zero_or_one | No | Specifies the time when the PE binary was created. |

### WindowsPEFileHeader

*A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the overall nature and structure of the file.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEFileHeader`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| timeDateStamp | dateTime | zero_or_one | No | Specifies the time when the PE binary was created. |

### WindowsPEOptionalHeader

*A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the executable code structure of the file.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEOptionalHeader`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| addressOfEntryPoint | unsignedInt | zero_or_more | No | Specifies the address of the entry point relative to the image base when the executable is loaded into memory. |
| baseOfCode | unsignedInt | zero_or_more | No | Specifies the address that is relative to the image base of the beginning-of-code section when it is loaded into memory. |
| checksum | unsignedInt | zero_or_more | No | Specifies the checksum of the PE binary. |
| dllCharacteristics | unsignedShort | zero_or_more | No | Specifies the flags that characterize the PE binary. |
| fileAlignment | unsignedInt | zero_or_more | No | Specifies the factor (in bytes) that is used to align the raw data of sections in the image file. |
| imageBase | unsignedInt | zero_or_more | No | Specifies the address that is relative to the image base of the beginning-of-data section when it is loaded into memory. |
| loaderFlags | unsignedInt | zero_or_more | No | Specifies the reserved loader flags |
| magic | unsignedShort | zero_or_more | No | Specifies the value that indicates the type of the PE binary. |
| majorImageVersion | unsignedShort | zero_or_more | No | Specifies the major version number of the image. |
| majorLinkerVersion | byte | zero_or_more | No | Specifies the linker major version number. |
| majorOSVersion | unsignedShort | zero_or_more | No | Specifies the major version number of the required operating system. |
| majorSubsystemVersion | unsignedShort | zero_or_more | No | Specifies the major version number of the subsystem. |
| minorImageVersion | unsignedShort | zero_or_more | No | Specifies the minor version number of the image. |
| minorLinkerVersion | byte | zero_or_more | No | Specifies the linker minor version number. |
| minorOSVersion | unsignedShort | zero_or_more | No | Specifies the minor version number of the required operating system. |
| minorSubsystemVersion | unsignedShort | zero_or_more | No | Specifies the minor version number of the subsystem.            |
| numberOfRVAAndSizes | unsignedInt | zero_or_more | No | Specifies the number of data-directory entries in the remainder of the optional header. |
| sectionAlignment | unsignedInt | zero_or_more | No | Specifies the alignment (in bytes) of PE sections when they are loaded into memory. |
| sizeOfCode | unsignedInt | zero_or_more | No | Specifies the size of the code (text) section. If there are multiple such sections, this refers to the sum of the siz... |
| sizeOfHeaders | unsignedInt | zero_or_more | No | Specifies the combined size of the MS-DOS, PE header, and section headers, rounded up a multiple of the value specifi... |
| sizeOfHeapCommit | unsignedInt | zero_or_more | No | Specifies the size of the local heap space to commit. |
| sizeOfHeapReserve | unsignedInt | zero_or_more | No | Specifies the size of the local heap space to reserve. |
| sizeOfImage | unsignedInt | zero_or_more | No | Specifies the size, in bytes, of the image, including all headers, as the image is loaded in memory. |
| sizeOfInitializedData | unsignedInt | zero_or_more | No | Specifies the size of the initialized data section. If there are multiple such sections, this refers to the sum of th... |
| sizeOfStackCommit | unsignedInt | zero_or_more | No | Specifies the size of the stack to commit. |
| sizeOfStackReserve | unsignedInt | zero_or_more | No | Specifies the size of the stack to reserve. |
| sizeOfUninitializedData | unsignedInt | zero_or_more | No | Specifies the size of the uninitialized data section. If there are multiple such sections, this refers to the sum of ... |
| subsystem | unsignedShort | zero_or_more | No | Specifies the subsystem (e.g., GUI, device driver, etc.) that is required to run this image. |
| win32VersionValue | unsignedInt | zero_or_more | No | Specifies the reserved win32 version value. |

### WindowsPESection

*A Windows PE section is a grouping of characteristics unique to a specific default or custom-defined region of a Windows PE (Portable Executable) file, consisting of an individual portion of the actual executable content of the file delineated according to unique purpose and memory protection requirements.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPESection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| entropy | decimal | zero_or_one | No | Shannon entropy (a measure of randomness) of the data. |
| hashes | Hash | zero_or_more | No | Specifies any hashes computed over the section. |
| size | integer | zero_or_one | No | Specifies the size of the section, in bytes. |

### WindowsPrefetch

*The Windows prefetch contains entries in a Windows prefetch file (used to speed up application startup starting with Windows XP).*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetch`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsPrefetchFacet

*A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefetch file (used to speed up application startup starting with Windows XP).*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetchFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| accessedDirectory | ObservableObject | zero_or_more | No | Directories accessed by the prefetch application during startup. |
| accessedFile | ObservableObject | zero_or_more | No | Files (e.g., DLLs and other support files) used by the application during startup. |
| applicationFileName | string | zero_or_one | No | Name of the executable of the prefetch file. |
| firstRun | dateTime | zero_or_one | No | Timestamp of when the prefetch application was first run. |
| lastRun | dateTime | zero_or_one | No | Timestamp of when the prefetch application was last run. |
| prefetchHash | string | zero_or_one | No | An eight character hash of the location from which the application was run. |
| timesExecuted | integer | zero_or_one | No | The number of times the prefetch application has executed. |
| volume | ObservableObject | zero_or_one | No | The volume from which the prefetch application was run. If the applicatin was run from multiple volumes, there will b... |

### WindowsProcess

*A Windows process is a program running on a Windows operating system.*

**Parents:** Process | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcess`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsProcessFacet

*A Windows process facet is a grouping of characteristics unique to a program running on a Windows operating system.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcessFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| aslrEnabled | boolean | zero_or_one | No |  |
| depEnabled | boolean | zero_or_one | No |  |
| ownerSID | string | zero_or_one | No |  |
| priority | string | zero_or_one | No | The priority of the email. |
| startupInfo | Dictionary | zero_or_one | No |  |
| windowTitle | string | zero_or_one | No |  |

### WindowsRegistryHive

*The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to use the registry). [based on https://en.wikipedia.org/wiki/Windows_Registry]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHive`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsRegistryHiveFacet

*A Windows registry hive facet is a grouping of characteristics unique to a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to use the registry). [based on https://en.wikipedia.org/wiki/Windows_Registry]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHiveFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| hiveType | string | zero_or_one | No | The type of a registry hive. |

### WindowsRegistryKey

*A Windows registry key is a particular key within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to use the registry). [based on https://en.wikipedia.org/wiki/Windows_Registry]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKey`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsRegistryKeyFacet

*A Windows registry key facet is a grouping of characteristics unique to a particular key within a Windows registry (A hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to use the registry). [based on https://en.wikipedia.org/wiki/Windows_Registry]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKeyFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| creator | ObservableObject | zero_or_one | No | Specifies the name of the creator of the registry key. |
| key | string | zero_or_one | No |  |
| modifiedTime | dateTime | zero_or_one | No | The date and time at which the Object was last modified. |
| numberOfSubkeys | integer | zero_or_one | No |  |
| registryValues | WindowsRegistryValue | zero_or_more | No | The values that were enumerated as a result of the action on the object. |

### WindowsRegistryValue

*A Windows registry value is a grouping of characteristics unique to a particular value within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to use the registry. [based on https://en.wikipedia.org/wiki/Windows_Registry]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryValue`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| data | string | zero_or_one | No |  |
| dataType | string | zero_or_one | No |  |

### WindowsService

*A Windows service is a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UNIX daemon runs on UNIX). [based on https://en.wikipedia.org/wiki/Windows_service]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsService`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsServiceFacet

*A Windows service facet is a grouping of characteristics unique to a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UNIX daemon runs on UNIX). [based on https://en.wikipedia.org/wiki/Windows_service]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| descriptions | string | zero_or_more | No |  |
| displayName | string | zero_or_one | No | Display name specifies the name to display for some entity within a user interface. |
| groupName | string | zero_or_one | No |  |
| serviceName | string | zero_or_one | No |  |
| serviceStatus | string | zero_or_one | No |  |
| serviceType | string | zero_or_one | No |  |
| startCommandLine | string | zero_or_one | No |  |
| startType | string | zero_or_one | No |  |

### WindowsSystemRestore

*A Windows system restore is a capture of a Windows computer's state (including system files, installed applications, Windows Registry, and system settings) at a particular point in time such that the computer can be reverted to that state in the event of system malfunctions or other problems. [based on https://en.wikipedia.org/wiki/System_Restore]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsSystemRestore`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsTask

*A Windows task is a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler. [based on http://msdn.microsoft.com/en-us/library/windows/desktop/aa381311(v=vs.85).aspx]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsTask`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsTaskFacet

*A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler). [based on http://msdn.microsoft.com/en-us/library/windows/desktop/aa381311(v=vs.85).aspx]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsTaskFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| account | ObservableObject | zero_or_one | No | Specifies the account referenced in an event log entry or used to run the scheduled task. See also: http://msdn.micro... |
| accountLogonType | string | zero_or_one | No | Specifies the security logon method required to run the tasks associated with the account. See also: http://msdn.micr... |
| accountRunLevel | string | zero_or_one | No | Specifies the permission level of the account that the task will be run at. |
| actionList | TaskActionType | zero_or_more | No | Specifies a list of actions to be performed by the scheduled task. |
| application | ObservableObject | zero_or_one | No | The application associated with this object. |
| exitCode | integer | zero_or_one | No | Specifies the last exit code of the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/desktop... |
| flags | string | zero_or_more | No | Specifies any flags that modify the behavior of the scheduled task. See also: http://msdn.microsoft.com/en-us/library... |
| imageName | string | zero_or_one | No | Specifies the image name for the task. |
| maxRunTime | integer | zero_or_one | No | Specifies the maximum run time of the scheduled task before terminating, in milliseconds. See also: http://msdn.micro... |
| mostRecentRunTime | dateTime | zero_or_one | No | Specifies the most recent run date/time of this scheduled task. See also: http://msdn.microsoft.com/en-us/library/win... |
| nextRunTime | dateTime | zero_or_one | No | Specifies the next run date/time of the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/des... |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| parameters | string | zero_or_one | No | Specifies the command line parameters used to launch the scheduled task. See also: http://msdn.microsoft.com/en-us/li... |
| priority | integer | zero_or_more | No | The priority of the email. |
| status | string | zero_or_more | No | Specifies a list of statuses for a given Whois entry. |
| taskComment | string | zero_or_one | No | Specifies a comment for the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/desktop/aa38123... |
| taskCreator | string | zero_or_one | No | Specifies the name of the creator of the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/de... |
| triggerList | TriggerType | zero_or_more | No | Specifies a set of triggers used by the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/des... |
| workItemData | ObservableObject | zero_or_one | No | Specifies application defined data associated with the scheduled task. See also: http://msdn.microsoft.com/en-us/libr... |
| workingDirectory | ObservableObject | zero_or_one | No | Specifies the working directory for the scheduled task. See also: http://msdn.microsoft.com/en-us/library/windows/des... |

### WindowsThread

*A Windows thread is a single thread of execution within a Windows process.*

**Parents:** ProcessThread | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsThread`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WindowsThreadFacet

*A Windows thread facet is a grouping os characteristics unique to a single thread of execution within a Windows process.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsThreadFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| context | string | zero_or_one | No |  |
| creationFlags | unsignedInt | zero_or_more | No |  |
| creationTime | dateTime | zero_or_one | No |  |
| observableCreatedTime | dateTime | zero_or_one | No | The date and time at which the observable object being characterized was created. This time pertains to an intrinsic ... |
| parameterAddress | hexBinary | zero_or_more | No |  |
| priority | integer | zero_or_one | No | The priority of the email. |
| runningStatus | string | zero_or_one | No |  |
| securityAttributes | string | zero_or_one | No |  |
| stackSize | nonNegativeInteger | zero_or_more | No |  |
| startAddress | hexBinary | zero_or_more | No |  |
| threadID | nonNegativeInteger | zero_or_more | No |  |

### WindowsVolumeFacet

*A Windows volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single Windows file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsVolumeFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| driveLetter | string | zero_or_one | No | Specifies the drive letter of a windows volume. |
| driveType | string | zero_or_more | No | Specifies the drive type of a windows volume. |
| windowsVolumeAttributes | WindowsVolumeAttributeVocab | zero_or_more | No | Specifies the attributes of a windows volume. |

### WindowsWaitableTime

*A Windows waitable timer is a synchronization object within the Windows operating system whose state is set to signaled when a specified due time arrives. There are two types of waitable timers that can be created: manual-reset and synchronization. A timer of either type can also be a periodic timer. [based on https://docs.microsoft.com/en-us/windows/win32/sync/waitable-timer-objects]*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsWaitableTime`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WirelessNetworkConnection

*A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 standards-confromant digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** NetworkConnection | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnection`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### WirelessNetworkConnectionFacet

*A wireless network connection facet is a grouping of characteristics unique to a connection (completed or attempted) across an IEEE 802.11 standards-conformant digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.html]*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnectionFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| baseStation | string | zero_or_one | No | The base station. |
| password | string | zero_or_one | No | Specifies an authentication password. |
| ssid | string | zero_or_one | No | Network identifier. |
| wirelessNetworkSecurityMode | string | zero_or_more | No | Specifies the security mode of a wireless network (None, WEP, WPA, etc). |

### WriteBlocker

*A write blocker is a device that allows read-only access to storage mediums in order to preserve the integrity of the data being analyzed. Examples include Tableau, Cellibrite, Talon, etc.*

**Parents:** Device | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WriteBlocker`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### X509Certificate

*A X.509 certificate is a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard.*

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/X509Certificate`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### X509CertificateFacet

*A X.509 certificate facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard. *

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/X509CertificateFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| isSelfSigned | boolean | zero_or_one | No |  |
| issuer | string | zero_or_one | No |  |
| issuerHash | Hash | zero_or_one | No | A hash calculated on the certificate issuer name. |
| serialNumber | string | zero_or_one | No |  |
| signature | string | zero_or_one | No | A |
| signatureAlgorithm | string | zero_or_one | No |  |
| subject | string | zero_or_one | No | The subject of the email. |
| subjectHash | Hash | zero_or_one | No | A hash calculated on the certificate subject name. |
| subjectPublicKeyAlgorithm | string | zero_or_one | No |  |
| subjectPublicKeyExponent | integer | zero_or_one | No |  |
| subjectPublicKeyModulus | string | zero_or_one | No |  |
| thumbprintHash | Hash | zero_or_one | No | A hash calculated on the entire certificate including signature. |
| validityNotAfter | dateTime | zero_or_one | No |  |
| validityNotBefore | dateTime | zero_or_one | No |  |
| version | string | zero_or_one | No |  |
| x509v3extensions | X509V3ExtensionsFacet | zero_or_one | No |  |

### X509V3Certificate

*An X.509 v3 certificate is a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard. *

**Parents:** ObservableObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/X509V3Certificate`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| hasChanged | boolean | zero_or_one | No |  |
| state | string | zero_or_one | No |  |

### X509V3ExtensionsFacet

*An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/X509V3ExtensionsFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| authorityKeyIdentifier | string | zero_or_one | No |  |
| basicConstraints | string | zero_or_one | No |  |
| certificatePolicies | string | zero_or_one | No |  |
| crlDistributionPoints | string | zero_or_one | No |  |
| extendedKeyUsage | string | zero_or_one | No |  |
| inhibitAnyPolicy | string | zero_or_one | No |  |
| issuerAlternativeName | string | zero_or_one | No |  |
| keyUsage | string | zero_or_one | No |  |
| nameConstraints | string | zero_or_one | No |  |
| policyConstraints | string | zero_or_one | No |  |
| policyMappings | string | zero_or_one | No |  |
| privateKeyUsagePeriodNotAfter | dateTime | zero_or_one | No |  |
| privateKeyUsagePeriodNotBefore | dateTime | zero_or_one | No |  |
| subjectAlternativeName | string | zero_or_one | No |  |
| subjectDirectoryAttributes | string | zero_or_one | No |  |
| subjectKeyIdentifier | string | zero_or_one | No |  |

## uco.pattern

### LogicalPattern

*A logical pattern is a grouping of characteristics unique to an informational pattern expressed via a structured pattern expression following the rules of logic.*

**Parents:** Pattern | **IRI:** `https://ontology.unifiedcyberontology.org/uco/pattern/LogicalPattern`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| patternExpression | PatternExpression | zero_or_one | No | An explicit logical pattern expression. |

### Pattern

*A pattern is a combination of properties, acts, tendencies, etc., forming a consistent or characteristic arrangement.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/pattern/Pattern`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### PatternExpression

*A pattern expression is a grouping of characteristics unique to an explicit logical expression defining a pattern (e.g., regular expression, SQL Select expression, etc.).*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression`

*No direct or inherited properties.*

## uco.role

### BenevolentRole

*A benevolent role is a role with positive and/or beneficial intent.*

**Parents:** Role | **IRI:** `https://ontology.unifiedcyberontology.org/uco/role/BenevolentRole`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### MaliciousRole

*A malicious role is a role with malevolent intent.*

**Parents:** Role | **IRI:** `https://ontology.unifiedcyberontology.org/uco/role/MaliciousRole`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### NeutralRole

*A neutral role is a role with impartial intent.*

**Parents:** Role | **IRI:** `https://ontology.unifiedcyberontology.org/uco/role/NeutralRole`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### Role

*A role is a usual or customary function based on contextual perspective.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/role/Role`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

## uco.tool

### AnalyticTool

*An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of explanation, interpretation or logical reasoning.*

**Parents:** Tool | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/AnalyticTool`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| creator | Identity | zero_or_one | No | The creator organization for a particular tool. |
| references | anyURI | zero_or_more | No | References to information describing a particular tool. |
| servicePack | string | zero_or_one | No | An appropriate service pack descriptor for a particular tool. |
| toolType | string | zero_or_one | No | The type of tool. |
| version | string | zero_or_one | No | An appropriate version descriptor of a particular tool. |

### BuildFacet

*A build facet is a grouping of characteristics unique to a particular version of a software.*

**Parents:** Facet | **Type:** Facet | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/BuildFacet`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| buildInformation | BuildInformationType | zero_or_one | No | Describes how a particular tool was built. |

### BuildInformationType

*A build information type is a grouping of characteristics that describe how a particular version of software was converted from source code to executable code.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/BuildInformationType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| buildConfiguration | Configuration | zero_or_one | No | How the build utility was configured for a particular build of a particular software. |
| buildID | string | zero_or_one | No | An externally defined unique identifier for a particular build of a software. |
| buildLabel | string | zero_or_one | No | Relevant label for a particular build of a particular software. |
| buildOutputLog | string | zero_or_one | No | The output log of the build process for a software. |
| buildProject | string | zero_or_one | No | The project name of a build of a software. |
| buildScript | string | zero_or_one | No | The actual build script for a particular build of a particular software. |
| buildUtility | BuildUtilityType | zero_or_one | No | Identifies the utility used to build a software. |
| buildVersion | string | zero_or_one | No | The appropriate version descriptor of a particular build of a particular software. |
| compilationDate | dateTime | zero_or_one | No | The compilation date for the build of a software. |
| compilers | CompilerType | zero_or_more | No | The compilers utilized during a particular build of a particular software. |
| libraries | LibraryType | zero_or_more | No | The libraries incorporated into a particular build of a software. |

### BuildUtilityType

*A build utility type characterizes the tool used to convert from source code to executable code for a particular version of software.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/BuildUtilityType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| buildUtilityName | string | zero_or_one | No | The informally defined name of the utility used to build a particular software. |
| cpeid | string | zero_or_one | No | Specifies the Common Platform Enumeration identifier for the software. |
| swid | string | zero_or_one | No | Specifies the SWID tag for the software. |

### CompilerType

*A compiler type is a grouping of characteristics unique to a specific program that translates computer code written in one programming language (the source language) into another language (the target language). Typically a program that translates source code from a high-level programming language to a lower-level language (e.g., assembly language, object code, or machine code) to create an executable program. [based on https://en.wikipedia.org/wiki/Compiler]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/CompilerType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| compilerInformalDescription | string | zero_or_one | No | An informal description of a compiler. |
| cpeid | string | zero_or_one | No | Specifies the Common Platform Enumeration identifier for the software. |
| swid | string | zero_or_one | No | Specifies the SWID tag for the software. |

### ConfiguredTool

*A ConfiguredTool is a Tool that is known to be configured to run in a more specified manner than some unconfigured or less-configured Tool.*

**Parents:** Tool | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/ConfiguredTool`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| creator | Identity | zero_or_one | No | The creator organization for a particular tool. |
| references | anyURI | zero_or_more | No | References to information describing a particular tool. |
| servicePack | string | zero_or_one | No | An appropriate service pack descriptor for a particular tool. |
| toolType | string | zero_or_one | No | The type of tool. |
| version | string | zero_or_one | No | An appropriate version descriptor of a particular tool. |
| isConfigurationOf | Tool | zero_or_one | No | The object which has been configured to run in a more specified manner than another object.  This property is expecte... |
| usesConfiguration | Configuration | zero_or_one | No | A configuration used by an object. |

### DefensiveTool

*A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of guarding.*

**Parents:** Tool | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/DefensiveTool`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| creator | Identity | zero_or_one | No | The creator organization for a particular tool. |
| references | anyURI | zero_or_more | No | References to information describing a particular tool. |
| servicePack | string | zero_or_one | No | An appropriate service pack descriptor for a particular tool. |
| toolType | string | zero_or_one | No | The type of tool. |
| version | string | zero_or_one | No | An appropriate version descriptor of a particular tool. |

### LibraryType

*A library type is a grouping of characteristics unique to a collection of resources incorporated into the build of a software.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/LibraryType`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| libraryName | string | zero_or_one | No | The name of the library. |
| libraryVersion | string | zero_or_one | No | The version of the library. |

### MaliciousTool

*A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent task or purpose.*

**Parents:** Tool | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/MaliciousTool`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| creator | Identity | zero_or_one | No | The creator organization for a particular tool. |
| references | anyURI | zero_or_more | No | References to information describing a particular tool. |
| servicePack | string | zero_or_one | No | An appropriate service pack descriptor for a particular tool. |
| toolType | string | zero_or_one | No | The type of tool. |
| version | string | zero_or_one | No | An appropriate version descriptor of a particular tool. |

### Tool

*A tool is an element of hardware and/or software utilized to carry out a particular function.*

**Parents:** UcoObject | **IRI:** `https://ontology.unifiedcyberontology.org/uco/tool/Tool`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |
| creator | Identity | zero_or_one | No | The creator organization for a particular tool. |
| references | anyURI | zero_or_more | No | References to information describing a particular tool. |
| servicePack | string | zero_or_one | No | An appropriate service pack descriptor for a particular tool. |
| toolType | string | zero_or_one | No | The type of tool. |
| version | string | zero_or_one | No | An appropriate version descriptor of a particular tool. |

## uco.types

### ControlledDictionary

*A controlled dictionary is a list of (term/key, value) pairs where each term/key exists no more than once and is constrained to an explicitly defined set of values.*

**Parents:** Dictionary | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| entry | ControlledDictionaryEntry | zero_or_more | No | A dictionary entry. |

### ControlledDictionaryEntry

*A controlled dictionary entry is a single (term/key, value) pair where the term/key is constrained to an explicitly defined set of values.*

**Parents:** DictionaryEntry | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionaryEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| key | string | exactly_one | Yes | A key property of a single dictionary entry. |
| value | string | exactly_one | Yes | A specific property value. |

### Dictionary

*A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist no more than once.  types:Dictionary alone does not validate this expectation, but validation is available.  For use cases where this expectation must be validated, the subclass types:ProperDictionary should be used instead of types:Dictionary.  For instances where this expectation has been found to be violated, the subclass types:ImproperDictionary should be used instead of types:Dictionary.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/Dictionary`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| entry | DictionaryEntry | zero_or_more | No | A dictionary entry. |

### DictionaryEntry

*A dictionary entry is a single (term/key, value) pair.*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| key | string | exactly_one | Yes | A key property of a single dictionary entry. |
| value | string | exactly_one | Yes | A specific property value. |

### Hash

*A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the 'hash') and is a one-way function, that is, a function which is practically infeasible to invert. This is commonly used for integrity checking of data. [based on https://en.wikipedia.org/wiki/Cryptographic_hash_function]*

**Parents:** UcoInherentCharacterizationThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/Hash`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| hashMethod | string | zero_or_more | No | A particular cryptographic hashing method (e.g., MD5). |
| hashValue | hexBinary | exactly_one | Yes | A cryptographic hash value. |

### ImproperDictionary

**Parents:** Dictionary | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/ImproperDictionary`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| entry | DictionaryEntry | zero_or_more | No | A dictionary entry. |
| repeatsKey | string | zero_or_more | No | A key found to be repeated in multiple dictionary entries within one dictionary. |

### ProperDictionary

*A proper dictionary is list of (term/key, value) pairs with each term/key existing no more than once.*

**Parents:** Dictionary | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/ProperDictionary`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| entry | DictionaryEntry | zero_or_more | No | A dictionary entry. |

### Thread

*A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Thread is similar to a Collections Ontology List, except a Thread may fork and merge - that is, one of its members may have two or more direct successors, and two or more direct predecessors.*

**Parents:** UcoThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/Thread`

*No direct or inherited properties.*

### ThreadItem

*A ThreadItem is a member of a thread.*

**Parents:** UcoThing | **IRI:** `https://ontology.unifiedcyberontology.org/uco/types/ThreadItem`

*No direct or inherited properties.*

## uco.victim

### Victim

*A victim is a role played by a person or organization that is/was the target of some malicious action.*

**Parents:** NeutralRole | **IRI:** `https://ontology.unifiedcyberontology.org/uco/victim/Victim`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

### VictimTargeting

*A victim targeting is a grouping of characteristics unique to people or organizations that are the target of some malicious activity.*

**Parents:** Victim | **IRI:** `https://ontology.unifiedcyberontology.org/uco/victim/VictimTargeting`

| Property | Type | Cardinality | Required | Description |
|----------|------|-------------|----------|-------------|
| createdBy | IdentityAbstraction | zero_or_one | No | The identity that created a characterization of a concept. |
| description | string | zero_or_more | No | A description of a particular concept characterization. |
| externalReference | ExternalReference | zero_or_more | No | Specifies a reference to a resource outside of the UCO. |
| hasFacet | Facet | zero_or_more | No | Further sets of properties characterizing a concept based on the particular context of the class and of the particula... |
| modifiedTime | dateTime | zero_or_more | No | Specifies the time that this particular version of the object was modified. The object creator can use the time it de... |
| name | string | zero_or_one | No | The name of a particular concept characterization. |
| objectCreatedTime | dateTime | zero_or_one | No | The time at which a characterization of a concept is created. This time pertains to the time of creating the record o... |
| objectMarking | MarkingDefinitionAbstraction | zero_or_more | No | Marking definitions to be applied to a particular concept characterization in its entirety. |
| objectStatus | string | zero_or_one | No | The current state of formality and acceptance for a UCO object. |
| specVersion | string | zero_or_one | No | The version of UCO ontology or subontology specification used to characterize a concept. |
| tag | string | zero_or_more | No | A generic tag/label. |

## Vocabulary Types

Enumerated vocabulary types define constrained sets of allowed values for certain properties.

### AccountTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/AccountTypeVocab`

| Member |
|--------|
| `ldap` |
| `nis` |
| `openid` |
| `radius` |
| `tacacs` |
| `unix` |
| `windows_domain` |
| `windows_local` |

### ActionArgumentNameVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionArgumentNameVocab`

| Member |
|--------|
| `APC Address` |
| `APC Mode` |
| `API` |
| `Access Mode` |
| `Application Name` |
| `Base Address` |
| `Callback Address` |
| `Code Address` |
| `Command` |
| `Control Code` |
| `Control Parameter` |
| `Creation Flags` |
| `Database Name` |
| `Delay Time (ms)` |
| `Destination Address` |
| `Error Control` |
| `File Information Class` |
| `Flags` |
| `Function Address` |
| `Function Name` |
| `Function Ordinal` |
| `Hook Type` |
| `Host Name` |
| `Hostname` |
| `Initial Owner` |
| `Mapping Offset` |
| `Number of Bytes Per Send` |
| `Options` |
| `Parameter Address` |
| `Password` |
| `Privilege Name` |
| `Protection` |
| `Proxy Bypass` |
| `Proxy Name` |
| `Reason` |
| `Request Size` |
| `Requested Version` |
| `Server` |
| `Service Name` |
| `Service State` |
| `Service Type` |
| `Share Mode` |
| `Shutdown Flag` |
| `Size (bytes)` |
| `Sleep Time (ms)` |
| `Source Address` |
| `Starting Address` |
| `System Metric Index` |
| `Target PID` |
| `Transfer Flags` |
| `Username` |

### ActionNameVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionNameVocab`

| Member |
|--------|
| `Accept Socket Connection` |
| `Add Connection to Network Share` |
| `Add Network Share` |
| `Add Scheduled Task` |
| `Add System Call Hook` |
| `Add User` |
| `Add Windows Hook` |
| `Allocate Virtual Memory in Process` |
| `Bind Address to Socket` |
| `Change Service Configuration` |
| `Check for Remote Debugger` |
| `Close Port` |
| `Close Registry Key` |
| `Close Socket` |
| `Configure Service` |
| `Connect to IP` |
| `Connect to Named Pipe` |
| `Connect to Network Share` |
| `Connect to Socket` |
| `Connect to URL` |
| `Control Driver` |
| `Control Service` |
| `Copy File` |
| `Create Dialog Box` |
| `Create Directory` |
| `Create Event` |
| `Create File` |
| `Create File Alternate Data Stream` |
| `Create File Mapping` |
| `Create File Symbolic Link` |
| `Create Hidden File` |
| `Create Mailslot` |
| `Create Module` |
| `Create Mutex` |
| `Create Named Pipe` |
| `Create Process` |
| `Create Process as User` |
| `Create Registry Key` |
| `Create Registry Key Value` |
| `Create Remote Thread in Process` |
| `Create Service` |
| `Create Socket` |
| `Create Symbolic Link` |
| `Create Thread` |
| `Create Window` |
| `Delete Directory` |
| `Delete File` |
| `Delete Named Pipe` |
| `Delete Network Share` |
| `Delete Registry Key` |
| `Delete Registry Key Value` |
| `Delete Service` |
| `Delete User` |
| `Disconnect from Named Pipe` |
| `Disconnect from Network Share` |
| `Disconnect from Socket` |
| `Download File` |
| `Enumerate DLLs` |
| `Enumerate Network Shares` |
| `Enumerate Processes` |
| `Enumerate Protocols` |
| `Enumerate Registry Key Subkeys` |
| `Enumerate Registry Key Values` |
| `Enumerate Services` |
| `Enumerate System Handles` |
| `Enumerate Threads` |
| `Enumerate Threads in Process` |
| `Enumerate Users` |
| `Enumerate Windows` |
| `Find File` |
| `Find Window` |
| `Flush Process Instruction Cache` |
| `Free Library` |
| `Free Process Virtual Memory` |
| `Get Disk Free Space` |
| `Get Disk Type` |
| `Get Elapsed System Up Time` |
| `Get File Attributes` |
| `Get Function Address` |
| `Get Host By Address` |
| `Get Host By Name` |
| `Get Host Name` |
| `Get Library File Name` |
| `Get Library Handle` |
| `Get NetBIOS Name` |
| `Get Process Current Directory` |
| `Get Process Environment Variable` |
| `Get Process Startup Information` |
| `Get Processes Snapshot` |
| `Get Registry Key Attributes` |
| `Get Service Status` |
| `Get System Global Flags` |
| `Get System Host Name` |
| `Get System Local Time` |
| `Get System NetBIOS Name` |
| `Get System Network Parameters` |
| `Get System Time` |
| `Get Thread Context` |
| `Get Thread Username` |
| `Get User Attributes` |
| `Get Username` |
| `Get Windows Directory` |
| `Get Windows System Directory` |
| `Get Windows Temporary Files Directory` |
| `Hide Window` |
| `Impersonate Process` |
| `Impersonate Thread` |
| `Inject Memory Page` |
| `Kill Process` |
| `Kill Thread` |
| `Kill Window` |
| `Listen on Port` |
| `Listen on Socket` |
| `Load Driver` |
| `Load Library` |
| `Load Module` |
| `Load and Call Driver` |
| `Lock File` |
| `Logon as User` |
| `Map File` |
| `Map Library` |
| `Map View of File` |
| `Modify File` |
| `Modify Named Pipe` |
| `Modify Process` |
| `Modify Registry Key` |
| `Modify Registry Key Value` |
| `Modify Service` |
| `Monitor Registry Key` |
| `Move File` |
| `Open File` |
| `Open File Mapping` |
| `Open Mutex` |
| `Open Port` |
| `Open Process` |
| `Open Registry Key` |
| `Open Service` |
| `Open Service Control Manager` |
| `Protect Virtual Memory` |
| `Query DNS` |
| `Query Disk Attributes` |
| `Query Process Virtual Memory` |
| `Queue APC in Thread` |
| `Read File` |
| `Read From Named Pipe` |
| `Read From Process Memory` |
| `Read Registry Key Value` |
| `Receive Data on Socket` |
| `Receive Email Message` |
| `Release Mutex` |
| `Rename File` |
| `Revert Thread to Self` |
| `Send Control Code to File` |
| `Send Control Code to Pipe` |
| `Send Control Code to Service` |
| `Send DNS Query` |
| `Send Data on Socket` |
| `Send Data to Address on Socket` |
| `Send Email Message` |
| `Send ICMP Request` |
| `Send Reverse DNS Query` |
| `Set File Attributes` |
| `Set NetBIOS Name` |
| `Set Process Current Directory` |
| `Set Process Environment Variable` |
| `Set System Global Flags` |
| `Set System Host Name` |
| `Set System Time` |
| `Set Thread Context` |
| `Show Window` |
| `Shutdown System` |
| `Sleep Process` |
| `Sleep System` |
| `Start Service` |
| `Unload Driver` |
| `Unload Module` |
| `Unlock File` |
| `Unmap File` |
| `Upload File` |
| `Write to File` |
| `Write to Process Virtual Memory` |

### ActionRelationshipTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionRelationshipTypeVocab`

| Member |
|--------|
| `Dependent_On` |
| `Equivalent_To` |
| `Followed_By` |
| `Initiated` |
| `Initiated_By` |
| `Preceded_By` |
| `Related_To` |

### ActionStatusTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab`

| Member |
|--------|
| `Finish` |
| `Error` |
| `Fail` |
| `Ongoing` |
| `Pending` |
| `Success` |
| `Unknown` |

### ActionTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionTypeVocab`

| Member |
|--------|
| `Accept` |
| `Access` |
| `Add` |
| `Alert` |
| `Allocate` |
| `Archive` |
| `Assign` |
| `Audit` |
| `Backup` |
| `Bind` |
| `Block` |
| `Call` |
| `Change` |
| `Check` |
| `Clean` |
| `Click` |
| `Close` |
| `Compare` |
| `Compress` |
| `Configure` |
| `Connect` |
| `Control` |
| `Duplicate` |
| `Create` |
| `Decode` |
| `Decompress` |
| `Decrypt` |
| `Deny` |
| `Depress` |
| `Detect` |
| `Disconnect` |
| `Download` |
| `Draw` |
| `Drop` |
| `Encode` |
| `Encrypt` |
| `Enumerate` |
| `Execute` |
| `Extract` |
| `Filter` |
| `Find` |
| `Flush` |
| `Fork` |
| `Free` |
| `Get` |
| `Hide` |
| `Hook` |
| `Impersonate` |
| `Initialize` |
| `Inject` |
| `Install` |
| `Interleave` |
| `Join` |
| `Kill` |
| `Listen` |
| `Load` |
| `Lock` |
| `Logon` |
| `Logoff` |
| `Map` |
| `Merge` |
| `Modify` |
| `Monitor` |
| `Move` |
| `Open` |
| `Pack` |
| `Pause` |
| `Press` |
| `Protect` |
| `Quarantine` |
| `Query` |
| `Queue` |
| `Raise` |
| `Read` |
| `Receive` |
| `Release` |
| `Delete` |
| `Rename` |
| `Replicate` |
| `Restore` |
| `Resume` |
| `Revert` |
| `Run` |
| `Save` |
| `Scan` |
| `Schedule` |
| `Search` |
| `Send` |
| `Set` |
| `Shutdown` |
| `Sleep` |
| `Snapshot` |
| `Start` |
| `Stop` |
| `Suspend` |
| `Synchronize` |
| `Throw` |
| `Transmit` |
| `Unblock` |
| `Unhide` |
| `Unhook` |
| `Uninstall` |
| `Unload` |
| `Unlock` |
| `Unmap` |
| `Unpack` |
| `Update` |
| `Upgrade` |
| `Upload` |
| `Purge` |
| `Write` |

### BitnessVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/BitnessVocab`

| Member |
|--------|
| `32` |
| `64` |

### CharacterEncodingVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/CharacterEncodingVocab`

| Member |
|--------|
| `ASCII` |
| `UTF-16` |
| `UTF-32` |
| `UTF-8` |
| `Windows-1250` |
| `Windows-1251` |
| `Windows-1252` |
| `Windows-1253` |
| `Windows-1254` |
| `Windows-1255` |
| `Windows-1256` |
| `Windows-1257` |
| `Windows-1258` |

### ContactAddressScopeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactAddressScopeVocab`

| Member |
|--------|
| `home` |
| `school` |
| `work` |

### ContactEmailScopeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactEmailScopeVocab`

| Member |
|--------|
| `cloud` |
| `home` |
| `school` |
| `work` |

### ContactPhoneScopeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactPhoneScopeVocab`

| Member |
|--------|
| `home` |
| `home fax` |
| `main` |
| `mobile` |
| `pager` |
| `school` |
| `work` |
| `work fax` |

### ContactSIPScopeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactSIPScopeVocab`

| Member |
|--------|
| `home` |
| `school` |
| `work` |

### ContactURLScopeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactURLScopeVocab`

| Member |
|--------|
| `home` |
| `homepage` |
| `school` |
| `work` |

### DiskTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/DiskTypeVocab`

| Member |
|--------|
| `CDRom` |
| `Fixed` |
| `RAMDisk` |
| `Remote` |
| `Removable` |

### EndiannessTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/EndiannessTypeVocab`

| Member |
|--------|
| `Big-endian` |
| `Little-endian` |
| `Middle-endian` |

### HashNameVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/HashNameVocab`

| Member |
|--------|
| `MD5` |
| `MD6` |
| `SHA1` |
| `SHA224` |
| `SHA256` |
| `SHA3-224` |
| `SHA3-256` |
| `SHA3-384` |
| `SHA3-512` |
| `SHA384` |
| `SHA512` |
| `SSDEEP` |

### InvestigationFormVocab

**IRI:** `https://ontology.caseontology.org/case/vocabulary/InvestigationFormVocab`

| Member |
|--------|
| `case` |
| `incident` |
| `suspicious-activity` |

### LibraryTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/LibraryTypeVocab`

| Member |
|--------|
| `Dynamic` |
| `Other` |
| `Remote` |
| `Shared` |
| `Static` |

### MemoryBlockTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/MemoryBlockTypeVocab`

| Member |
|--------|
| `Bit-mapped` |
| `Byte-mapped` |
| `Initialized` |
| `Overlay` |
| `Uninitialized` |

### NetworkSocketAddressFamily

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketAddressFamily`

| Member |
|--------|
| `af_appletalk` |
| `af_bth` |
| `af_inet` |
| `af_inet6` |
| `af_ipx` |
| `af_irda` |
| `af_netbios` |
| `af_unspec` |

### NetworkSocketProtocolFamily

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketProtocolFamily`

| Member |
|--------|
| `pf_appletalk` |
| `pf_ash` |
| `pf_atmpvc` |
| `pf_atmsvc` |
| `pf_ax25` |
| `pf_bluetooth` |
| `pf_bridge` |
| `pf_decnet` |
| `pf_econet` |
| `pf_inet` |
| `pf_inet6` |
| `pf_ipx` |
| `pf_irda` |
| `pf_key` |
| `pf_netbeui` |
| `pf_netlink` |
| `pf_netrom` |
| `pf_packet` |
| `pf_pppox` |
| `pf_rose` |
| `pf_route` |
| `pf_security` |
| `pf_sna` |
| `pf_wanpipe` |
| `pf_x25` |

### NetworkSocketType

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketType`

| Member |
|--------|
| `sock_dgram` |
| `sock_raw` |
| `sock_rdm` |
| `sock_seqpacket` |
| `sock_stream` |

### ObjectStatusVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/core/ObjectStatusVocab`

| Member |
|--------|
| `Deprecated` |
| `Draft` |
| `Final` |

### ObservableObjectRelationshipVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectRelationshipVocab`

| Member |
|--------|
| `Allocated` |
| `Allocated_By` |
| `Attachment_Of` |
| `Bound` |
| `Bound_By` |
| `Characterized_By` |
| `Characterizes` |
| `Child_Of` |
| `Closed` |
| `Closed_By` |
| `Compressed` |
| `Compressed_By` |
| `Compressed_From` |
| `Compressed_Into` |
| `Connected_From` |
| `Connected_To` |
| `Contained_Within` |
| `Contains` |
| `Copied` |
| `Copied_By` |
| `Copied_From` |
| `Copied_To` |
| `Created` |
| `Created_By` |
| `Decoded` |
| `Decoded_By` |
| `Decompressed` |
| `Decompressed_By` |
| `Decrypted` |
| `Decrypted_By` |
| `Deleted` |
| `Deleted_By` |
| `Deleted_From` |
| `Downloaded` |
| `Downloaded_By` |
| `Downloaded_From` |
| `Downloaded_To` |
| `Dropped` |
| `Dropped_By` |
| `Encoded` |
| `Encoded_By` |
| `Encrypted` |
| `Encrypted_By` |
| `Encrypted_From` |
| `Encrypted_To` |
| `Extracted_From` |
| `FQDN_Of` |
| `Freed` |
| `Freed_By` |
| `Had_Attachment` |
| `Hooked` |
| `Hooked_By` |
| `Initialized_By` |
| `Initialized_To` |
| `Injected` |
| `Injected_As` |
| `Injected_By` |
| `Injected_Into` |
| `Installed` |
| `Installed_By` |
| `Joined` |
| `Joined_By` |
| `Killed` |
| `Killed_By` |
| `Listened_On` |
| `Listened_On_By` |
| `Loaded_From` |
| `Loaded_Into` |
| `Locked` |
| `Locked_By` |
| `Mapped_By` |
| `Mapped_Into` |
| `Merged` |
| `Merged_By` |
| `Modified_Properties_Of` |
| `Monitored` |
| `Monitored_By` |
| `Moved` |
| `Moved_By` |
| `Moved_From` |
| `Moved_To` |
| `Opened` |
| `Opened_By` |
| `Packed` |
| `Packed_By` |
| `Packed_From` |
| `Packed_Into` |
| `Parent_Of` |
| `Paused` |
| `Paused_By` |
| `Previously_Contained` |
| `Properties_Modified_By` |
| `Properties_Queried` |
| `Properties_Queried_By` |
| `Read_From` |
| `Read_From_By` |
| `Received` |
| `Received_By` |
| `Received_From` |
| `Received_Via_Upload` |
| `Redirects_To` |
| `Related_To` |
| `Renamed` |
| `Renamed_By` |
| `Renamed_From` |
| `Renamed_To` |
| `Resolved_To` |
| `Resumed` |
| `Resumed_By` |
| `Root_Domain_Of` |
| `Searched_For` |
| `Searched_For_By` |
| `Sent` |
| `Sent_By` |
| `Sent_To` |
| `Sent_Via_Upload` |
| `Set_From` |
| `Set_To` |
| `Signed_By` |
| `Sub-domain_Of` |
| `Supra-domain_Of` |
| `Suspended` |
| `Suspended_By` |
| `Unhooked` |
| `Unhooked_By` |
| `Unlocked` |
| `Unlocked_By` |
| `Unpacked` |
| `Unpacked_By` |
| `Uploaded` |
| `Uploaded_By` |
| `Uploaded_From` |
| `Uploaded_To` |
| `Used` |
| `Used_By` |
| `Values_Enumerated` |
| `Values_Enumerated_By` |
| `Written_To_By` |
| `Wrote_To` |

### ObservableObjectStateVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectStateVocab`

| Member |
|--------|
| `Active` |
| `Closed` |
| `Does Not Exist` |
| `Exists` |
| `Inactive` |
| `Locked` |
| `Open` |
| `Started` |
| `Stopped` |
| `Unlocked` |

### PartitionTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/PartitionTypeVocab`

| Member |
|--------|
| `PARTITION_ENTRY_UNUSED` |
| `PARTITION_EXTENDED` |
| `PARTITION_FAT32` |
| `PARTITION_FAT32_XINT13` |
| `PARTITION_FAT_12` |
| `PARTITION_FAT_16` |
| `PARTITION_HUGE` |
| `PARTITION_IFS` |
| `PARTITION_LDM` |
| `PARTITION_NTFT` |
| `PARTITION_OS2BOOTMGR` |
| `PARTITION_PREP` |
| `PARTITION_UNIX` |
| `PARTITION_XENIX_1` |
| `PARTITION_XENIX_2` |
| `PARTITION_XINT13` |
| `PARTITION_XINT13_EXTENDED` |
| `UNKNOWN` |
| `VALID_NTFT` |

### ProcessorArchVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ProcessorArchVocab`

| Member |
|--------|
| `ARM` |
| `Alpha` |
| `IA-64` |
| `MIPS` |
| `Motorola 68k` |
| `Other` |
| `PowerPC` |
| `SPARC` |
| `eSi-RISC` |
| `x86-32` |
| `x86-64` |
| `Architecture` |

### RecoveredObjectStatusVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/RecoveredObjectStatusVocab`

| Member |
|--------|
| `overwritten` |
| `partially recovered` |
| `recovered` |
| `unknown` |

### RegionalRegistryTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/RegionalRegistryTypeVocab`

| Member |
|--------|
| `APNIC` |
| `ARIN` |
| `AfriNIC` |
| `LACNIC` |
| `RIPE NCC` |

### RegistryDatatype

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/RegistryDatatype`

| Member |
|--------|
| `reg_binary` |
| `reg_dword` |
| `reg_dword_big_endian` |
| `reg_expand_sz` |
| `reg_full_resource_descriptor` |
| `reg_invalid_type` |
| `reg_link` |
| `reg_multi_sz` |
| `reg_none` |
| `reg_qword` |
| `reg_resource_list` |
| `reg_resource_requirements_list` |
| `reg_sz` |

### RegistryDatatypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/RegistryDatatypeVocab`

| Member |
|--------|
| `reg_binary` |
| `reg_dword` |
| `reg_dword_big_endian` |
| `reg_expand_sz` |
| `reg_full_resource_descriptor` |
| `reg_invalid_type` |
| `reg_link` |
| `reg_multi_sz` |
| `reg_none` |
| `reg_qword` |
| `reg_resource_list` |
| `reg_resource_requirements_list` |
| `reg_sz` |

### SIMFormVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMFormVocab`

| Member |
|--------|
| `Full-size SIM` |
| `Micro SIM` |
| `Nano SIM` |

### SIMTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMTypeVocab`

| Member |
|--------|
| `SIM` |
| `UICC` |
| `USIM` |

### TaskActionTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskActionTypeVocab`

| Member |
|--------|
| `TASK_ACTION_COM_HANDLER` |
| `TASK_ACTION_EXEC` |
| `TASK_ACTION_SEND_EMAIL` |
| `TASK_ACTION_SHOW_MESSAGE` |

### TaskFlagVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskFlagVocab`

| Member |
|--------|
| `TASK_FLAG_DELETE_WHEN_DONE` |
| `TASK_FLAG_DISABLED` |
| `TASK_FLAG_DONT_START_IF_ON_BATTERIES` |
| `TASK_FLAG_HIDDEN` |
| `TASK_FLAG_INTERACTIVE` |
| `TASK_FLAG_KILL_IF_GOING_ON_BATTERIES` |
| `TASK_FLAG_KILL_ON_IDLE_END` |
| `TASK_FLAG_RESTART_ON_IDLE_RESUME` |
| `TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET` |
| `TASK_FLAG_RUN_ONLY_IF_LOGGED_ON` |
| `TASK_FLAG_START_ONLY_IF_IDLE` |
| `TASK_FLAG_SYSTEM_REQUIRED` |
| `TASK_FLAG_ZERO` |

### TaskPriorityVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskPriorityVocab`

| Member |
|--------|
| `ABOVE_NORMAL_PRIORITY_CLASS` |
| `BELOW_NORMAL_PRIORITY_CLASS` |
| `HIGH_PRIORITY_CLASS` |
| `IDLE_PRIORITY_CLASS` |
| `NORMAL_PRIORITY_CLASS` |
| `REALTIME_PRIORITY_CLASS` |

### TaskStatusVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskStatusVocab`

| Member |
|--------|
| `SCHED_E_ACCOUNT_DBASE_CORRUPT` |
| `SCHED_E_ACCOUNT_INFORMATION_NOT_SET` |
| `SCHED_E_ACCOUNT_NAME_NOT_FOUND` |
| `SCHED_E_CANNOT_OPEN_TASK` |
| `SCHED_E_INVALID_TASK` |
| `SCHED_E_NO_SECURITY_SERVICES` |
| `SCHED_E_SERVICE_NOT_INSTALLED` |
| `SCHED_E_SERVICE_NOT_RUNNING` |
| `SCHED_E_TASK_NOT_READY` |
| `SCHED_E_TASK_NOT_RUNNING` |
| `SCHED_E_TRIGGER_NOT_FOUND` |
| `SCHED_E_UNKNOWN_OBJECT_VERSION` |
| `SCHED_E_UNSUPPORTED_ACCOUNT_OPTION` |
| `SCHED_S_EVENT_TRIGGER` |
| `SCHED_S_TASK_DISABLED` |
| `SCHED_S_TASK_HAS_NOT_RUN` |
| `SCHED_S_TASK_NOT_SCHEDULED` |
| `SCHED_S_TASK_NO_MORE_RUNS` |
| `SCHED_S_TASK_NO_VALID_TRIGGERS` |
| `SCHED_S_TASK_READY` |
| `SCHED_S_TASK_RUNNING` |
| `SCHED_S_TASK_TERMINATED` |
| `TASK_STATE_QUEUED` |
| `TASK_STATE_UNKNOWN` |

### ThreadRunningStatusVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/ThreadRunningStatusVocab`

| Member |
|--------|
| `Initialized` |
| `Ready` |
| `Running` |
| `Standby` |
| `Terminated` |
| `Transition` |
| `Unknown` |
| `Waiting` |

### TimestampPrecisionVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TimestampPrecisionVocab`

| Member |
|--------|
| `day` |
| `hour` |
| `minute` |
| `month` |
| `second` |
| `year` |

### TrendVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TrendVocab`

| Member |
|--------|
| `Decreasing` |
| `Increasing` |

### TriggerFrequencyVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerFrequencyVocab`

| Member |
|--------|
| `TASK_EVENT_TRIGGER_AT_LOGON` |
| `TASK_EVENT_TRIGGER_AT_SYSTEMSTART` |
| `TASK_EVENT_TRIGGER_ON_IDLE` |
| `TASK_TIME_TRIGGER_DAILY` |
| `TASK_TIME_TRIGGER_MONTHLYDATE` |
| `TASK_TIME_TRIGGER_MONTHLYDOW` |
| `TASK_TIME_TRIGGER_ONCE` |
| `TASK_TIME_TRIGGER_WEEKLY` |

### TriggerTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerTypeVocab`

| Member |
|--------|
| `TASK_TRIGGER_BOOT` |
| `TASK_TRIGGER_EVENT` |
| `TASK_TRIGGER_IDLE` |
| `TASK_TRIGGER_LOGON` |
| `TASK_TRIGGER_REGISTRATION` |
| `TASK_TRIGGER_SESSION_STATE_CHANGE` |
| `TASK_TRIGGER_TIME` |

### URLTransitionTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/URLTransitionTypeVocab`

| Member |
|--------|
| `auto_bookmark` |
| `auto_subframe` |
| `auto_toplevel` |
| `form_submit` |
| `generated` |
| `keyword` |
| `keyword_generated` |
| `link` |
| `manual_subframe` |
| `reload` |
| `typed` |

### UnixProcessStateVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/UnixProcessStateVocab`

| Member |
|--------|
| `Dead` |
| `InterruptibleSleep` |
| `Paging` |
| `Running` |
| `Stopped` |
| `UninterruptibleSleep` |
| `Zombie` |

### WhoisContactTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisContactTypeVocab`

| Member |
|--------|
| `ADMIN` |
| `BILLING` |
| `TECHNICAL` |

### WhoisDNSSECTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab`

| Member |
|--------|
| `Signed` |
| `Unsigned` |

### WhoisStatusTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisStatusTypeVocab`

| Member |
|--------|
| `ADD_PERIOD` |
| `AUTO_RENEW_PERIOD` |
| `CLIENT_DELETE_PROHIBITED` |
| `CLIENT_HOLD` |
| `CLIENT_RENEW_PROHIBITED` |
| `CLIENT_TRANSFER_PROHIBITED` |
| `CLIENT_UPDATE_PROHIBITED` |
| `DELETE_PROHIBITED` |
| `HOLD` |
| `INACTIVE` |
| `OK` |
| `PENDING_DELETE_RESTORABLE` |
| `PENDING_DELETE_SCHEDULED_FOR_RELEASE` |
| `PENDING_RESTORE` |
| `RENEW_PERIOD` |
| `RENEW_PROHIBITED` |
| `TRANSFER_PERIOD` |
| `TRANSFER_PROHIBITED` |
| `UPDATE_PROHIBITED` |

### WindowsDriveTypeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsDriveTypeVocab`

| Member |
|--------|
| `DRIVE_CDROM` |
| `DRIVE_FIXED` |
| `DRIVE_NO_ROOT_DIR` |
| `DRIVE_RAMDISK` |
| `DRIVE_REMOTE` |
| `DRIVE_REMOVABLE` |
| `DRIVE_UNKNOWN` |

### WindowsPEBinaryType

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryType`

| Member |
|--------|
| `dll` |
| `exe` |
| `sys` |

### WindowsServiceStartType

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStartType`

| Member |
|--------|
| `service_auto_start` |
| `service_boot_start` |
| `service_demand_start` |
| `service_disabled` |
| `service_system_alert` |

### WindowsServiceStatus

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStatus`

| Member |
|--------|
| `service_continue_pending` |
| `service_pause_pending` |
| `service_paused` |
| `service_running` |
| `service_start_pending` |
| `service_stop_pending` |
| `service_stopped` |

### WindowsServiceType

**IRI:** `https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceType`

| Member |
|--------|
| `service_file_system_driver` |
| `service_kernel_driver` |
| `service_win32_own_process` |
| `service_win32_share_process` |

### WindowsVolumeAttributeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab`

| Member |
|--------|
| `Hidden` |
| `NoDefaultDriveLetter` |
| `ReadOnly` |
| `ShadowCopy` |

### WirelessNetworkSecurityModeVocab

**IRI:** `https://ontology.unifiedcyberontology.org/uco/vocabulary/WirelessNetworkSecurityModeVocab`

| Member |
|--------|
| `None` |
| `WEP` |
| `WPA` |
| `WPA2-Enterprise` |
| `WPA2-PSK` |
| `WPA3-Enterprise` |
| `WPA3-PSK` |
