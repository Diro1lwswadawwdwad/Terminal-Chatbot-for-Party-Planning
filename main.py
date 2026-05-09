import json
import os
import sys

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {"parties": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def create_new_party(party_name):
    data = load_data()
    if party_name in data["parties"]:
        return f"❌ Ошибка: Вечеринка '{party_name}' уже существует!"
    data["parties"][party_name] = {
        "date": None,
        "venue": None,
        "guests": [],
        "bills": {},
        "suggestions": {},
        "voting": {
            "options": [],
            "votes": {}
        }
    }
    save_data(data)
    return f"✅ Вечеринка '{party_name}' создана! Самое время добавить гостей."

def add_guest_to_party(party_name, guest_name):
    data = load_data()
    party = data["parties"].get(party_name)
    if not party:
        return f"❌ Вечеринка '{party_name}' не найдена."
    if guest_name in party["guests"]:
        return f"⚠️ {guest_name} уже в списке гостей '{party_name}'."
    party["guests"].append(guest_name)
    party["bills"][guest_name] = 0
    save_data(data)
    return f"➕ Гость {guest_name} успешно добавлен в '{party_name}'!"

def start_voting(party_name, dates_str):
    data = load_data()
    party = data["parties"].get(party_name)
    if not party:
        print(f"❌ Вечеринка '{party_name}' не найдена.")
        return
    dates = dates_str.split()
    party["voting"]["options"] = dates
    party["voting"]["votes"] = {}
    save_data(data)
    print(f"📊 Голосование за даты началось! Варианты: {', '.join(dates)}")
    print("Чтобы проголосовать: голос [вечеринка] [имя] [дата]")

def cast_vote(party_name, guest_name, date):
    data = load_data()
    party = data["parties"].get(party_name)
    if not party:
        print(f"❌ Вечеринка '{party_name}' не найдена.")
        return
    if date not in party["voting"]["options"]:
        print(f"❌ Дата '{date}' не предложена для голосования.")
        return
    if guest_name not in party["guests"]:
        print(f"❌ {guest_name} не является участником вечеринки.")
        return
    party["voting"]["votes"][guest_name] = date
    save_data(data)
    print(f"✅ {guest_name} проголосовал за {date}!")

def add_bill(party_name, guest_name, amount):
    data = load_data()
    party = data["parties"].get(party_name)
    if not party:
        print(f"❌ Вечеринка '{party_name}' не найдена.")
        return
    if guest_name not in party["guests"]:
        print(f"❌ Гость '{guest_name}' не найден в списке.")
        return
    try:
        amount = float(amount)
        party["bills"][guest_name] += amount
        save_data(data)
        print(f"💸 {guest_name} теперь должен {party['bills'][guest_name]:.2f} руб.")
    except ValueError:
        print("❌ Сумма должна быть числом.")

def show_budget(party_name):
    data = load_data()
    party = data["parties"].get(party_name)
    if not party:
        print(f"❌ Вечеринка '{party_name}' не найдена.")
        return
    print(f"\n💰 === БЮДЖЕТ ВЕЧЕРИНКИ '{party_name}' ===")
    total = 0
    for guest, debt in party["bills"].items():
        print(f"  {guest}: {debt:.2f} руб.")
        total += debt
    print(f"  ➡️ Общий бюджет: {total:.2f} руб.")

def print_help():
    print("\n" + "=" * 50)
    print("  ДОСТУПНЫЕ КОМАНДЫ БОТА-ОРГАНИЗАТОРА")
    print("=" * 50)
    print("  создать [название]       - Новая вечеринка")
    print("  пригласить [гость] в [вечеринка]")
    print("  статус [вечеринка]       - Показать инфо о гостях и планах")
    print("  голосование [вечеринка] [дата1 дата2 ...]")
    print("  голос [вечеринка] [гость] [дата]")
    print("  долг [вечеринка] [гость] [сумма]")
    print("  бюджет [вечеринка]       - Финансовый отчет")
    print("  очистить                 - Очистить экран")
    print("  выход                    - Закрыть бота")
    print("=" * 50 + "\n")

def main():
    print("🎉 Добро пожаловать в PartyPlanner Bot v1.0!")
    print_help()
    while True:
        command = input("🤖 > ").strip()
        if not command:
            continue
        parts = command.split()
        if parts[0] == "выход":
            print("👋 До новых встреч!")
            sys.exit(0)
        elif parts[0] == "помощь":
            print_help()
        elif parts[0] == "очистить":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_help()
        elif parts[0] == "создать":
            if len(parts) > 1:
                name = " ".join(parts[1:])
                print(create_new_party(name))
            else:
                print("🤔 Укажите название: создать День Рождения")
        elif parts[0] == "пригласить":
            try:
                split_by_in = command.split(" в ", 1)
                guest_part = split_by_in[0].split(" ", 1)[1]
                party_part = split_by_in[1]
                print(add_guest_to_party(party_part, guest_part))
            except (IndexError, ValueError):
                print("😕 Формат: пригласить [имя] в [название вечеринки]")
        elif parts[0] == "статус":
            if len(parts) > 1:
                party_name = " ".join(parts[1:])
                data = load_data()
                party = data["parties"].get(party_name)
                if not party:
                    print(f"❌ Вечеринка '{party_name}' не найдена.")
                else:
                    print(f"\n📋 === СТАТУС ВЕЧЕРИНКИ '{party_name}' ===")
                    print(f"📅 Дата: {party.get('date') or 'Не выбрана'}")
                    print(f"📍 Место: {party.get('venue') or 'Не выбрано'}")
                    guests = party.get('guests', [])
                    print(f"👥 Гости ({len(guests)}): {', '.join(guests) if guests else 'Пока никого'}")
            else:
                print("🤔 Укажите название: статус День Рождения")
        elif parts[0] == "голосование":
            if len(parts) > 2:
                party_name = parts[1]
                dates_str = " ".join(parts[2:])
                start_voting(party_name, dates_str)
            else:
                print("😕 Формат: голосование [вечеринка] [список дат через пробел]")
        elif parts[0] == "голос":
            if len(parts) > 3:
                party_name = parts[1]
                guest_name = parts[2]
                date = parts[3]
                cast_vote(party_name, guest_name, date)
            else:
                print("😕 Формат: голос [вечеринка] [имя гостя] [дата]")
        elif parts[0] == "долг":
            if len(parts) > 3:
                party_name = parts[1]
                guest_name = parts[2]
                amount = parts[3]
                add_bill(party_name, guest_name, amount)
            else:
                print("😕 Формат: долг [вечеринка] [гость] [сумма]")
        elif parts[0] == "бюджет":
            if len(parts) > 1:
                party_name = " ".join(parts[1:])
                show_budget(party_name)
            else:
                print("😕 Формат: бюджет [вечеринка]")
        else:
            print(f"🤖 Неизвестная команда: '{parts[0]}'. Введите 'помощь' для списка команд.")

if __name__ == "__main__":
    main()