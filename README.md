## New Functionalities 🆕

### `generate_images` Function

The `generate_images` function allows you to generate images based on a text prompt. It makes a request to an external API that returns a set of images that match the prompt.

**Example of usage**:

```python
response = generate_images(
    prompt='A serene beach at sunset',
    negative_prompt='low quality',
    samples=4,
    guidance_scale=7.5,
    height=1080,
    width=1920,
    num_inference_steps=50
)
print(response)
```

### `create_voice` Function

The `create_voice` function allows you to convert text to voice. It calls an external API that processes the text and returns an audio file in the desired voice.

**Example of usage**:

```python
response = create_voice(
    prompt='Welcome to Whisper-TikTok tutorial',
    voice_id='jack_sparrow'
)
print(response)
```

Remember to handle the responses from these functions appropriately. This may include checking for any 'wait' status and resending requests or processing the received images and audio files.# Introducing Whisper-TikTok 🤖🎥

Discover Whisper-TikTok, an innovative AI-powered tool that leverages the prowess of **Edge TTS**, **OpenAI-Whisper**, and **FFMPEG** to craft captivating TikTok videos. Harnessing the capabilities of OpenAI's Whisper model, Whisper-TikTok effortlessly generates an accurate **transcription** from provided audio files, laying the foundation for the creation of mesmerizing TikTok videos through the utilization of **FFMPEG**. Additionally, the program seamlessly integrates the **Microsoft Edge Cloud Text-to-Speech (TTS) API** to lend a vibrant **voiceover** to the video. Opting for Microsoft Edge Cloud TTS API's voiceover is a deliberate choice, as it delivers a remarkably **natural and authentic** auditory experience, setting it apart from the often monotonous and artificial voiceovers prevalent in numerous TikTok videos.

## Demo Video 🎬

<https://github.com/MatteoFasulo/Whisper-TikTok/assets/74818541/68e25504-c305-4144-bd39-c9acc218c3a4>

# Welcome to the Whisper-TikTok Repository

This repository houses an innovative Streamlit application that expertly utilizes the OpenAI Whisper model, Microsoft Edge's read aloud feature, and FFmpeg to craft creative and captivating TikTok videos with seamless voiceovers and video processing capabilities.

## Streamlit App

![Streamlit App Screenshot](/assets/streamlit-app-screenshot.png)

To use and explore the Streamlit app, please refer to the "How to Start the App" section below for detailed instructions on getting the app up and running.

## How to Start the App

To start the Streamlit application, navigate to the root directory of this repository and execute the script located in `src/main.py` with the following command:

```bash
streamlit run src/main.py
```

Feel free to access the application's interface and enjoy the functionalities it offers.

## Operating Principle

Employing Whisper-TikTok is a breeze: simply modify the [video.json](video.json). The JSON file contains the following fields:

- `series`: The name of the series.
- `part`: The part number of the video.
- `text`: The text to be spoken in the video.
- `outro`: The outro text to be spoken in the video.
- `tags`: The tags to be used for the video.

Summarizing the program's functionality:

> Furnished with a structured JSON dataset containing details such as the **series name**, **video part number**, **video text** and **outro text**, the program orchestrates the synthesis of a video incorporating the provided text and outro. Subsequently, the generated video is stored within the designated `output` folder.

### In-Depth Insights

The program conducts the **sequence of actions** outlined below:

