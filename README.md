# Alfred Emoji Pack Update

This is an updated version of the original alfred emoji pack to include new emojis in unicode 12.
Even if the script was written quickly, it is now more useable, and supports I18N.

There are 3 packs that allow some flexibility in inserting emojis:

1. `Emoji Pack Update` requires a prefix, a suffix (to be set in Alfred, see [Install](./README.md#install) section below), and uses underscore to separate words, just like GitHub <br>
  `:lady_beetle:` to insert 🐞 (use `:` for consistency)
2. `Emoji Pack DecolSp` still requires a prefix and a suffix, but uses a more convenient `␣` space to separate words <br>
  `;lady beetle;` to insert 🐞 (use `;` to avoid <kbd>⇧</kbd> for `:`)
3. `Emoji Pack DecolDedup` only requires a prefix, uses a more convenient `-` to separate words, and sometimes `␣` to signify emoji ending to avoid shorter keywords overriding the longer compound ones <br>
  `;lady-beetle` to insert 🐞 <br>
  `;+1␣` to insert 👍️ (extra space allows entering `;+1-tone5` to insert 👍🏿)

## Important links

* See the [snippets](./snippets/) folder for the pre-generated files
* The original emoji pack and instructions are available here: https://github.com/califa/alfred-emoji-pack
* Emojis are downloaded from EmojiBase: https://github.com/milesj/emojibase - https://cdn.jsdelivr.net/npm/emojibase-data@latest/en/

## Install

1. Download either (or all) of the 3 generated snippets files: [Emoji_Pack_Update](https://github.com/paris-ci/Alfred-Emoji-Pack-Update/raw/master/snippets/Emoji%20Pack%20Update.alfredsnippets), [Emoji Pack DecolSp](https://github.com/paris-ci/Alfred-Emoji-Pack-Update/raw/master/snippets/Emoji%20Pack%20DecolSp.alfredsnippets), [Emoji-Pack-DecolDedup](https://github.com/paris-ci/Alfred-Emoji-Pack-Update/raw/master/snippets/Emoji%20Pack%20DecolDedup.alfredsnippets)
2. Import them into alfred, **uncheck the** strip snippets of auto-expand flag checkbox.
   ![autoexpand.png](manual/autoexpand.png)
3. Set your desired prefix and suffix by right clicking the collection in the snippets view:
    1. Edit the collection ![edit.png](manual/edit.png)
    2. Set your prefix and suffix ![prefixsuffix.png](manual/prefixsuffix.png)
4. Enjoy ! 