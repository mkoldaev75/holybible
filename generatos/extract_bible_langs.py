import os
import xml.etree.ElementTree as ET

input_dir = "xml"
output_file = "languages.txt"

with open(output_file, "w", encoding="utf-8") as out_f:
    for filename in sorted(os.listdir(input_dir)):
        if not filename.endswith(".xml"):
            continue
        filepath = os.path.join(input_dir, filename)
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            version_elem = root.find(".//version")
            if version_elem is not None and "language" in version_elem.attrib:
                lang_code = version_elem.get("language")
                lang_name = version_elem.text.strip() if version_elem.text else ""
                out_f.write(f"{lang_code} - {lang_name}\n")
                print(f"✅ {lang_code}: {lang_name}")
            else:
                print(f"⚠️  Пропущен (нет <version language=...>): {filename}")
        except ET.ParseError as e:
            print(f"❌ Ошибка разбора XML в {filename}: {e}")
        except Exception as e:
            print(f"💥 Неожиданная ошибка с {filename}: {e}")

print(f"\nГотово! Результат сохранён в '{output_file}'")