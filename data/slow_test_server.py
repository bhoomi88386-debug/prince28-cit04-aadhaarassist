import contextlib
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FILE_DATA = b"A" * (2 * 1024 * 1024)
INTERRUPTED_ONCE = False


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global INTERRUPTED_ONCE

        if self.path == "/robots.txt":
            body = b"User-agent: *\nAllow: /\n"
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path != "/slow.pdf":
            self.send_error(404)
            return

        range_header = self.headers.get("Range")

        if range_header:
            try:
                start = int(range_header.replace("bytes=", "").split("-")[0])
            except ValueError:
                self.send_error(400)
                return

            if start < 0 or start >= len(FILE_DATA):
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{len(FILE_DATA)}")
                self.end_headers()
                return

            remaining = FILE_DATA[start:]

            self.send_response(206)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(remaining)))
            self.send_header(
                "Content-Range", f"bytes {start}-{len(FILE_DATA) - 1}/{len(FILE_DATA)}"
            )
            self.end_headers()
            self.wfile.write(remaining)
            print(f"RESUME: sent bytes starting at {start}")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Length", str(len(FILE_DATA)))
        self.end_headers()

        if not INTERRUPTED_ONCE:
            INTERRUPTED_ONCE = True
            half = len(FILE_DATA) // 2
            self.wfile.write(FILE_DATA[:half])
            self.wfile.flush()
            print(f"INTERRUPTED: sent first {half} bytes")

            with contextlib.suppress(OSError):
                self.connection.shutdown(socket.SHUT_RDWR)

            self.connection.close()
            return

        self.wfile.write(FILE_DATA)

    def log_message(self, format, *args):
        print(format % args)


print("Range test server running at http://127.0.0.1:8765")
ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
