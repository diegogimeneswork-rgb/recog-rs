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
- Implementation: the corpus, standalone crate, and CI baseline are in place; the Ruby behavior port has not started.

The imported corpus contains 51 XML files and 4,677 fingerprint definitions,
including `http_cookies.xml`, a static database of cookie fingerprints.
Matching and verification semantics, the inventoried Ruby API, and all five
Ruby CLI tools remain in scope. No API or CLI exclusions are approved. Lattice
gates report evidence and release state; they do not grant runtime or
production authority.

See [`docs/superpowers/specs/2026-10-11-recog-rs-standalone-design.md`](docs/superpowers/specs/2026-10-11-recog-rs-standalone-design.md)
and [`docs/superpowers/plans/2026-10-11-recog-rs-standalone-port.md`](docs/superpowers/plans/2026-10-11-recog-rs-standalone-port.md).
