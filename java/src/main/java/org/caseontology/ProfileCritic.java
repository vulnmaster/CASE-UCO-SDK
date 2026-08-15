package org.caseontology;

/** Logical ProfileCritic surface. Construction findings stay on InvestigationBuilder. */
public final class ProfileCritic {
    public final ProfileContract contract;

    public ProfileCritic(ProfileContract contract) {
        this.contract = contract;
    }

    public static ProfileCritic forProfile(String profileId) {
        return new ProfileCritic(ProfileContract.load(profileId));
    }
}
