from src.args_parser import parse_args
from src.video_downloader import download_video as download_video_async
from src.tts_converter import convert_to_tts
from src.subtitle_creator import create_srt
from src.video_preparer import prepare_video_background
from src.tiktok_uploader import tiktok_upload

import platform
import requests
import json
import os
from pathlib import Path
import random
import re
import json
import sys
import subprocess
import asyncio
import multiprocessing
import logging
from typing import Tuple
import datetime
import argparse

# PyTorch
import torch

# ENV
from dotenv import load_dotenv, find_dotenv

# OpenAI Whisper Model PyTorch
import whisper

from src.image_generator import generate_image
from src.voice_generator import generate_voice
# MicrosoftEdge TTS
import edge_tts

# FFMPEG (Python)
import ffmpeg

# TikTok Uploader
from tiktok_uploader.upload import upload_video


# utils.py
from utils import *

# msg.py
import msg

# Default directory
HOME = Path.cwd()

# Logging
log_directory = HOME / 'log'
if not log_directory.exists():
    log_directory.mkdir()

with KeepDir() as keep_dir:
    keep_dir.chdir(log_directory)
    log_filename = f'{datetime.date.today()}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
        ]
    )
    logger = logging.getLogger(__name__)


###########################
#        VIDEO.JSON       #
###########################

video_json_path = HOME / 'video.json'
jsonData = json.loads(video_json_path.read_text(encoding='utf-8'))


#######################
#         CODE        #
#######################


