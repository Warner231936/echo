"""Simple simulated social environment for agents."""

from typing import List, Dict, Tuple

class Agent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inbox: List[Tuple[str, str]] = []

    def receive(self, sender: str, message: str) -> None:
        self.inbox.append((sender, message))

class SocialEnvironment:
    def __init__(self, agents: List[str] | None = None) -> None:
        self.agents: Dict[str, Agent] = {n: Agent(n) for n in agents or []}
        self.history: List[Tuple[str, str, str]] = []

    def send(self, sender: str, recipient: str, message: str) -> None:
        self.history.append((sender, recipient, message))
        agent = self.agents.get(recipient)
        if agent:
            agent.receive(sender, message)
