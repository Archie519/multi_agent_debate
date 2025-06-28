from transformers import pipeline

# Load model only once
flan_t5 = pipeline("text2text-generation", model="google/flan-t5-small")

def clean_response(text, memory):
    """Clean and filter out short or repeated responses."""
    text = text.strip()
    memory = [m.lower() for m in memory]
    if len(text) < 15 or text.lower() in memory:
        return "Let me offer a new angle to this issue."
    return text

def agent_a_response(topic, last_opponent_point, memory=[]):
    """Scientist responds with logical argument based on opponent's last point."""
    last_opponent_point = last_opponent_point or "No previous argument yet."
    prompt = f"""
You are a Scientist in a formal AI debate.

Debate Topic: {topic}

Your opponent recently said: "{last_opponent_point}"

Reply with your next logical argument in 1–2 thoughtful and concise sentences.
""".strip()

    result = flan_t5(prompt, max_new_tokens=100, do_sample=True, temperature=0.9, top_k=50)
    return clean_response(result[0]['generated_text'], memory)

def agent_b_response(topic, last_opponent_point, memory=[]):
    """Philosopher responds with thoughtful argument based on opponent's last point."""
    last_opponent_point = last_opponent_point or "No previous argument yet."
    prompt = f"""
You are a Philosopher in a formal AI debate.

Debate Topic: {topic}

Your opponent recently said: "{last_opponent_point}"

Reply with your next thoughtful argument in 1–2 sentences.
""".strip()

    result = flan_t5(prompt, max_new_tokens=100, do_sample=True, temperature=0.9, top_k=50)
    return clean_response(result[0]['generated_text'], memory)