async def main() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"], type=str)
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--url", metavar='U', default="https://www.youtube.com/watch?v=intRX7BRA90",
                        help="Youtube URL to download as background video.", type=str)
    parser.add_argument("--tts", default="en-US-ChristopherNeural",
                        help="Voice to use for TTS", type=str)
    parser.add_argument(
        "--list-voices", help="Use `edge-tts --list-voices` to list all voices", action='help')
    parser.add_argument("--random_voice", action='store_true',
                        help="Random voice for TTS", default=False)
    parser.add_argument("--gender", choices=["Male", "Female"],
                        help="Gender of the random TTS voice", type=str)
    parser.add_argument(
        "--language", help="Language of the random TTS voice for example: en-US", type=str)
    parser.add_argument("--sub_format",
                        help="Subtitle format", choices=["u", "i", "b"], default="b", type=str)
    parser.add_argument("--font_color", help="Subtitle font color in hex format: #FFFFFF",
                        default="#FFFFFF", type=str)
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Verbose")
    args = parser.parse_args()

    if args.random_voice:  # Random voice
        args.tts = None
        if not args.gender:
            console.log(
                f"{msg.ERROR}When using --random_voice, please specify both --gender and --language arguments.")
            sys.exit(1)

        elif not args.language:
            console.log(
                f"{msg.ERROR}When using --random_voice, please specify both --gender and --language arguments.")
            sys.exit(1)

        elif args.gender and args.language:
            # Check if voice is valid
            voices = await edge_tts.VoicesManager.create()
            voices = voices.find(Gender=args.gender, Locale=args.language)
            if len(voices) == 0:
                # Voice not found
                console.log(
                    f"{msg.ERROR}Specified TTS language not found. Make sure you are using the correct format. For example: en-US")
                sys.exit(1)

            args.tts = voices['Name']

            # Check if language is english
            if not str(args.language).startswith('en'):
                args.non_english = True

    else:
        # Check if voice is valid
        voices = await edge_tts.VoicesManager.create()
        args.language = '-'.join(i for i in args.tts.split('-')[0:2])
        voices = voices.find(Locale=args.language)
        if len(voices) == 0:
            # Voice not found
            console.log(
                f"{msg.ERROR}Specified TTS voice not found. Use `edge-tts --list-voices` to list all voices.")
            sys.exit(1)

    # Extract language from TTS voice
    if args.tts:
        lang_prefix = args.tts.split('-')[0]
        if not lang_prefix.startswith('en'):
            args.non_english = True

    # Clear terminal
    console.clear()

    logger.debug('Creating video')
    with console.status(msg.STATUS) as status:
        load_dotenv(find_dotenv())  # Optional

        console.log(
            f"{msg.OK}Finish loading environment variables")
        logger.info('Finish loading environment variables')

        # Check if GPU is available for PyTorch (CUDA).
        if torch.cuda.is_available():
            console.log(f"{msg.OK}PyTorch GPU version found")
            logger.info('PyTorch GPU version found')
        else:
            console.log(
                f"{msg.WARNING}PyTorch GPU not found, using CPU instead")
            logger.warning('PyTorch GPU not found')

        await download_video(url=args.url)

        # Generate images using the generate_images function
        images_response = generate_images(
            prompt='Sample prompt for image generation',
            negative_prompt='low quality',
            samples=4,
            guidance_scale=7.5,
            height=1920,
            width=1080,
            num_inference_steps=50
        )
        # Handle images response...
        
        # Create voice using the create_voice function
        voice_response = create_voice(
            prompt='Sample prompt for voice generation',
            voice_id='voice_example_id'
        )
        # Handle voice response...

        # OpenAI-Whisper Model
        model = args.model
        if args.model != "large" and not args.non_english:
            model = args.model + ".en"
        whisper_model = whisper.load_model(model)

        console.log(
            f"{msg.OK}OpenAI-Whisper model loaded successfully ({model})")
        logger.info(f'OpenAI-Whisper model loaded successfully ({model})')

        # Text 2 Speech (Edge TTS API)
        media_folder = HOME / 'media'
        if not media_folder.exists():
            media_folder.mkdir()

        for video in jsonData:
            series = video['series']
            part = video['part']
            outro = video['outro']
            path = Path(media_folder).absolute()
            text = video['text']
            tags = video.get('tags', [])

            req_text, filename = create_full_text(
                path, series, part, text, outro)

            console.log(f"{msg.OK}Text converted successfully")
            logger.info('Text converted successfully')

            await convert_to_tts(req_text, outfile=filename, voice=args.tts, args=args)

            # Generate image from the prompt
            image_result = generate_image(
                prompt=video['image_prompt'],
                negative_prompt=video.get('negative_prompt', ''),
                samples=video.get('samples', 1),
                guidance_scale=video.get('guidance_scale', 7.5),
                height=video.get('height', 1024),
                width=video.get('width', 1024),
                num_inference_steps=video.get('num_inference_steps', 50),
                key=os.getenv('IMAGE_API_KEY')
            )
            # Save the image result to a file or process further
            # TODO: Implement saving or further processing

            # Generate voice from the prompt
            voice_result = generate_voice(
                prompt=video['voice_prompt'],
                voice_id=video.get('voice_id', 'default_voice'),
                key=os.getenv('VOICE_API_KEY')
            )
            # Save the voice result to a file or process further
            # TODO: Implement saving or further processing

            console.log(
                f"{msg.OK}Text2Speech mp3 file generated successfully with voice {args.tts}")
            logger.info(
                f'Text2Speech mp3 file generated successfully with voice {args.tts}')

            # Whisper Model to create SRT file from Speech recording
            srt_filename = create_srt(
                whisper_model, path, series, part, text, filename)
            srt_filename = Path(srt_filename).absolute()

            console.log(
                f"{msg.OK}Transcription srt file saved successfully!")
            logger.info('Transcription srt file saved successfully!')

            # Apply highlight words to SRT file
            highlight_words(srt_filename, subtitle_format=args.sub_format,
                            font_color=args.font_color)

            # Background video with srt and duration
            background_mp4 = random_background()

            file_info = get_info(background_mp4, verbose=args.verbose)

            filename = Path(filename).absolute()
            final_video = prepare_video_background(
                background_mp4, filename_mp3=filename, filename_srt=srt_filename, duration=int(file_info.get('duration')), verbose=args.verbose)
            final_video = Path(final_video).absolute()

            console.log(
                f"{msg.OK}MP4 video saved successfully!\nPath: {final_video}")
            logger.info(
                f'MP4 video saved successfully!\nPath: {final_video}')

            # Upload to TikTok
            console.log(f"{msg.OK}Uploading to TikTok...")
            logger.info('Uploading to TikTok...')


            uploaded = tiktok_upload(
                str(final_video), title=f"{series} - {part}", tags=tags, headless=not args.verbose)

            if uploaded:
                console.log(f"{msg.OK}Uploaded to TikTok successfully!")
                logger.info('Uploaded to TikTok successfully!')

            else:
                console.log(f"{msg.ERROR}Error uploading to TikTok")
                logger.error('Error uploading to TikTok')

    console.log(f'{msg.DONE}')
    return True


