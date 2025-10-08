**List of languages ​​of the Holy Bible:**
```
af - Bybel
am - መጽሐፍ ቅዱስ
ara - الكتاب المقدس
be - Біблія
bg - Библия
## HolyBible — корпуса переводов Библии

Проект собирает и поставляет тексты Библии на множестве языков в двух форматах в репозитории:

- `xml/` — исходные XML-файлы переводов (по коду языка, напр. `ru` → `ru*bible.xml`);
- `sqlite/` — предварительно сформированные sqlite-базы для каждого языка (`ru_bible.db`, `en_bible.db` и т.д.);
- `src/python/<lang>/bible_app.py` — небольшой примерный python-приложение для каждого языка (запуск и поиск по Библии);
- `generatos/` — утилиты для извлечения/генерации данных (скрипты и shell-обёртки).

Цель: дать простой набор переводов и минимальные приложения для их просмотра и интеграции.

## Быстрый старт

1) Создайте виртуальное окружение и установите зависимости (в каталоге `src/python` или корне проекта):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # если файла нет — установите нужные пакеты вручную
```

2) Запуск примера для языка (например, русский):

```bash
cd src/python
python ./ru/bible_app.py
```

Каждая папка `src/python/<код_языка>/` может содержать свой `requirements.txt` и `bible_app.py` — смотрите соответствующую папку.

## Структура репозитория — ключевые директории

- `xml/` — исходные XML-файлы переводов. Используются генераторами для построения sqlite.
- `sqlite/` — sqlite-файлы, готовые для использования приложениями.
- `src/python/` — демо-приложения на Python по языкам. Внутри каждой папки: `bible_app.py`, `requirements.txt`.
- `generatos/` — вспомогательные скрипты (например, `extract_bible_langs.py`, `generate_apps.sh`).

## Список поддерживаемых языков (код → название)

af — Bybel
am — መጽሐፍ ቅዱስ
ara — الكتاب المقدس
be — Біблія
bg — Библия
bn — পবিত্র বাইবেল
cs — Bible
da — Bibelen
de — Bibel
du — Bijbel
en — The Bible
es — Biblia
et — Piibel
fa — کتاب مقدس
fi — Raamattu
fr — La Bible
gr — Αγία Γραφή
heb — הקודש במקרא
hin — पवित्र बाइबिल
hr — Biblija
hu — Szent Biblia
hy — ԱՍՏՈՒԱԾԱՇՈՒՆՉ
is — Biblían
it — Bibbia
jap — 日本聖書
ka — ბიბლია
kk — Киелі Кітап
ko — 성경
la — Biblia Sacra
lt — Biblija
lv — BĪBELE
mk — Библија
no — Bibelen
pl — Biblia, Pismo Święte
pt — Bíblia
ro — Biblia
ru — Библия. Русский Синодальный перевод
sk — Biblia
sq — Bibla e Shenjtë
sr — Библија
sv — BIBELN
sw — Biblia Takatifu
tam — பரிசுத்த வேதாகமம்
th — คัมภีร์ไบเบิล
tl — Bibliya
tr — Kutsal Kitap
uk — Біблія
ur — انجیل مقدس
vi — Kinh Thánh
zh — 简体中文和合本

## Полезные примечания для разработчиков

- Если вы хотите пересобрать sqlite-базы — посмотрите `generatos/generate_apps.sh` и `generatos/extract_bible_langs.py`.
- В `src/python/*/bible_app.py` демонстрируется простой способ открытия sqlite и выполнения поиска по стихам — используйте его как шаблон для новых интеграций.
- Файлы переводов большие — учитывайте время чтения/парсинга при разработке.

Если нужно — могу оформить более подробный раздел «Как собрать sqlite из XML» или добавить пример Для Docker/CI.
