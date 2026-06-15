# Local Free 3D Virtual Idol Pipeline

This guide documents a free, local-first path for creating and operating a 3D virtual idol / anime-style character. It prioritizes character ownership, repeatable content production, and high creative freedom over one-click SaaS convenience.

## Recommended direction

Use a **VRM-based 3D character pipeline** as the main path:

1. Create or customize a VRM anime-style character.
2. Load the VRM into a local stage/viewer or VTuber app.
3. Add pose, facial expression, camera, motion, and lip-sync.
4. Record with OBS in a short-form 9:16 canvas.
5. Use AI tools only as optional helpers for concept art, scripts, voices, backgrounds, and thumbnails.

This is more controllable than pure AI video generation because the same character can be reused, posed, dressed, animated, and recorded repeatedly.

## Tool map

| Area | Recommended tool | Why use it | Freedom | Difficulty |
| --- | --- | --- | --- | --- |
| 3D anime character creation | VRoid Studio | Fastest free path to anime-style VRM characters | Medium-high | Low |
| Open VRM customization | CharacterStudio | Open-source VRM/GLB avatar creation and optimization | High | Medium |
| Advanced model editing | Blender + UniVRM | Full control over mesh, textures, bones, blendshapes, and export | Very high | High |
| Webcam VRM tracking | VCam | Mac-native VRM avatar app with face, mouth, hand, finger, virtual-camera, and OBS-friendly output | Medium-high | Low |
| Virtual idol stage | Lobe Vidol | VRM upload, character interaction, MMD-style direction | High | Medium |
| AI VTuber interaction | Open-LLM-VTuber | Local LLM/STT/TTS-oriented virtual character stack | High | Medium-high |
| Recording | OBS | Free standard for capture, scenes, 9:16 output, audio mixing | High | Low-medium |
| Concept art and thumbnails | ComfyUI or Stable Diffusion WebUI Forge | Local anime image generation and style exploration | High | Medium-high |
| Talking-head experiments | LivePortrait, SadTalker, MuseTalk | Useful for experiments, not the main 3D idol path | Medium | Medium-high |

## MVP workflow

### 1. Prepare the machine

Recommended Windows baseline for AI-heavy workflows:

- Windows 11
- NVIDIA GPU with 12GB+ VRAM
- 32GB system RAM if possible
- Git
- Node.js LTS
- Python 3.10 or 3.11 for AI tools
- Blender
- OBS Studio

Current Mac MVP baseline used for this setup:

- macOS on Apple Silicon M1 Pro
- 16GB unified memory
- Git, Node.js, npm, Python3, Homebrew
- VRoid Studio 2.12.0
- Blender 5.1.2
- OBS 32.1.2
- VCam 0.13.3
- First exported VRM prototype: `<local-output-dir>/local-idol-prototype.vrm`
- OBS vertical canvas configured: `720x1280`, 30 FPS

Keep paid SaaS optional. Do not put API keys or paid service credentials into tracked files.

### 2. Create the first character

Start with the lowest-friction route:

1. Use **VRoid Studio** to create a custom anime-style character.
2. Export as `.vrm`.
3. Save the source project and exported VRM in a local assets folder outside this repository.
4. Keep a small license note for every outfit, texture, hair preset, and accessory.

Use **CharacterStudio** when you want more open customization, batch generation, or VRM/GLB optimization. Use **Blender + UniVRM** when you need advanced editing such as custom outfits, mesh cleanup, blendshape repair, or export fixes.

### 3. Build the local stage

Load the VRM into a local viewer or virtual idol app.

Recommended first test:

1. Import the VRM.
2. Confirm the model loads without missing textures.
3. Test idle pose, smile, blink, mouth open, and camera framing.
4. Set a simple background: transparent, green screen, room image, or generated background.
5. Capture the window in OBS.

For idol-style motion, test VMD/MMD motion import where supported. Keep a motion-license note before using a dance in public content.

### 4. Add voice and lip-sync

Start simple before adding AI complexity:

1. Record a short voice line manually or generate a WAV with a free/local TTS tool.
2. Play the audio while the avatar app drives mouth movement.
3. Check whether the app uses simple amplitude mouth movement or phoneme/blendshape mapping.
4. Tune the script for short phrases because short phrases sync better than long paragraphs.

For a local AI extension, evaluate local TTS options after the stage is stable. Do not clone voices without rights.

### 5. Record a short-form video

OBS settings for a first vertical test:

- Canvas: `1080x1920` if the machine handles it, otherwise `720x1280`.
- FPS: 30 for first tests.
- Scene sources: avatar capture, background, text overlay, audio.
- Output: MP4 or MKV remuxed to MP4.

Acceptance test:

- 15-30 second clip records without dropped frames.
- Character remains framed from waist-up or bust-up.
- Mouth movement roughly matches the audio.
- Background and captions are readable on mobile.


## Current Mac execution status

This repository was used to prepare the current Mac for the MVP path.

