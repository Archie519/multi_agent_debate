def log_message(message):
    with open("debate_log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\\n")
