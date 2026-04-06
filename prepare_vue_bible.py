#!/usr/bin/env python3
"""
Генератор JSON для всех языков Библии.
Формат: один файл на книгу (все главы внутри).
  translations/<code>/index.json         — список книг
  translations/<code>/books/<NN>-<CODE>.json — все главы книги
  translations/translations.json        — мастер-индекс
"""

import sqlite3
import json
from pathlib import Path
from collections import defaultdict

SQLITE_DIR = Path("sqlite")
OUTPUT_DIR = Path("vue-bible-project")
TRANSLATION_VERSION = "2025-04-06"
LICENSE = "CC-BY-4.0"

LANGUAGES = {
    "af":  ("af_afrikaans",   "Bybel",                "af"),
    "am":  ("am_amharic",     "መጽሐፍ ቅዱስ",             "am"),
    "ara": ("ara_arabic",     "الكتاب المقدس",          "ara"),
    "be":  ("be_belarusian",  "Біблія",                "be"),
    "bg":  ("bg_bulgarian",   "Библия",                "bg"),
    "bn":  ("bn_bengali",     "পবিত্র বাইবেল",           "bn"),
    "cs":  ("cs_czech",       "Bible",                 "cs"),
    "da":  ("da_danish",      "Bibelen",               "da"),
    "de":  ("de_luther",      "Bibel",                 "de"),
    "du":  ("du_dutch",       "Bijbel",                "du"),
    "en":  ("en_kjv",         "The Bible (KJV)",       "en"),
    "es":  ("es_reina",       "Biblia",                "es"),
    "et":  ("et_estonian",    "Piibel",                "et"),
    "fa":  ("fa_persian",     "کتاب مقدس",              "fa"),
    "fi":  ("fi_finnish",     "Raamattu",              "fi"),
    "fr":  ("fr_louis",       "La Bible",              "fr"),
    "gr":  ("gr_greek",       "Αγία Γραφή",            "gr"),
    "heb": ("heb_hebrew",     "הקודש במקרא",            "heb"),
    "hin": ("hin_hindi",      "पवित्र बाइबिल",            "hin"),
    "hr":  ("hr_croatian",    "Biblija",               "hr"),
    "hu":  ("hu_hungarian",   "Szent Biblia",          "hu"),
    "hy":  ("hy_armenian",    "Աdelays",              "hy"),
    "is":  ("is_icelandic",   "Biblían",               "is"),
    "it":  ("it_riveduta",    "Bibbia",                "it"),
    "jap": ("jap_japanese",   "日本聖書",                "jap"),
    "ka":  ("ka_georgian",    "ბიბლია",                "ka"),
    "kk":  ("kk_kazakh",      "Киелі Кітап",           "kk"),
    "ko":  ("ko_korean",      "성경",                    "ko"),
    "la":  ("la_latin",       "Biblia Sacra",          "la"),
    "lt":  ("lt_lithuanian",  "Biblija",               "lt"),
    "lv":  ("lv_latvian",     "Bībele",                "lv"),
    "mk":  ("mk_macedonian",  "Библија",               "mk"),
    "no":  ("no_norwegian",   "Bibelen",               "no"),
    "pl":  ("pl_polish",      "Biblia",                "pl"),
    "pt":  ("pt_portuguese",  "Bíblia",                "pt"),
    "ro":  ("ro_romanian",    "Biblia",                "ro"),
    "ru":  ("ru_synodal",     "Библия",                "ru"),
    "sk":  ("sk_slovak",      "Biblia",                "sk"),
    "sq":  ("sq_albanian",    "Bibla e Shenjtë",       "sq"),
    "sr":  ("sr_serbian",     "Библија",               "sr"),
    "sv":  ("sv_swedish",     "Bibeln",                "sv"),
    "sw":  ("sw_swahili",     "Biblia Takatifu",       "sw"),
    "tam": ("tam_tamil",      "பரிசுத்த வேதாகமம்",        "tam"),
    "th":  ("th_thai",        "คัมภีร์ไบเบิล",             "th"),
    "tl":  ("tl_tagalog",     "Bibliya",               "tl"),
    "tr":  ("tr_turkish",     "Kutsal Kitap",          "tr"),
    "uk":  ("uk_ukrainian",   "Біблія",                "uk"),
    "ur":  ("ur_urdu",        "انجیل مقدس",             "ur"),
    "vi":  ("vi_vietnamese",  "Kinh Thánh",            "vi"),
    "zh":  ("zh_chinese",     "简体中文和合本",           "zh"),
}

SYNODAL_LANGS = {"ru", "be", "uk", "ka", "mk"}
RTL_LANGS = {"ara", "heb", "fa", "ur"}

