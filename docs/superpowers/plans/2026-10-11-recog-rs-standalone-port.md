# Recog-RS Standalone Port Implementation Plan

Date: 2026-10-11
Target: `/home/diego/laplace/recog-rs` (`diegogimeneswork-rgb/recog-rs`)
Approved design: [`../specs/2026-10-11-recog-rs-standalone-design.md`](../specs/2026-10-11-recog-rs-standalone-design.md)
Current compatibility: `NOT_VERIFIED`
Current production admission: `DENY`

## Global constraints

- Keep `/home/diego/laplace/mycommander` and its feature worktree separate and unchanged. Treat its current Rust candidate, harnesses, and corpus snapshots as read-only source material. Never reset, clean, stage, or commit its existing dirty files.
- Copy only enumerated files after recording their source revision, status, path, SHA-256, license, and destination. The standalone project must have no runtime path into MyCommander and no network fetch at build or test time.
- Preserve the remote repository's initial commit, `.gitignore`, and MIT `LICENSE`. Develop locally on `feat/recog-rust-migration`; create the remote feature branch from remote `main`. Do not force-push or rewrite remote history. Commit locally and remotely in the logical stages below, using exact file paths per commit. Do not stage the whole tree.
- Follow TDD for each implementation task: add the named failing test, observe its failure, implement the smallest change, then run the focused test and offline checks. Keep commits green at each completed stage.
- Preserve all API and CLI matrix rows. No exclusions are approved. A missing or unadmitted Ruby oracle means `NOT_VERIFIED`, not a pass. Keep production admission `DENY`.
- Do not execute the Ruby OCI oracle unless its publisher signature, digest, SBOM, provenance, and vulnerability admission checks pass. Do not initialize submodules, probe targets, use network tests, publish a release, or deploy.
- Keep `.github` workflows least-privilege, pin Actions to reviewed full commit SHAs, and use no secrets for forkable CI jobs.
- The local `gh` executable is already present (`2.102.0`) but is not authenticated. Use it for local inspection only until authenticated. GitHub App access can make authorized content commits; it cannot modify the repository's administrative security settings. Record any settings that remain blocked instead of claiming they changed.

## Review focus

1. **Unsafe XML and path access** — verify entity expansion, malformed/oversized documents, traversal, and symlink escape are rejected by `tests/corpus_security.rs` and `harness/test_corpus_inputs.py`.
2. **Regex divergence or unbounded work** — compare captures, byte inputs, flags, backtracking, and unsupported constructs in `tests/regex_contract.rs` and `harness/test_regex_differential.py`; keep unproven limits from being described as hard timeouts.
3. **Lost API rows or order/null behavior** — test all inventoried public methods, ordering, nil values, errors, and Nizer methods in `tests/api_contract.rs` and `harness/test_api_matrix.py`.
4. **CLI wire behavior and destructive cleanup** — assert stdout, stderr, flags, exit codes, and multi-file behavior in `tests/cli_contract.rs`; run cleanup only in `TempDir` copies.
5. **False green evidence and repository security drift** — make missing oracle, changed digests, missing matrix entries, unpinned Actions, excessive workflow permissions, or missing Dependabot ecosystems fail in `harness/test_evidence_gate.py` and `harness/test_repo_security_config.py`.

## File map

- `Cargo.toml`, `Cargo.lock`: standalone Rust crate and exact offline dependency graph.
- `src/lib.rs`, `src/error.rs`, `src/model.rs`, `src/corpus.rs`: public crate root, typed errors/models, and safe corpus reader.
- `src/regex.rs`, `src/engine.rs`, `src/verify.rs`, `src/nizer_best.rs`: bounded pattern adapter and match/verify/lifecycle services.
- `src/bin/`: the five inventoried Recog command-line entry points, each a thin adapter.
- `tests/`: reader, matcher, API, CLI, resource, and security contracts.
- `vendor/recog/`: copied XML fingerprint corpus and upstream license text; never executable runtime instructions.
- `vendor/PROVENANCE.md` and `harness/source-manifest.json`: source hashes, licenses, and immutable import inventory.
- `compat/`: versioned public API, CLI, fingerprint, pattern-feature, and divergence matrices.
- `harness/`: bounded offline differential runners, fixed fixtures, and fail-closed evidence validation.
- `.lattice/`: standalone verification config and read-only evidence gates.
- `.github/workflows/`, `.github/dependabot.yml`, `SECURITY.md`, `docs/repository-security.md`: least-privilege CI, dependency updates, vulnerability reporting, and remote settings guidance.
- `README.md`, `docs/`: user-facing status, architecture, usage, and migration decisions.

