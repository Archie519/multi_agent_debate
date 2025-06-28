from transformers import pipeline, set_seed
from nodes.user_input_node import get_topic
from nodes.memory_node import update_memory, get_agent_memory
from utils.logger import log_message
from utils.validators import is_valid_turn, is_unique_argument
import torch
import re
import os
import logging

# ✅ Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Application started")

# ✅ Device check
device = 0 if torch.cuda.is_available() else -1
print(f"✅ Device set to: {'GPU' if device == 0 else 'CPU'}")

# ✅ Load reliable model
generator = pipeline("text2text-generation", model="google/flan-t5-large", device=device)
set_seed(42)

AGENT_A = "Scientist"
AGENT_B = "Philosopher"

state = {
    "topic": "",
    "turn": 1,
    "agent_a_history": [],
    "agent_b_history": [],
    "memory": {},
    "used_arguments": set()
}

# ✅ Generate response with cleaned output
def generate_response(role, prompt):
    clean_prompt = (
        f"You are a {role} participating in a formal academic debate.\n"
        f"Debate Topic: {state['topic']}\n"
        f"Previous statement: {prompt}\n\n"
        f"{role}'s response (avoid repetition and be logical):"
    )

    result = generator(clean_prompt, max_new_tokens=120, num_return_sequences=1)
    raw_output = result[0]['generated_text'].replace(clean_prompt, '').strip()

    # ✅ Sentence-level duplicate filtering
    sentences = [s.strip() for s in raw_output.split('. ') if s.strip()]
    seen = set()
    unique_sentences = []
    for s in sentences:
        lower = s.lower()
        if lower not in seen:
            seen.add(lower)
            unique_sentences.append(s)
    return '. '.join(unique_sentences)

def judge_debate(topic, history):
    recent_transcript = "\n".join(history[-6:]).lower()

    # crude keyword scoring
    scientist_score = sum([
        recent_transcript.count("risk"),
        recent_transcript.count("safety"),
        recent_transcript.count("fda"),
        recent_transcript.count("public health")
    ])
    philosopher_score = sum([
        recent_transcript.count("freedom"),
        recent_transcript.count("philosophy"),
        recent_transcript.count("autonomy"),
        recent_transcript.count("society")
    ])

    print("📦 [Judge] Using fallback keyword-based logic...")

    if scientist_score > philosopher_score:
        winner = "Scientist"
        reason = "Presented more concrete and safety-based arguments."
    elif philosopher_score > scientist_score:
        winner = "Philosopher"
        reason = "Focused more on societal and ethical implications."
    else:
        winner = "Undecided"
        reason = "Both made valid points, but no clear dominance."

    summary = (
        "Scientist emphasized risk mitigation and public safety through regulation, "
        "while Philosopher raised concerns about freedom, ethics, and overregulation."
    )

    return summary, winner, reason




# ✅ Main debate flow with smarter prompts
def run_debate():
    state["topic"] = get_topic().strip()
    if not state["topic"]:
        print("❌ No topic entered.")
        return

    print(f"\n🎯 Debate Topic: {state['topic']}\n")
    log_message("Debate topic: " + state["topic"])
    print(f"🔊 Starting debate between {AGENT_A} and {AGENT_B}...\n")

    last_msg = ""

    for round_num in range(1, 9):
        speaker = AGENT_A if round_num % 2 == 1 else AGENT_B
        history_key = "agent_a_history" if speaker == AGENT_A else "agent_b_history"

        # ✅ Dynamic prompt update based on round number
        if round_num == 1:
            last_msg = f"Opening statement on: {state['topic']}"
        elif round_num == 2:
            last_msg = "Respond to the previous point with a counterargument."
        else:
            last_msg = f"Consider what was said before and elaborate your position further."

        print(f"[Round {round_num}] {speaker}:")
        memory = get_agent_memory(state, speaker)
        response = generate_response(speaker, last_msg)

        if not is_valid_turn(state["turn"], speaker):
            raise Exception("❌ Invalid turn order!")

        if not is_unique_argument(response, state["used_arguments"]):
            print("⚠️ Duplicate detected, continuing anyway.")

        print(response + "\n")
        log_message(f"[Round {round_num}] {speaker}: {response}")

        state[history_key].append(response)
        state["used_arguments"].add(response.lower().strip())  # ✅ Improved repetition check
        update_memory(state, speaker, response)
        state["turn"] += 1
        last_msg = response

    print("👨‍⚖️ [Judge] Evaluating debate...\n")
    summary, winner, reason = judge_debate(state["topic"], state["agent_a_history"] + state["agent_b_history"])

    log_message("[Judge] Summary: " + summary)
    log_message(f"[Judge] Winner: {winner}")
    log_message("[Judge] Reason: " + reason)

    print(f"📋 [Summary]: {summary}\n")
    print(f"🏆 [Winner]: {winner}")
    print(f"💬 [Reason]: {reason}")

if __name__ == '__main__':
    run_debate()
















import logging
import os

# Make sure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Sample log message
logging.info("Application started")

