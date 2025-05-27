from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Kanji:
    """
    Représente un kanji avec ses propriétés.

    Attributes:
        id (int):  Identifiant un kanji
        kanji (str) : Caractère kanji
        onyomi (list[str]) : Lectures on'yomi (chinoise)
        kunyomi (list[str]) : Lectures kun'yomi (japonaise)
        JLPT (str) : Niveau JLPT (N1 à N5)
    """
    id: int
    kanji: str
    onyomi: list[str]
    kunyomi: list[str]
    meaning: str
    JLPT: str


kanjis: dict[int, str, Kanji] = {}


@dataclass
class Hiragana:
    """
    Représente un caractère hiragana.

    Attributes:
        id (int): Identifiant unique
        kana (str): Caractère hiragana
        romaji (str): Transcription en romaji
    """
    id: int
    kana: str
    romaji: str


hiraganas: dict[int, str, Hiragana] = {}


@dataclass
class Katakana:
    """
    Représente un caractère katakana.

    Attributes:
        id (int): Identifiant unique
        kana (str): Caractère katakana
        romaji (str): Transcription en romaji
    """
    id: int
    kana: str
    romaji: str


katakanas: dict[int, str, Katakana] = {}


@dataclass
class User:
    """
    Représente un utilisateur du système.

    Attributes :
        id (int): Identifiant unique
        username (str): Nom d'utilisateur
        password (str): Mot de passe "hashed"
    """
    id: int
    username: str
    password: str


@dataclass
class KanaItem(BaseModel):
    """
    Modèle Pydantic pour les items kana (hiragana/katakana/kanji).

    Attributes:
        id (str): Identifiant
        contenu (str) : Caractère japonais
        romaji (str, optional): Caractère kanji si applicable
    """
    id: str
    contenu: str
    romaji: str | None = None  # si c'est un hira ou kata
    kanji: str | None = None  # si c'est un kanji