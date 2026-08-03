"""Quantitative figures for the paper (matplotlib -> PDF, IEEE column width).

Palette: three categorical slots validated with the dataviz checker on white
(CVD-safe adjacent pairs; magenta is sub-3:1 so every figure carries a legend
or direct labels). Text/ink tokens stay neutral; series color marks identity only.
"""

import os

os.environ.setdefault("SOURCE_DATE_EPOCH", "0")  # reproducible PDF metadata

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import CONTROL_NAMES, DATA_DIR, FIGURES_DIR, MODEL_NAMES
from matplotlib.axes import Axes

COL_W = 3.45  # inches, ~IEEEtran \columnwidth

INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"

BLUE = "#2a78d6"
GREEN = "#008300"
MAGENTA = "#e87ba4"

# Insertion order is the order controls appear on axes and in legends.
CONTROL_COLOR = {
    "prompt_only": BLUE,
    "masked_composite": GREEN,
    "masked_inpaint": MAGENTA,
}
IDENTITY_FLOOR = 0.6
JITTER_SEED = 20260716  # fixed so rebuilds stay byte-reproducible

plt.rcParams.update({
    "font.size": 8,
    "font.family": "sans-serif",
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.6,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelcolor": INK,
    "ytick.labelcolor": INK,
    "grid.color": GRID,
    "grid.linewidth": 0.5,
    "legend.frameon": False,
    "pdf.fonttype": 42,
})


def style_axes(ax: Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, axis="both", zorder=0)
    ax.set_axisbelow(True)


def slant_xticks(ax: Axes) -> None:
    """Angle the category labels just enough to keep long model names from colliding."""
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(12)
        lbl.set_ha("right")


def dot_marker(label: str, color: str, *, marker: str = "o", edge: str = "white",
               size: float = 5) -> plt.Line2D:
    """A legend proxy matching the scatter marks (they carry no label themselves)."""
    return plt.Line2D([], [], marker=marker, ls="", markersize=size,
                      markerfacecolor=color, markeredgecolor=edge, label=label)


def controls_present(df: pd.DataFrame) -> list[str]:
    """The control rungs actually in the data, in the canonical axis/legend order."""
    present = set(df.control)
    return [c for c in CONTROL_COLOR if c in present]


def fig_scatter(df: pd.DataFrame) -> None:
    """Identity vs localization: the two failure modes in one plot.

    Color encodes the control rung only; the per-model breakdown lives in the
    dot-strip figure and Table 2, so the model dimension is annotated rather
    than encoded (seven marker shapes were illegible at column width).
    """
    d = df.dropna(subset=["identity_cosine", "change_localization"])
    controls = controls_present(d)
    fig, ax = plt.subplots(figsize=(COL_W, 2.9))
    for control in controls:
        g = d[d.control == control]
        ax.scatter(
            g.change_localization, g.identity_cosine, s=20, marker="o",
            facecolors=CONTROL_COLOR[control], edgecolors="white",
            linewidths=0.5, zorder=3, alpha=0.9,
        )
    ax.axhline(IDENTITY_FLOOR, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.text(0.02, 0.605, "identity reference (0.6)", color=MUTED, fontsize=7, va="bottom")

    def note(text: str, xy: tuple[float, float], xytext: tuple[float, float]) -> None:
        ax.annotate(text, xy=xy, xytext=xytext, ha="center", fontsize=7, color=INK,
                    arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6})

    note("off-target edits\n(beauty-filter risk)", (0.5, 0.9), (0.13, 0.8))
    note("region-confined", (0.99, 0.72), (0.8, 0.62))
    low = d[d.identity_cosine < IDENTITY_FLOOR]
    if len(low):
        share = (low.model == "flux_2_pro").mean()
        note("low identity,\nmostly FLUX.2 [pro]" if share >= 0.5 else "low identity",
             (low.change_localization.median(), low.identity_cosine.median()), (0.1, 0.44))
    ax.set_xlabel(r"Edit localization  $\Delta E_{\mathrm{tgt}}/(\Delta E_{\mathrm{tgt}}+\Delta E_{\mathrm{off}})$")
    ax.set_ylabel("ArcFace identity cosine")
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(min(0.38, d.identity_cosine.min() - 0.05), 1.02)
    style_axes(ax)

    fig.legend(handles=[dot_marker(CONTROL_NAMES[c], CONTROL_COLOR[c]) for c in controls],
               loc="lower left", bbox_to_anchor=(0.1, 0.0),
               ncols=3, fontsize=6.5, title="Control", title_fontsize=7,
               alignment="left", columnspacing=0.8, handletextpad=0.3)
    fig.set_size_inches(COL_W, 3.1)
    fig.tight_layout(rect=(0, 0.1, 1, 1), pad=0.4)
    fig.savefig(FIGURES_DIR / "scatter_identity_localization.pdf")
    plt.close(fig)


