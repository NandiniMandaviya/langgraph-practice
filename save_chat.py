from datetime import datetime


def save_chat(user_message, assistant_message, response_type="AI"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"User: {user_message}\n")
        f.write(f"{response_type}: {assistant_message}\n")
        f.write("=" * 60 + "\n\n")