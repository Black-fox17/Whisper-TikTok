from os import os

import whisper
from main import torch
from whisper import utils


def srt_create(model, path: str, series: str, part: int, text: str, filename: str) -> bool:
    series = series.replace(' ', '_')
    srt_path = f"{path}{os.sep}{series}{os.sep}"

    word_options = {
        "highlight_words": True,
        "max_line_count": 1,
        "max_line_width": 40,
        "preserve_segments": False,
    }

    transcribe = model.transcribe(
        filename, task="transcribe", word_timestamps=True, fp16=torch.cuda.is_available())
    vtt_writer = utils.get_writer(
        output_format="srt", output_dir=srt_path)
    vtt_writer(transcribe, filename, word_options)

    srt_filename = f"{srt_path}{series}_{part}.srt"

    return srt_filename
