# Novelty and claim-boundary notes (updated 2026-07-17)

## Defensible contribution

The paper is a pilot comparison of a client-side control ladder across hosted,
black-box image-editing endpoints for two cosmetic-surgery preview requests. The
contribution is the controlled hosted-API comparison and implementation audit, not
a new compositing algorithm, surgical outcome model, or clinically validated
metric.

## Critical near-neighbor

Envisage (`agarwal2026envisage`, arXiv:2606.28628) evaluates a local FLUX.1-Fill
rhinoplasty pipeline on 211 cases with MediaPipe masks, hard compositing, clinical
presets, ground-truth-relative ArcFace analysis, and a mask-decomposed SurgicalScore.
It directly establishes that full-face identity metrics are confounded after hard
compositing. Our paper must not imply stronger clinical validation than Envisage.

The distinction is the setting, not scale: Envisage assumes an open-weight
inpainter the operator hosts, so neither its pipeline nor any internals-based
localization method transfers to a hosted black-box endpoint - which is exactly
the setting we study, with multiple hosted endpoints, two requested edit types,
and prompt-only/client-composite/native-mask control as the manipulated variable.
The current study is much smaller and has no surgeon ratings; do not imply
stronger clinical validation than Envisage.

## Required claim boundaries

- Say that compositing enforces off-mask pixel preservation; do not call this proof
  of anatomical correctness or clinical plausibility.
- Treat CIELAB localization as a limited target/keep-zone diagnostic, not a new or
  clinically validated metric.
- Treat ArcFace 0.6 as a heuristic reference, not an acceptance threshold.
- Call postoperative cosine an identity reference because no input baseline is
  available.
- Describe the two chained outputs on one face as a feasibility probe only.
- Generalize neither from one Qwen endpoint to masked inpainting nor from 15 faces
  to clinical populations.
- Report 210 attempted cells, 196 scoreable outputs, and 14 exclusions.
- State that one output was generated per cell and that GPT Image 2 and Seedream
  5.0 Lite do not expose seeds.
- Cite Nano Banana 2 as Gemini 3.1 Flash Image (2026), not the 2025 Nano Banana.
- Name the tested ByteDance endpoint Seedream 5.0 Lite, not Seedream 5.0 Pro.

## Required work before archival submission

- Obtain blinded ratings from multiple surgeons and report inter-rater agreement.
- Add repeated generations and patient-clustered analysis on a larger cohort.
- Record input-to-postoperative baselines and a mask-decomposed fidelity measure.
- Extend off-target scoring beyond the upper-face keep zone and support profiles.
- Record demographics and stratified failures.
- Release or archive the complete generation/scoring pipeline and resolved configs.
- Complete the public-source provenance, permission, and IRB checklist.
