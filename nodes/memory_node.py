import re

def has_repeating_phrases(text, min_len=3, max_len=8):
    """
    Detect repeating n-grams that might indicate a looped or degenerate response.
    """
    tokens = text.lower().split()
    for size in range(min_len, max_len + 1):
        for i in range(len(tokens) - size):
            phrase = " ".join(tokens[i:i + size])
            rest = " ".join(tokens[i + size:])
            if phrase in rest:
                return True
    return False


def update_memory(state, speaker, new_point):
    """
    Add a cleaned, non-repetitive, and unique argument to the speaker's memory log.
    Filters out empty or duplicate entries (case-insensitive).
    """
    if not new_point:
        return

    if "memory" not in state:
        state["memory"] = {}

    if speaker not in state["memory"]:
        state["memory"][speaker] = []

    cleaned_point = new_point.strip()
    normalized_memory = {p.strip().lower() for p in state["memory"][speaker]}

    if cleaned_point.lower() not in normalized_memory and not has_repeating_phrases(cleaned_point):
        state["memory"][speaker].append(cleaned_point)


def get_agent_memory(state, speaker):
    """
    Return last 2 unique opponent arguments for context, filtered for duplicates (case-insensitive).
    """
    opponent = "Scientist" if speaker == "Philosopher" else "Philosopher"
    memory = state.get("memory", {}).get(opponent, [])

    seen = set()
    recent = []
    for point in reversed(memory):
        key = point.strip().lower()
        if key not in seen:
            seen.add(key)
            recent.insert(0, point.strip())
        if len(recent) == 2:
            break

    return " | ".join(recent) if recent else "No previous argument yet."
