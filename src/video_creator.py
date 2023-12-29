import ffmpeg


def create_video(images, voice):
    video = ffmpeg.input('pipe:', format='image2pipe', framerate=24).output(voice, 'output.mp4').run(input=images, capture_stdout=True, capture_stderr=True)
    return video
