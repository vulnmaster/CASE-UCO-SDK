package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class Sentence {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/Sentence";

    private String outcomeScope;
    private String sentenceKind;
    private String sentenceStatus;
    private String sentenceTerm;

    public String getOutcomeScope() { return outcomeScope; }
    public void setOutcomeScope(String outcomeScope) { this.outcomeScope = outcomeScope; }
    public String getSentenceKind() { return sentenceKind; }
    public void setSentenceKind(String sentenceKind) { this.sentenceKind = sentenceKind; }
    public String getSentenceStatus() { return sentenceStatus; }
    public void setSentenceStatus(String sentenceStatus) { this.sentenceStatus = sentenceStatus; }
    public String getSentenceTerm() { return sentenceTerm; }
    public void setSentenceTerm(String sentenceTerm) { this.sentenceTerm = sentenceTerm; }
}