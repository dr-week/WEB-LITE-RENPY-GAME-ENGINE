"""Unit tests for Google Flow CDP automation helpers."""

import json
import unittest
from unittest.mock import patch

from flow_automate import build_flow_batch_payload
from flow_automation.cdp import find_flow_target
from flow_automation.flow_dom import INSPECT_JS, build_set_prompt_js


class _FakeResp:
    def __init__(self, payload: list[dict]):
        self._data = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FlowAutomateTests(unittest.TestCase):
    def test_find_flow_target_matches_flow_tab(self):
        tabs = [
            {"type": "page", "url": "https://example.com", "webSocketDebuggerUrl": "ws://1"},
            {"type": "page", "url": "https://flow.google/project/123", "webSocketDebuggerUrl": "ws://2"},
        ]
        with patch("urllib.request.urlopen", return_value=_FakeResp(tabs)):
            hit = find_flow_target(9222)
        self.assertEqual(hit["webSocketDebuggerUrl"], "ws://2")

    def test_build_flow_batch_payload_and_js_helpers(self):
        text, n = build_flow_batch_payload(source="story", count=5, seed=7)
        self.assertEqual(n, 5)
        self.assertIn("Generate 5 16:9 images using the attached reference images", text)
        self.assertIn("[ASSET_ID:", text)
        self.assertNotIn("shameless", text.lower())
        js = build_set_prompt_js(text)
        self.assertIn("execCommand", js)
        self.assertIn("hasInput", INSPECT_JS)


if __name__ == "__main__":
    unittest.main()
