import sqlite3
import json
from pathlib import Path

# ====================== НАСТРОЙКИ ======================
DB_PATH = "sqlite/ru_bible.db"
PROJECT_NAME = "the-holy-bible"
OUTPUT_DIR = Path("vue-bible-project")

TRANSLATION_CODE = "ru_synodal"
TRANSLATION_VERSION = "2025-04-06"
LANGUAGE = "ru"
LICENSE = "CC-BY-4.0"

# =====================================================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=== Исправленная генерация с UTF-8 ===\n")

    create_structure()
    generate_json_fixed_encoding()
    print("\nJSON-файлы готовы. Теперь пересобери проект:")
    print(f"cd {OUTPUT_DIR}")
    print("npm run build")
    print("npx wrangler pages deploy dist --project-name the-holy-bible --commit-dirty=true")


def create_structure():
    (OUTPUT_DIR / "public" / "translations" / TRANSLATION_CODE / "books").mkdir(parents=True, exist_ok=True)
    print("✓ Папки созданы")


def generate_json_fixed_encoding():
    json_base = OUTPUT_DIR / "public" / "translations" / TRANSLATION_CODE / "books"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Получаем книги
    cursor.execute("SELECT _id, biblename, chapters FROM rubible ORDER BY _id")
    books = cursor.fetchall()

    for book in books:
        book_id = book[0]
        book_name = book[1]
        max_chapters = book[2] or 150

        # Принудительно декодируем название книги
        if isinstance(book_name, bytes):
            book_name = book_name.decode('windows-1251', errors='replace')
        book_name = str(book_name).strip()

        book_code = {
            1:"GEN",2:"EXO",3:"LEV",4:"NUM",5:"DEU",6:"JOS",7:"JDG",8:"RUT",
            9:"1SA",10:"2SA",11:"1KI",12:"2KI",13:"1CH",14:"2CH",15:"EZR",16:"NEH",
            17:"EST",18:"JOB",19:"PSA",20:"PRO",21:"ECC",22:"SNG",23:"ISA",24:"JER",
            25:"LAM",26:"EZK",27:"DAN",28:"HOS",29:"JOL",30:"AMO",31:"OBA",32:"JON",
            33:"MIC",34:"NAM",35:"HAB",36:"ZEP",37:"HAG",38:"ZEC",39:"MAL",
            40:"MAT",41:"MRK",42:"LUK",43:"JHN",44:"ACT",45:"ROM",46:"1CO",47:"2CO",
            48:"GAL",49:"EPH",50:"PHP",51:"COL",52:"1TH",53:"2TH",54:"1TI",55:"2TI",
            56:"TIT",57:"PHM",58:"HEB",59:"JAS",60:"1PE",61:"2PE",62:"1JN",63:"2JN",
            64:"3JN",65:"JUD",66:"REV"
        }.get(book_id, f"UNK{book_id:02d}")

        book_no = f"{book_id:02d}"
        book_dir = json_base / f"{book_no}-{book_code}"
        book_dir.mkdir(parents=True, exist_ok=True)

        for ch in range(1, max_chapters + 1):
            cursor.execute("""
                SELECT poem, poemtext 
                FROM rutext 
                WHERE bible = ? AND chapter = ? 
                ORDER BY poem
            """, (book_id, ch))

            verses = cursor.fetchall()

            if not verses:
                continue

            clean_verses = []
            for v in verses:
                text = v[1]
                if isinstance(text, bytes):
                    text = text.decode('windows-1251', errors='replace')
                clean_verses.append({"verse": v[0], "text": text})

            data = {
                "translation": TRANSLATION_CODE,
                "translation_version": TRANSLATION_VERSION,
                "language": LANGUAGE,
                "license": LICENSE,
                "book": book_name,
                "book_code": book_code,
                "book_number": book_id,
                "chapter": ch,
                "verses": clean_verses
            }

            with open(book_dir / f"{ch:03d}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ {book_name} ({book_code}) — {max_chapters} глав")

    conn.close()
    print("\n✓ Все JSON-файлы сгенерированы с правильной кодировкой UTF-8")


if __name__ == "__main__":
    main()
