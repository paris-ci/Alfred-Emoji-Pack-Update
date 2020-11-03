"""
Quick and dirty script to generate alfred snippets for emojis

We'll use these files :
https://cdn.jsdelivr.net/npm/emojibase-data@latest/LANG/data.json
"""
import json
import os
import shutil
from typing import Dict, List

import requests
import uuid

import config


def download_emoji_file(language) -> List[Dict]:
    file = requests.get(f"https://cdn.jsdelivr.net/npm/emojibase-data@latest/{language}/data.json")
    return file.json()

def download_shortcodes(language) -> Dict:
    file = requests.get(f"https://cdn.jsdelivr.net/npm/emojibase-data@latest/{language}/shortcodes/emojibase.json")
    return file.json()

def generate_alfred_snippet_file(key, value):
    uid = str(uuid.uuid4())

    content = {
        "alfredsnippet": {
            "snippet": f"{value}",
            "uid": uid,
            "name": f"{value} :{key}:",
            "keyword": f":{key}:"
        }
    }
    try:
        with open(f"{config.cache_dir}/{value} {key} - {uid}.json", "w") as f:
            json.dump(content, f, ensure_ascii=False)
    except OSError:
        pass

def get_shortcodes(shortcodes, hexcode):
    codes = shortcodes.get(hexcode, [])
    if type(codes) is not list:
        codes = [codes]
    return codes

def main():
    emojis_to_convert = {}  # {"shortcode": "emoji"}

    for language in config.languages_to_generate:
        shortcodes = download_shortcodes(language)
        emoji_file = download_emoji_file(language)
        for emoji_info in emoji_file:
            emoji = emoji_info["emoji"]
            for shortcode in get_shortcodes(shortcodes, emoji_info['hexcode']):
                emojis_to_convert[shortcode] = emoji
            if config.enable_skins:
                for skin in emoji_info.get("skins", []):
                    for shortcode in get_shortcodes(shortcodes, skin['hexcode']):
                        emojis_to_convert[shortcode] = skin["emoji"]

    for shortcode, emoji in emojis_to_convert.items():
        print(f":{shortcode}: -> {emoji}")
        generate_alfred_snippet_file(shortcode, emoji)

    shutil.copyfile("icon.png", config.cache_dir + "icon.png")
    file_name = f"./{config.output_dir}Emoji Pack Update.alfredsnippets"
    print(f"Saving to {file_name}")

    shutil.make_archive(file_name, "zip", root_dir=config.cache_dir)
    os.rename(file_name + ".zip", file_name)


if __name__ == '__main__':
    main()