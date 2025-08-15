import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from agent_registry import AgentRegistry
from multi_agent import TaskDelegator


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))
        result = data.get("task", "")[::-1]
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())

    def log_message(self, format, *args):
        # Suppress default logging to keep test output clean
        pass


@pytest.fixture
def server():
    httpd = HTTPServer(("localhost", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        yield f"http://localhost:{httpd.server_port}"
    finally:
        httpd.shutdown()
        thread.join()


def test_remote_agent_delegation(tmp_path, server):
    cfg = tmp_path / "agents.json"
    cfg.write_text(json.dumps({"reverse": server}))
    reg = AgentRegistry()
    reg.load_config(str(cfg))
    delegator = TaskDelegator(reg)
    assert delegator.delegate("reverse", "abc") == "cba"
