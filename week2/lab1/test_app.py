from pathlib import Path
import unittest


class TracedClaudeClientTest(unittest.TestCase):
    def test_app_uses_the_client_instrumented_by_langsmith(self):
        app_source = Path(__file__).with_name("app.py").read_text()

        self.assertIn(
            "async with ClaudeSDKClient(options=options) as client:", app_source
        )
        self.assertIn("await client.query(\"tell me a joke\")", app_source)
        self.assertIn("async for message in client.receive_response():", app_source)

    def test_app_prints_text_deltas_as_they_arrive(self):
        app_source = Path(__file__).with_name("app.py").read_text()

        self.assertIn("include_partial_messages=True", app_source)
        self.assertIn("if isinstance(message, StreamEvent):", app_source)
        self.assertIn("if event.get(\"type\") == \"content_block_delta\":", app_source)
        self.assertIn("print(text, end=\"\", flush=True)", app_source)


if __name__ == "__main__":
    unittest.main()
