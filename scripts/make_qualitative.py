"""Qualitative figure grids (PIL) from run images, honoring the real-face license gate.

Builds, for each verified stem, side-by-side panels: input | prompt-only | masked
composite (teaser), multi-row grids for the qualitative figure, and the profile
rhinoplasty strip against the real post-op photographs.
"""

from functools import cache
from pathlib import Path

import pandas as pd
from config import DATA_DIR, FIGURES_DIR, MODEL_NAMES, POC_ROOT, RUNS_DIR
from figure_stems import (
    GRID_FACES,
    PROFILE_RHINO_FACES,
    PROFILE_RHINO_MODEL,
    STRIP_FACE,
    STRIP_MODELS,
    TEASER_FACE,
    Stem,
)
from PIL import Image, ImageDraw, ImageFont

PANEL = 384      # px per face panel
CONTROLS = ("prompt_only", "masked_composite", "masked_inpaint")


def image_for(row: pd.Series) -> Path:
    return RUNS_DIR / row.run_id / "images" / f"{row.stem}.png"


def input_for(s: Stem) -> Path:
    return POC_ROOT / "data" / "faces" / s.procedure / f"{s.face_id}.png"


def ground_truth_for(s: Stem) -> Path:
    return POC_ROOT / "data" / "ground_truth" / s.procedure / f"{s.face_id}.png"


@cache
def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def panel(img_path: Path, label: str, label_size: int = 16) -> Image.Image:
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((PANEL, PANEL))
    canvas = Image.new("RGB", (PANEL, PANEL + label_size + 12), "white")
    canvas.paste(img, ((PANEL - img.width) // 2, 0))
    draw = ImageDraw.Draw(canvas)
    font = _font(label_size)
    w = draw.textlength(label, font=font)
    draw.text(((PANEL - w) // 2, PANEL + 5), label, fill="#0b0b0b", font=font)
    return canvas


def hstack(panels: list[Image.Image], gap: int = 6) -> Image.Image:
    w = sum(p.width for p in panels) + gap * (len(panels) - 1)
    h = max(p.height for p in panels)
    out = Image.new("RGB", (w, h), "white")
    x = 0
    for p in panels:
        out.paste(p, (x, 0))
        x += p.width + gap
    return out


def vstack(rows: list[Image.Image], gap: int = 6) -> Image.Image:
    w = max(r.width for r in rows)
    h = sum(r.height for r in rows) + gap * (len(rows) - 1)
    out = Image.new("RGB", (w, h), "white")
    y = 0
    for r in rows:
        out.paste(r, (0, y))
        y += r.height + gap
    return out


def cleared(s: Stem, figure: str) -> bool:
    """The real-face license gate; an uncleared face simply doesn't appear."""
    if not s.verified:
        print(f"{figure}: {s.face_id} not verified - skipped")
    return s.verified


def edit_panel(
    df: pd.DataFrame, s: Stem, control: str, label: str,
    *, model: str | None = None, label_size: int = 16,
) -> Image.Image | None:
    """The rendered edit for one (face, procedure, control[, model]) cell, if it exists."""
    g = df[(df.face_id == s.face_id) & (df.procedure == s.procedure) & (df.control == control)]
    if model is not None:
        g = g[g.model == model]
    if g.empty or not image_for(g.iloc[0]).exists():
        return None
    return panel(image_for(g.iloc[0]), label, label_size)


def save(rows: list[Image.Image], name: str) -> bool:
    if not rows:
        return False
    vstack(rows).save(FIGURES_DIR / name)
    return True


def make_teaser(df: pd.DataFrame) -> bool:
    s = TEASER_FACE
    if not cleared(s, "teaser"):
        return False
    edits = [edit_panel(df, s, "prompt_only", "Prompt only"),
             edit_panel(df, s, "masked_composite", "Masked composite")]
    if any(e is None for e in edits):
        print(f"teaser: missing control rows for {s.face_id}")
        return False
    hstack([panel(input_for(s), "Input"), *edits]).save(FIGURES_DIR / "teaser_triptych.png")
    return True


def make_grid(df: pd.DataFrame) -> bool:
    rows = []
    for s in GRID_FACES:
        if not cleared(s, "grid"):
            continue
        edits = [edit_panel(df, s, c, c.replace("_", " ").capitalize()) for c in CONTROLS]
        edits = [e for e in edits if e is not None]
        if edits:
            rows.append(hstack([panel(input_for(s), "Input"), *edits]))
        else:
            print(f"grid: {s.face_id}/{s.procedure} has no rows in the canonical set - skipped")
    return save(rows, "qualitative_grid.png")


def make_model_strip(df: pd.DataFrame) -> bool:
    """The same face composited by every editor: the model-comparison figure."""
    s = STRIP_FACE
    if not cleared(s, "strip"):
        return False
    panels = [panel(input_for(s), "Input", label_size=36)]
    for model in STRIP_MODELS:
        p = edit_panel(df, s, "masked_composite", MODEL_NAMES.get(model, model),
                       model=model, label_size=36)
        if p is None:
            print(f"strip: no composited {model} edit for {s.face_id} - skipped")
        else:
            panels.append(p)
    if len(panels) < 3:
        return False
    hstack(panels).save(FIGURES_DIR / "model_strip.png")
    return True


def make_profile_strip(df: pd.DataFrame) -> bool:
    """Profile rhinoplasty: input | edit | real post-op. Profiles are pose-gated, so
    the edit is the model's raw output and only identity/ground-truth are scored."""
    label = f"Edit ({MODEL_NAMES.get(PROFILE_RHINO_MODEL, PROFILE_RHINO_MODEL)})"
    rows = []
    for s in PROFILE_RHINO_FACES:
        if not cleared(s, "profile"):
            continue
        edit = edit_panel(df, s, "prompt_only", label, model=PROFILE_RHINO_MODEL)
        gt = ground_truth_for(s)
        if edit is None or not gt.exists():
            print(f"profile: missing edit or post-op image for {s.face_id} - skipped")
            continue
        rows.append(hstack([panel(input_for(s), "Input"), edit, panel(gt, "Real post-op")]))
    return save(rows, "profile_rhino_gt.png")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "canonical_rows.csv")
    made = [make_teaser(df), make_grid(df), make_model_strip(df), make_profile_strip(df)]
    if not any(made):
        print("no qualitative figures generated - real-face gate is closed")


if __name__ == "__main__":
    main()
