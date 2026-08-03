"""Input-to-postoperative ArcFace baseline for every face with a post-op photo.

The main results carry an edit-to-postoperative cosine (`gt_identity_cosine`), but
interpreting it needs the matching input-to-postoperative cosine for the same face.
This script computes that baseline from photographs that already exist; it makes no
API requests and generates no images.

Self-contained: it uses insightface directly (installed via this repo's `baseline`
extra) with the same settings the experiment pipeline used - buffalo_l on CPU,
det_size 640, det_thresh 0.15, largest detected face, plain RGB loading - so the
baselines are comparable with the published cosines. The experiment repo is read
strictly read-only, for photographs and the manifest only.

Run with:

    make baseline        (= uv run --extra baseline python scripts/gt_baseline.py)

Writes data/gt_baseline.csv, which aggregate.py merges into the delta macros.
"""

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from config import DATA_DIR, POC_ROOT
from PIL import Image

# Mirrors the experiment pipeline's detection setup: SCRFD confidence scores are
# deflated in that stack (real faces score ~0.2, not ~0.8), so the stock 0.5
# threshold would reject every face.
DET_THRESH = 0.15


def face_analysis():
    try:
        from insightface.app import FaceAnalysis
    except ImportError:
        sys.exit(
            "insightface is not installed - run `make baseline`, which uses "
            "this repo's `baseline` extra (uv run --extra baseline ...)"
        )
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"],
        allowed_modules=["detection", "recognition"],
    )
    app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=DET_THRESH)
    return app


def embedding(app, path: Path) -> np.ndarray | None:
    """L2-normalized embedding of the largest detected face, or None if none found."""
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)
    bgr = np.ascontiguousarray(rgb[:, :, ::-1])  # insightface wants contiguous BGR
    faces = app.get(bgr)
    if not faces:
        return None
    faces.sort(key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
    return faces[0].normed_embedding


def manifest_gt_paths() -> dict[str, str]:
    """manifest `face_id` ('<proc>/<stem>') -> non-empty `ground_truth_path` (data-relative)."""
    manifest = POC_ROOT / "data" / "manifest.csv"
    if not manifest.exists():
        return {}
    with manifest.open(newline="", encoding="utf-8") as fh:
        return {
            r["face_id"]: rel
            for r in csv.DictReader(fh)
            if (rel := (r.get("ground_truth_path") or "").strip())
        }


def ground_truth_path(proc: str, face: str, manifest: dict[str, str]) -> Path | None:
    """The real after-photo path: manifest entry first, then the on-disk convention."""
    rel = manifest.get(f"{proc}/{face}")
    path = POC_ROOT / "data" / (rel or f"ground_truth/{proc}/{face}.png")
    return path if path.exists() else None


def main() -> None:
    rows = pd.read_csv(DATA_DIR / "canonical_rows.csv")
    faces = (
        rows[rows.gt_identity_cosine.notna()][["procedure", "face_id"]]
        .drop_duplicates()
        .sort_values(["procedure", "face_id"])
    )
    manifest = manifest_gt_paths()
    app = face_analysis()

    records = []
    for proc, face in faces.itertuples(index=False):
        input_path = POC_ROOT / "data" / "faces" / proc / f"{face}.png"
        gt_path = ground_truth_path(proc, face, manifest)
        if not input_path.exists() or gt_path is None:
            print(f"skip {proc}/{face}: missing input or ground truth", file=sys.stderr)
            continue
        a = embedding(app, input_path)
        b = embedding(app, gt_path)
        cosine = float((a * b).sum()) if a is not None and b is not None else float("nan")
        records.append({"procedure": proc, "face_id": face, "gt_baseline_cosine": cosine})
        print(f"{proc}/{face}: {cosine:.3f}")

    out = pd.DataFrame(records)
    DATA_DIR.mkdir(exist_ok=True)
    out.to_csv(DATA_DIR / "gt_baseline.csv", index=False)
    print(f"wrote {len(out)} baselines to {DATA_DIR / 'gt_baseline.csv'}")


if __name__ == "__main__":
    main()
