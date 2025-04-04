CREATE TABLE flashcards (
    id INTEGER PRIMARY KEY,
    character TEXT,
    romaji TEXT,
    meaning TEXT,
    audio_url TEXT,
    type TEXT CHECK(type IN ('hiragana', 'hiraganaCombi', 'katakana', 'katakanaCombi' 'kanji'))
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    flashcard_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id)
);
