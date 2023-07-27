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
    parser.add_argument('--captions', '-c', help='Presence or absence of captions', default=None)

    return parser.parse_args()


class Loader:
    """
    YouTube download user argument controller

    Attributes:
        link (str): Link to YouTube video or playlist  | https://www.youtube.com/...
        path (str): Output path for saving video clips | Absolute or relative path
        resolution (str): Video clip quality           | '720p', '480p', '360p', '240p', '144p'
        captions (str): Captions for uploading video   | 'en', 'ru', 'esp' etc

    Methods:
        load(self) -> None: Download a video(s) from the specified URL
    """

    __slots__ = '__link', '__path', '__resolution', '__captions'

    def __init__(self, link, path='.', resolution='720p', captions=None):
        self.__link = link
        self.__path = path
        self.__resolution = resolution
        self.__captions = captions

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        self.__link = value

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, value):
        if value in ('720p', '480p', '360p', '240p', '144p'):
            self.__resolution = value

    def load(self) -> None:
        video = YouTube(self.__link).streams.filter(resolution=self.__resolution, )
        video.first().download(self.__path)
        print('Your video has been successfully uploaded!')

    def __is_playlist(self) -> bool:
        ...

    def __is_video(self) -> bool:
        ...


if __name__ == '__main__':
    args = get_args()
    loader = Loader(args.link, args.path, args.resolution, args.captions)
    loader.load()
