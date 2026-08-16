"""Tests for the publisher's custom phrase."""

import unittest

from nasser_ros2_tasks.phrase_content import PROJECT_MESSAGE


class PhraseContentTests(unittest.TestCase):
    def test_phrase_is_not_hello_world(self) -> None:
        self.assertNotEqual(PROJECT_MESSAGE.casefold().strip(), "hello world")

    def test_phrase_contains_student_name(self) -> None:
        self.assertIn("Nasser Mamdouh Alshareef", PROJECT_MESSAGE)


if __name__ == "__main__":
    unittest.main()

