
import unittest
from unittest.mock import patch
import subprocess

import app


class CommandInjectionTests(unittest.TestCase):

    def test_vulnerable_path_uses_shell(self):
        payload = "127.0.0.1 & echo INJECTION_PROOF"

        fake_result = subprocess.CompletedProcess(
            args="mock command",
            returncode=0,
            stdout="INJECTION_PROOF",
            stderr=""
        )

        with patch(
            "app.subprocess.run",
            return_value=fake_result
        ) as mocked_run:
            output = app.run_diagnostic(payload, "vulnerable")

        self.assertIn("INJECTION_PROOF", output)
        self.assertTrue(mocked_run.call_args.kwargs["shell"])

    def test_secure_path_rejects_injection_input(self):
        payload = "127.0.0.1 & echo INJECTION_PROOF"

        with patch("app.subprocess.run") as mocked_run:
            output = app.run_diagnostic(payload, "secure")

        self.assertIn("BLOCKED", output)
        mocked_run.assert_not_called()

    def test_secure_path_uses_argument_list(self):
        fake_result = subprocess.CompletedProcess(
            args=["ping"],
            returncode=0,
            stdout="Mock ping output",
            stderr=""
        )

        with patch(
            "app.subprocess.run",
            return_value=fake_result
        ) as mocked_run:
            output = app.run_diagnostic("127.0.0.1", "secure")

        self.assertIn("SECURED MODE", output)
        args, kwargs = mocked_run.call_args

        self.assertIsInstance(args[0], list)
        self.assertFalse(kwargs["shell"])


if __name__ == "__main__":
    unittest.main()