def generate_images(prompt, negative_prompt, samples, guidance_scale, height, width, num_inference_steps):
    url = 'https://modelslab.com/api/v6/realtime/text2img'
    payload = {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'samples': samples,
        'guidance_scale': guidance_scale,
        'height': height,
        'width': width,
        'num_inference_steps': num_inference_steps
    }
    response = requests.post(url, json=payload)
    while response.json().get('status') == 'wait':
        response = requests.post(url, json=payload)
    return response.json()
    """
    Downloads a video from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the video to download.
        folder (str, optional): The name of the folder to save the video in. Defaults to 'background'.
    """
    directory = HOME / folder
    if not directory.exists():
        directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        with subprocess.Popen(['yt-dlp', '-f bestvideo[ext=mp4]+bestaudio[ext=m4a]', '--restrict-filenames', url]) as process:
            pass
        console.log(
            f"{msg.OK}Background video downloaded successfully")
        logger.info('Background video downloaded successfully')
    return


def random_background(folder: str = "background") -> str:
    """
    Returns the filename of a random file in the specified folder.

    Args:
        folder(str): The folder containing the files.

    Returns:
        str: The filename of a randomly selected file in the folder.
    """
    directory = Path(folder).absolute()
    if not directory.exists():
        directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        files = os.listdir(".")
        random_file = random.choice(files)
        return Path(random_file).absolute()


def get_info(filename: str, verbose: bool = False):
    """
    Get information about a video file.

    Args:
        filename (str): The path to the video file.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        dict: A dictionary containing information about the video file, including width, height, bit rate, and duration.
    """
    try:
        probe = ffmpeg.probe(filename)
        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        try:
            duration = float(audio_stream['duration'])
        except Exception:
            if verbose:
                console.log(
                    f"{msg.WARNING}MP4 default metadata not found")
                logger.warning('MP4 default metadata not found')
            duration = (datetime.datetime.strptime(
                audio_stream['DURATION'], '%H:%M:%S.%f') - datetime.datetime.min).total_seconds()
        if video_stream is None:
            if verbose:
                console.log(
                    f"{msg.WARNING}No video stream found")
                logger.warning('No video stream found')
            bit_rate = int(audio_stream['bit_rate'])
            return {'bit_rate': bit_rate, 'duration': duration}

        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return {'width': width, 'height': height, 'duration': duration}

    except ffmpeg.Error as e:
        console.log(f"{msg.ERROR}{e.stderr}")
        logger.exception(e.stderr)
        sys.exit(1)


