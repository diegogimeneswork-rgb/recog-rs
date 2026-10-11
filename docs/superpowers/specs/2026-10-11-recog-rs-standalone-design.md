# Recog-RS Standalone Ruby-to-Rust Design

Date: 2026-10-11
Status: approved migration design; standalone repository boundary added at the user's direction; plan and implementation review continue.
Compatibility: `NOT_VERIFIED`
Production admission: `DENY`

## Intent and scope

Complete the local migration of the pinned Rapid7 Recog fingerprint corpus and Ruby behavior into the standalone Rust project at `/home/diego/laplace/recog-rs`. The project must be independently buildable and must not depend on the `mycommander` repository at runtime or inherit its execution permissions.

The existing Rust candidate, frozen XML corpus, API/CLI inventories, and compatibility harness in the MyCommander worktree are read-only inputs. Copy only reviewed, licensed, and hashed files into this repository. Do not move, reset, stage, or otherwise alter the MyCommander worktree or its uncommitted changes. Do not fetch or initialize its uninitialized submodules.

Scope includes all 51 XML files and 4,677 inventoried fingerprint definitions; parsing and matching behavior; parameter extraction and interpolation; CPE handling; database lifecycle and verification behavior; the complete Ruby public API inventory; and all five public Ruby CLI tools. No API or CLI exclusion is approved. Destructive cleanup behavior may run only on disposable scratch copies.

## Observed evidence and limits

The existing worktree records scoped observations of 15,102/15,102 corpus example and deterministic-mutant comparisons, 96/96 bounded best-OS/service selections, 12/12 bounded lifecycle observations, 14/14 read-only CLI cases, and six scoped `recog_verify` cases. These counts are historical observations, not proof of complete parity. The new repository must bind any accepted result to exact source, corpus, oracle, and candidate digests before reporting it.

The full public API and CLI parity remains `NOT_VERIFIED`. An independent publisher signature for the Ruby OCI oracle is not verified, and the production verdict remains `DENY`. Do not execute that oracle or claim a parity result until its existing admission gate passes. Missing oracle, stale evidence, missing matrix rows, timeout, or changed digest must fail closed to `NOT_VERIFIED`.

## Repository and architecture boundary

The standalone repository owns its Rust crate, tests, compatibility matrix, copied test-only reference inputs, provenance manifest, CI, and Lattice verification configuration. It must not use absolute paths into another repository, MyCommander MCP at runtime, shell execution from imported fingerprint data, or inherited allowlists.

The data flow is:

`pinned local XML -> bounded XML reader -> typed domain -> match/verify services -> Rust API and CLI adapters`

Compatibility checks use the same fixed, bounded fixtures for the Rust candidate and an independently admitted offline Ruby oracle. Lattice checks validate provenance, coverage, resource limits, and evidence; they do not evaluate imported XML instructions or grant production authority.

The domain uses explicit typed failures for invalid input, corpus errors, unsupported patterns, and resource limits. XML parsing must reject malformed, oversized, entity-expanding, or out-of-root content. Regex semantics and isolation remain a design gate: select a backend only after differential and resource measurements. A backtracking counter alone is not a proven wall-clock or memory limit.

## Compatibility rules

- Preserve byte inputs, match order, duplicate fingerprints, captures, parameters, temporary fields, interpolation, CPE output, lifecycle results, diagnostics, standard output, standard error, and exit codes where Ruby defines them.
- Inventory every public Ruby API method and every CLI option, error, and output mode. Every row must map to Rust behavior and a bounded test or remain an explicit open divergence that keeps the gate closed.
- Do not silently skip a pattern or downgrade unsupported syntax. Return a typed failure and preserve the exact affected inventory rows.
- Finite fixtures establish only their declared scope. Do not label scoped green evidence as full or universal parity.

## Security and release boundaries

- Imported XML and regex text remain data. Never evaluate them, invoke a shell for them, or permit them to authorize a target, path, network request, or runtime action.
- Keep corpus reads inside the repository's designated corpus root; reject traversal and symlink escapes.
- Set and test input, pattern, corpus, output, CPU, wall-time, and memory budgets. Where the chosen regex backend cannot enforce the needed bounds, isolate it or keep the affected behavior unsupported and the gate closed.
- Preserve the repository's MIT license and add provenance/license notices for copied sources and third-party dependencies before distributing them.
- Keep `production_admission=DENY` until complete matrix coverage, admitted oracle provenance, differential evidence, security/resource checks, and required release review all pass.
- Do not change the Laplace catalog, runtime allowlist, deployment state, or network policy. Do not publish releases or deploy.

## Repository security baseline

Use least-privilege CI permissions, pinned third-party Actions, locked Rust dependencies, scheduled Dependabot updates for Cargo and GitHub Actions, and tests for the security configuration. Enable GitHub secret scanning and push protection, Dependabot alerts/security updates, and a `main` branch ruleset that blocks force pushes and deletion and requires pull requests with passing CI. Do not require an approval count that the sole repository owner cannot satisfy.

## Acceptance

1. The Rust project, corpus, fixtures, and verification commands work from this repository alone in offline mode after dependencies are cached.
2. Every inventoried fingerprint, public API method, and CLI operation is accounted for in versioned matrices with exact numerators and denominators.
3. Differential and negative tests preserve wire/API/CLI behavior and fail closed for unsupported patterns, unsafe XML, path escapes, resource exhaustion, stale evidence, or missing oracle admission.
4. CI and repository security configuration are reviewable, least-privilege, and have no hard-coded credentials.
5. The project's verification suite and the workspace-required Lattice suite pass. Passing verification alone does not prove full Ruby equivalence or production admission.

## Delivery

Keep MyCommander unchanged as a separate project and as the source of reviewed reference inputs. Make small, logical commits in the standalone Recog repository after each verified stage. Mirror the reviewed commits to the authorized GitHub repository without force-pushing or rewriting its initial commit. Keep implementation and deployment as separate activities.
