#!/bin/usr/env python3
"""
This script is required to upload video clips, playlist and captions to YouTube
"""

import argparse
from argparse import Namespace
import re
import os
from pytube import YouTube, Playlist


def get_args() -> Namespace:
    """
    Argument parser
    :return: Namespace
    """
    parser = argparse.ArgumentParser('youtube_loader')
    parser.add_argument('--link', '-l', help='Link to the video', required=True)
    parser.add_argument('--path', '-p', help='The way to save the video', default='.')
    parser.add_argument('--resolution', '-r', help='Video quality', default='720p')
    return parser.parse_args()


class Loader:
    """
    YouTube download user argument controller

    Attributes:
        link (str): Link to YouTube video or playlist  | https://www.youtube.com/...
        path (str): Output path for saving video clips | Absolute or relative path
        resolution (str): Video clip quality           | '720p', '480p', '360p', '240p', '144p'

    Methods:
        load(self) -> None: Download a video(s) from the specified URL
    """

    __slots__ = '__link', '__path', '__resolution'

    def __init__(self, link, path='.', resolution='720p'):
        self.link = link
        self.path = path
        self.resolution = resolution

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, url_link: str) -> None:
        if self.__is_video(url_link) or self.__is_playlist(url_link):
            self.__link = url_link
        else:
            print('Incorrect link to a youtube video!')
            exit()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        if not os.path.isdir(path):
            print('Unable to access the specified directory!')
            exit()
        else:
            self.__path = path

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, value):
        if value in ('720p', '480p', '360p', '240p', '144p'):
            self.__resolution = value

    def _download_playlist(self) -> None:
        playlist = Playlist(self.__link)
        for url_link in playlist.video_urls:
            self._download_video(url_link)

    def _download_video(self, url_link: str) -> None:
        video = YouTube(url_link).streams.filter(resolution=self.__resolution)
        video.first().download(self.__path)
        print('Your video has been successfully uploaded!')

    def load(self) -> None:
        if self.__is_playlist(self.__link):
            self._download_playlist()
        elif self.__is_video(self.__link):
            self._download_video(self.__link)

    @staticmethod
    def __is_playlist(link: str) -> bool | None:
        return re.search(r'https?://(www.)?youtube\.com/playlist\?list=\w+', link)

    @staticmethod
    def __is_video(link: str) -> bool | None:
        return re.search(r'https?://(www.)?youtube\.com/watch\?v=\w+(?:$|&list=\w+&index=\d)', link)


if __name__ == '__main__':
    args = get_args()
    loader = Loader(args.link, args.path, args.resolution)
    loader.load()
