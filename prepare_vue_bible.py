import sqlite3
import json
from pathlib import Path

# ====================== НАСТРОЙКИ ======================
DB_PATH = "sqlite/ru_bible.db"          # Убедись, что путь правильный!
PROJECT_NAME = "the-holy-bible"
OUTPUT_DIR = Path("vue-bible-project")

TRANSLATION_CODE = "ru_synodal"
TRANSLATION_VERSION = "2025-04-06"
LANGUAGE = "ru"
LICENSE = "CC-BY-4.0"

# =====================================================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=== Создание Vue.js Библии для Cloudflare Pages ===\n")

    create_project_structure()
    generate_json_files()
    create_vue_files()

    print("=" * 85)
    print("✅ ГОТОВО!")
    print(f"Папка проекта: {OUTPUT_DIR.resolve()}")
    print("\nТеперь выполни:")
    print(f"   cd {OUTPUT_DIR}")
    print("   npm install")
    print("   npm run deploy")
    print("=" * 85)


def create_project_structure():
    (OUTPUT_DIR / "public" / "translations" / TRANSLATION_CODE / "books").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "src" / "components").mkdir(parents=True, exist_ok=True)
    print("✓ Структура папок создана")


def generate_json_files():
    json_base = OUTPUT_DIR / "public" / "translations" / TRANSLATION_CODE / "books"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT _id, biblename, chapters FROM rubible ORDER BY _id")
    books = cursor.fetchall()

    print(f"Найдено книг: {len(books)}")

    for book in books:
        book_id = book["_id"]
        book_name = book["biblename"].strip()
        max_chapters = book["chapters"] or 150

        book_code = {
            1:"GEN", 2:"EXO", 3:"LEV", 4:"NUM", 5:"DEU", 6:"JOS", 7:"JDG", 8:"RUT",
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

            data = {
                "translation": TRANSLATION_CODE,
                "translation_version": TRANSLATION_VERSION,
                "language": LANGUAGE,
                "license": LICENSE,
                "book": book_name,
                "book_code": book_code,
                "book_number": book_id,
                "chapter": ch,
                "verses": [{"verse": row["poem"], "text": row["poemtext"]} for row in verses]
            }

            with open(book_dir / f"{ch:03d}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    conn.close()
    print("✓ JSON-файлы успешно созданы\n")


def create_vue_files():
    base = OUTPUT_DIR

    # package.json
    (base / "package.json").write_text(f"""{{
  "name": "{PROJECT_NAME}",
  "version": "1.0.0",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "npm run build && wrangler pages deploy dist --project-name {PROJECT_NAME}",
    "deploy:preview": "npm run build && wrangler pages deploy dist --project-name {PROJECT_NAME} --branch preview"
  }},
  "dependencies": {{
    "vue": "^3.4.0",
    "vue-router": "^4.3.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }}
}}
""", encoding="utf-8")

    # vite.config.js
    (base / "vite.config.js").write_text("""import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/',
  build: { outDir: 'dist' }
})
""", encoding="utf-8")

    (base / "tailwind.config.js").write_text("""module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: { extend: {} },
  plugins: [],
}
""", encoding="utf-8")

    (base / "postcss.config.js").write_text("""module.exports = {
  plugins: { tailwindcss: {}, autoprefixer: {} }
}
""", encoding="utf-8")

    (base / "index.html").write_text("""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Святая Библия</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
""", encoding="utf-8")

    (base / "src" / "main.js").write_text("""import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/:translation?/:bookCode?/:chapter?', component: () => import('./components/BibleViewer.vue') }]
})

createApp(App).use(router).mount('#app')
""", encoding="utf-8")

    (base / "src" / "App.vue").write_text("""<template><router-view /></template>""", encoding="utf-8")

    (base / "src" / "index.css").write_text("""@tailwind base; @tailwind components; @tailwind utilities;""", encoding="utf-8")

    (base / "src" / "components" / "BibleViewer.vue").write_text("""<template>
  <div class="max-w-3xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8 text-center">{{ data?.book }} — Глава {{ data?.chapter }}</h1>
    <div v-if="data" class="space-y-5 text-lg leading-relaxed">
      <p v-for="verse in data.verses" :key="verse.verse">
        <span class="font-medium text-blue-600">{{ verse.verse }}.</span> {{ verse.text }}
      </p>
    </div>
    <div v-else class="text-center py-12 text-gray-500">Загрузка...</div>
  </div>
</template>

<script>
export default {
  data() { return { data: null } },
  async mounted() {
    try {
      const res = await fetch('/translations/ru_synodal/books/01-GEN/001.json')
      this.data = await res.json()
    } catch (e) {
      console.error(e)
    }
  }
}
</script>
""", encoding="utf-8")

    print("✓ Все Vue файлы созданы\n")


if __name__ == "__main__":
    main()
