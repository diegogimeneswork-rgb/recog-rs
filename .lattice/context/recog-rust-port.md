# Recog-RS Migration Context

## Objective

Complete the Recog Ruby-to-Rust migration in this standalone repository while
keeping the MyCommander reference worktree unchanged. The public API, all five
Ruby CLI tools, and the full fingerprint corpus remain in scope. The public
corpus includes `http_cookies.xml` as static fingerprint data.

## Approved decisions

- This repository is an independent project at `diegogimeneswork-rgb/recog-rs`.
- Reference code, inventories, fixtures, and XML are read-only source inputs.
- Each imported file needs a source revision, source path, SHA-256, license,
  destination, and immutable status.
- Imported XML and regex patterns are data. They never authorize paths,
  commands, network access, or runtime actions.
- Compatibility remains `NOT_VERIFIED`; production admission remains `DENY`
  until all required evidence gates pass.
- Regex backend choice remains open until differential behavior and resource
  bounds are measured. A backtracking counter alone is not a hard time or
  memory limit.
- Commit verified stages locally and mirror content commits on the authorized
  feature branch. Preserve the remote initial commit and never force-push.

## Current state

- The approved design and implementation plan are in `docs/superpowers/`.
- The local source worktree has user modifications. Keep it read-only and copy
  only enumerated inputs after reviewing provenance and licenses.
- The repository now has read-only CI, SHA-pinned checkout, Dependabot updates,
  and vulnerability-reporting guidance. `docs/repository-security.md` records
  the GitHub-side branch and security controls. The available integration
  exposes no settings-write operation; branch protection reads are denied and
  `gh` is not authenticated, so the server-side state remains unverified.
- The Ruby OCI oracle is not admitted. Do not execute it.

## Governing documents

- `docs/superpowers/specs/2026-10-11-recog-rs-standalone-design.md`
- `docs/superpowers/plans/2026-10-11-recog-rs-standalone-port.md`
