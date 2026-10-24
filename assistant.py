"""Rule-based terminal assistant with simple intent recognition."""
from datetime import datetime


def detect_intent(message):
    text = message.lower().strip()
    if any(word in text for word in ("hello", "hi", "hey", "namaste")):
        return "greeting"
    if any(word in text for word in ("time", "clock")):
        return "time"
    if any(word in text for word in ("date", "day today", "today's date")):
        return "date"
    if any(word in text for word in ("help", "commands", "what can you do")):
        return "help"
    if any(word in text for word in ("your name", "who are you", "name")):
        return "identity"
    if any(word in text for word in ("bye", "exit", "quit", "goodbye")):
        return "goodbye"
    if any(word in text for word in ("thank", "thanks")):
        return "thanks"
    return "unknown"


def respond(message):
    intent = detect_intent(message)
    responses = {
        "greeting": "Hello! How can I help you today?",
        "time": f"The current local time is {datetime.now().astimezone().strftime('%H:%M:%S')}.",
        "date": f"Today's date is {datetime.now().astimezone().strftime('%d %B %Y')}.",
        "help": "Try: hello, time, date, your name, thanks, or bye.",
        "identity": "I am a simple rule-based terminal assistant written in Python.",
        "goodbye": "Goodbye! Have a great day.",
        "thanks": "You're welcome!",
        "unknown": "I didn't understand that yet. Type 'help' to see supported commands.",
    }
    return intent, responses[intent]


def main():
    print("=== Terminal Assistant ===")
    print("Type 'help' for commands, or 'bye' to exit.")
    while True:
        try:
            message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAssistant: Session ended. Goodbye!")
            break
        if not message:
            print("Assistant: Please type a message.")
            continue
        intent, answer = respond(message)
        print(f"Assistant: {answer}")
        if intent == "goodbye":
            break


if __name__ == "__main__":
    main()
