"""Regression checks for the tracker and its security-sensitive helpers."""

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import parcel_tracker as tracker


class ParcelTrackerTests(unittest.TestCase):
    """Check behavior that the static analysis tools cannot establish."""

    def setUp(self):
        tracker.PARCELS.clear()

    def test_booking_history_and_status_boundary(self):
        history = []
        first = tracker.book_parcel("A", "B", 2.5, history)
        second = tracker.book_parcel("C", "D", 1)
        self.assertEqual(history, [first])
        self.assertNotEqual(first, second)
        self.assertEqual(tracker.book_parcel.__defaults__, (None,))
        self.assertFalse(tracker.is_with_courier(first))
        self.assertEqual(tracker.advance_status(first), "Picked Up")
        self.assertTrue(tracker.is_with_courier(first))
        self.assertEqual(tracker.advance_status(first), "In Transit")
        self.assertTrue(tracker.is_with_courier(first))
        for _ in range(10):
            final = tracker.advance_status(first)
        self.assertEqual(final, "Delivered")
        self.assertFalse(tracker.is_with_courier(first))

    def test_pricing_and_unknown_id(self):
        for weight, expected in ((0.8, 50), (1, 50), (2.5, 95), (4, 140)):
            self.assertEqual(tracker.shipping_cost(weight), expected)
        self.assertEqual(
            tracker.track_parcel("TRK00000"), "Unknown tracking id TRK00000"
        )
        with self.assertRaises(TypeError):
            tracker.track_parcel([])

    def test_label_files_exist_and_have_distinct_names(self):
        paths = []
        try:
            paths.extend([tracker.label_path(), tracker.label_path()])
            self.assertNotEqual(*paths)
            for path in paths:
                self.assertTrue(Path(path).is_file())
                Path(path).write_text("label", encoding="utf-8")
                self.assertEqual(Path(path).read_text(), "label")
        finally:
            for path in paths:
                Path(path).unlink(missing_ok=True)

    def test_malicious_hub_addresses_never_start_a_process(self):
        for address in (
            "127.0.0.1; echo injected", "127.0.0.1 & whoami",
            "-n 99", "$(whoami)", "example.com", "", "999.0.0.1",
        ):
            with self.subTest(address=address):
                with patch.object(tracker.subprocess, "check_output") as run:
                    with self.assertRaises(ValueError):
                        tracker.ping_hub(address)
                    run.assert_not_called()

    def test_ping_uses_resolved_path_argument_list_and_no_shell(self):
        for platform, option in (("nt", "-n"), ("posix", "-c")):
            for address in ("127.0.0.1", "::1"):
                with self.subTest(platform=platform, address=address):
                    with patch.object(tracker.os, "name", platform):
                        with patch.object(
                            tracker.shutil, "which", return_value="/safe/ping"
                        ):
                            with patch.object(
                                tracker.subprocess, "check_output",
                                return_value=b"reply",
                            ) as run:
                                self.assertEqual(
                                    tracker.ping_hub(address), b"reply"
                                )
                                run.assert_called_once_with(
                                    ["/safe/ping", option, "1", address],
                                    shell=False, timeout=10,
                                )

    def test_ping_missing_utility_and_timeout_are_visible(self):
        with patch.object(tracker.shutil, "which", return_value=None):
            with self.assertRaises(FileNotFoundError):
                tracker.ping_hub("127.0.0.1")
        with patch.object(tracker.shutil, "which", return_value="/safe/ping"):
            with patch.object(
                tracker.subprocess, "check_output",
                side_effect=subprocess.TimeoutExpired("ping", 10),
            ):
                with self.assertRaises(subprocess.TimeoutExpired):
                    tracker.ping_hub("127.0.0.1")

    def test_demo_matches_original_except_random_otp(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            tracker.main()
        before = Path("reports/before/demo_output.txt").read_text()
        without_otp = lambda text: [
            line for line in text.splitlines()
            if not line.startswith("Delivery OTP for")
        ]
        self.assertEqual(without_otp(output.getvalue()), without_otp(before))
        for random_value in (0, 8999):
            tracker.PARCELS.clear()
            output = io.StringIO()
            with patch.object(
                tracker.secrets, "randbelow", return_value=random_value
            ) as secure_random:
                with contextlib.redirect_stdout(output):
                    tracker.main()
                secure_random.assert_called_once_with(9000)
                self.assertIn(
                    f" is {1000 + random_value}\n", output.getvalue()
                )

    def test_import_does_not_run_demo(self):
        spec = importlib.util.spec_from_file_location(
            "tracker_import_check", "parcel_tracker.py"
        )
        module = importlib.util.module_from_spec(spec)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            spec.loader.exec_module(module)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(module.PARCELS, {})


if __name__ == "__main__":
    unittest.main()