## Implementation tasks

### 1. Bind the source baseline and import the licensed corpus

**Commit:** `docs: record Recog source provenance and standalone layout`

1. Add `harness/test_source_manifest.py` first. Require a manifest row for every copied file, with source path/revision, SHA-256, license, destination, and immutable status; reject an unlisted file, changed source digest, or a path outside the reviewed source roots.
2. Run `python3 -m unittest harness.test_source_manifest -v` and confirm the empty/incomplete manifest fails.
3. Inventory current remote `main`, local worktree HEAD/status, candidate files, XML corpus, harness inputs, license files, and existing exact counts. Record that earlier receipts may be stale because the reference worktree contains modifications.
4. Copy the reviewed XML corpus and upstream license files into `vendor/recog/` without moving or changing their source. Do not copy MyCommander-specific runtime, allowlist, credential, or deployment configuration.
5. Record source hashes and upstream license notices in `vendor/PROVENANCE.md` and `harness/source-manifest.json`; do not accept historical pass counts as new evidence.
6. Keep the candidate crate, API/CLI inventories, fixtures, and harnesses as read-only inputs until each file is separately reviewed and included in a later implementation stage.
7. Run `python3 -m unittest harness.test_source_manifest -v` and inspect `git diff --check`. Commit only the manifest, provenance, and enumerated corpus files.

### 2. Establish the standalone crate and repository CI baseline

**Commit:** `chore: bootstrap standalone Recog crate and CI`

1. Add `harness/test_repo_security_config.py` before creating workflows. It must reject write permissions on pull-request jobs, unpinned `uses:` references, missing Cargo/GitHub Actions Dependabot entries, and workflows triggered with secrets on untrusted pull requests.
2. Run `python3 -m unittest harness.test_repo_security_config -v` and confirm the starter config fails.
3. Create the root `Cargo.toml`, `src/lib.rs`, and an offline `cargo test` smoke test; keep the package independent from MyCommander paths.
4. Add `.github/dependabot.yml`, `SECURITY.md`, and CI for formatting, locked offline-capable tests, and Clippy. Pin each Action to a verified full SHA and grant only `contents: read` unless a job proves it needs less or more.
5. Run `cargo fmt --all -- --check`, `CARGO_NET_OFFLINE=true cargo test --offline --locked`, and `cargo clippy --offline --locked --all-targets`; run the Python security-config test.
6. Commit only crate bootstrap, CI, security guidance, Dependabot config, and their tests.

### 3. Build typed domain and safe XML corpus reader

**Commit:** `feat: add typed Recog corpus reader`

1. Add failing tests in `tests/corpus_security.rs` for malformed XML, DTD/entity expansion, invalid UTF-8, oversized XML, excessive depth/count, traversal, absolute paths, and symlink escape. Add positive tests for all 51 XML files and 4,677 expected definitions from the freshly hashed manifest.
2. Run `cargo test --offline --test corpus_security`; confirm each rejection case fails before implementation.
3. Add typed `RecogError` variants `InvalidInput`, `CorpusError`, `UnsupportedPattern`, and `ResourceLimit`; add `FingerprintId`, `Fingerprint`, `Param`, `Example`, and `Corpus` models without changing source order or duplicate handling.
4. Implement `load_corpus(root: &Path) -> Result<Corpus, RecogError>` with root confinement, explicit size/depth/count budgets, no external entities, and all-or-error results.
5. Run `cargo test --offline --test corpus_security` and `cargo test --offline --test corpus_contract`; assert every manifest XML file is parsed and its definition count equals the pinned manifest.
6. Commit model, reader, and focused tests only.

### 4. Preserve matcher, parameter, CPE, and verification semantics

**Commit:** `feat: implement bounded Recog matching and verification`

1. Add failing tests in `tests/regex_contract.rs` and `tests/match_contract.rs` for binary/NUL banners, captures, duplicate fingerprints, source-order priority, temporary fields, interpolation, CPE mapping, multi-match, best match, and verify diagnostics.
2. Add tests for every observed regex feature class, flags, unsupported constructs, catastrophic inputs, and output/capture budgets. Run the focused tests and record the pre-implementation failures.
3. Compare candidate engines against the fixed offline reference fixtures. Document compatibility and CPU/wall-time/memory measurements in `docs/decisions/regex-engine.md` before finalizing the adapter.
4. Do not call a backtrack counter a wall-time limit. If a hard resource bound cannot be demonstrated in-process, isolate matching under an explicit process budget or return typed `UnsupportedPattern`/`ResourceLimit` and leave affected parity rows open.
5. Implement `RegexMatcher::compile(pattern: &str, flags: RegexFlags) -> Result<CompiledPattern, RecogError>` and `Engine::match_banner(&self, banner: &[u8]) -> Result<Vec<MatchRecord>, RecogError>`; never return partial results after a resource failure.
6. Implement the corresponding verification and best-selection services, preserving nil/order/error behavior from fixtures.
7. Run `cargo test --offline --test regex_contract --test match_contract --test verify_contract`; commit only matcher/services and their tests/decision record.

