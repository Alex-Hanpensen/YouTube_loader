#!/bin/usr/env python3
"""
This script is required to upload video clips, playlist and captions to YouTube
"""

import argparse
from argparse import Namespace
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


if __name__ == '__main__':
    args = get_args()

