import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QLabel
)

#for resource loading
# def resource_path(filename):
#     """Возвращает путь к ресурсу внутри .app или рядом со скриптом"""
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, filename)
#     return os.path.join(os.path.abspath("."), filename)
# DB_PATH = resource_path("ur_bible.db")
DB_PATH = "../../sqlite/ur_bible.db"
print("DB_PATH =", DB_PATH) 

class BibleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bible ur (SQLite)")
        self.resize(800, 600)

        # Layouts
        main_layout = QVBoxLayout()
        combo_layout = QHBoxLayout()

        # Виджеты
        self.book_label = QLabel("Книга:")
        self.book_combo = QComboBox()
        self.chapter_label = QLabel("Глава:")
        self.chapter_combo = QComboBox()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        # Компоновка
        combo_layout.addWidget(self.book_label)
        combo_layout.addWidget(self.book_combo)
        combo_layout.addWidget(self.chapter_label)
        combo_layout.addWidget(self.chapter_combo)

        main_layout.addLayout(combo_layout)
        main_layout.addWidget(self.text_area)

        self.setLayout(main_layout)

        # Подключение к БД
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Загрузка книг
        self.load_books()

        # События
        self.book_combo.currentIndexChanged.connect(self.load_chapters)
        self.chapter_combo.currentIndexChanged.connect(self.load_text)

    def load_books(self):
        self.cursor.execute("SELECT _id, biblename FROM urbible ORDER BY _id")
        books = self.cursor.fetchall()
        self.book_combo.clear()
        for book_id, name in books:
            self.book_combo.addItem(name, book_id)
        self.load_chapters()

    def load_chapters(self):
        book_id = self.book_combo.currentData()
        if book_id is None:
            return
        self.cursor.execute("SELECT chapters FROM urbible WHERE _id = ?", (book_id,))
        max_chapter = self.cursor.fetchone()[0]
        self.chapter_combo.clear()
        for ch in range(1, max_chapter + 1):
            self.chapter_combo.addItem(str(ch), ch)
        self.load_text()

    def load_text(self):
        book_id = self.book_combo.currentData()
        chapter = self.chapter_combo.currentData()
        if book_id is None or chapter is None:
            return
        self.cursor.execute(f"""
            SELECT poem, poemtext
            FROM urtext
            WHERE bible = ? AND chapter = ?
            ORDER BY poem
        """, (book_id, chapter))
        verses = self.cursor.fetchall()
        content = "\n".join([f"{v}. {t}" for v, t in verses])
        self.text_area.setPlainText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BibleApp()
    window.show()
    sys.exit(app.exec_())
