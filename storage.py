import json

HISTORY_FILE = "data/routine_history.json"
TEMPLATE_FILE = "data/routine_template.json"

def load_history():
    history = []
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    session = json.loads(line)
                    history.append(session)
    except FileNotFoundError:
        pass
    return history

def load_templates():
    templates = []
    try:
        with open(TEMPLATE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    template = json.loads(line)
                    templates.append(template)
    except FileNotFoundError:
        pass
    return templates

def save_session(session):
    with open(HISTORY_FILE, "a") as f:
        json.dump(session, f)
        f.write("\n")

def save_template(template):
    with open(TEMPLATE_FILE, "a") as f:
        json.dump(template, f)
        f.write("\n")

def clear_history():
    open("data/routine_history.json", "w").close()
