"""
Provides classes for working with a video API.

It contains the following classes:

Video: a named tuple representing a video in the API.
FrameX: a utility class that provides access to the FrameX API.
FrameXBisector: a class that helps manage the display of images from a video launch.
"""

import os

from typing import List, NamedTuple, Text
from urllib.parse import quote, urljoin

import requests

API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/")
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)


class Video(NamedTuple):
    """
    Represents a video from the API.

    Attributes:
        name (str): The name of the video.
        width (int): The width of the video in pixels.
        height (int): The height of the video in pixels.
        frames (int): The total number of frames in the video.
        frame_rate (List[int]): A list of integers representing the frames per second (fps).
        url (str): The URL of the video.
        first_frame (str): The filename or path of the first frame of the video.
        last_frame (str): The filename or path of the last frame of the video.
    """

    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text


class FrameX:
    """
    A utility class that provides access to the FrameX API.

    Public Methods:
    ---------------
    video(video: Text) -> Video:
        Fetches information about the specified video.
    video_frame(video: Text, frame: int) -> bytes:
        Fetches the JPEG data of the specified frame from the specified video.

    Public Instance Variables:
    --------------------------
    api_base: str
        The base URL for the FrameX API.
    session: requests.Session
        The session used for HTTP requests.
    """

    def __init__(self, api_base: str = API_BASE):
        """
        Initializes a new instance of the `FrameX` class.

        Parameters:
        -----------
        api_base: str
            The base URL for the FrameX API.
        """
        self.api_base = api_base
        self.session = requests.Session()
        self.session.timeout = 30

    def __del__(self):
        """
        Close the HTTP session when the FrameX instance is garbage collected
        """
        self.session.close()

    def video(self, video: Text) -> Video:
        """
        Fetches information about the specified video.

        Parameters:
        -----------
        video: Text
            The name of the video to fetch information about.

        Returns:
        --------
        Video:
            A `Video` object containing information about the specified video.

        Raises:
        -------
        requests.exceptions.HTTPError:
            If the server returns an error response.
        """
        response = self.session.get(urljoin(self.api_base, f"video/{quote(video)}/"))
        response.raise_for_status()
        return Video(**response.json())

    def video_frame(self, video: Text, frame: int) -> bytes:
        """
        Fetches the JPEG data of the specified frame from the specified video.

        Parameters:
        -----------
        video: Text
            The name of the video to fetch the frame from.
        frame: int
            The index of the frame to fetch.

        Returns:
        --------
        bytes:
            The JPEG data of the specified frame.

        Raises:
        -------
        requests.exceptions.HTTPError:
            If the server returns an error response.
        """

        response = self.session.get(
            urljoin(self.api_base, f'video/{quote(video)}/frame/{quote(f"{frame}")}/')
        )
        response.raise_for_status()
        return response.content


class FrameXBisector:
    """
    A class that helps manage the display of images from a video launch.

    Public Methods:
    ---------------
    go_to_mid()
        Move the current index to the midpoint of the current range.
    process_input(current_has_taken_off: bool)
        Update the range based on the input boolean value.
    reset()
        Reset all attributes to their default values.

    Public Instance Variables:
    --------------------------
    index: int
        The current frame index.
    count: int
        The total number of frames in the video.
    is_finished: bool
        Indicates whether the bisecting process is finished.
    """

    def __init__(self, api_base: str = API_BASE, video_name: str = VIDEO_NAME):
        """
        Initializes a new instance of the FrameXBisector class.

        Parameters:
        -----------
        api_base: str
            The base URL of the FrameX API.
        video_name: str
            The name of the video to retrieve frames from.
        """
        self.api = FrameX(api_base)
        self.video = self.api.video(video_name)
        self._index = 0
        self.image = None
        self.left = 0
        self.right = self.count - 1

    @property
    def index(self):
        """
        Gets the current frame index.

        Returns:
        --------
        int:
            The current frame index.
        """
        return self._index

    @index.setter
    def index(self, value):
        """
        Sets the current frame index and downloads the new frame.

        Parameters:
        -----------
        value: int
            The new frame index.
        """

        self._index = value
        self.image = self.api.video_frame(self.video.name, value)

    @property
    def count(self):
        """
        Gets the total number of frames in the video.

        Returns:
        --------
        int:
            The total number of frames in the video.
        """
        return self.video.frames

    def go_to_mid(self):
        """
        Moves the current index to the midpoint of the current range.
        """
        self.index = (self.left + self.right) // 2

    @property
    def is_finished(self):
        """
        Indicates whether the bisecting process is finished.

        Returns:
        --------
        bool:
            True if the left and right bounds are equal, False otherwise.
        """
        return self.left == self.right

    def process_input(self, current_has_taken_off: bool):
        """
        Updates the range based on the input boolean value.

        Parameters:
        -----------
        current_has_taken_off: bool
            Indicates whether the current image shows the rocket taking off or not.
        """
        if current_has_taken_off:
            self.right = self.index
        else:
            self.left = min(self.index + 1, self.right)

    def reset(self):
        """
        Resets all attributes to their default values.
        """
        self._index = 0
        self.image = None
        self.left = 0
        self.right = self.count - 1


# Examples of search:

# NNN
# Initial state: {L: 0, R: 2}
# Search progresses as follows:
# Index: 1, has_taken_off: False, updated state: {L: 2, R: 2}
# Index: 0, has_taken_off: False, updated state: {L: 0, R: 1}
# Final state: {L: 0, R: 1}

# NNY
# Initial state: {L: 0, R: 2}
# Search progresses as follows:
# Index: 1, has_taken_off: False, updated state: {L: 2, R: 2}
# Index: 2, has_taken_off: True, updated state: {L: 1, R: 1}
# Final state: {L: 1, R: 1}
