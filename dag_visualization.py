from graphviz import Digraph

def generate_dag():
    dot = Digraph()
    dot.attr(rankdir='LR')
    dot.node("UserInput")
    for i in range(1, 9):
        agent = "AgentA" if i % 2 == 1 else "AgentB"
        dot.node(f"Round {i}: {agent}")
    dot.node("MemoryNode")
    dot.node("JudgeNode")

    dot.edge("UserInput", "Round 1: AgentA")
    for i in range(1, 8):
        dot.edge(f"Round {i}: {'AgentA' if i % 2 == 1 else 'AgentB'}", f"Round {i+1}: {'AgentA' if (i+1) % 2 == 1 else 'AgentB'}")
    dot.edge("Round 8: AgentB", "MemoryNode")
    dot.edge("MemoryNode", "JudgeNode")

    dot.render("debate_dag", format="png", cleanup=True)
    print("DAG diagram saved as 'debate_dag.png'")

if __name__ == "__main__":
    generate_dag()
