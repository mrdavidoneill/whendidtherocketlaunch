"""
Module containing unit tests for the chatbot application's sanity check.

This module provides a test case for ensuring that the chatbot application runs
without errors and does not exit prematurely. The test case spawns a separate
process to run the application and waits for a fixed amount of time to ensure
that the application is still running after the expected duration.

Classes:
    SanityCheck: A unit test case for the chatbot application's sanity check.

Methods:
    test_run: A test method that spawns a subprocess to run the chatbot
        application and checks that it continues to run after a fixed duration.

    tearDown: A method that cleans up the spawned subprocess after the test has
        completed.
"""

import unittest
import subprocess
import time

RUNTIME_SECONDS_SANITY_CHECK = 10


class TestSanity(unittest.TestCase):
    """
    A unittest.TestCase class to test the functionality of the chatbot.

    """

    def setUp(self):
        """
        The setUp method initializes the process attribute to None.
        This method is called before every test method is executed.
        """
        self.process = None

    def test_run(self):
        """
        Test that the chatbot runs for at least 10 seconds without exiting.

        Uses subprocess.Popen to run the chatbot in a separate process and
        checks that the process has not exited for at least 10 seconds using
        time.monotonic().

        """
        self.process = subprocess.Popen(
            ["bash", "-c", "source env/bin/activate && python chatbot/run.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        start_time = time.monotonic()
        exit_code = self.process.poll()
        print(f"Waiting {RUNTIME_SECONDS_SANITY_CHECK} seconds...")
        while (
            time.monotonic() < start_time + RUNTIME_SECONDS_SANITY_CHECK
            or exit_code is not None
        ):
            exit_code = self.process.poll()

        self.assertEqual(exit_code, None, msg="Process has not exited")

    def tearDown(self):
        """
        Clean up the subprocess and its resources after the test is finished.

        Closes the stdout and stderr file handles, terminates the process, and waits for it to exit.

        """
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.terminate()
        self.process.wait()


if __name__ == "__main__":
    unittest.main()
