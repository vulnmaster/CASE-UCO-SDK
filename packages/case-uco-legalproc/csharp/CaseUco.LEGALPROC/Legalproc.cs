// Legal Process and Procedure Extension — legalproc module
namespace CaseUco.Ext.LEGALPROC.Legalproc
{
    public class ChargingInstrument
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/ChargingInstrument";
        public string? InstrumentType { get; set; }
    }

    public class CriminalCharge
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/CriminalCharge";
        public List<ChargingInstrument> AssertedIn { get; set; } = new();
        public string? ChargeClassification { get; set; }
        public List<string> ChargeDisposition { get; set; } = new();
        public string? CountLabel { get; set; }
        public List<ulong> CountNumber { get; set; } = new();
        public List<CriminalCharge> ObjectOffense { get; set; } = new();
        public string? OffenseForm { get; set; }
        public List<string> StatuteCitation { get; set; } = new();
    }

    public class CriminalProceeding
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/CriminalProceeding";
        public string? ProceedingType { get; set; }
    }

    public class DisclosureObligation
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/DisclosureObligation";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public List<UcoObject> ConcernsEvidence { get; set; } = new();
        public string? DisclosureKind { get; set; }
        public string? DisclosureSourceCitation { get; set; }
        public string? DisclosureStatus { get; set; }
    }

    public class DiscoveryProduction
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/DiscoveryProduction";
        public string? DisclosureSourceCitation { get; set; }
        public List<DisclosureObligation> SatisfiesObligation { get; set; } = new();
    }

    public class FederalCharge
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/FederalCharge";
        public string? JurisdictionKind { get; set; }
    }

    public class FederalJurisdiction
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/FederalJurisdiction";
    }

    public class ForfeitureOrder
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/ForfeitureOrder";
        public string? CurrencyCode { get; set; }
        public decimal? MonetaryAmount { get; set; }
    }

    public class Plea
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/Plea";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? OutcomeScope { get; set; }
        public string? PleaType { get; set; }
    }

    public class PleaAgreement
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/PleaAgreement";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? OutcomeScope { get; set; }
        public List<Plea> RecordsPlea { get; set; } = new();
    }

    public class PotentialPenalty
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/PotentialPenalty";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? OutcomeScope { get; set; }
        public string? PotentialPenaltyKind { get; set; }
    }

    public class PretrialReleaseCondition
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/PretrialReleaseCondition";
        public string? ReleaseConditionKind { get; set; }
    }

    public class RestitutionOrder
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/RestitutionOrder";
        public string? CurrencyCode { get; set; }
        public decimal? MonetaryAmount { get; set; }
    }

    public class Sentence
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/Sentence";
        public string? OutcomeScope { get; set; }
        public string? SentenceKind { get; set; }
        public string? SentenceStatus { get; set; }
        public string? SentenceTerm { get; set; }
    }

    public class StateCharge
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/StateCharge";
        public string? JurisdictionKind { get; set; }
    }

    public class StateJurisdiction
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/StateJurisdiction";
    }

    public class SuppressionMotion
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/SuppressionMotion";
        public string? DisclosureSourceCitation { get; set; }
        public string? ProceedingType { get; set; }
    }

    public class Verdict
    {
        public static readonly string ClassIri = "https://ontology.caseontology.org/case/criminal/Verdict";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? VerdictType { get; set; }
    }

}