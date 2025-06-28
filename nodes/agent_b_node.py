from transformers import pipeline

# Load model once
flan_t5 = pipeline("text2text-generation", model="google/flan-t5-small")

def clean_response(text, memory=None):
    """
    Clean generated text and avoid duplication if memory is provided.
    """
    text = text.strip()
    if not text or len(text) < 10:
        return "Philosophical inquiry must consider broader implications."
    
    if memory:
        memory_lower = [m.lower() for m in memory]
        if text.lower() in memory_lower:
            return "Let's approach this idea from a different philosophical angle."
    
    return text

def agent_b_response(topic, last_opponent_point, memory=None):
    """
    Generate a thoughtful argument from the Philosopher based on the opponent's last point.
    Avoids duplicates if memory is provided.
    """
    last_opponent_point = last_opponent_point.strip() if last_opponent_point else "No previous argument yet."

    prompt = f"""
You are a Philosopher participating in a formal debate.

Debate Topic: {topic}

Your opponent recently said: "{last_opponent_point}"

Respond with your next logical argument in 1–2 thoughtful and concise sentences.
""".strip()

    result = flan_t5(prompt, max_new_tokens=100, do_sample=True, temperature=0.9, top_k=50)
    generated = result[0]['generated_text']
    
    return clean_response(generated, memory)
