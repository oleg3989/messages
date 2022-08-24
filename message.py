from flask import Flask, request, render_template
from datetime import datetime
import json

DB_FILE = "./db.json"

app = Flask(__name__)  # Create new app


def load_messages():
    # json_file = open(DB_FILE, "r")
    # json_data = json.load(json_file)
    with open(DB_FILE, "r") as json_file:
        json_data = json.load(json_file)
    return json_data["messages"]


def save_messages():
    data = {
        "messages": all_messages
    }
    with open(DB_FILE, "w") as json_file:
        json.dump(data, json_file)


@app.route("/")
def index_page():
    return "Hello from <b>index page</b>!"


# Get list of all messages
# Flask кодирует в JSON если функция возвращает словарь
@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}  # json-valid format


# Print message
def print_message(message):
    print(f"[{message['time']} {message['sender']}]: {message['text']}")


@app.route("/chat")
def display_chat():
    return render_template("form.html")


# Add new message
def add_message(sender, text):
    # dictionary
    # key : value
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime('%H:%M')
    }
    all_messages.append(new_message)


@app.route("/message_count")
def message_count():
    return f"There's {len(all_messages)} messages in our chat."
#
#
@app.route("/send_message")
def send_message():
    # get sender name and message text
    sender = request.args["name"]
    text = request.args["text"]

    if len(sender) < 3 or len(sender) > 10:
        add_message("Server", "Длина имени пользователя должна быть от 3 до 10 символов!")
    else:
        if len(text) < 3 or len(text) > 3000:
            add_message("Server", "Длина сообщения должна быть от 3 до 3000 символов!")
        else:
            add_message(sender, text)

    save_messages()

    return "OK"


all_messages = load_messages()  # list of all messages


app.run()