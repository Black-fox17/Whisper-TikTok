import os
import subprocess

from utils import KeepDir


def download_video(url: str, folder: str = 'background'):
    """
    Downloads a video from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the video to download.
        folder (str, optional): The name of the folder to save the video in. Defaults to 'background'.
    """
    directory = os.getcwd() / folder
    if not directory.exists():
        directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        with subprocess.Popen(['yt-dlp', '-f bestvideo[ext=mp4]+bestaudio[ext=m4a]', '--restrict-filenames', url]) as process:
            pass
    return
