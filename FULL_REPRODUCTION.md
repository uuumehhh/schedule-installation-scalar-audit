# Fixed-study search and physics reproduction v2.0.0

The full source-and-input artifact is **[full_reproduction114_v1.zip](https://github.com/uuumehhh/schedule-installation-scalar-audit/releases/download/v2.0.0/full_reproduction114_v1.zip)**. It covers the fixed two-input LOW10/HIGH20 study from the supplied nominal seeds: prescribed 40-call COBYQA search, candidate generation and retention, saved-array planning audit, selection, exact command/context binding, and 26 selected-command MuJoCo replays with saved-array evaluation.

Download the release asset named above, not GitHub's automatically generated Source code archive. The latter contains this small release index and the original scalar-only package. The full search and simulation source, model assets, nominal inputs, commands, pinned dependencies, licenses and run instructions are inside the release asset.

## Observed validation

On the same Windows host, using a newly installed public CPython 3.12.14 runtime and 14 hash-pinned public wheels, search produced 40 optimizer calls, 2,252 within-call unique visits, 28 references and 384 candidate pairs. The original search supervisor then failed in runtime-ledger reporting. A separately reviewed saved-output audit passed within the original 25,200-second deadline. The original failure and missing producer runtime ledger remain explicit; the corrected reporting guard has not been rerun as a new uninterrupted search execution.

The exact bridge passed 16 standard winner cells, 24 commands, six contexts and 26 execution identities / 32 views. Physical reproduction and its independent stored-array audit completed all 26 runs in 1,009.780008 seconds within one 1,800-second limit. All 1,881 declared per-run and policy numeric comparisons recorded zero differences. This is agreement in those semantic fields, not a claim that every raw byte matches.

All 26 runs passed the original physical and task/contact criteria; 22 passed the external 7.99 mm check and zero passed the separate strict criterion. Unknown classification is retained. Policy results and the original scientific conclusions are unchanged. These reruns are not additional independent study samples.

The artifact reproduces this fixed study from provided nominal seeds, not the upstream development of those seeds or every historical experiment. Validation is on the same host, not another machine, graphics stack or physical robot. See the archive's `README.md`, `ENVIRONMENT.md`, `validation114.json` and component documentation for precise commands, limits and observed failures.

## Integrity and licenses

- ZIP bytes: 69566201
- ZIP SHA-256: `80a7ae22e247fb122dcd9edc4a2be3c05ac9c8e18e92d77ad80802c6146d7f82`
- Internal release manifest SHA-256: `faa07c6367fe9d06d7a75bce098afda669b941727ac0d846ff7321ef6bc928a3`
- Files in the full artifact: 203
- Project code and documentation: MIT.
- Generated input, command and scalar data, expected results and manifests: CC0-1.0.
- Upstream SOARM100 meshes and derived XML: Apache-2.0; see `NOTICE.md` and `LICENSES/` for exact provenance and modifications.

No credentials, private workspace logs, author conversations, reviewer reports or environment caches are included. Component file inventories are preserved. Availability of this artifact does not establish a novel optimizer, universal policy superiority, hardware validation, official IROS 2027 compliance or acceptance.

The [v1.0.0 scalar-only release](https://github.com/uuumehhh/schedule-installation-scalar-audit/releases/tag/v1.0.0) remains unchanged.
