# Recog-RS

Standalone Rust migration of Rapid7 Recog. The target repository is
`diegogimeneswork-rgb/recog-rs`; it is developed independently from the
`mycommander` repository.

The existing Recog candidate and frozen reference material in the local
workspace are source inputs only. This repository must build and run without a
path dependency, runtime file access, or Lattice permission inherited from
`mycommander`.

## Status

- Compatibility: `NOT_VERIFIED`
- Production admission: `DENY`
- Implementation: migration plan prepared; implementation has not started.

The migration covers the fingerprint corpus, matching and verification
semantics, the inventoried Ruby API, and all five Ruby CLI tools. No API or CLI
exclusions are approved. Lattice gates report evidence and release state; they
do not grant runtime or production authority.

See [`docs/superpowers/specs/2026-10-11-recog-rs-standalone-design.md`](docs/superpowers/specs/2026-10-11-recog-rs-standalone-design.md)
and [`docs/superpowers/plans/2026-10-11-recog-rs-standalone-port.md`](docs/superpowers/plans/2026-10-11-recog-rs-standalone-port.md).
