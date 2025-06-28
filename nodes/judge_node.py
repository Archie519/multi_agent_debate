import re




def judge_debate(topic, history):
    recent_transcript = "\n".join(history[-6:])
    prompt = (
        f"You are an impartial judge of a formal debate.\n"
        f"Debate Topic: {topic}\n\n"
        f"Debate Transcript:\n{recent_transcript}\n\n"
        f"Summarize both the Scientist and Philosopher's arguments.\n"
        f"Declare the winner in this format:\n"
        f"Summary: <summary>\n"
        f"Winner: <Scientist or Philosopher>\n"
        f"Reason: <brief justification>\n"
        f"Only respond in this format. Don't repeat the transcript."
    )

    result = generator(prompt, max_new_tokens=250, num_return_sequences=1)
    generated = result[0]["generated_text"].strip()

    # 🛡️ Check if model followed format
    if not re.search(r"Winner:\s*(Scientist|Philosopher)", generated):
        print("⚠️ Judge failed to select a winner. Using fallback logic.")
        return (
            "Both participants presented arguments, but the model did not summarize them clearly.",
            "Undecided",
            "The model's output did not follow the expected format."
        )

    print("\n📦 Raw Judge Output:\n", generated)

    summary_match = re.search(r"Summary:\s*(.*?)(?:\nWinner:|$)", generated, re.DOTALL)
    winner_match = re.search(r"Winner:\s*(Scientist|Philosopher)", generated)
    reason_match = re.search(r"Reason:\s*(.*)", generated)

    summary = summary_match.group(1).strip() if summary_match else "Summary could not be parsed."
    winner = winner_match.group(1).strip().capitalize() if winner_match else "Undecided"
    reason = reason_match.group(1).strip() if reason_match else "Model did not give a clear reason."

    return summary, winner, reason






























