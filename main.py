import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import csv
import os
import requests
from io import StringIO
from colorama import init, Fore, Back, Style
import random

# Инициализация colorama
init(autoreset=True)

# ========== ССЫЛКА НА ТВОЙ CSV С ГИТХАБА ==========
GITHUB_CSV_URL = "https://raw.githubusercontent.com/твой-логин/твой-репозиторий/main/doxbar.csv"

# ========== ГРАДИЕНТНЫЕ ЦВЕТА (ЗЕЛЁНЫЙ) ==========
GREEN_GRADIENT = [
    Fore.LIGHTBLACK_EX + Style.BRIGHT,  # Тёмно-серый (для контраста)
    Fore.GREEN,                          # Зелёный
    Fore.LIGHTGREEN_EX,                   # Светло-зелёный
    Fore.GREEN + Style.BRIGHT,            # Ярко-зелёный
    Fore.LIGHTGREEN_EX + Style.BRIGHT,    # Очень светлый
]

def gradient_text(text, colors=GREEN_GRADIENT):
    """Применяет градиент к тексту"""
    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += color + char
    return result + Style.RESET_ALL

def print_gradient_banner():
    """Печатает баннер с градиентом"""
    banner = """
    ⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⡿⠋⠉⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠙⠿⣿⣿⣿
    ⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢹⣿⣿
    ⣿⣿⠁⠄⣀⣤⣤⣄⣀⠄⠄⠄⠄⠄⠄⣀⣤⣤⣤⣄⠄⠄⢿⣿
    ⣿⡇⠄⠚⠉⠛⠿⢿⣿⣷⡄⠄⠄⢠⣾⣿⡿⠿⠛⠉⠓⠄⢸⣿
    ⣿⡇⠄⠄⠄⣀⣀⠄⠙⣿⡅⠄⠄⢨⡿⠋⠄⣀⣀⠄⠄⠄⢸⣿
    ⣿⡇⢀⣴⣿⣿⣿⣿⣶⣼⣷⠄⠄⠈⢠⣶⣿⣿⣿⣿⣦⣀⣸⣿
    ⣿⡇⠘⠋⠉⠉⠉⠁⠄⢸⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⣿
    ⣿⣿⡄⠄⠄⠄⠄⠄⠄⣾⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣼⣿
    ⣿⣿⡽⣦⣤⠤⠤⠄⣾⢿⣿⠄⠄⠄⠳⡄⠠⠤⣤⣤⣴⢿⣿⣿
    ⣿⣿⣧⣻⣽⣦⣄⠄⠉⠸⡇⠄⠄⡀⠄⠁⠄⢀⣾⢏⡟⣼⣿⣿
    ⣿⣿⣿⣧⡹⣿⠿⢿⣷⣿⣿⠟⢿⣿⣶⣶⣾⠿⣿⡟⣼⣿⣿⣿
    ⣿⣿⣿⣿⣧⡘⢿⣦⡈⡉⠉⠛⠒⠋⠉⠉⠁⣠⢏⣼⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣷⡘⢿⠄⠁⠙⣿⣿⠂⠄⠄⡴⢃⣾⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣎⠄⠄⢰⣿⣿⠄⠄⠄⣠⣿⣿⣿⣿⣿⣿⣿
    """
    print(gradient_text(banner))
    print(gradient_text("🔥 DOX BAR — OSINT TOOL (GITHUB CSV)"))
    print()

def print_menu():
    """Печатает меню с градиентом"""
    menu_items = [
        "1. Поиск по номеру",
        "2. Поиск по юзернейму",
        "3. Поиск по фото (имитация)",
        "4. Добавить запись в CSV",
        "5. Показать всю базу",
        "0. Назад к командам"
    ]
    
    for i, item in enumerate(menu_items):
        if i == 0:
            print(GREEN_GRADIENT[1] + "╔══════════════════════════╗")
        color = GREEN_GRADIENT[i % len(GREEN_GRADIENT)]
        print(color + f"║ {item:<24} ║")
        if i == len(menu_items) - 1:
            print(GREEN_GRADIENT[1] + "╚══════════════════════════╝")
        else:
            print(GREEN_GRADIENT[1] + "╟──────────────────────────╢")

def download_csv_from_github():
    """Скачивает CSV с GitHub и возвращает список словарей"""
    try:
        print(Fore.YELLOW + "🔄 Загружаем базу данных с GitHub...")
        response = requests.get(GITHUB_CSV_URL)
        response.raise_for_status()
        content = response.text
        reader = csv.DictReader(StringIO(content))
        data = list(reader)
        print(Fore.GREEN + f"✅ Загружено {len(data)} записей с GitHub")
        return data
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка загрузки CSV: {e}")
        return []

