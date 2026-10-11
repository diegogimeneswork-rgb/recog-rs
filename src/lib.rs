//! Standalone Rust implementation of the Recog fingerprint database.
//!
//! The initial crate boundary deliberately has no runtime dependencies. The
//! corpus reader and matching API are introduced in the next migration stage.

#![forbid(unsafe_code)]
