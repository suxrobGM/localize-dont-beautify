# Public-source face provenance and permission checklist

The experimental inputs are publicly accessible before/after photographs of real,
identifiable people. Public access alone does not establish permission for academic
republication, derivative AI processing, or transmission to a hosted service.

Before an image may appear in an archival submission, record and verify:

- [x] Exact source URL, publisher, and access date.
- [x] Copyright owner or authorized licensor.
- [ ] Terms permitting reproduction in an academic publication.
- [ ] Terms permitting derivative and hosted-AI processing.
- [ ] Required attribution in the figure caption or acknowledgments.
- [ ] Patient/subject authorization where applicable.
- [ ] Institutional IRB or exemption determination.
- [x] Hosted-provider retention and deletion settings used during processing
      (recorded below; upstream model-provider retention remains undocumented).

## Recorded sources (2026-07-17)

| Collection | Source | Copyright owner | Terms found |
| --- | --- | --- | --- |
| Facelift before/after images (manifest 2026-06-22) | <https://galleryofcosmeticsurgery.com/gallery-category/face/deep-plane-facelift/> | Gallery of Cosmetic Surgery & Aesthetic Lounge (Drs. Kevin Sadati, Ali Tehrani; Newport Beach, CA) | Clinic marketing gallery; footer copyright, no reuse license located |
| Rhinoplasty before/after images (manifest 2026-06-30) | <https://www.refinesurgery.com> (gallery; per-face item URLs still to be recorded) | Refine Facial Plastic Surgery and Aesthetics (Dr. Lucas Bryant; Nashville, TN) | "All Rights Reserved"; no reuse license located |

Both sources are private surgical practices' patient galleries. Patients consented
to display on the clinic's own site; that consent does not extend to third-party
republication or AI processing, and neither site publishes a license permitting
reuse. The experiment manifest's `consent` label ("licensed - consented for AI
use") predates this provenance check and overstates what is documented.

## Hosted-processing record (2026-07-17)

All generation ran through fal.ai endpoints. The pipeline's fal adapter
(`plastyvue/adapters/api/fal.py`) sends input images inline as data URIs (no
`fal_client.upload_file`, so no input objects are created in fal storage) and
sets `sync_mode: true` on every request, which per the endpoint schemas returns
output media inline as a data URI. No media lifecycle objects were deliberately
created.

Caveats that keep this from being a zero-retention claim:

- fal's privacy policy contains no zero-retention guarantee; stored-media
  retention is user-configurable (`X-Fal-Object-Lifecycle-Preference`) and only
  applies to objects in fal storage, which this pipeline avoided creating.
- fal routes requests to third-party model providers (OpenAI, Google, ByteDance,
  Black Forest Labs, Alibaba). What those providers retain from proxied requests
  is not documented by fal and has not been verified.

The ethics section may say images were "transmitted inline without creating
stored media objects," not that providers retained nothing.

## Current status

| Collection | Publicly accessible | Exact source recorded | Republication permission documented | Hosted processing documented | IRB/exemption | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Facelift before/after images | Yes | Yes | No | Settings recorded; upstream unknown | No | **Not submission-ready** |
| Rhinoplasty before/after images | Yes | Partial (site recorded; per-face URLs owed) | No | Settings recorded; upstream unknown | No | **Not submission-ready** |

## What would clear the remaining items

1. Written permission from each practice covering (a) reproduction of the specific
   images in an academic paper and (b) the derivative AI processing already
   performed, plus their required attribution wording. The practices would need
   their own patient photo releases to cover this grant.
2. Record the per-face source URLs in the experiment manifest and correct its
   `consent` column to reflect the documented status.
3. An institutional IRB or exemption determination (publicly available identifiable
   images, secondary use).
4. If permission is not obtained: replace the qualitative-figure images (synthetic
   or properly licensed faces) before any public posting or submission; the
   quantitative results can stand as-is since the score table contains no images.

The qualitative figures remain in the working draft for internal review only.
