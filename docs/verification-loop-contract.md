# Verification Loop Contract

This contract turns failures into evidence and repeatable fixes.

## Goal

Every significant failure should produce enough information for the next Codex run or human reviewer to reproduce, fix, and prevent it.

## Minimum loop

1. Capture the failing command or user flow.
2. Save the relevant log, screenshot, artifact, or error excerpt.
3. Identify the smallest suspected cause.
4. Propose a focused fix.
5. Add or name a regression check.
6. Re-run the same command or flow.
7. Record what changed and what remains unverified.

## Use cases

- failed CI check
- failing test or lint command
- flaky browser or emulator QA
- build failure after dependency or platform update
- runtime error in auth, payment, admin, or data flow
- repeated design or copy QA finding

## Env surface

- `CODEX_VERIFICATION_LOOP_MODE=contract|local`

`contract` means the loop is documented and used by agents. `local` means an approved local harness or external tool may assist, but normal validation must still pass without it.

## Output shape

A verification-loop report should include:

- failure summary
- reproduction command
- evidence path or excerpt
- suspected cause
- smallest fix candidate
- regression test candidate
- validation result
- follow-up risk

## Boundaries

- Do not hide failing validation.
- Do not retry blindly without adding evidence or a new hypothesis.
- Do not call a failure fixed until the same failing command or flow passes or a blocker is documented.
- Do not install external harness tools without approval.
