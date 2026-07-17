"""Shared configuration for the paper's analysis scripts.

The scripts read the experiment repo strictly read-only; every generated artifact
lands inside this paper repo.
"""

import os
from pathlib import Path

POC_ROOT = Path(os.environ.get("PLASTYVUE_POC", r"c:\Users\admin\source\repos\plastyvue-poc"))
RUNS_DIR = POC_ROOT / "outputs" / "runs"
MODEL_CONFIGS_DIR = POC_ROOT / "configs" / "models"
MANIFEST = POC_ROOT / "data" / "manifest.csv"

PAPER_ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = PAPER_ROOT / "tables"
FIGURES_DIR = PAPER_ROOT / "figures" / "generated"
DATA_DIR = PAPER_ROOT / "data"

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
    "seedream_5_0": "Seedream 5.0",
    "qwen_image_edit_inpaint": "Qwen-Image-Edit (inpaint)",
    "qwen_image_edit": "Qwen-Image-Edit (local)",
}

PROCEDURE_NAMES = {
    "deep_plane_facelift": "Deep plane facelift",
    "facelift": "Deep plane facelift",
    "rhinoplasty": "Rhinoplasty",
    "blepharoplasty": "Blepharoplasty",
}

CONTROL_NAMES = {
    "prompt_only": "Prompt only",
    "masked_composite": "Masked composite",
    "masked_inpaint": "Masked inpaint",
}


def tex_escape(s: str) -> str:
    return s.replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")
