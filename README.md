# Schedule and installation: scalar audit

A small, standalone arithmetic artifact for a finite simulation case study. It reconstructs reported policy summaries from 16 saved case/budget/installation/delay cells. Python 3.9+ and the standard library are sufficient; no network access, simulator or third-party package is needed at runtime.

## Reproduce

Download release `v1.0.0`, extract it, and run in that folder:

```sh
python -I verify.py
```

This verifies the frozen archive and member hashes, runs `reproduce/audit.py` in isolated Python, and compares its complete JSON output to `reproduce/expected_results.json`. Expected final status: `PASS: file hashes, paper rounding checks, and exact expected JSON`.

To inspect the full results:

```sh
python -I reproduce/audit.py
```

The same five-file original artifact is retained at `archive/scalar_candidate113.zip` (5,850 bytes). Its SHA-256 is `5d7c6bf0ebd4ac8cca2a1a6fe6959456e5b80939ae37b442db3f12949dcd494a`.

## What is reproduced

- The original fixed-installation and frozen schedule-dependent policy summaries.
- All four delay-only installation mappings and the planning-derived choices.
- Hindsight class maxima for shared fixed, delay-only, case-only, and case-plus-delay choices.
- Both orders for decomposing the gap gain and their mixed difference.

The ranking prioritizes aggregate original success, then mean worst-world clearance M. In these data all policies tie on original success. The four class maxima are order independent; decomposition of their gain can depend on the nesting order. Case-aware classes assume the case is known when selecting the installation. These are post-hoc arithmetic comparisons on overlapping views, not independent trials or causal effects.

## Scope and limits

This release reproduces scalar arithmetic only. It does not reproduce optimization, candidate generation, trajectories, geometry, classification, physics or raw-array auditing. It does not contain a complete simulation capsule. Neither equality with the recorded output nor public availability establishes robustness, methodological novelty or a population result.

The archive and its internal README are an unchanged pre-release snapshot. The internal statement that publication/licensing is pending is superseded by this release and `LICENSES/NOTICE.md`. Table labels in that snapshot refer to the earlier manuscript numbering; the numerical definitions and expected results are unchanged.

## Licenses and version

Code and original documentation: MIT (`LICENSE`). Scalar data, expected arithmetic and manifests: CC0 1.0 (`LICENSES/CC0-1.0.txt`). These terms apply to this artifact only. Repository revisions and the version tag identify the published state; `release_manifest.json` binds individual files by SHA-256.

This public repository identifies its hosting account. Its public URL is not a certification of anonymous-submission compliance; any submission link must follow the venue's applicable policy.

## Additional public replay and sensitivity artifacts

The scope above describes the original `v1.0.0` scalar artifact. Related source and input packages are available separately:

- [Planning and physics source/input capsule (`v2.0.1`)](https://github.com/uuumehhh/schedule-installation-scalar-audit/releases/tag/v2.0.1).
- [Sensitivity runtime source (`sensitivity-runtime-v1.0.0`)](https://github.com/uuumehhh/schedule-installation-scalar-audit/releases/tag/sensitivity-runtime-v1.0.0).

On 3 November 2026, the unchanged sensitivity package's completed-workspace importer was exercised once against the already-completed author-host nominal workspace. It verified 650 unique file hashes and the recorded links for 26 runs and 32 budget/world views. Its saved-JSON scalar projection matched an independent reconstruction and, separately, the author reference. The check completed in 9.634 seconds within a 600-second cap. It performed no new physics, optimization or array decoding.

The [machine-readable validation record](validation/completed-workspace-import124.json) gives the exact scope and public source hashes. This closes the actual completed-workspace importer compatibility check. Fresh-host reproduction, relocated physical execution, numerical/graphics portability and full R52 sensitivity execution remain unverified. The recorded O/T/E/S values belong to the prior runs and are not new trials.
