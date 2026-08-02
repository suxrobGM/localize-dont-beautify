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

CONTROL_COLOR = {
    "prompt_only": "#2a78d6",       # blue
    "masked_composite": "#008300",  # green
    "masked_inpaint": "#e87ba4",    # magenta
}
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


def fig_scatter(df: pd.DataFrame) -> None:
    """Identity vs localization: the two failure modes in one plot.

    Color encodes the control rung only; the per-model breakdown lives in the
    dot-strip figure and Table 2, so the model dimension is annotated rather
    than encoded (seven marker shapes were illegible at column width).
    """
    d = df.dropna(subset=["identity_cosine", "change_localization"])
    fig, ax = plt.subplots(figsize=(COL_W, 2.9))
    for control in [c for c in CONTROL_COLOR if c in set(d.control)]:
        g = d[d.control == control]
        ax.scatter(
            g.change_localization, g.identity_cosine, s=20, marker="o",
            facecolors=CONTROL_COLOR[control], edgecolors="white",
            linewidths=0.5, zorder=3, alpha=0.9,
        )
    ax.axhline(0.6, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.text(0.02, 0.605, "identity reference (0.6)", color=MUTED, fontsize=7, va="bottom")
    ax.annotate("off-target edits\n(beauty-filter risk)", xy=(0.5, 0.9), xytext=(0.13, 0.8),
                ha="center", fontsize=7, color=INK,
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6})
    ax.annotate("region-confined", xy=(0.99, 0.72), xytext=(0.8, 0.62),
                ha="center", fontsize=7, color=INK,
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6})
    low = d[d.identity_cosine < 0.6]
    if len(low):
        share = (low.model == "flux_2_pro").mean()
        label = "low identity,\nmostly FLUX.2 [pro]" if share >= 0.5 else "low identity"
        ax.annotate(label,
                    xy=(low.change_localization.median(), low.identity_cosine.median()),
                    xytext=(0.1, 0.44), ha="center", fontsize=7, color=INK,
                    arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6})
    ax.set_xlabel(r"Edit localization  $\Delta E_{\mathrm{tgt}}/(\Delta E_{\mathrm{tgt}}+\Delta E_{\mathrm{off}})$")
    ax.set_ylabel("ArcFace identity cosine")
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(min(0.38, d.identity_cosine.min() - 0.05), 1.02)
    style_axes(ax)

    ctrl_handles = [
        plt.Line2D([], [], marker="o", ls="", markersize=5,
                   markerfacecolor=c, markeredgecolor="white", label=CONTROL_NAMES[k])
        for k, c in CONTROL_COLOR.items() if k in set(d.control)
    ]
    fig.legend(handles=ctrl_handles, loc="lower left", bbox_to_anchor=(0.1, 0.0),
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
    fig, axes = plt.subplots(1, 2, figsize=(COL_W * 2 + 0.3, 2.4))

    order = [c for c in ["prompt_only", "masked_composite", "masked_inpaint"] if c in set(df.control)]
    for i, c in enumerate(order):
        _dot_column(axes[0], i, df[df.control == c].change_localization.dropna(),
                    CONTROL_COLOR[c], rng)
    axes[0].set_xticks(range(len(order)), [CONTROL_NAMES[c] for c in order])
    axes[0].set_xlim(-0.6, len(order) - 0.4)
    axes[0].set_ylabel("Edit localization")
    axes[0].set_title("(a) Localization by control", fontsize=8, color=INK)
    for lbl in axes[0].get_xticklabels():
        lbl.set_rotation(12)
        lbl.set_ha("right")

    models = sorted(set(df.model), key=lambda m: -df[df.model == m].identity_cosine.median())
    for i, m in enumerate(models):
        _dot_column(axes[1], i, df[df.model == m].identity_cosine.dropna(),
                    "#2a78d6", rng)
    axes[1].axhline(0.6, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    axes[1].set_xticks(range(len(models)), [MODEL_NAMES[m] for m in models])
    axes[1].set_xlim(-0.6, len(models) - 0.4)
    axes[1].set_ylabel("ArcFace identity cosine")
    axes[1].set_title("(b) Identity by model", fontsize=8, color=INK)
    axes[1].tick_params(axis="x", labelsize=6.5)
    for lbl in axes[1].get_xticklabels():
        lbl.set_rotation(12)
        lbl.set_ha("right")

    for ax in axes:
        style_axes(ax)
        ax.grid(False, axis="x")
    fig.tight_layout(pad=0.6)
    fig.savefig(FIGURES_DIR / "strip_localization_identity.pdf")
    plt.close(fig)


def fig_gt_strip(df: pd.DataFrame) -> None:
    """Ground-truth cosine strip plot: a soft sanity check, deliberately small."""
    d = df.dropna(subset=["gt_identity_cosine"])
    procs = sorted(set(d.procedure))
    fig, ax = plt.subplots(figsize=(COL_W, 1.8))
    for i, proc in enumerate(procs):
        g = d[d.procedure == proc]
        jitter = (pd.Series(range(len(g))) % 5 - 2) * 0.045
        ax.scatter(g.gt_identity_cosine, [i + j for j in jitter], s=14,
                   facecolors="#2a78d6", edgecolors="white", linewidths=0.4, alpha=0.85, zorder=3)
        ax.plot([g.gt_identity_cosine.median()] * 2, [i - 0.28, i + 0.28],
                color=INK, lw=1.4, zorder=4)
    ax.set_yticks(range(len(procs)))
    proc_labels = {
        "deep_plane_facelift": "Facelift-style",
        "rhinoplasty": "Rhinoplasty",
    }
    ax.set_yticklabels([proc_labels.get(p, p.replace("_", " ").capitalize()) for p in procs])
    ax.set_xlabel("ArcFace cosine, edited vs. post-op photo")
    ax.set_ylim(-0.6, len(procs) - 0.4)
    style_axes(ax)
    ax.grid(False, axis="y")
    fig.tight_layout(pad=0.4)
    fig.savefig(FIGURES_DIR / "strip_gt_cosine.pdf")
    plt.close(fig)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "canonical_rows.csv")
    fig_scatter(df)
    fig_strips(df)
    fig_gt_strip(df)
    print(f"wrote 3 figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
