"""Stems selected for qualitative figures in the internal working draft.

Every face is a real person from a publicly accessible before/after source. The
legacy ``verified`` flag permits working-draft figure generation only; it does not
assert consent, copyright permission, IRB review, or submission readiness. See
docs/real_face_checklist.md before public or archival use.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stem:
    face_id: str        # e.g. "real_01"
    procedure: str      # canonical procedure slug
    verified: bool      # allowed in the internal working draft only


# Teaser (Fig. 1): working-draft use only until the checklist is complete.
TEASER_FACE = Stem("real_01", "deep_plane_facelift", verified=True)

# Qualitative grid: one row per procedure/control contrast. Faces must be in the
# registered matrix runs (facelift real_01-08; rhino real_01-04 + *_front).
GRID_FACES = [
    Stem("real_07", "deep_plane_facelift", verified=True),
    Stem("real_06", "deep_plane_facelift", verified=True),
    Stem("real_06_front", "rhinoplasty", verified=True),
]

# Model-comparison strip: the same face composited by all six editors.
STRIP_FACE = Stem("real_02", "deep_plane_facelift", verified=True)
STRIP_MODELS = [
    "gpt_image_2", "gpt_image_2_low", "nano_banana_pro",
    "nano_banana_2", "seedream_5_0", "flux_2_pro",
]

# Profile rhinoplasty strip: input | edit | real post-op photograph. Profiles are
# pose-gated (no compositing), so the edit shown is the model's raw output.
PROFILE_RHINO_FACES = [
    Stem("real_04", "rhinoplasty", verified=True),
    Stem("real_02", "rhinoplasty", verified=True),
]
PROFILE_RHINO_MODEL = "gpt_image_2"
