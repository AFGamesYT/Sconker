# import TranslationModule as tm
# from TranslationModule import TranslatedString as tStr
#
#  tm.create_key(key="hello", default="en")
#  tm.add_translation(key="hello", lang="ru", translation="привет")
#
#  -----------
#  name = "Igor"
#  print(tStr(f"$'hello'$, {name}!"))
#
#
import json

def create_key(key, default=None, path="translation.json"):
    with open(path, "r") as f:
        try:
            trnsl = json.load(f)
        except json.decoder.JSONDecodeError:
            print("[TranslationModule] File is empty!")
            trnsl = {}

    with open(path, "w") as f:
        if default is not None:
            trnsl[key] = {default: key}

        json.dump(trnsl, f)


def add_translation(key, lang, translation, path="translation.json"):
    with open(path, "r") as f:
        try:
            trnsl = json.load(f)
        except json.decoder.JSONDecodeError:
            print("[TranslationModule] File is empty!")
            trnsl = {}

    with open(path, "w") as f:
        trnsl.setdefault(key, {}).setdefault(lang, []).append(translation)
        trnsl[key][lang] = translation

        json.dump(trnsl, f)


class TranslatedString:
    def __init__(self, string_to_translate: str, lang, path="translation.json"):
        self.string_to_translate = string_to_translate
        self.lang = lang
        self.path = path

        return

    def t(self) -> str:
        stt = self.string_to_translate

        if "$/" in stt:
            stt = stt.split("$/")

        stt = [val for val in stt if val != ""]

        keys = []
        for val in stt:
            if "/" in val:
                keys.append(val[0:val.index("/")])

        with open(self.path, "r") as f:
            try:
                trnsl = json.load(f)
            except json.decoder.JSONDecodeError:
                print("[TranslationModule] File is empty!")
                trnsl = {}

        for key in keys:
            converted = trnsl[key][self.lang]
            self.string_to_translate = self.string_to_translate.replace(f"$/{key}/", converted)

        result = self.string_to_translate

        return result

    def __str__(self):
        self.t()


if __name__ == "__main__":
    create_key(key="menu_settings")
    add_translation("menu_settings", "en", "Settings")
    add_translation("menu_settings", "ru", "Настройки")
    print(TranslatedString("$/menu_exit/", "en").t())
