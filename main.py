import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import csv
import os
import requests
import time
import sys
from io import StringIO
from colorama import init, Fore, Style, Back

# Инициализация colorama
init(autoreset=True)

# ========== ТЫ ВСТАВЛЯЕШЬ СВОЮ ССЫЛКУ ЗДЕСЬ ==========
MY_CSV_URL = "https://raw.githubusercontent.com/твой-логин/твой-репозиторий/main/твой-файл.csv"
# ====================================================

# ========== ТВОЙ РИСУНОК ==========
YOUR_ASCII = """
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
"""

# ========== ЦВЕТА ==========
GREEN1 = Fore.GREEN
GREEN2 = Fore.LIGHTGREEN_EX
GREEN3 = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL

# ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
csv_data = []  # Сюда загружаются данные из CSV

def loading_animation(text="Загрузка", duration=1.5):
    """Красивая анимация загрузки"""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    for i in range(duration * 10):
        for char in chars:
            sys.stdout.write(f"\r{GREEN2}{text} {char} {GREEN1}{'█' * (i % 10)}")
            sys.stdout.flush()
            time.sleep(0.03)
    print()

def print_ascii():
    """Печатает твой ASCII-арт"""
    lines = YOUR_ASCII.split('\n')
    colors = [GREEN1, GREEN2, GREEN3, GREEN2]
    
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)
    print(RESET)

def load_csv_from_url():
    """Загружает CSV по ссылке из переменной MY_CSV_URL"""
    global csv_data
    try:
        print(YELLOW + f"🔗 Загружаем: {MY_CSV_URL}")
        loading_animation("Загрузка CSV", 2)
        
        # Проверяем, что ссылка заканчивается на .csv
        if not MY_CSV_URL.lower().endswith('.csv'):
            print(RED + "❌ Ссылка должна вести на .csv файл!")
            return False
        
        response = requests.get(MY_CSV_URL)
        response.raise_for_status()
        
        # Пробуем разные кодировки
        try:
            content = response.content.decode('utf-8')
        except:
            try:
                content = response.content.decode('cp1251')
            except:
                content = response.content.decode('latin-1')
        
        reader = csv.DictReader(StringIO(content))
        csv_data = list(reader)
        
        print(GREEN2 + f"✅ Загружено {len(csv_data)} записей")
        print(GREEN1 + f"📋 Колонки: {', '.join(reader.fieldnames)}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(RED + f"❌ Ошибка загрузки: {e}")
        return False
    except Exception as e:
        print(RED + f"❌ Ошибка чтения CSV: {e}")
        return False

def search_by_number():
    """Поиск по номеру телефона"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    
    number = input(GREEN2 + "Введите номер (+79161234567): ").strip()
    
    # Поиск в CSV
    found = False
    for row in csv_data:
        if row.get('phone', '').strip() == number:
            print(GREEN1 + "\n✅ Найдено в CSV:")
            for key, value in row.items():
                print(GREEN2 + f"{key}: {value}")
            found = True
            break
    
    if not found:
        print(YELLOW + "ℹ️ В CSV не найдено, ищем через библиотеку...")
    
    # Поиск через библиотеку phonenumbers
    try:
        parsed = phonenumbers.parse(number)
        loc = geocoder.description_for_number(parsed, "ru")
        oper = carrier.name_for_number(parsed, "ru")
        tz = timezone.time_zones_for_number(parsed)
        
        print(GREEN1 + "\n📡 Данные оператора:")
        print(GREEN2 + f"📍 Страна/регион: {loc}")
        print(GREEN2 + f"📡 Оператор: {oper}")
        print(GREEN2 + f"🕒 Часовой пояс: {tz}")
    except:
        print(RED + "❌ Не удалось получить данные через библиотеку")

def search_by_username():
    """Поиск по юзернейму"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    
    username = input(GREEN2 + "Введите username (без @): ").strip()
    
    found = False
    for row in csv_data:
        if row.get('username', '').strip().lower() == username.lower():
            print(GREEN1 + "\n✅ Найдено в CSV:")
            for key, value in row.items():
                print(GREEN2 + f"{key}: {value}")
            found = True
            break
    
    if not found:
        print(YELLOW + "❌ В CSV не найдено")

def search_by_photo():
    """Имитация поиска по фото"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    
    print(GREEN2 + "🔍 Поиск по фото (имитация)")
    loading_animation("Поиск по фото", 2)
    print(YELLOW + "📸 Функция в разработке")
    print(GREEN1 + "⚡ Скоро будет доступна")

def show_all_data():
    """Показать все загруженные данные"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    
    if not csv_data:
        print(RED + "❌ Нет загруженных данных")
        return
    
    print(GREEN1 + f"📊 Всего записей: {len(csv_data)}")
    print(GREEN2 + "-" * 50)
    
    for i, row in enumerate(csv_data, 1):
        print(GREEN3 + f"Запись {i}:")
        for key, value in row.items():
            if value:
                print(GREEN2 + f"  {key}: {value}")
        print(GREEN1 + "-" * 30)

def main():
    global csv_data
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    
    # Автоматически загружаем CSV при старте
    print(YELLOW + "🔄 Автоматическая загрузка CSV...")
    if load_csv_from_url():
        print(GREEN2 + "✅ CSV успешно загружен")
    else:
        print(RED + "❌ Не удалось загрузить CSV. Проверь ссылку в переменной MY_CSV_URL")
        input(YELLOW + "Нажми Enter для продолжения...")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_ascii()
        
        print(GREEN1 + "╔" + "═" * 50 + "╗")
        print(GREEN2 + "║" + " " * 15 + "DOX BAR — МЕНЮ" + " " * 16 + "║")
        print(GREEN3 + "╠" + "═" * 50 + "╣")
        print(GREEN1 + "║  1. Поиск по номеру телефона        ║")
        print(GREEN2 + "║  2. Поиск по юзернейму              ║")
        print(GREEN3 + "║  3. Поиск по фото (имитация)        ║")
        print(GREEN1 + "║  4. Показать все данные             ║")
        print(GREEN2 + "║  5. Перезагрузить CSV               ║")
        print(GREEN3 + "║  0. Выход                            ║")
        print(GREEN1 + "╚" + "═" * 50 + "╝")
        print(GREEN2 + f"📁 CSV записей: {len(csv_data)}")
        print()
        
        choice = input(GREEN2 + "Выбери пункт: ").strip()
        
        if choice == "1":
            search_by_number()
        elif choice == "2":
            search_by_username()
        elif choice == "3":
            search_by_photo()
        elif choice == "4":
            show_all_data()
        elif choice == "5":
            load_csv_from_url()
        elif choice == "0":
            print(GREEN3 + "👋 Выход...")
            break
        else:
            print(RED + "❌ Неверный выбор")
        
        input(GREEN2 + "\nНажми Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()
