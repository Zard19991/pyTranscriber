'''
   (C) 2025 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

class Whisper:

    supported_languages_list = None
    supported_languages_dict = {
                "en": "english",
                "zh": "chinese",
                "de": "german",
                "es": "spanish",
                "ru": "russian",
                "ko": "korean",
                "fr": "french",
                "ja": "japanese",
                "pt": "portuguese",
                "tr": "turkish",
                "pl": "polish",
                "ca": "catalan",
                "nl": "dutch",
                "ar": "arabic",
                "sv": "swedish",
                "it": "italian",
                "id": "indonesian",
                "hi": "hindi",
                "fi": "finnish",
                "vi": "vietnamese",
                "he": "hebrew",
                "uk": "ukrainian",
                "el": "greek",
                "ms": "malay",
                "cs": "czech",
                "ro": "romanian",
                "da": "danish",
                "hu": "hungarian",
                "ta": "tamil",
                "no": "norwegian",
                "th": "thai",
                "ur": "urdu",
                "hr": "croatian",
                "bg": "bulgarian",
                "lt": "lithuanian",
                "la": "latin",
                "mi": "maori",
                "ml": "malayalam",
                "cy": "welsh",
                "sk": "slovak",
                "te": "telugu",
                "fa": "persian",
                "lv": "latvian",
                "bn": "bengali",
                "sr": "serbian",
                "az": "azerbaijani",
                "sl": "slovenian",
                "kn": "kannada",
                "et": "estonian",
                "mk": "macedonian",
                "br": "breton",
                "eu": "basque",
                "is": "icelandic",
                "hy": "armenian",
                "ne": "nepali",
                "mn": "mongolian",
                "bs": "bosnian",
                "kk": "kazakh",
                "sq": "albanian",
                "sw": "swahili",
                "gl": "galician",
                "mr": "marathi",
                "pa": "punjabi",
                "si": "sinhala",
                "km": "khmer",
                "sn": "shona",
                "yo": "yoruba",
                "so": "somali",
                "af": "afrikaans",
                "oc": "occitan",
                "ka": "georgian",
                "be": "belarusian",
                "tg": "tajik",
                "sd": "sindhi",
                "gu": "gujarati",
                "am": "amharic",
                "yi": "yiddish",
                "lo": "lao",
                "uz": "uzbek",
                "fo": "faroese",
                "ht": "haitian creole",
                "ps": "pashto",
                "tk": "turkmen",
                "nn": "nynorsk",
                "mt": "maltese",
                "sa": "sanskrit",
                "lb": "luxembourgish",
                "my": "myanmar",
                "bo": "tibetan",
                "tl": "tagalog",
                "mg": "malagasy",
                "as": "assamese",
                "tt": "tatar",
                "haw": "hawaiian",
                "ln": "lingala",
                "ha": "hausa",
                "ba": "bashkir",
                "jw": "javanese",
                "su": "sundanese",
                "yue": "cantonese",
            }

    @staticmethod
    def convert_dict_to_list():
        Whisper.supported_languages_list = list()
        for (k, v) in Whisper.supported_languages_dict.items():
            Whisper.supported_languages_list.append(k + " - " + v)

    @staticmethod
    def get_supported_languages():
        if Whisper.supported_languages_list is None:
            Whisper.convert_dict_to_list()
        return Whisper.supported_languages_list