def is_valid_turn(turn, speaker):
    return (turn % 2 == 1 and speaker == "Scientist") or (turn % 2 == 0 and speaker == "Philosopher")



def is_unique_argument(response, used_arguments):
    normalized = response.lower().strip()
    return normalized not in (arg.lower().strip() for arg in used_arguments)
