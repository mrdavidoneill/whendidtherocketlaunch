"""
Unit tests for video and related functionality.
"""

import unittest
from unittest.mock import Mock, patch

from video.bisector import FrameXBisector


class TestFrameXBisector(unittest.TestCase):
    """
    Unit tests for the FrameXBisector class.
    """

    @patch("video.bisector.FrameX")
    def setUp(self, mock_FrameX):
        """
        Set up a mock FrameX object that returns a mock Video object and
        create a FrameXBisector object.

        Args:
            mock_FrameX (MagicMock): A mock FrameX object.
        """
        # Create a mock FrameX object that returns a mock Video object
        self.mock_video = Mock(name="Video")
        self.mock_video.name = "mock_video"
        self.mock_video.frames = 10
        self.mock_video.url = "https://example.com/api/video/mock_video/"
        mock_FrameX.return_value.video.return_value = self.mock_video
        mock_FrameX.return_value.video_frame.return_value = b"mock JPEG data"

        # Create a FrameXBisector object
        self.bisector = FrameXBisector()

    def test_count(self):
        """
        Tests that the count attribute of the FrameXBisector object is
        equal to the number of frames in the video.
        """
        self.assertEqual(self.bisector.count, self.mock_video.frames)

    def test_index(self):
        """
        Tests that the index attribute of the FrameXBisector object can be set and
        retrieved correctly.
        """
        self.bisector.index = 50
        self.assertEqual(self.bisector.index, 50)

    def test_go_to_mid(self):
        """
        Tests that the bisector can move to the midpoint of the current range correctly,
        for both even and odd numbers of frames.
        """
        # Test when even elements
        self.bisector.left = 0
        self.bisector.right = 10
        self.bisector.go_to_mid()
        self.assertEqual(self.bisector.index, 5)
        # Test when odd elements
        self.bisector.left = 0
        self.bisector.right = 3
        self.bisector.go_to_mid()
        self.assertEqual(self.bisector.index, 1)

    def test_is_finished(self):
        """
        Tests that the is_finished() method of the FrameXBisector object returns True
        when the bisector has found the frame where the event occurs, and False otherwise.
        """
        # Test when left equals right
        self.bisector.left = 5
        self.bisector.right = 5
        self.assertTrue(self.bisector.is_finished)

        # Test when left is less than right
        self.bisector.left = 2
        self.bisector.right = 3
        self.assertFalse(self.bisector.is_finished)

    def test_process_input(self):
        """
        Test the process_input() method of the FrameXBisector object.
        """
        # Test when current_has_taken_off is True
        self.bisector.index = 5
        self.bisector.left = 2
        self.bisector.right = 8
        self.bisector.process_input(True)
        self.assertEqual(self.bisector.right, 5)

        # Test when current_has_taken_off is False
        self.bisector.index = 5
        self.bisector.left = 2
        self.bisector.right = 8
        self.bisector.process_input(False)
        self.assertEqual(self.bisector.left, 6)

    def test_binary_search(self):
        """
        Test the binary_search() functionality of FrameXBisector.

        Tests the functionality by searching for the frame with "takeoff" using a mock API response.
        The method replaces the real API methods with mock ones and simulates user input based on
        the contents of the frame's image. The test checks that the method correctly identifies the
        frame with the takeoff and that it takes less than log n tries to do so.
        """
        test_cases = [
            {"frames": frames, "takeoff_index": index}
            for frames in range(1, 10)
            for index in range(frames)
        ]

        for test_case in test_cases:
            # Define a mock API response
            def mock_video_frame(_video_name: str, frame_number: int) -> bytes:
                if frame_number < test_case["takeoff_index"]:
                    return b"mock JPEG data"
                return b"mock JPEG data with takeoff"

            # Replace the real API methods with the mock ones
            self.bisector.api.video_frame = mock_video_frame
            self.mock_video.frames = test_case["frames"] + 1
            self.bisector.reset()

            # Search for the frame with the takeoff
            print(
                f"\nTEST: index {test_case['takeoff_index']} in {test_case['frames']} frames"
            )
            tries = 0
            while not self.bisector.is_finished:
                tries += 1
                self.bisector.go_to_mid()
                print(
                    f"Testing:{self.bisector.index} L:{self.bisector.left} R:{self.bisector.right}"
                )
                has_taken_off = b"takeoff" in self.bisector.image
                print(f"User input: {has_taken_off}")
                self.bisector.process_input(has_taken_off)
                print(f"Now: L: {self.bisector.left} R: {self.bisector.right}")
            self.bisector.go_to_mid()

            # Check that the correct frame was found
            self.assertEqual(self.bisector.index, test_case["takeoff_index"])

            # Check that it took less than log n tries:
            self.assertLessEqual(tries, self.bisector.count // 2 + 1)


if __name__ == "__main__":
    unittest.main()
