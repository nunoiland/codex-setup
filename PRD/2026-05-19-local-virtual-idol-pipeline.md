# Local Free 3D Virtual Idol Pipeline

## Goal

Create a repository-backed guide for building a free, local-first 3D virtual idol / anime-style character production pipeline.

The outcome should help a user create a custom VRM-style character, animate it locally, add speech or lip-sync, and record short-form videos without relying on paid avatar-generation SaaS.

## Scope

- In scope:
  - Document a local-first stack for 3D virtual idol character creation and operation.
  - Compare the main free/open-source tools by freedom, difficulty, and fit.
  - Define an MVP workflow from character creation to OBS recording.
  - Include extension paths for AI conversation, local TTS, ComfyUI concept art, and MMD/VMD dance workflows.
  - Call out licensing and hardware constraints.
- In scope:
  - Prefer Windows + NVIDIA GPU 12GB+ as the primary environment.

## Non-goals

- Out of scope:
  - Installing or vendoring third-party repositories into this repo.
  - Adding new runtime dependencies to this repo.
  - Creating an actual VRM model file, video output, or trained voice model.
  - Bypassing commercial terms, watermarks, or paid limits of third-party SaaS.
  - Recreating or impersonating real idols or real people.

## Context

The user wants a free local alternative to paid tools like HeyGen, focused on high-freedom virtual idol / anime-style character creation and animation. The preferred direction is 3D VRM character control, not one-off AI video generation.

## Constraints

- Technical constraints:
  - Original high-end target: Windows with NVIDIA GPU 12GB+.
  - Actual local setup target: macOS Apple Silicon M1 Pro with 16GB unified memory.
  - Keep cloud services optional; local-first by default.
  - Avoid adding dependencies to this repository.
- Product constraints:
  - Prioritize character freedom, repeatability, and local ownership.
  - Keep the first workflow practical enough for a solo creator.
- Time or release constraints:
  - Deliver as documentation and planning artifacts only.

## Acceptance criteria

1. A detailed guide exists under `docs/` describing the recommended local virtual idol pipeline.
2. The guide identifies the MVP stack, optional tools, workflow steps, validation checklist, and risks.
3. `docs/README.md` links to the new guide.
4. A plan exists in `PLANS/` capturing the implementation boundary.
5. Validation runs successfully for documentation-only changes.

## Edge cases

- User does not have NVIDIA GPU 12GB+.
- Tool repositories change, break, or are abandoned.
- Free tools still require paid assets, commercial licenses, or manual rigging labor.
- MMD/VMD motions, VRM assets, outfits, and voice models may have license restrictions.
- Local AI video generation may be too slow or inconsistent for production.

## Platform target

- docs

## Delivery mode

- existing repository + focused documentation change

## Reporting mode

- local_thread

## Secret profile

- Required secret: none
- Source of injection: not applicable
- Owner or approver: not applicable

## Human handoff

- QA checks:
  - Review the tool choices against the user's actual PC specs.
  - Confirm licenses before publishing or monetizing outputs.
- Manual release or infra tasks:
  - None.
- Final approver:
  - User.

## Strategy focus

- Establish a free/local creator pipeline that can later support repeatable short-form virtual idol content.

## Validation commands

```bash
./scripts/validate.sh
```

## Current implementation status

Installed Mac MVP tools:

- VRoid Studio 2.12.0
- Blender 5.1.2
- OBS 32.1.2
- VCam 0.13.3

Created MVP asset and baseline capture settings:

- First original VRoid prototype exported to `<local-output-dir>/local-idol-prototype.vrm`.
- OBS configured for vertical `720x1280` canvas/output at 30 FPS.
- VCam loaded the VRM and auto-loads the prototype on restart.
- VCam tracking is configured for built-in webcam face/eye/mouth, hand, and finger tracking.
- Smoothness tuning was applied with OBS closed: tracking FPS `45`, shoulder rotation weight `0.6`, finger opening/closing sensitivity `0.8`, and a calibration pass.
- OBS has a VCam virtual-camera source framed for 9:16, and a 26.87 second `720x1280` recording smoke test was created at `<local-output-dir>/recording-smoke-test.mov`.

Manual follow-up remains: judge the VCam motion quality with OBS closed, keep face/shoulders/hands inside the camera frame, lower VCam tracking FPS toward `30` if `45` overloads the Mac, and validate Blender VRM import/export only when model editing becomes necessary.

## Done when

- PRD, plan, and docs guide are committed-ready.
- Validation result is reported honestly.
- Risks and follow-ups are documented.
