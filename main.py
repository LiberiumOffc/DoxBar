import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import csv
import os
import requests
from io import StringIO

# ========== ССЫЛКА НА ТВОЙ CSV С ГИТХАБА ==========
# Пример: https://raw.githubusercontent.com/твой-логин/твой-репозиторий/main/doxbar.csv
GITHUB_CSV_URL = "https://raw.githubusercontent.com/твой-логин/твой-репозиторий/main/doxbar.csv"

def download_csv_from_github():
    """Скачивает CSV с GitHub и возвращает список словарей"""
    try:
        response = requests.get(GITHUB_CSV_URL)
        response.raise_for_status()
        content = response.text
        reader = csv.DictReader(StringIO(content))
        data = list(reader)
        print(f"✅ Загружено {len(data)} записей с GitHub")
        return data
    except Exception as e:
        print(f"❌ Ошибка загрузки CSV: {e}")
        return []

def search_in_csv(data, search_term, field="phone"):
    """Ищет запись по полю (phone или username)"""
    results = []
    for row in data:
        if row.get(field, "").lower() == search_term.lower():
            results.append(row)
    return results

def ascii_logo():
    print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡒⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡖⠁⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠈⢳⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⢹⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⡿⠀⠀⢠⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢻⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⠁⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠈⣯⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⡞⠀⠀⠀⠈⢻⡀⠀⠀⠀⠀⠀⣀⣤⡴⠶⠞⠛⠛⠛⠛⠛⠻⠶⢶⣤⣀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⢸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠘⣷⡀⠀⣀⡴⢛⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡛⢦⣄⠀⠀⣼⠇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀
⢰⡀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠈⠳⣾⣭⢤⣄⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⢀⡤⣈⣷⠞⠃⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⡄
⢸⢷⡀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⡜⡇
⠈⣇⠱⣄⠀⠸⣧⠀⠀⠀⠀⠀⠄⣀⣀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣀⣀⠠⠀⠀⠀⠀⠀⣰⠇⠀⢀⠞⢰⠃
⠀⢿⠀⠈⢦⡀⠘⢷⣄⠀⢀⣀⡀⣀⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣀⣀⡀⢀⠀⣠⡼⠋⢀⡴⠁⠀⣹⠀
⠀⠸⡄⠑⡀⠉⠢⣀⣿⠛⠒⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠒⠋⢻⣀⠴⠋⢀⠄⢀⡇⠀
⠀⠀⢣⠀⠈⠲⢄⣸⡇⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢔⠀⠀⠀⠘⣏⣀⠔⠁⠂⡸⠀⠀
⠀⠀⠘⡄⠀⠀⠀⠉⢻⡄⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠋⠀⠀⠀⢠⠇⠀⠀
⠀⠀⠀⠙⢶⠀⠀⠀⢀⡿⠀⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠀⢾⡀⠀⠀⠀⡴⠎⠀⠀⠀
⠀⠀⠀⠀⠀⠙⢦⡀⣸⠇⠀⠀⠀⠈⠹⡑⠲⠤⣀⡀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⢊⠍⠃⠀⠀⠀⠘⣧⢀⡤⠊⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⣿⠀⠀⠀⠀⠀⠀⠈⠒⢤⠤⠙⠗⠦⠼⠀⠀⠀⠠⠴⠺⠟⠤⡤⠔⠁⠀⠀⠀⠀⠀⠀⢸⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣄⠀⠀⡑⢯⡁⠀⠀⠀⠀⠀⠇⠀⠀⠀⠰⠀⠀⠀⠀⠀⢈⡩⢋⠀⠀⢠⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠈⠀⠻⢦⠀⠀⠀⡰⠀⠀⠀⠀⠀⢇⠀⠀⠀⡠⡛⠀⠁⠀⢰⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⢡⠑⠤⣀⠈⢢⠀⠀⠀⡴⠃⣀⠤⠊⡄⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⣄⠀⠀⠀⠳⠀⢀⠉⠙⢳⠀⡜⠉⠁⡀⠀⠼⠀⠀⠀⣠⡴⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⠀⠘⣆⠐⠐⠌⠂⠚⠀⠡⠊⠀⢠⠃⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠠⠈⠢⣄⡀⠀⠀⠀⢀⣀⠴⠃⠀⣴⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡁⠐⠀⠈⠉⠁⠈⠁⠀⠒⢀⡴⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⣄⣀⣀⣀⣀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)
    print("🔥 DOX BAR — OSINT TOOL (GitHub CSV)")
    print("1. Поиск по номеру")
    print("2. Поиск по юзернейму")
    print("0. Назад к командам")
    print()

def search_by_number(data):
    number = input("Введите номер (+79161234567): ").strip()
    results = search_in_csv(data, number, field="phone")
    
    if results:
        print("\n✅ Найдено в базе:")
        for r in results:
            print(f"👤 Имя: {r.get('fullname', '—')}")
            print(f"📞 Телефон: {r.get('phone', '—')}")
            print(f"🌐 Username: {r.get('username', '—')}")
            print(f"📍 Адрес: {r.get('address', '—')}")
            print(f"🔗 Соцсети: {r.get('social_links', '—')}")
            print(f"📝 Комментарий: {r.get('comment', '—')}")
    else:
        print("❌ В базе не найдено.")
    
    # Доп. инфо через библиотеку
    try:
        parsed = phonenumbers.parse(number)
        loc = geocoder.description_for_number(parsed, "ru")
        oper = carrier.name_for_number(parsed, "ru")
        tz = timezone.time_zones_for_number(parsed)
        print(f"\n📍 Регион: {loc}")
        print(f"📡 Оператор: {oper}")
        print(f"🕒 Часовой пояс: {tz}")
    except:
        print("⚠️ Не удалось получить данные через библиотеку.")

def search_by_username(data):
    username = input("Введите username (без @): ").strip()
    results = search_in_csv(data, username, field="username")
    
    if results:
        print("\n✅ Найдено в базе:")
        for r in results:
            print(f"👤 Имя: {r.get('fullname', '—')}")
            print(f"📞 Телефон: {r.get('phone', '—')}")
            print(f"🌐 Username: {r.get('username', '—')}")
            print(f"📍 Адрес: {r.get('address', '—')}")
            print(f"🔗 Соцсети: {r.get('social_links', '—')}")
            print(f"📝 Комментарий: {r.get('comment', '—')}")
    else:
        print("❌ В базе не найдено.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Загружаем базу с GitHub
    print("🔄 Загружаем базу данных с GitHub...")
    db_data = download_csv_from_github()
    
    if not db_data:
        print("❌ Не удалось загрузить базу. Проверь ссылку.")
        input("Нажми Enter для выхода...")
        return
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ascii_logo()
        choice = input("Выбери опцию: ").strip()
        
        if choice == "1":
            search_by_number(db_data)
        elif choice == "2":
            search_by_username(db_data)
        elif choice == "0":
            print("Возврат к командам...")
            break
        else:
            print("Неверный ввод.")
        
        input("\nНажми Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()
