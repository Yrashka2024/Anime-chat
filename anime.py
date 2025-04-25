import json
import random
import os


def load_custom_models():
    if os.path.exists("models.json"):
        with open("models.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_custom_model(model_id, model_data):
    models = load_custom_models()
    models[model_id] = model_data
    with open("models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)


LANGUAGES = {
    "ru": "Русский 🇷🇺",
    "en": "English 🇺🇸"
}

print("🌍 Choose language / Выберите язык:")
for key, lang in LANGUAGES.items():
    print(f"{key} - {lang}")
lang = input("> ").lower()
if lang not in LANGUAGES:
    lang = "ru"

print(f"\n🌐 Language set to: {LANGUAGES[lang]}")
name = input("📝 " + ("Введи своё имя: " if lang == "ru" else "Enter your name: "))


CHARACTERS = {
    "neko": {
        "name": "Neko-chan" if lang == "en" else "Аниме-кошечка",
        "prefix": "nya~" if lang == "en" else "мяу~",
        "style": [
            "I missed you, {name}~" if lang == "en" else "Я скучала по тебе, {name}~",
            "You're so sweet, {name}!" if lang == "en" else "{name}, ты такой добрый, ня~",
            "Don't forget to rest, {name}~" if lang == "en" else "Не забывай отдыхать, {name}~",
        ],
    },
    "tsundere": {
        "name": "Tsundere-chan",
        "prefix": "b-b-baka!" if lang == "en" else "б-б-бака!",
        "style": [
            "I-it's not like I like you or anything!" if lang == "en" else "Я не для тебя это делаю! Просто так!",
            "You're such an idiot!" if lang == "en" else "Ты глупый! Б-б-бака!",
        ],
    }
}


def create_custom_model():
    print("\n🎨 " + ("Create your own anime girl" if lang == "en" else "Создание собственной аниме-девочки"))
    model_name = input("🧸 " + ("Name: " if lang == "en" else "Имя модели: "))
    prefix = input("🔤 " + ("Prefix (e.g. 'nya~'): " if lang == "en" else "Приставка-фраза (например, 'ня~'): "))
    style = []
    print("💬 " + ("Enter phrases (type 'stop' to finish):" if lang == "en" else "Вводи фразы (напиши 'стоп' чтобы закончить):"))
    while True:
        line = input("> ")
        if line.lower() in ["stop", "стоп"]:
            break
        style.append(line)
    custom_id = f"custom_{len(load_custom_models())+1}"
    model = {
        "name": model_name,
        "prefix": prefix,
        "style": style
    }
    save_custom_model(custom_id, model)
    return model


def choose_character():
    base_keys = list(CHARACTERS.keys())
    custom_models = load_custom_models()
    all_keys = base_keys + list(custom_models.keys())

    print("\n🎌 " + ("Choose your anime girl:" if lang == "en" else "Выбери аниме-девочку:"))
    for i, key in enumerate(base_keys, 1):
        print(f"{i}. {CHARACTERS[key]['name']}")
    for j, key in enumerate(custom_models.keys(), len(base_keys)+1):
        print(f"{j}. {custom_models[key]['name']} 🛠️")
    print(f"{len(all_keys)+1}. ✨ " + ("Create your own" if lang == "en" else "Создать свою ✨"))

    choice = input("> ")
    if choice == str(len(all_keys)+1):
        return create_custom_model()
    else:
        index = int(choice)-1
        if index < len(base_keys):
            return CHARACTERS[base_keys[index]]
        else:
            return custom_models[list(custom_models.keys())[index - len(base_keys)]]

char = choose_character()


def generate_response(user_input):
    lower = user_input.lower()
    if lang == "ru":
        if "привет" in lower or "хай" in lower:
            return random.choice(["Приветик!", f"Хай, {name}~", "Йоу~"])
        elif "люб" in lower:
            return random.choice(["Я т-тоже тебя... >///<", f"Ч-что ты такое говоришь, {name}?"])
        elif "груст" in lower:
            return random.choice([f"Не грусти, {name}, всё будет хорошо~", "Я с тобой."])
    else:
        if "hi" in lower or "hello" in lower:
            return random.choice([f"Hi {name}~", "Hello there!", "Hehe, welcome back~"])
        elif "love" in lower:
            return random.choice(["W-what? I mean... maybe I do...", f"I love you too, {name}~"])
        elif "sad" in lower:
            return random.choice(["Don't be sad, I'm here.", f"Cheer up, {name}!"])

    return random.choice([phrase.format(name=name) for phrase in char["style"]])


print(f"\n✨ Now chatting with {char['name']}! Type 'exit' or 'выход' to stop.\n")
while True:
    msg = input("You: ")
    if msg.lower() in ["exit", "выход", "quit"]:
        print(f"{char['name']}: " + ("See you soon!" if lang == "en" else "До встречи!"))
        break
    print(f"{char['name']}: {generate_response(msg)} {char['prefix']}")


if __name__ == "__main__":
    print("Script executed successfully.")