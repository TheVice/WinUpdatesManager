import os
from core.unknownSubstance import UnknownSubstance


class Languages(UnknownSubstance):

    def __init__(self):

        self.Neutral = 'Neutral'
        self.Arabic = 'Arabic'
        self.Chinese_Simplified = 'Chinese (Simplified)'
        self.Chinese_Traditional = 'Chinese (Traditional)'
        self.Czech = 'Czech'
        self.Danish = 'Danish'
        self.Dutch = 'Dutch'
        self.English = 'English'
        self.Finnish = 'Finnish'
        self.French = 'French'
        self.German = 'German'
        self.Greek = 'Greek'
        self.Hebrew = 'Hebrew'
        self.Hungarian = 'Hungarian'
        self.Italian = 'Italian'
        self.Japanese = 'Japanese'
        self.Korean = 'Korean'
        self.Norwegian = 'Norwegian'
        self.Polish = 'Polish'
        self.Portuguese_Brazil = 'Portuguese (Brazil)'
        self.Portuguese_Portugal = 'Portuguese (Portugal)'
        self.Russian = 'Russian'
        self.Spanish = 'Spanish'
        self.Swedish = 'Swedish'
        self.Turkish = 'Turkish'

        languages = {}

        languages[os.sep + 'Neutral' + os.sep] = self.Neutral
        languages[os.sep + 'Arabic' + os.sep] = self.Arabic
        languages[os.sep + 'Chinese (Simplified)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'Chinese (Traditional)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'Czech' + os.sep] = self.Czech
        languages[os.sep + 'Danish' + os.sep] = self.Danish
        languages[os.sep + 'Dutch' + os.sep] = self.Dutch
        languages[os.sep + 'English' + os.sep] = self.English
        languages[os.sep + 'Finnish' + os.sep] = self.Finnish
        languages[os.sep + 'French' + os.sep] = self.French
        languages[os.sep + 'German' + os.sep] = self.German
        languages[os.sep + 'Greek' + os.sep] = self.Greek
        languages[os.sep + 'Hebrew' + os.sep] = self.Hebrew
        languages[os.sep + 'Hungarian' + os.sep] = self.Hungarian
        languages[os.sep + 'Italian' + os.sep] = self.Italian
        languages[os.sep + 'Japanese (Japan)' + os.sep] = self.Japanese
        languages[os.sep + 'Korean' + os.sep] = self.Korean
        languages[os.sep + 'Norwegian'] = self.Norwegian
        languages[os.sep + 'Polish' + os.sep] = self.Polish
        languages[os.sep + 'Portuguese (Brazil)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'Portuguese (Portugal)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'Russian' + os.sep] = self.Russian
        languages[os.sep + 'Spanish (Traditional Sort)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'Swedish' + os.sep] = self.Swedish
        languages[os.sep + 'Turkish' + os.sep] = self.Turkish

        self.mCalligraphicLanguages = dict(languages)

        languages[os.sep + 'neutral' + os.sep] = self.Neutral
        languages[os.sep + 'arabic' + os.sep] = self.Arabic
        languages[os.sep + 'chinese (simplified)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'chinese (traditional)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'czech' + os.sep] = self.Czech
        languages[os.sep + 'danish' + os.sep] = self.Danish
        languages[os.sep + 'dutch' + os.sep] = self.Dutch
        languages[os.sep + 'english' + os.sep] = self.English
        languages[os.sep + 'finnish' + os.sep] = self.Finnish
        languages[os.sep + 'french' + os.sep] = self.French
        languages[os.sep + 'german' + os.sep] = self.German
        languages[os.sep + 'greek' + os.sep] = self.Greek
        languages[os.sep + 'hebrew' + os.sep] = self.Hebrew
        languages[os.sep + 'hungarian' + os.sep] = self.Hungarian
        languages[os.sep + 'italian' + os.sep] = self.Italian
        languages[os.sep + 'japanese (japan)' + os.sep] = self.Japanese
        languages[os.sep + 'japanese' + os.sep] = self.Japanese
        languages[os.sep + 'korean' + os.sep] = self.Korean
        languages[os.sep + 'norwegian'] = self.Norwegian
        languages[os.sep + 'polish' + os.sep] = self.Polish
        languages[os.sep + 'portuguese (brazil)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'portuguese (portugal)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'russian' + os.sep] = self.Russian
        languages[os.sep + 'spanish (traditional sort)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'swedish' + os.sep] = self.Swedish
        languages[os.sep + 'turkish' + os.sep] = self.Turkish

        languages[os.sep + 'NEUTRAL' + os.sep] = self.Neutral
        languages[os.sep + 'ARABIC' + os.sep] = self.Arabic
        languages[os.sep + 'CHINESE (SIMPLIFIED)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'CHINESE (TRADITIONAL)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'CZECH' + os.sep] = self.Czech
        languages[os.sep + 'DANISH' + os.sep] = self.Danish
        languages[os.sep + 'DUTCH' + os.sep] = self.Dutch
        languages[os.sep + 'ENGLISH' + os.sep] = self.English
        languages[os.sep + 'FINNISH' + os.sep] = self.Finnish
        languages[os.sep + 'FRENCH' + os.sep] = self.French
        languages[os.sep + 'GERMAN' + os.sep] = self.German
        languages[os.sep + 'GREEK' + os.sep] = self.Greek
        languages[os.sep + 'HEBREW' + os.sep] = self.Hebrew
        languages[os.sep + 'HUNGARIAN' + os.sep] = self.Hungarian
        languages[os.sep + 'ITALIAN' + os.sep] = self.Italian
        languages[os.sep + 'JAPANESE (JAPAN)' + os.sep] = self.Japanese
        languages[os.sep + 'KOREAN' + os.sep] = self.Korean
        languages[os.sep + 'NORWEGIAN'] = self.Norwegian
        languages[os.sep + 'POLISH' + os.sep] = self.Polish
        languages[os.sep + 'PORTUGUESE (BRAZIL)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'PORTUGUESE (PORTUGAL)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'RUSSIAN' + os.sep] = self.Russian
        languages[os.sep + 'SPANISH (TRADITIONAL SORT)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'SWEDISH' + os.sep] = self.Swedish
        languages[os.sep + 'TURKISH' + os.sep] = self.Turkish

        languages[os.sep + 'NEU' + os.sep] = self.Neutral
        languages[os.sep + 'ARA' + os.sep] = self.Arabic
        languages[os.sep + 'CHS' + os.sep] = self.Chinese_Simplified
        languages[os.sep + 'CHT' + os.sep] = self.Chinese_Traditional
        languages[os.sep + 'CSY' + os.sep] = self.Czech
        languages[os.sep + 'DAN' + os.sep] = self.Danish
        languages[os.sep + 'NLD' + os.sep] = self.Dutch
        languages[os.sep + 'ENU' + os.sep] = self.English
        languages[os.sep + 'FIN' + os.sep] = self.Finnish
        languages[os.sep + 'FRA' + os.sep] = self.French
        languages[os.sep + 'DEU' + os.sep] = self.German
        languages[os.sep + 'ELL' + os.sep] = self.Greek
        languages[os.sep + 'HEB' + os.sep] = self.Hebrew
        languages[os.sep + 'HUN' + os.sep] = self.Hungarian
        languages[os.sep + 'ITA' + os.sep] = self.Italian
        languages[os.sep + 'JPN' + os.sep] = self.Japanese
        languages[os.sep + 'KOR' + os.sep] = self.Korean
        languages[os.sep + 'NOR' + os.sep] = self.Norwegian
        languages[os.sep + 'PLK' + os.sep] = self.Polish
        languages[os.sep + 'PTB' + os.sep] = self.Portuguese_Brazil
        languages[os.sep + 'PTG' + os.sep] = self.Portuguese_Portugal
        languages[os.sep + 'RUS' + os.sep] = self.Russian
        languages[os.sep + 'ESN' + os.sep] = self.Spanish
        languages[os.sep + 'SVE' + os.sep] = self.Swedish
        languages[os.sep + 'TRK' + os.sep] = self.Turkish

        languages[os.sep + 'neu' + os.sep] = self.Neutral
        languages[os.sep + 'ara' + os.sep] = self.Arabic
        languages[os.sep + 'chs' + os.sep] = self.Chinese_Simplified
        languages[os.sep + 'cht' + os.sep] = self.Chinese_Traditional
        languages[os.sep + 'csy' + os.sep] = self.Czech
        languages[os.sep + 'dan' + os.sep] = self.Danish
        languages[os.sep + 'nld' + os.sep] = self.Dutch
        languages[os.sep + 'enu' + os.sep] = self.English
        languages[os.sep + 'fin' + os.sep] = self.Finnish
        languages[os.sep + 'fra' + os.sep] = self.French
        languages[os.sep + 'deu' + os.sep] = self.German
        languages[os.sep + 'ell' + os.sep] = self.Greek
        languages[os.sep + 'heb' + os.sep] = self.Hebrew
        languages[os.sep + 'hun' + os.sep] = self.Hungarian
        languages[os.sep + 'ita' + os.sep] = self.Italian
        languages[os.sep + 'jpn' + os.sep] = self.Japanese
        languages[os.sep + 'kor' + os.sep] = self.Korean
        languages[os.sep + 'nor' + os.sep] = self.Norwegian
        languages[os.sep + 'plk' + os.sep] = self.Polish
        languages[os.sep + 'ptb' + os.sep] = self.Portuguese_Brazil
        languages[os.sep + 'ptg' + os.sep] = self.Portuguese_Portugal
        languages[os.sep + 'rus' + os.sep] = self.Russian
        languages[os.sep + 'esn' + os.sep] = self.Spanish
        languages[os.sep + 'sve' + os.sep] = self.Swedish
        languages[os.sep + 'trk' + os.sep] = self.Turkish

        self.mLanguages = languages

    def getLanguage(self, aPath):

        language = UnknownSubstance.getItemByPath(self.mLanguages, aPath)

        if language is not None:
            return language

        return UnknownSubstance.unknown('UNKNOWN LANGUAGE', aPath)

    def getPathKey(self, aValue):

        return UnknownSubstance.getKeyPathByValue(
            self.mCalligraphicLanguages, aValue)