WESTERN = {
    1:"GEN",2:"EXO",3:"LEV",4:"NUM",5:"DEU",6:"JOS",7:"JDG",8:"RUT",
    9:"1SA",10:"2SA",11:"1KI",12:"2KI",13:"1CH",14:"2CH",15:"EZR",16:"NEH",
    17:"EST",18:"JOB",19:"PSA",20:"PRO",21:"ECC",22:"SNG",23:"ISA",24:"JER",
    25:"LAM",26:"EZK",27:"DAN",28:"HOS",29:"JOL",30:"AMO",31:"OBA",32:"JON",
    33:"MIC",34:"NAM",35:"HAB",36:"ZEP",37:"HAG",38:"ZEC",39:"MAL",
    40:"MAT",41:"MRK",42:"LUK",43:"JHN",44:"ACT",
    45:"ROM",46:"1CO",47:"2CO",48:"GAL",49:"EPH",50:"PHP",51:"COL",
    52:"1TH",53:"2TH",54:"1TI",55:"2TI",56:"TIT",57:"PHM",
    58:"HEB",59:"JAS",60:"1PE",61:"2PE",62:"1JN",63:"2JN",64:"3JN",
    65:"JUD",66:"REV"
}
SYNODAL = dict(WESTERN)
SYNODAL.update({
    45:"JAS",46:"1PE",47:"2PE",48:"1JN",49:"2JN",50:"3JN",51:"JUD",
    52:"ROM",53:"1CO",54:"2CO",55:"GAL",56:"EPH",57:"PHP",58:"COL",
    59:"1TH",60:"2TH",61:"1TI",62:"2TI",63:"TIT",64:"PHM",65:"HEB",66:"REV"
})


def dec(v):
    if isinstance(v, bytes):
        for e in ('utf-8', 'windows-1251', 'latin-1'):
            try: return v.decode(e)
            except UnicodeDecodeError: pass
        return v.decode('latin-1', errors='replace')
    return str(v).strip()


def generate_language(lang_code, translation_code, display_name, db_prefix):
    db_path = SQLITE_DIR / f"{lang_code}_bible.db"
    if not db_path.exists():
        print(f"  ✗ {lang_code}: not found")
        return False

    books_dir = OUTPUT_DIR / "public" / "translations" / translation_code / "books"
    books_dir.mkdir(parents=True, exist_ok=True)

    codes = SYNODAL if lang_code in SYNODAL_LANGS else WESTERN

    conn = sqlite3.connect(str(db_path))
    conn.text_factory = bytes
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT _id, biblename FROM {db_prefix}bible ORDER BY _id")
    except Exception as e:
        print(f"  ✗ {lang_code}: {e}")
        conn.close()
        return False

    book_info = {r[0]: dec(r[1]) for r in cur.fetchall()}

    # Один запрос — все стихи
    cur.execute(f"SELECT bible, chapter, poem, poemtext FROM {db_prefix}text ORDER BY bible, chapter, poem")
    all_verses = cur.fetchall()
    conn.close()

    # Группируем: book_id -> chapter -> [(poem, text)]
    tree = defaultdict(lambda: defaultdict(list))
    for row in all_verses:
        tree[row[0]][row[1]].append((row[2], dec(row[3])))

    books_meta = []
    for book_id in sorted(tree.keys()):
        code = codes.get(book_id, f"UNK{book_id:02d}")
        name = book_info.get(book_id, f"Book {book_id}")
        chapters = tree[book_id]
        filename = f"{book_id:02d}-{code}.json"

        # Один файл на книгу: все главы внутри
        chapters_data = {}
        for ch in sorted(chapters.keys()):
            chapters_data[str(ch)] = [{"verse": v[0], "text": v[1]} for v in chapters[ch]]

        book_data = {
            "translation": translation_code,
            "language": lang_code,
            "book": name,
            "book_code": code,
            "book_number": book_id,
            "chapters": chapters_data
        }

        with open(books_dir / filename, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False)

        books_meta.append({
            "file": filename,
            "code": code,
            "name": name,
            "chapters": len(chapters),
            "number": book_id
        })

    # index.json
    idx_path = OUTPUT_DIR / "public" / "translations" / translation_code / "index.json"
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump({
            "translation": translation_code,
            "translation_version": TRANSLATION_VERSION,
            "language": lang_code,
            "books": books_meta
        }, f, ensure_ascii=False)

    total_ch = sum(b["chapters"] for b in books_meta)
    print(f"  ✓ {lang_code:4s} → {len(books_meta)} книг, {total_ch} глав, {len(books_meta)+1} файлов")
    return True


def generate_master_index():
    items = []
    for lc in sorted(LANGUAGES.keys()):
        tc, name, _ = LANGUAGES[lc]
        idx = OUTPUT_DIR / "public" / "translations" / tc / "index.json"
        if not idx.exists():
            continue
        with open(idx, "r", encoding="utf-8") as f:
            d = json.load(f)
        if not d["books"]:
            continue
        items.append({
            "code": tc,
            "language": lc,
            "name": name,
            "books": len(d["books"]),
            "rtl": lc in RTL_LANGS
        })
    with open(OUTPUT_DIR / "public" / "translations" / "translations.json", "w", encoding="utf-8") as f:
        json.dump({"translations": items}, f, ensure_ascii=False, indent=2)
    print(f"\n✓ translations.json — {len(items)} переводов")


def main():
    print("=== Генерация Библии для всех языков ===\n")
    print("Формат: один файл на книгу (все главы внутри)\n")
    ok = err = 0
    for lc in sorted(LANGUAGES.keys()):
        tc, dn, dp = LANGUAGES[lc]
        if generate_language(lc, tc, dn, dp):
            ok += 1
        else:
            err += 1
    generate_master_index()

    # Подсчёт файлов
    total_files = sum(1 for _ in (OUTPUT_DIR / "public" / "translations").rglob("*") if _.is_file())
    print(f"\nГотово: {ok} языков, {err} ошибок")
    print(f"Всего файлов: {total_files} (лимит CF Pages: 20 000)")
    print(f"\ncd {OUTPUT_DIR} && npm run build")
    print("npx wrangler pages deploy dist --project-name the-holy-bible --commit-dirty=true")


if __name__ == "__main__":
    main()