def _dot_column(ax: Axes, i: int, vals: pd.Series, color: str,
                rng: np.random.Generator) -> None:
    """One jittered dot column with a median bar; every output stays visible."""
    x = i + rng.uniform(-0.16, 0.16, len(vals))
    ax.scatter(x, vals, s=13, facecolors=color, edgecolors="white",
               linewidths=0.4, alpha=0.85, zorder=3)
    ax.plot([i - 0.27, i + 0.27], [vals.median()] * 2, color=INK, lw=1.4, zorder=4)


def fig_strips(df: pd.DataFrame) -> None:
    """Localization per control rung (left) and identity per model (right).

    Jittered dot strips instead of box plots: with fewer than ten faces per
    cell a five-number summary hides the data, so every output is drawn and
    only the median is overlaid.
    """
    rng = np.random.default_rng(JITTER_SEED)
    fig, (ax_loc, ax_id) = plt.subplots(1, 2, figsize=(COL_W * 2 + 0.3, 2.4))

    controls = controls_present(df)
    for i, c in enumerate(controls):
        _dot_column(ax_loc, i, df[df.control == c].change_localization.dropna(),
                    CONTROL_COLOR[c], rng)
    ax_loc.set_xticks(range(len(controls)), [CONTROL_NAMES[c] for c in controls])
    ax_loc.set_xlim(-0.6, len(controls) - 0.4)
    ax_loc.set_ylabel("Edit localization")
    ax_loc.set_title("(a) Localization by control", fontsize=8, color=INK)
    slant_xticks(ax_loc)

    models = sorted(set(df.model), key=lambda m: -df[df.model == m].identity_cosine.median())
    for i, m in enumerate(models):
        _dot_column(ax_id, i, df[df.model == m].identity_cosine.dropna(), BLUE, rng)
    ax_id.axhline(IDENTITY_FLOOR, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    ax_id.set_xticks(range(len(models)), [MODEL_NAMES[m] for m in models])
    ax_id.set_xlim(-0.6, len(models) - 0.4)
    ax_id.set_ylabel("ArcFace identity cosine")
    ax_id.set_title("(b) Identity by model", fontsize=8, color=INK)
    ax_id.tick_params(axis="x", labelsize=6.5)
    slant_xticks(ax_id)

    for ax in (ax_loc, ax_id):
        style_axes(ax)
        ax.grid(False, axis="x")
    fig.tight_layout(pad=0.6)
    fig.savefig(FIGURES_DIR / "strip_localization_identity.pdf")
    plt.close(fig)


PROC_LABELS = {"deep_plane_facelift": "Facelift-style", "rhinoplasty": "Rhinoplasty"}


def fig_gt_strip(df: pd.DataFrame, base: pd.DataFrame) -> None:
    """Ground-truth cosine strip plot: a soft sanity check, deliberately small.

    Open diamonds are the input-to-postoperative baselines (one per face,
    scripts/gt_baseline.py), drawn just below each row so the edited outputs can
    be read against the similarity the unedited photo already had."""
    d = df.dropna(subset=["gt_identity_cosine"])
    procs = sorted(set(d.procedure))
    fig, ax = plt.subplots(figsize=(COL_W, 2.0))
    for i, proc in enumerate(procs):
        g = d[d.procedure == proc]
        jitter = (np.arange(len(g)) % 5 - 2) * 0.045
        ax.scatter(g.gt_identity_cosine, i + jitter, s=14,
                   facecolors=BLUE, edgecolors="white", linewidths=0.4, alpha=0.85, zorder=3)
        ax.plot([g.gt_identity_cosine.median()] * 2, [i - 0.28, i + 0.28],
                color=INK, lw=1.4, zorder=4)
        b = base[base.procedure == proc].gt_baseline_cosine.dropna()
        ax.scatter(b, [i - 0.38] * len(b), s=16, marker="D", facecolors="none",
                   edgecolors=INK, linewidths=0.7, zorder=3)
    fig.legend(
        handles=[
            dot_marker("edited output vs. post-op", BLUE, size=4.5),
            dot_marker("input photo vs. post-op (baseline)", "none",
                       marker="D", edge=INK, size=4.5),
        ],
        loc="upper left", bbox_to_anchor=(0.12, 1.0),
        ncols=1, fontsize=6.5, handletextpad=0.3, labelspacing=0.2,
    )
    ax.set_yticks(range(len(procs)))
    ax.set_yticklabels([PROC_LABELS.get(p, p.replace("_", " ").capitalize()) for p in procs])
    ax.set_xlabel("ArcFace cosine vs. post-op photo")
    ax.set_ylim(-0.6, len(procs) - 0.4)
    style_axes(ax)
    ax.grid(False, axis="y")
    fig.tight_layout(rect=(0, 0, 1, 0.86), pad=0.4)
    fig.savefig(FIGURES_DIR / "strip_gt_cosine.pdf")
    plt.close(fig)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "canonical_rows.csv")
    base = pd.read_csv(DATA_DIR / "gt_baseline.csv")
    fig_scatter(df)
    fig_strips(df)
    fig_gt_strip(df, base)
    print(f"wrote figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