### 5. Complete public API and all CLI entry points

**Commit:** `feat: complete Recog Rust API and CLI contracts`

1. Add `harness/test_api_matrix.py` and `tests/api_contract.rs` first. Assert all discovered Ruby public methods (currently observed as 67 non-Nizer plus 8 Nizer methods), all 30 separately classified private runtime entries, exact result order, nullable fields, error behavior, and zero unapproved exclusions.
2. Add `harness/test_cli_matrix.py` and `tests/cli_contract.rs` for each of the five Ruby CLI tools. Cover help, every flag, stdin/files, multiple files, output format, stdout, stderr, and exit status. Run cleanup tests only against disposable `TempDir` copies.
3. Re-discover method and command inventories from the pinned Ruby reference data; do not assume the historical 67+8 and five counts without confirming the source digest.
4. Implement a Rust API adapter for every matrix row and five thin CLI binaries. Represent unsupported cases explicitly and keep the parity gate closed until each required row has a passing bounded fixture.
5. Run `cargo test --offline --test api_contract --test cli_contract` and `python3 -m unittest harness.test_api_matrix harness.test_cli_matrix -v`; commit API, CLI, matrices, and focused tests together only when the stage is green.

### 6. Port the fail-closed differential harness and Lattice gates

**Commit:** `test: add offline Recog differential and Lattice gates`

1. Add `harness/test_evidence_gate.py` first. Test missing oracle, stale source/corpus hashes, unbound receipts, omitted API/CLI rows, timeout, mismatched stderr/exit, and unsupported patterns; all must report `NOT_VERIFIED` and production `DENY`.
2. Copy and adapt the reviewed, bounded differential runner and fixed fixtures. Bind every receipt to candidate, corpus, fixture, and oracle digests. Generate reports from source inventories; do not hand-edit generated JSON.
3. Keep Ruby oracle invocation behind the existing admission checks. Since its publisher signature is currently unverified, tests must prove the runner denies oracle execution and reports `NOT_VERIFIED`.
4. Add `.lattice/verification.yaml` and standalone evidence gates that do not read MyCommander paths, mutate repository data, run imported content, or invoke targets/network.
5. Run `python3 -m unittest discover -s harness -p 'test_*.py' -v`, the bounded offline Rust differential tests, and the standalone Lattice suite; commit only harness, fixtures, gates, and generated evidence.

### 7. Document operational use and final migration status

**Commit:** `docs: document Recog-RS usage and compatibility status`

1. Document install/build/use, API and CLI mapping, corpus provenance, error types, regex limits, supported pattern inventory, and how to reproduce bounded offline checks.
2. Add a final coverage report with exact numerator/denominator for corpus definitions, API rows, CLI rows, pattern features, and accepted oracle cases. Preserve every unresolved divergence.
3. Recheck that no file or runtime dependency crosses into MyCommander; no credentials or generated verification logs are committed; `.gitignore` excludes build and verification output.
4. Run repository formatting, locked offline Rust checks, harness suite, standalone Lattice suite, then the required workspace verifier from `/home/diego/laplace/.lattice/verification.yaml` using the `verifier` subagent. Read only its summary; do not open or paste failed logs.
5. If any required gate is red or oracle admission remains unavailable, report the failing stage and keep compatibility `NOT_VERIFIED` and production `DENY`. Commit final docs/status only after the exact state is reflected.

## Commit discipline

Make one local commit and one corresponding remote commit for each completed task, in the order above. Use `git add <explicit paths>`; never `git add .`, amend, squash, force-push, or rewrite the remote initial commit. Before each commit, inspect `git diff --check`, status, and the exact staged diff. The local-only execution policy blocks `git clone`/`fetch`/`push`, and `gh` has no authenticated session, so remote content commits must use the authorized GitHub App API on a feature branch created from remote `main`. This leaves local and remote commit IDs and parent histories different; compare exact changed paths and blob contents, and record both SHAs without claiming the histories are synchronized. Do not merge to `main` or publish a release as part of this migration.
