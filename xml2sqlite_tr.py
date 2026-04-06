#!/usr/bin/env python3
"""
Конвертер trbible.xml → sqlite/tr_bible.db
Формат XML: <verse id="book.chapter.verse">текст</verse>
"""

import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

XML_PATH = Path("xml/trbible.xml")
DB_PATH = Path("sqlite/tr_bible.db")


def main():
    print(f"Парсинг {XML_PATH}...")
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    # Книги из <booknames>
    books = {}
    for book_el in root.findall(".//booknames/book"):
        name = book_el.get("name")
        idbook = book_el.get("idbook")
        chapters = int(book_el.get("chapters", 0))
        book_id = int(idbook.replace("book", ""))
        books[book_id] = {"name": name, "chapters": chapters}

    print(f"  Найдено {len(books)} книг")

    # Стихи из <verse id="book.chapter.verse">
    verses = []
    for verse_el in root.iter("verse"):
        vid = verse_el.get("id")
        text = (verse_el.text or "").strip()
        if not vid or not text:
            continue
        parts = vid.split(".")
        if len(parts) != 3:
            continue
        verses.append((int(parts[0]), int(parts[1]), int(parts[2]), text))

    print(f"  Найдено {len(verses)} стихов")

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE trbible (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            biblename TEXT,
            chapters INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE trtext (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            bible INTEGER,
            chapter INTEGER,
            poem INTEGER,
            poemtext TEXT
        )
    """)

    for book_id in sorted(books.keys()):
        b = books[book_id]
        cur.execute("INSERT INTO trbible (_id, biblename, chapters) VALUES (?, ?, ?)",
                    (book_id, b["name"], b["chapters"]))

    cur.executemany("INSERT INTO trtext (bible, chapter, poem, poemtext) VALUES (?, ?, ?, ?)", verses)

    conn.commit()
    conn.close()
    print(f"\n✓ {DB_PATH}: {len(books)} книг, {len(verses)} стихов")


if __name__ == "__main__":
    main()
