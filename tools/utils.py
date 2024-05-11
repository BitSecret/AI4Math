import json
keywords = ["math", "arithmetic", "numerical", "reason", "symbolic"]


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def save_text(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
