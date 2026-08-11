# NULL//SYSTEM — Organizer Writeup

## Intended insight

The player should abandon the Linux-shell mental model.

`scan` does not list files. It lists entities with states.

`observe` reveals:
- type
- state
- links
- prerequisites

The system therefore behaves like a deterministic graph/state machine.

## Solution

```text
scan

observe A7
wake A7

observe B2
observe C1

wake B2
wake C1

observe D9
wake D9
enter D9
```

D9 exposes hexadecimal bytes. Decode them as ASCII:

```text
64 34 72 6b 7b 79 6f 75 5f 73 74 6f 70 70 65 64
5f 74 68 69 6e 6b 69 6e 67 5f 69 6e 5f 6c 69 6e
75 78 7d 63 30 64 65
```

This yields:

```text
d4rk{you_stopped_thinking_in_linux}c0de
```

Then activate the decoder:

```text
observe E4
wake E4
enter E4
emit E4
```

The server emits the same flag.

## Why the second path exists

The hex is the recognition step. E4 exists to make the final action require understanding the state machine rather than simply submitting decoded text immediately. Both paths converge on the same static CTFd flag.

## Difficulty tuning

For easier:
- expose `help` in the banner
- make `observe` available without prerequisites
- make hints free

For harder:
- remove `help` from the banner
- require the player to discover `observe`
- hide the manual until they request it
- make `trace` necessary to discover the B2/C1 branch

Do not add fake commands or misleading entities; the challenge's intended skill is inference, not guessing.