Installed and verified:

- **VRoid Studio 2.12.0** from the official macOS installer.
- **Blender 5.1.2** via Homebrew cask.
- **OBS 32.1.2** via Homebrew cask.
- **VCam 0.13.3** from the official GitHub release.
- **Local Idol Prototype VRM** exported from VRoid Studio to `<local-output-dir>/local-idol-prototype.vrm`.
- **OBS vertical recording baseline** configured to `720x1280` canvas/output at 30 FPS.
- **VCam tracking baseline** configured for built-in webcam face, eye, mouth, hand, and finger tracking.
- **VCam smoothness pass** applied: OBS was stopped to reduce load, tracking FPS was raised to `45`, shoulder rotation weight was reduced to `0.6`, and finger open/close sensitivity was reduced to `0.8`.
- **VCam calibration** was triggered once from the main window after tuning.
- **OBS VCam source** exists as `VCam Virtual Camera MVP`; the failed `VCam Display Capture MVP` source was hidden and the virtual-camera source was framed as a 9:16 portrait close-up.
- **OBS recording smoke test** produced `<local-output-dir>/recording-smoke-test.mov` at `720x1280`, 30 FPS, 26.87 seconds.

Observed caveats:

- Homebrew does not currently provide a `vroid-studio` cask, so VRoid Studio was installed from the official VRoid download page.
- The `obs --version` shell wrapper can fail in the headless Codex terminal with a Qt CPU-feature message, but `/Applications/OBS.app` is installed as an Apple Silicon `arm64` app and launches as a GUI application.
- Ollama is installed, but local server access was not available during this setup pass, so LLM-driven interaction remains a later step.
- VCam webcam-only upper-body and hand tracking is limited by lighting, camera distance, and whether hands stay visible in frame.
- Higher VCam tracking FPS can improve smoothness, but if movement stutters under load, lower it from `45` toward `30` before changing other settings.
- Blender launches as a GUI app, but a headless CLI smoke test crashed in this environment; use the GUI for first VRM checks.

Next manual MVP step:

1. Use VCam first, with OBS closed, to judge whether body motion is now smoother.
2. Keep the face and shoulders centered in the MacBook camera and keep both hands inside the camera frame when testing hand tracking.
3. If motion still feels choppy, lower VCam `FPS (tracking)` from `45` to `30`; if it feels responsive but jittery, keep `45` and reduce shoulder/finger sensitivity slightly more.
4. Re-open OBS only after VCam motion feels natural enough for recording.
5. Open Blender only when model-level fixes are needed, such as clothing, hair, blendshape, or rig cleanup.

## High-freedom production path

For maximum character freedom, use this progression:

1. **Concept**: Generate or sketch a character sheet with front-facing style references.
2. **Base model**: Build the body and face in VRoid Studio or CharacterStudio.
3. **Custom details**: Edit hair, clothing, accessories, and textures in Blender.
4. **Expressions**: Add or tune blendshapes for smile, anger, surprise, wink, and mouth shapes.
5. **Performance**: Use VMD/MMD motions, manual posing, or motion capture.
6. **Brand kit**: Keep character colors, catchphrases, outfit rules, and visual guidelines in a local document.
7. **Output loop**: Record shorts, review, adjust model/voice/camera, and repeat.

This route takes longer than SaaS avatar generation, but it creates reusable assets and better long-term control.

## AI helper path

Use local AI as a helper, not the core system, until the VRM workflow is stable.

Good helper uses:

- Character concept art
- Outfit variations
- Background plates
- Thumbnails
- Caption cards
- Script drafts
- Voice line experiments

Avoid depending on AI video generation for the MVP because it can drift across frames, change the character identity, and become expensive in GPU time.

## Recommended first milestone

Build one reusable character and one repeatable 30-second recording flow.

Done when:

- One original VRM character exists.
- The character loads in a local stage app.
- At least three expressions work.
- One audio line drives mouth movement.
- OBS records a vertical 15-30 second clip.
- All assets have source and license notes.

## Cost and license checklist

Free software does not mean every output is risk-free.

Before publishing or monetizing, check:

- VRM base model terms
- Outfit and accessory terms
- Texture terms
- MMD/VMD motion terms
- TTS voice terms
- Background image terms
- Music terms
- Whether commercial use is allowed
- Whether attribution is required

Do not use real idol likenesses, real-person voice clones, or identifiable private-person references without rights.

## Practical recommendation

Use this sequence first:

1. **VRoid Studio** for the first character.
2. **OBS** for capture.
3. **Lobe Vidol or another VRM-compatible local stage** for motion and presentation.
4. **Blender + UniVRM** only when the base character needs advanced fixes.
5. **ComfyUI** later for concept art, thumbnails, and backgrounds.
6. **Open-LLM-VTuber** later for live AI interaction.

This gives the best balance of free tooling, high character freedom, repeatable output, and realistic setup effort.