1. Retrieve **environment variables** from the optional .env file.
2. Validate the presence of **PyTorch** with **CUDA** installation. If the requisite dependencies are **absent**, the **program will use the CPU instead of the GPU**.
3. Download a random video from platforms like YouTube, e.g., a Minecraft parkour gameplay clip.
4. Load the OpenAI Whisper model into memory.
5. Extract the video text from the provided JSON file and initiate a **Text-to-Speech** request to the Microsoft Edge Cloud TTS API, preserving the response as an .mp3 audio file.
6. Utilize the OpenAI Whisper model to generate a detailed **transcription** of the .mp3 file, available in .srt format.
7. Select a **random background** video from the dedicated folder.
8. Integrate the srt file into the chosen video using FFMPEG, creating a final .mp4 output.
9. Upload the video to TikTok using the TikTok session cookie. For this step it is required to have a TikTok account and to be logged in on your browser. Then the required `cookies.txt` file can be generated using [this guide available here](https://github.com/kairi003/Get-cookies.txt-LOCALLY). The `cookies.txt` file must be placed in the root folder of the project.
10. Voila! In a matter of minutes, you've crafted a captivating TikTok video while sipping your favorite coffee ☕️.

## Prerequisites 🛠️

Whisper-TikTok has undergone rigorous testing on Windows 10, Windows 11 and Ubuntu 23.04 systems equipped with Python versions 3.8, 3.9 and 3.11.
To streamline the installation of necessary dependencies, execute the following command within your terminal:

```python
pip install -U -r requirements.txt
```

It also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:

```bash
# on Ubuntu or Debian

sudo apt update && sudo apt install ffmpeg

# on Arch Linux

sudo pacman -S ffmpeg

# on MacOS using Homebrew (<https://brew.sh/>)

brew install ffmpeg

# on Windows using Chocolatey (<https://chocolatey.org/>)

choco install ffmpeg

# on Windows using Scoop (<https://scoop.sh/>)

scoop install ffmpeg
```

Please note that for optimal performance, it's advisable to have a GPU when using the OpenAI Whisper model for speech recognition. However, the program will work without a GPU, but it will run more slowly. This performance difference is because GPUs efficiently handle fp16 computation, while CPUs use fp32 or fp64 (depending on your machine), which are slower.

## Repository Contents

The repository includes:
- Python scripts for generating images (`image_generator.py`), creating videos (`video_creator.py`), and generating voice (`voice_generator.py`).
- Guides for the installation of FFmpeg and CUDA: [FFmpeg Installation Guide](docs/1-ffmpeg.md), [CUDA Installation Guide](docs/2-cuda.md).

These components enable the creation and manipulation of content for TikTok videos using a blend of AI models and multimedia processing techniques.

## Usage Guidelines 📝

To use the new `generate_images` and `create_voice` functionalities, please follow these guidelines:

- **generate_images**: Use this function to generate images from a textual prompt. Provide parameters such as the prompt, negative prompts to avoid, number of samples to generate, guidance scale, and the dimensions and resolution of the images.
- **create_voice**: This function converts your text into a spoken voiceover. You'll need to supply the text and choose a voice ID from the available options.

After calling these functions, make sure to handle their responses correctly, including any 'wait' status from the `generate_images` function, and processing the returned images and voice files appropriately.

To get started with the main functionality of Whisper-TikTok, run the following command in your terminal:

```bash
python main.py
```

## Command-Line Options

Whisper-TikTok supports the following command-line options:

```
python main.py [OPTIONS]

Options:
  --model TEXT        Model to use
                      [tiny|base|small|medium|large] (Default: small)
  --non_english       Use general model, not the English one specifically. (Flag)
  --url TEXT          YouTube URL to download as background video.
                      (Default: <https://www.youtube.com/watch?v=intRX7BRA90>)
  --tts TEXT          Voice to use for TTS (Default: en-US-ChristopherNeural)
  --list-voices       Use `edge-tts --list-voices` to list all voices.
  --random_voice      Random voice for TTS (Flag)
  --gender TEXT       Gender of the random TTS voice [Male|Female].
  --language TEXT     Language of the random TTS voice
                      (e.g., en-US)
  --sub_format TEXT   Subtitle format to use [u|i|b] (Default: b) | b (Bold), u (Underline), i (Italic)
  --font_color TEXT   Font color to use for subtitles in HEX format (Default: #FFFFFF). Suggested: #FFF000 (Yellow)
  -v, --verbose       Verbose (Flag)
```

> If you use the --random_voice option, please specify both --gender and --language arguments. Also you will need to specify the --non_english argument if you want to use a non-English voice otherwise the program will use the English model. Whisper model will auto-detect the language of the audio file and use the corresponding model.

## Usage Examples

- Generate a TikTok video using a specific TTS model and voice:

```bash
python main.py --model medium --tts en-US-EricNeural
```

- Generate a TikTok video without using the English model:

```bash
python main.py --non_english --tts de-DE-KillianNeural
```

- Use a custom YouTube video as the background video:

```bash
python main.py --url https://www.youtube.com/watch?v=dQw4w9WgXcQ --tts en-US-JennyNeural
```

- Modify the font color of the subtitles:

```
python main.py --sub_format b --font_color #FFF000 --tts en-US-JennyNeural
```

- Generate a TikTok video with a random TTS voice:

```bash
python main.py --random_voice --gender Male --language en-US
```

- List all available voices:

```bash
edge-tts --list-voices
```

## Code of Conduct

Please review our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing to Whisper-TikTok.

## Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for more information.

## Upcoming Features 🔮

- Integration with the OpenAI API to generate more advanced responses.
- Improved user interface for a more seamless experience.

## OpenAI Whisper Forum Discussion

- <https://github.com/openai/whisper/discussions/223>

## Acknowledgments

- We'd like to give a huge thanks to [@rany2](https://www.github.com/rany2) for their [edge-tts](https://github.com/rany2/edge-tts) package, which made it possible to use the Microsoft Edge Cloud TTS API with Whisper-TikTok.
- We also acknowledge the contributions of the Whisper model by [@OpenAI](https://github.com/openai/whisper) for robust speech recognition via large-scale weak supervision
