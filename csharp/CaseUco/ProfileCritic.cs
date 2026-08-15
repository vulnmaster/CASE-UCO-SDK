// Logical ProfileCritic surface — construction findings stay on InvestigationBuilder.

namespace CaseUco
{
    public sealed class ProfileCritic
    {
        public ProfileContract Contract { get; }

        public ProfileCritic(ProfileContract contract)
        {
            Contract = contract;
        }

        public static ProfileCritic ForProfile(string profileId)
        {
            return new ProfileCritic(ProfileContract.Load(profileId));
        }
    }
}
