# NULL//SYSTEM

A beginner/intermediate intuition challenge for d4rkc0de.

The participant connects to a custom TCP interpreter and must infer a deterministic state machine. It deliberately resembles neither a Linux shell nor a conventional filesystem.

## Run

```bash
docker compose up --build
nc localhost 31337
```

Manual:

```bash
cd manual
python3 -m http.server 8080
```

## Intended solve

1. `help`
2. `scan`
3. `observe A7`
4. `wake A7`
5. `observe A7`
6. `trace A7`
7. Follow B2 and C1.
8. Wake B2 and C1.
9. Observe D9.
10. Wake D9.
11. `enter D9`
12. Recognize the hexadecimal bytes.
13. `read D9` gives the decoded text.
14. Observe/wake E4.
15. `enter E4`
16. `emit E4`
17. Submit the output as the flag.

The exact final flag is:

`d4rk{you_stopped_thinking_in_linux}c0de`

## Design rule

There are no fake clues or intentional dead ends. Every response gives information that can be used to build the correct mental model.

## CTFd

The included `challenge.yml` follows the standard ctfcli challenge structure documented by CTFd.