def save_to_csv(data):
    """Сохраняет данные обратно в CSV"""
    try:
        with open('doxbar_local.csv', 'w', newline='', encoding='utf-8') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        print(Fore.GREEN + "✅ Данные сохранены в doxbar_local.csv")
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка сохранения: {e}")

def search_in_csv(data, search_term, field="phone"):
    """Ищет запись по полю (phone или username)"""
    results = []
    for row in data:
        if row.get(field, "").lower() == search_term.lower():
            results.append(row)
    return results

def print_result(result):
    """Печатает результат с градиентом"""
    print(gradient_text("\n" + "═" * 50))
    print(gradient_text(f"👤 Имя: {result.get('fullname', '—')}"))
    print(gradient_text(f"📞 Телефон: {result.get('phone', '—')}"))
    print(gradient_text(f"🌐 Username: {result.get('username', '—')}"))
    print(gradient_text(f"📍 Адрес: {result.get('address', '—')}"))
    print(gradient_text(f"🔗 Соцсети: {result.get('social_links', '—')}"))
    print(gradient_text(f"📝 Комментарий: {result.get('comment', '—')}"))
    print(gradient_text("═" * 50))

def search_by_number(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gradient_banner()
    
    number = input(gradient_text("Введите номер (+79161234567): ")).strip()
    results = search_in_csv(data, number, field="phone")
    
    if results:
        print(gradient_text("\n✅ Найдено в базе:"))
        for r in results:
            print_result(r)
    else:
        print(Fore.RED + "❌ В базе не найдено.")
    
    # Доп. инфо через библиотеку
    try:
        parsed = phonenumbers.parse(number)
        loc = geocoder.description_for_number(parsed, "ru")
        oper = carrier.name_for_number(parsed, "ru")
        tz = timezone.time_zones_for_number(parsed)
        print(gradient_text("\n📡 Дополнительная информация:"))
        print(gradient_text(f"📍 Регион: {loc}"))
        print(gradient_text(f"📡 Оператор: {oper}"))
        print(gradient_text(f"🕒 Часовой пояс: {tz}"))
    except:
        print(Fore.YELLOW + "⚠️ Не удалось получить данные через библиотеку.")

def search_by_username(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gradient_banner()
    
    username = input(gradient_text("Введите username (без @): ")).strip()
    results = search_in_csv(data, username, field="username")
    
    if results:
        print(gradient_text("\n✅ Найдено в базе:"))
        for r in results:
            print_result(r)
    else:
        print(Fore.RED + "❌ В базе не найдено.")

def search_by_photo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gradient_banner()
    
    print(gradient_text("🔍 Поиск по фото (имитация)"))
    print(gradient_text("📸 В разработке..."))

def add_record(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gradient_banner()
    
    print(gradient_text("➕ Добавление новой записи"))
    
    new_record = {
        'phone': input(gradient_text("Телефон: ")).strip(),
        'username': input(gradient_text("Username: ")).strip(),
        'fullname': input(gradient_text("Полное имя: ")).strip(),
        'address': input(gradient_text("Адрес: ")).strip(),
        'social_links': input(gradient_text("Соцсети: ")).strip(),
        'comment': input(gradient_text("Комментарий: ")).strip()
    }
    
    data.append(new_record)
    save_to_csv(data)
    print(gradient_text("✅ Запись добавлена!"))

def show_all(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gradient_banner()
    
    if not data:
        print(Fore.RED + "❌ База пуста")
        return
    
    print(gradient_text(f"📊 Всего записей: {len(data)}"))
    for i, row in enumerate(data, 1):
        print(gradient_text(f"\n--- Запись {i} ---"))
        print(gradient_text(f"📞 {row.get('phone', '—')}"))
        print(gradient_text(f"👤 {row.get('fullname', '—')}"))
        print(gradient_text(f"🌐 @{row.get('username', '—')}"))

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Загружаем базу с GitHub
    db_data = download_csv_from_github()
    
    if not db_data:
        print(Fore.RED + "❌ Не удалось загрузить базу. Проверь ссылку.")
        input(Fore.YELLOW + "Нажми Enter для выхода...")
        return
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_gradient_banner()
        print_menu()
        
        choice = input(gradient_text("\nВыбери опцию: ")).strip()
        
        if choice == "1":
            search_by_number(db_data)
        elif choice == "2":
            search_by_username(db_data)
        elif choice == "3":
            search_by_photo()
        elif choice == "4":
            add_record(db_data)
        elif choice == "5":
            show_all(db_data)
        elif choice == "0":
            print(gradient_text("👋 Выход..."))
            break
        else:
            print(Fore.RED + "❌ Неверный ввод.")
        
        input(gradient_text("\nНажми Enter, чтобы продолжить..."))

if __name__ == "__main__":
    main()
