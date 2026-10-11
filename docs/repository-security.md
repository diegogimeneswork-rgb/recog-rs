# GitHub repository security settings

The files in this repository configure least-privilege CI, pin the checkout
action to a reviewed full commit SHA, check the project offline, and schedule
Dependabot version updates. `SECURITY.md` directs vulnerability reports to a
private channel.

GitHub account settings are separate from committed files. Apply these
controls to the public repository `diegogimeneswork-rgb/recog-rs`:

## Actions

- Set the default `GITHUB_TOKEN` permission to read-only.
- Require Actions to be pinned to a full commit SHA.
- Restrict allowed actions to the minimum set used by the workflows.

## Default branch

Create an active ruleset targeting branch `main`:

- Require a pull request before merging.
- Require the CI status check `verify` to pass.
- Block force pushes and branch deletion.
- Keep required approving reviews at zero until another maintainer can review;
  requiring the sole repository owner to approve their own pull request would
  prevent merges.

## Code security

- Enable Dependabot alerts and Dependabot security updates.
- Enable secret scanning and push protection.
- Enable private vulnerability reporting.
- Enable code scanning after the Rust implementation is present.

Recheck these settings after changing repository ownership, visibility, or
default-branch rules.
