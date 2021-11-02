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

def generate_alfred_snippet_file(key, value, cache_dir, decolsp=False, decol=False):
    """
    decolsp (bool): "DeColon" names
      1. emoji names    — remove ':', replace '_' with ' ', convert to Title Case
      2. emoji keywords —             replace '_' with ' '
    decol (bool):
      1. emoji names    — same as 'decolsp'
      2. emoji keywords —             replace '_' with '-'
    """
    uid = str(uuid.uuid4())

    key_space = f"{key}".replace('_',' ')
    key_dash  = f"{key}".replace('_','-')
    key_title = f"{key_space}".title()
    if decolsp: name = f"{value} {key_title}"; keyword = f"{key_space}"
    elif decol: name = f"{value} {key_title}"; keyword = f"{key_dash}"
    else:       name = f"{value} :{key}:"    ; keyword = f"{key}"
    content = {
        "alfredsnippet": {
            "snippet": f"{value}",
            "uid": uid,
            "name": f"{name}",
            "keyword": f"{keyword}"
        }
    }
    try:
        with open(f"{cache_dir}/{value} {key} - {uid}.json", "w") as f:
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
        print(f":{shortcode}:  ⟶  {emoji}")
        generate_alfred_snippet_file(shortcode, emoji, config.cache_dir_def)
        generate_alfred_snippet_file(shortcode, emoji, config.cache_dir_decolsp, decolsp=True)
        if any((sc.startswith(shortcode) and sc != shortcode) for sc in emojis_to_convert):
          shortcode += ' '
          print(f":{shortcode}: ⟶  {emoji} (deduped version)")
        generate_alfred_snippet_file(shortcode, emoji, config.cache_dir_dedupedecol, decol=True)

    shutil.copyfile("icon.png", config.cache_dir_def         + "icon.png")
    shutil.copyfile("icon.png", config.cache_dir_dedupedecol + "icon.png")
    file_name_def         = f"./{config.output_dir}Emoji Pack Update.alfredsnippets"
    file_name_dedupedecol = f"./{config.output_dir}Emoji Pack Update DedupedDecoled.alfredsnippets"
    shutil.copyfile("icon.png", config.cache_dir_decolsp    + "icon.png")
    file_name_decolsp    = f"./{config.output_dir}Emoji Pack Upd DecolSp.alfredsnippets"

    print(f"Saving to {file_name_def}")
    shutil.make_archive(file_name_def, "zip", root_dir=config.cache_dir_def)
    os.rename(file_name_def + ".zip", file_name_def)

    print(f"Saving to {file_name_decolsp}")
    shutil.make_archive(file_name_decolsp, "zip", root_dir=config.cache_dir_decolsp)
    os.rename(file_name_decolsp + ".zip", file_name_decolsp)

    print(f"Saving to {file_name_dedupedecol}")
    shutil.make_archive(file_name_dedupedecol, "zip", root_dir=config.cache_dir_dedupedecol)
    os.rename(file_name_dedupedecol + ".zip", file_name_dedupedecol)

if __name__ == '__main__':
    main()
