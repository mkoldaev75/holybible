## Python demo apps — краткий старт

Ниже — аккуратные и понятные инструкции для запуска демонстрационных Python-приложений, которые находятся в каталогах `src/python/<код_языка>/`.

1) Создайте виртуальное окружение и установите зависимости (рекомендуется выполнять из корня проекта или `src/python`):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # если файла нет — установите нужные пакеты вручную
```

2) Запуск примера для конкретного языка

Перейдите в `src/python` и запустите нужный скрипт. Пример для русского:

```bash
cd src/python
python ./ru/bible_app.py
```

Для другого языка — замените `ru` на код языка (например, `en`, `fr`, `es`):

```bash
python ./en/bible_app.py
```

3) Формат папок и примечания

- Каждая подпапка `src/python/<код_языка>/` обычно содержит два файла: `bible_app.py` и `requirements.txt` (иногда `requirements.txt` может отсутствовать).
- Приложения открывают sqlite-файл из корневой папки `sqlite/` (например, `sqlite/ru_bible.db`). Если нужной базы нет — используйте генераторы в `generatos/`.
- Если перевод большой, первый запуск может занять время из-за чтения/парсинга базы/файла.

Если хотите, могу добавить в эту документацию пример создания sqlite из XML (команду/скрипт из `generatos/`) или краткий Dockerfile для запуска приложений в контейнере.

---

Short (English):

1) Create venv and install deps:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2) Run demo (from `src/python`):

```bash
python ./ru/bible_app.py
```
