"""Minimal Python stdlib Chrome DevTools Protocol (CDP) client."""

import base64
import hashlib
import json
import os
import socket
import struct
import urllib.parse
import urllib.request


def find_flow_target(port: int = 9222) -> dict | None:
    """Return the first open Chrome tab matching flow.google or labs.google."""
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3) as resp:
        targets = json.loads(resp.read().decode("utf-8"))
    for target in targets:
        url = target.get("url", "")
        if target.get("type") == "page" and ("flow.google" in url or "labs.google" in url):
            return target
    return None


class CdpSession:
    """Lightweight RFC 6455 WebSocket client for Chrome CDP."""

    def __init__(self, ws_url: str):
        parsed = urllib.parse.urlparse(ws_url)
        self.sock = socket.create_connection((parsed.hostname or "127.0.0.1", parsed.port or 9222), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        req = f"GET {path} HTTP/1.1\r\nHost: {parsed.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        self.sock.sendall(req.encode("ascii"))
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        if accept.encode() not in buf:
            raise RuntimeError("CDP WebSocket handshake failed")
        self._msg_id = 0

    def close(self):
        self.sock.close()

    def _send_text(self, payload: str):
        data = payload.encode("utf-8")
        mask = os.urandom(4)
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.extend([0x80 | 126, *struct.pack("!H", n)])
        else:
            header.extend([0x80 | 127, *struct.pack("!Q", n)])
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(bytes(header) + mask + masked)

    def _recv_exact(self, n: int) -> bytes:
        out = bytearray()
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise ConnectionError("CDP socket closed")
            out.extend(chunk)
        return bytes(out)

    def _recv_text(self) -> str:
        while True:
            b1, b2 = self._recv_exact(2)
            opcode = b1 & 0x0F
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            if b2 & 0x80:
                self._recv_exact(4)
            payload = self._recv_exact(length)
            if opcode == 0x8:
                raise ConnectionError("CDP closed")
            if opcode in (0x1, 0x0):
                return payload.decode("utf-8")

    def call(self, method: str, params: dict | None = None) -> dict:
        self._msg_id += 1
        cid = self._msg_id
        self._send_text(json.dumps({"id": cid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self._recv_text())
            if msg.get("id") == cid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def eval_js(self, expression: str):
        res = self.call("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
        return res.get("result", {}).get("value")
