# Novelty scan notes (2026-07-16)

Web sweep of ~30 sources across surgical simulation, editing benchmarks, training-free
localized editing, identity metrics, and clinical simulation literature. Section 2
(Related Work) is written FROM this file; every differentiation claim below is sourced
in refs.bib.

## Verdict

**Both contributions survive, in narrowed form.** No prior work combines all three of:
hosted/black-box commercial image-edit APIs + client-side region confinement +
surgical preview. But the claims must be scoped carefully (see "Claims to avoid").

**Critical near-neighbor - must cite and answer: Envisage** (`agarwal2026envisage`,
arXiv:2606.28628, June 26 2026). Rhinoplasty goal visualization: FLUX.1-Fill inpainting
+ MediaPipe masks + hard compositing + clinical presets; "SurgicalScore" masked
evaluation (masked LPIPS, edit direction, outside-mask preservation). Differences we
stand on: (1) local open-weight model vs our four hosted black-box APIs; (2) no control
ladder (no prompt-only rung, no API-mask rung, no pose gating); (3) masked-LPIPS score
vs our dE76 localization ratio; (4) rhinoplasty-only evaluation vs our three procedures.

**Envisage's ArcFace critique must be preempted**: identity cosine computed on a
composited output partially measures copied pixels (outside-mask pixels are identical
by construction). Our answer, to be written into Sec. 4 and 6: report ArcFace on the
prompt_only rung as the uncontaminated model-capability measure; treat composite-rung
ArcFace as a system-level property and lean on the localization metric inside the mask.
Not addressing this invites a direct rebuttal.

## Near neighbors by area (one line each + differentiation)

**(a) Surgical simulation**
- `knoedler2024rhinoplastygan` (Aesth Plast Surg 2024): GAN trained on 3,030 paired
  rhinoplasty photos; raters at ~chance. Differs: bespoke trained model vs off-the-shelf
  hosted models with zero surgical training data; single procedure; rater-only eval.
- `agarwal2026envisage`: see verdict above.
- `huang2024ptosisdiffusion` (Front Cell Dev Biol 2024): training-free SD-1.5 +
  ControlNet + mask inpainting for blepharoptosis. Differs: ControlNet conditioning is
  impossible against a hosted API; single procedure; no multi-model benchmark.
- `blepharoptosis2022poap` (Ophthalmology Science 2022): trained POAP predictor.
  Differs: trained, geometry-focused, single procedure.
- `lim2023generativecosmetic` (J Clin Med 2023): DALL-E 2/Midjourney generate *generic*
  cosmetic-surgery imagery for the same three procedures; finds demographic bias.
  Differs: text-to-image of generic faces, not identity-preserving edits of a patient
  photo; no quantitative identity/localization eval. Cite for procedures + bias.
- `fang2022acmtnet` (MICCAI 2022): bony-movement-driven 3D soft-tissue prediction.
  Differs: 3D biomechanics, orthognathic.

**(b) Clinical simulation / expectation management (motivation citations)**
- `yamamichi2025crisalix` (ASJ Open Forum 2025): Crisalix 3D simulation accuracy
  correlates rho=0.66 with post-op satisfaction -> accurate previews matter clinically.
- `threedvr2026aesthetic` (Comput Assist Surg 2026): 3D/VR improves decisions/satisfaction.
- `agarwal2007morph` (PRS 2007) + `sharp2002computerimaging` (JLO 2002): the decades-old
  manual-morphing practice we automate.
- `stephanian2024fpsamreview` (FPSAM 2024): systematic review of AI in facial aesthetic surgery.

**(c) Training-free localized editing - all require model internals; hosted APIs expose none.**
This is the cleanest argument for the masked_composite rung:
- Sampling-loop access: `meng2022sdedit`, `lugmayr2022repaint`, `couairon2023diffedit`
- Per-step latent blending: `avrahami2022blended`, `avrahami2023blendedlatent`
- Attention/feature access: `hertz2023prompt2prompt`, `tumanyan2023plugandplay`
Frame masked_composite as a post-hoc, model-agnostic analogue of blended compositing
that needs no internals and no mask parameter - NOT a new editing algorithm.

**(d) Editing benchmarks (hosted-API benchmarking is now common - scope claims by domain)**
- `qian2025giebench`: object-aware masked preservation scoring; finds GPT-Image-1
  "over-edits irrelevant regions". Closest eval-side neighbor; general-domain, no
  identity/clinical dimension. Cite as precedent for off-target measurement.
- `alebench2024`: target-external/internal leakage metrics - same, CLIP-based, general.
- `gptimgeval2025`, PhyEditBench (arXiv:2606.26551): hosted models benchmarked in other
  domains - avoid any "first to benchmark commercial editors" claim.
- `zhang2023magicbrush`, `wang2023editbench`, `sheynin2024emuedit`, `ku2024imagenhub`,
  `ma2024i2ebench`, `hui2025hqedit`, `liu2025step1xedit`: general-domain benchmarks/datasets.

**(e) Identity metrics**: ArcFace cosine is standard practice (e.g. FED-Bench
arXiv:2603.29697 validates it against human identity judgment) - the metric itself is
NOT a contribution; the pairing with the localization ratio and per-rung reporting is.

**(f) Critical overlap check**: no academic work combines hosted APIs + region
confinement + surgical preview. Marketing-grade "nano banana plastic surgery" demos
exist (blog-level, no evaluation). Envisage is the only academic work at the
editing+masks+cosmetic-surgery intersection: local model, single procedure, no ladder.

## Claims to avoid / required wording

1. NOT "first AI/generative cosmetic-surgery preview" (Knoedler, PtosisDiffusion,
   Envisage, 30 years of computer imaging). SAY: "first controlled benchmark of
   off-the-shelf, hosted image-editing APIs for identity-preserving surgical previews
   across three facial procedures."
2. NOT "first to measure off-target edits" (GIE-Bench, ALE-Bench, Emu Edit, Envisage).
   SAY: "a dE76-based localization ratio purpose-built to detect beauty-filter
   behavior, paired with identity drift as dual failure modes" + cite the
   general-domain precedents.
3. NOT "a new editing algorithm" for masked_composite. SAY: "adapting
   blended-compositing ideas to a pure black-box setting; studied as one rung of a
   controlled ladder." The ladder-as-experimental-design + pose gating + guardrail
   prompts is the defensible unit.
4. NOT "first benchmark of commercial image editors." Scope = clinical facial surgery
   domain + real post-op ground truth + controlled interventions.
5. Preempt the Envisage ArcFace-confounding critique (see verdict).
6. Seedream 5.0 has no tech report (blog only, Jul 8 2026): cite blog + Seedream 4.0
   arXiv as lineage; pin version/date-accessed for all hosted models.

## Follow-ups before submission

- [ ] Read the Envisage PDF in full; write the ArcFace rebuttal paragraph for Sec. 4.
- [ ] Resolve `% UNVERIFIED` fields in refs.bib from publisher pages (Session 4).
