languages_to_generate = ["en"]  # For now, there is no change between languages, but maybe in the future, shortcodes will be I18N'ed, and the script is ready for that.
output_dir = "snippets/"
cache_dir = "cache/"  # WARNING : This will get emptied!
enable_skins = True   # Use ok_hand_tone1 for example


# == Config test, do not edit after this line. ==

import os
import shutil


def ensure_directory(directory, empty=False):
    if not os.path.exists(directory):
        os.makedirs(directory)
    elif empty:
        shutil.rmtree(directory)
        os.makedirs(directory)

AVAILABLE_LANGS = ["da", "de", "en", "en-gb", "es", "es-mx", "fr", "it", "ja", "ko", "ms", "nl", "pl", "pt", "ru", "sv", "th", "zh", "zh-hant"]

assert set(languages_to_generate).issubset(set(AVAILABLE_LANGS)), "The language specified cound't be found."
ensure_directory(output_dir)
ensure_directory(cache_dir, empty=True)