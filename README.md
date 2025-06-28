# 🧠 Multi-Agent Debate System (LangGraph)

This project simulates a structured debate between two AI agents: a **Scientist** and a **Philosopher**. A third agent, the **Judge**, evaluates the debate and selects a winner. The system is built using [LangGraph](https://github.com/langchain-ai/langgraph), and the debate flow follows a Directed Acyclic Graph (DAG) of agent transitions.

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/multi_agent_debate.git
cd multi_agent_debate


2. Create and activate a virtual environment

python -m venv venv

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run the program

python main.py

🧠 LangGraph DAG Overview
The debate follows a multi-step DAG pipeline consisting of these nodes:

Node	Functionality
Scientist	Generates factual/scientific arguments
Memory      Update	Saves previous arguments from both agents
Philosopher	Responds with philosophical counterpoints
Judge	Evaluates last few rounds and selects a winner

🔁 DAG Flow:

[Start]
   ↓
[Scientist]
   ↓
[Memory Update]
   ↓
[Philosopher]
   ↓
[Memory Update]
   ↓
[Judge]

🗂️ Project Structure
graphql
Copy
Edit
multi_agent_debate/
├── main.py               # CLI debate control + LangGraph executor
├── dag_graph.py          # LangGraph DAG structure setup
├── requirements.txt      # Python dependencies
├── dag_diagram.png       # Visual DAG diagram (manual or auto-generated)
├── chat_log.txt          # Full chat & verdict log
├── README.md             # This file
│
├── memory/               # Memory management
│   └── memory_store.py
│
└── nodes/                # Modular node definitions
    ├── scientist_node.py
    ├── philosopher_node.py
    ├── judge_node.py
    └── memory_node.py


📜 Chat Log File
All actions, arguments, and verdicts are logged in chat_log.txt. This includes:

User prompts (if applicable)

Agent responses

Memory updates

Final verdict by Judge

📝 Sample Log 
Enter topic for debate: Should AI be regulated like medicine?

Starting debate between Scientist and Philosopher...

[Round 1] Scientist: AI must be regulated due to high-risk applications.
[Round 2] Philosopher: Regulation could stifle philosophical progress and autonomy.
[Round 3] Scientist: Like medicine, AI impacts lives — hence needs safety protocols.
[Round 4] Philosopher: But innovation thrives in freedom, not bureaucracy.
[Round 5] Scientist: Unregulated AI could lead to harmful unintended consequences.
[Round 6] Philosopher: History shows overregulation often delays societal evolution.
[Round 7] Scientist: Public trust grows with clear, ethical boundaries.
[Round 8] Philosopher: True, but ethics should evolve with usage, not precede it.

[Judge] Summary of debate:
The Scientist focused on safety, regulation, and risk management.
The Philosopher emphasized freedom, ethics, and progress.

[Judge] Winner: Scientist  
Reason: Presented more grounded, risk-based arguments aligned with public safety principles.


Logging is handled via Python’s logging module:

python
Copy
Edit
import logging

logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

🧾 DAG Diagram
A static DAG diagram (dag_graph.py.png) is included to visualize the process.

🛠 Tools to Create or Modify It:

Python graphviz package:
from graphviz import Digraph

dot = Digraph()
dot.node("Start")
dot.node("Scientist")
dot.node("Memory Update 1")
dot.node("Philosopher")
dot.node("Memory Update 2")
dot.node("Judge")

dot.edges([("Start", "Scientist"),
           ("Scientist", "Memory Update 1"),
           ("Memory Update 1", "Philosopher"),
           ("Philosopher", "Memory Update 2"),
           ("Memory Update 2", "Judge")])

dot.render("dag_diagram", format="png")


📽️ Demo Video
Watch the full demo here:
📺 [https://drive.google.com/file/d/1-eR-czEvS1qDSdv3-2S7ET3xOWWIbncA/view?usp=drivesdk]
