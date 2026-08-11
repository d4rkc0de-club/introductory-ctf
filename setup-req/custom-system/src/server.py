#!/usr/bin/env python3
import socket
import threading
import time
import re

HOST = "0.0.0.0"
PORT = 31337

FLAG = "d4rk{you_stopped_thinking_in_linux}c0de"

NODES = {
    "A7": {
        "type": "gateway", "state": "dormant",
        "links": ["B2", "C1"], "requires": []
    },
    "B2": {
        "type": "relay", "state": "dormant",
        "links": ["D9"], "requires": ["A7"]
    },
    "C1": {
        "type": "relay", "state": "dormant",
        "links": ["D9"], "requires": ["A7"]
    },
    "D9": {
        "type": "memory", "state": "sealed",
        "links": ["E4"], "requires": ["B2", "C1"]
    },
    "E4": {
        "type": "decoder", "state": "dormant",
        "links": [], "requires": ["D9"]
    },
}

MEMORY = bytes.fromhex("64 34 72 6b 7b 79 6f 75 5f 73 74 6f 70 70 65 64 5f 74 68 69 6e 6b 69 6e 67 5f 69 6e 5f 6c 69 6e 75 78 7d 63 30 64 65")
COMMANDS = {
    "scan", "observe", "wake", "trace", "enter", "read", "decode", "emit", "help", "status", "reset", "quit"
}

BANNER = """\
╔══════════════════════════════════════╗
║          NULL SYSTEM v0.3            ║
║          node: UNIDENTIFIED          ║
╚══════════════════════════════════════╝

awake.

The system is deterministic.
Every response contains information.
There are no false leads.

Type `help` if you need the interface.
"""

HELP = """\
known primitives:

  scan
  observe <entity>
  wake <entity>
  trace <entity>
  enter <entity>
  read <entity>
  decode <entity>
  emit <entity>
  status

Entities are identifiers such as A7, B2, C1...
"""

def send(conn, text):
    conn.sendall((text + "\n").encode())

def norm(s):
    return re.sub(r"[^a-z0-9_]+", "", s.lower())

class Session:
    def __init__(self):
        self.nodes = {k: dict(v) for k, v in NODES.items()}
        self.emitted = False

    def reset(self):
        self.nodes = {k: dict(v) for k, v in NODES.items()}
        self.emitted = False

    def node(self, raw):
        key = raw.upper()
        return self.nodes.get(key), key

    def handle(self, line):
        parts = line.strip().split()
        if not parts:
            return ""

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd not in COMMANDS:
            return "unknown primitive. Try `help`."

        if cmd == "help":
            return HELP
        if cmd == "quit":
            return "__QUIT__"
        if cmd == "reset":
            self.reset()
            return "system state reset."
        if cmd == "status":
            active = [k for k, v in self.nodes.items() if v["state"] == "active"]
            return "active: " + (", ".join(active) if active else "none")

        if cmd == "scan":
            return """\
A7  dormant
B2  dormant
C1  dormant
D9  sealed
E4  dormant
"""

        if not args:
            return f"{cmd} requires an entity."

        n, key = self.node(args[0])
        if n is None:
            return "entity not found."

        if cmd == "observe":
            links = " ".join(n["links"]) if n["links"] else "none"
            req = " ".join(n["requires"]) if n["requires"] else "none"
            return f"""\
entity: {key}
type: {n["type"]}
state: {n["state"]}
links: {links}
requires: {req}"""

        if cmd == "trace":
            if n["state"] == "dormant" or n["state"] == "sealed":
                return f"{key} is not active."
            return f"{key} -> " + (" -> ".join(n["links"]) if n["links"] else "end")

        if cmd == "wake":
            if n["state"] == "sealed":
                return f"{key} is sealed. It cannot be awakened."
            if n["state"] == "active":
                return f"{key} is already active."
            missing = [r for r in n["requires"] if self.nodes[r]["state"] != "active"]
            if missing:
                return f"cannot wake {key}. requires: " + " ".join(missing)
            n["state"] = "active"
            return f"{key} -> active"

        if cmd == "enter":
            missing = [r for r in n["requires"] if self.nodes[r]["state"] != "active"]
            if n["state"] not in ("active", "sealed"):
                return f"{key} is dormant."
            if missing:
                return f"{key} is inaccessible. requires: " + " ".join(missing)
            if key == "D9":
                return """\
SYSTEM MEMORY
=============
format: hexadecimal bytes
length: 40

64 34 72 6b 7b 79 6f 75 5f 73 74 6f 70 70 65 64
5f 74 68 69 6e 6b 69 6e 67 5f 69 6e 5f 6c 69 6e
75 78 7d 63 30 64 65

A decoder may be useful."""
            if key == "E4":
                return "decoder online. input source: D9"
            if key == "A7":
                return "gateway interior: links are B2 and C1."
            return f"entered {key}. nothing else is present."

        if cmd == "read":
            if key != "D9":
                return "no readable memory attached to this entity."
            if n["state"] != "active":
                return "memory is not active."
            return MEMORY.decode()

        if cmd == "decode":
            if key != "E4":
                return "no decoder attached to this entity."
            if self.nodes["D9"]["state"] != "active":
                return "decoder input unavailable."
            return "decoder accepts hexadecimal memory from D9."

        if cmd == "emit":
            if key != "E4":
                return "only the decoder can emit."
            missing = [r for r in n["requires"] if self.nodes[r]["state"] != "active"]
            if missing:
                return f"cannot emit. requires: " + " ".join(missing)
            self.emitted = True
            return f"OUTPUT: {FLAG}"

        return "no response."

def client(conn, addr):
    session = Session()
    conn.settimeout(300)
    try:
        send(conn, BANNER.rstrip())
        send(conn, ">")
        buf = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                raw, buf = buf.split(b"\n", 1)
                line = raw.decode("utf-8", "ignore").strip()
                if len(line) > 200:
                    send(conn, "input too long.")
                    send(conn, ">")
                    continue
                out = session.handle(line)
                if out == "__QUIT__":
                    send(conn, "connection closed.")
                    return
                if out:
                    for chunk in out.splitlines():
                        send(conn, chunk)
                send(conn, ">")
    except (ConnectionError, TimeoutError, socket.timeout):
        pass
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(32)
        print(f"NULL SYSTEM listening on {HOST}:{PORT}", flush=True)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
