from datetime import datetime as dt
from flask import Flask, request, render_template
import json

# flask - название пакета
# Flask - класс "веб приложение"
app = Flask(__name__)  # Создаем новое веб-приложение


def load_chat():
    with open("chat.json", "r") as json_file:
        data = json.load(json_file)
        return data["messages"]


def save_chat():
    data = {"messages": all_messages}
    with open("chat.json", "w") as json_file:
        json.dump(data, json_file)


all_messages = load_chat()


@app.route("/chat")
def display_chat():
    return render_template("form.html")


@app.route("/")
def index_page():
    return "Welcome to Skillbox Messenger"


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


# http://127.0.0.1:5000/send_message?name=Mike&text=Hello
@app.route("/send_message")
def send_message():
    sender = request.args["name"]
    text = request.args["text"]
    if 3 < len(sender) < 100:
        if 1 < len(text) < 3000:
            add_message(sender, text)
            save_chat()
        else:
            text = "ERROR MESSAGE"
            add_message(sender, text)
    else:
        text = "ERROR NAME"
        add_message(sender, text)

    return "OK"


@app.route("/info")
def info_chat():
    count = 0
    with open("chat.json", "r") as json_file:
        data = json.load(json_file)
        for _ in data["messages"]:
            count += 1
    return f"В чате {count} сообщений"


def add_message(sender, text):
    new_message = {
        "sender": sender,
        "text": text,
        "time": dt.now().strftime('%H:%M')
    }
    all_messages.append(new_message)


app.run()  # Запускаем приложение
