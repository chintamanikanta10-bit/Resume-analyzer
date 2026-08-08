import os
import tempfile
import unittest
from pathlib import Path

from utils.file_utils import sanitize_filename, validate_upload_bytes
from core.auth import create_token, decode_token


class SecurityHardeningTests(unittest.TestCase):
    def test_sanitize_filename_blocks_path_traversal(self):
        name = sanitize_filename("../../evil.pdf")
        self.assertTrue(name.endswith(".pdf"))
        self.assertNotIn("..", name)
        self.assertNotIn("/", name)
        self.assertNotIn("\\", name)

    def test_validate_upload_bytes_rejects_non_pdf(self):
        with self.assertRaises(ValueError):
            validate_upload_bytes(b"not a pdf", "evil.txt", max_size_bytes=10_000)

    def test_validate_upload_bytes_rejects_oversized_file(self):
        payload = b"%PDF-1.4\n" + b"A" * 10_000
        with self.assertRaises(ValueError):
            validate_upload_bytes(payload, "large.pdf", max_size_bytes=1_000)

    def test_jwt_round_trip(self):
        token = create_token(subject="user-42", expires_minutes=5)
        payload = decode_token(token)
        self.assertEqual(payload["sub"], "user-42")


if __name__ == "__main__":
    unittest.main()
