import argparse
from sys import sys

import edge_tts
from msg import msg
from utils import console


async def parse_args():
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

    return args
