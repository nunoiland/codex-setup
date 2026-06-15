# Plan: Local Free 3D Virtual Idol Pipeline

## Source PRD
- `PRD/2026-05-19-local-virtual-idol-pipeline.md`

## Status
- In progress: Mac MVP tools installed, first VRM exported, VCam webcam tracking configured, OBS vertical smoke test completed

## Platform target
- docs

## Affected files or directories
- `docs/local-virtual-idol-pipeline.md`
- `docs/README.md`
- `PRD/2026-05-19-local-virtual-idol-pipeline.md`
- `PLANS/2026-05-19-local-virtual-idol-pipeline.md`

## Tasks
1. Add a PRD capturing the user's local/free 3D virtual idol goal and constraints.
2. Add this approved plan as the execution boundary.
3. Create a detailed local pipeline guide covering tools, freedom tradeoffs, MVP workflow, validation, and risks.
4. Link the new guide from the docs index.
5. Run repository validation.

## Execution notes
- Mac environment detected: Apple Silicon M1 Pro with 16GB RAM.
- Installed VRoid Studio 2.12.0, Blender 5.1.2, and OBS 32.1.2.
- Installed VCam 0.13.3 from the official GitHub release.
- VRoid Studio required official DMG install because Homebrew has no `vroid-studio` cask.
- Created the first original VRoid prototype and exported it to `<local-output-dir>/local-idol-prototype.vrm`.
- Configured OBS video settings for vertical short-form output: `720x1280`, 30 FPS.
- Loaded the VRM in VCam and confirmed it auto-loads after restart.
- Enabled VCam built-in webcam face/eye/mouth, hand, and finger tracking.
- Tuned VCam for smoother body motion with OBS closed: tracking FPS `45`, shoulder rotation weight `0.6`, finger opening/closing sensitivity `0.8`, and one calibration click.
- Added OBS VCam virtual-camera source, hid the failed display-capture source, framed the source as a 9:16 portrait close-up, and created `<local-output-dir>/recording-smoke-test.mov` as a `720x1280` 30 FPS smoke test.
- Blender GUI launches, but headless CLI smoke testing crashed in this environment, so Blender VRM round-trip remains unvalidated.

## Risks and edge cases
- Some tools are free but not fully open source, and some assets may restrict commercial use.
- Local AI video generation can require more VRAM than the baseline system.
- Webcam-only VCam upper-body and hand tracking can still jitter or drop hands when lighting is weak, the user is too close, or hands leave frame.
- If VCam movement is still choppy at tracking FPS `45`, reduce it toward `30` before re-opening OBS.
- 2D Live2D-like workflows can become manual rigging projects and are not the recommended MVP.
- Real-person or real-idol likeness use can create rights and platform-policy risk.

## Validation commands
```bash
./scripts/validate.sh
```

## Review gates
- Docs verification
- QA review
- Security/licensing review

## Release and rollback notes
- Release note: add a local-first virtual idol production guide for free/open tooling.
- Rollback note: revert the documentation and planning files if this guide is no longer desired.