def prepare_background(background_mp4: str, filename_mp3: str, filename_srt: str, duration: int, verbose: bool = False) -> str:
    """
    Prepare a background video with an audio file and a subtitle file.

    Args:
        background_mp4 (str): The path to the background video file.
        filename_mp3 (str): The path to the audio file to be merged with the background video.
        filename_srt (str): The path to the subtitle file to be added to the background video.
        duration (int): The duration of the output video in seconds.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        str: The path to the output video file.
    """
    # Get length of MP3 file to be merged with
    audio_info = get_info(filename_mp3)

    # Get starting time:
    audio_duration = int(round(audio_info.get('duration'), 0))
    ss = random.randint(0, (duration-audio_duration))
    audio_duration = convert_time(audio_info.get('duration'))
    if ss < 0:
        ss = 0

    srt_filename = filename_srt.name
    srt_path = filename_srt.parent.absolute()

    # Create output directory
    directory = HOME / 'output'
    if not directory.exists():
        directory.mkdir()

    outfile = f"{HOME}{os.sep}output{os.sep}output_{ss}.mp4"

    if verbose:
        rich_print(
            f"{filename_srt = }\n{background_mp4 = }\n{filename_mp3 = }\n", style='bold green')   #
        # 'Alignment=9,BorderStyle=3,Outline=5,Shadow=3,Fontsize=15,MarginL=5,MarginV=25,FontName=Lexend Bold,ShadowX=-7.1,ShadowY=7.1,ShadowColour=&HFF000000,Blur=141'Outline=5
    args = [
        "ffmpeg",
        "-ss", str(ss),
        "-t", str(audio_duration),
        "-i", background_mp4,
        "-i", filename_mp3,
        "-map", "0:v",
        "-map", "1:a",
        "-filter:v",
        f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=bicubic, gblur=sigma=2, subtitles={srt_filename}:force_style=',Alignment=8,BorderStyle=7,Outline=3,Shadow=5,Blur=15,Fontsize=15,MarginL=45,MarginR=55,FontName=Lexend Bold'",
        "-c:v", "libx264", "-preset", "5",
        "-b:v", "5M",
        "-c:a", "aac", "-ac", "1",
        "-b:a", "96K",
        f"{outfile}", "-y",
        "-threads", f"{multiprocessing.cpu_count()//2}"]

    if verbose:
        rich_print('[i] FFMPEG Command:\n'+' '.join(args)+'\n', style='yellow')

    with KeepDir() as keep_dir:
        keep_dir.chdir(srt_path)
        with subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            pass

    return outfile


def srt_create(model, path: str, series: str, part: int, text: str, filename: str) -> bool:
    """
    Create an SRT file for a given video file using the specified model.

    Args:
        model: The model to use for transcription.
        path (str): The path to the directory where the SRT file should be saved.
        series (str): The name of the series the video belongs to.
        part (int): The part number of the video.
        text (str): The text to transcribe.
        filename (str): The name of the video file.

    Returns:
        bool: True if the SRT file was created successfully, False otherwise.
    """
    series = series.replace(' ', '_')
    srt_path = f"{path}{os.sep}{series}{os.sep}"

    word_options = {
        "highlight_words": True,  # keep this True otherwise the custom style won't be applied
        "max_line_count": 1,
        "max_line_width": 40,
        "preserve_segments": False,
    }

    transcribe = model.transcribe(
        filename, task="transcribe", word_timestamps=True, fp16=torch.cuda.is_available())
    vtt_writer = whisper.utils.get_writer(
        output_format="srt", output_dir=srt_path)
    vtt_writer(transcribe, filename, word_options)

    srt_filename = f"{srt_path}{series}_{part}.srt"

    return srt_filename


def highlight_words(srt_file: str, subtitle_format: str = "u", font_color: str = "#FFFFFF") -> bool:
    """
    Highlights words in a subtitle file by modifying the formatting tags.

    Args:
        srt_file (str): The path to the subtitle file.
        subtitle_format (str, optional): The subtitle format to be used. Defaults to "u".
        font_color (str, optional): The color of the font. Defaults to "#FFFFFF".

    Returns:
        bool: True if the subtitle file was formatted successfully, False otherwise.
    """
    subtitle_format = subtitle_format.lower()

    if not font_color.startswith('#'):
        console.log(
            f"{msg.ERROR}Invalid font color. Using default color: #FFFFFF")
        font_color = "#FFFFFF"
    else:
        font_color = font_color.upper()

    with open(srt_file, 'r', encoding='UTF-8') as f:
        content = f.read()

    content = content.replace(
        '<u>', f'<font color={font_color}><{subtitle_format}>').replace('</u>', f'</{subtitle_format}></font>')

    with open(srt_file, 'w', encoding='UTF-8') as f:
        f.write(content)

    console.log(
        f"{msg.OK}Subtitle file formatted successfully")

    return True


