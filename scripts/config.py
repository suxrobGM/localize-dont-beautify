"""Shared configuration for the paper's analysis scripts.

The scripts read the experiment repo strictly read-only; every generated artifact
lands inside this paper repo.
"""

import os
from pathlib import Path

POC_ROOT = Path(os.environ.get("PLASTYVUE_POC", r"c:\Users\admin\source\repos\plastyvue-poc"))
RUNS_DIR = POC_ROOT / "outputs" / "runs"
MODEL_CONFIGS_DIR = POC_ROOT / "configs" / "models"

PAPER_ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = PAPER_ROOT / "tables"
FIGURES_DIR = PAPER_ROOT / "figures" / "generated"
DATA_DIR = PAPER_ROOT / "data"

# Runs whose rows are eligible for the paper: the registered full-matrix runs
# (2026-07-16) plus the chained-procedures probe. Earlier runs were development
# iterations superseded cell-for-cell by the matrix; None = accept every run.
CANONICAL_RUN_PREFIXES: list[str] | None = ["20260716-", "20260709-035453"]

# Metric columns carried into the canonical row set.
METRIC_COLS = [
    "identity_cosine",
    "change_target",
    "change_offtarget",
    "change_localization",
    "gt_identity_cosine",
]

# Display names used in tables/figures (also keeps raw config slugs out of the paper).
MODEL_NAMES = {
    "gpt_image_2": "GPT Image 2",
    "gpt_image_2_low": "GPT Image 2 (low)",
    "nano_banana_pro": "Nano Banana Pro",
    "nano_banana_2": "Nano Banana 2",
    "seedream_5_0": "Seedream 5.0 Lite",
    "flux_2_pro": "FLUX.2 [pro]",
    "qwen_image_edit_inpaint": "Qwen-Image-Edit (inpaint)",
}

PROCEDURE_NAMES = {
    "deep_plane_facelift": "Facelift-style jaw--neck",
    "facelift": "Facelift-style jaw--neck",
    "rhinoplasty": "Rhinoplasty",
    "rhinoplasty_then_deep_plane_facelift": "Chained: rhino.\\ $\\to$ facelift",
    "deep_plane_facelift_then_rhinoplasty": "Chained: facelift $\\to$ rhino.",
}

CONTROL_NAMES = {
    "prompt_only": "Prompt only",
    "masked_composite": "Masked composite",
    "masked_inpaint": "Masked inpaint",
}


def tex_escape(s: str) -> str:
    return s.replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")