def convert_time(time_in_seconds):
    """
    Converts time in seconds to a string in the format "hh:mm:ss.mmm".

    Args:
        time_in_seconds (float): The time in seconds to be converted.

    Returns:
        str: The time in the format "hh:mm:ss.mmm".
    """
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def batch_create(filename: str) -> None:
    """
    Batch creates a file by concatenating all files in the './batch/' directory in alphanumeric order.

    Args:
    - filename (str): the name of the file to be created.

    Returns:
    - None
    """
    with open(filename, 'wb') as out:
        def sorted_alphanumeric(data):
            def convert(text): return int(
                text) if text.isdigit() else text.lower()
            def alphanum_key(key): return [convert(c)
                                           for c in re.split('([0-9]+)', key)]
            return sorted(data, key=alphanum_key)

        for item in sorted_alphanumeric(os.listdir('./batch/')):
            filestuff = open(f'.{os.sep}batch.{os.sep}item', 'rb').read()
            out.write(filestuff)


def create_full_text(path: str = '', series: str = '', part: int = 1, text: str = '', outro: str = '') -> Tuple[str, str]:
    """
    Creates full text and filename for a given series, part, text and outro.

    Args:
        path (str): The path where the file will be saved.
        series (str): The name of the series.
        part (int): The part number of the series.
        text (str): The main text of the series.
        outro (str): The outro of the series.

    Returns:
        Tuple[str, str]: A tuple containing the full text and filename.
    """
    req_text = f"{series}. {part}.\n{text}\n{outro}"
    series = series.replace(' ', '_')
    filename = f"{path}{os.sep}{series}{os.sep}{series}_{part}.mp3"

    # create directory if not exist
    if not os.path.isdir(f"{path}{os.sep}{series}"):
        os.mkdir(f"{path}{os.sep}{series}")
    return req_text, filename


async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", stdout: bool = False, outfile: str = "tts.mp3", args=None) -> bool:
    """
    Converts text to speech using Microsoft Edge Text-to-Speech API.

    Args:
        final_text (str): The text to be converted to speech.
        voice (str, optional): The name of the voice to use. Defaults to "en-US-ChristopherNeural".
        stdout (bool, optional): Whether to output the speech audio to stdout. Defaults to False.
        outfile (str, optional): The name of the output file. Defaults to "tts.mp3".
        args (object, optional): An object containing the gender and language to use when selecting a random voice. Defaults to None.

    Returns:
        bool: True if the text was successfully converted to speech and saved to a file, False otherwise.
    """
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True


def upload_tiktok(file, title: str, tags: list, headless: bool = False):
    if not os.path.isfile('cookies.txt'):
        console.log(f"{msg.ERROR}Cookie file not found. Please check the following link for instructions on how to get your TikTok cookie: https://github.com/kairi003/Get-cookies.txt-LOCALLY")
        logger.error('Cookie file not found')

    else:
        console.log(f"{msg.OK}Cookie file found")
        logger.info('Cookie file found')

        # Merge title and tags
        if len(tags) > 0:
            tags = ' '.join([f"#{tag}" for tag in tags])
            description = f"{title} {tags}"
        else:
            description = title

        try:
            upload_video(file, description=description, cookies='cookies.txt',
                         comment=True, stitch=False, duet=False, headless=headless)

        except Exception as e:
            console.log(f"{msg.ERROR}Error uploading to TikTok: {e}")
            logger.exception(e)
            return False

        return True


if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())

    except Exception as e:
        loop.close()
        console.log(f"{msg.ERROR}{e}")
        logger.exception(e)

    finally:
        loop.close()

    sys.exit(1)
