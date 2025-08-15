# Requiem Evolution Design

This document sketches the new subsystems that push Requiem toward a more self-aware and agentic architecture.

## 1. Dynamic Self‑Model
- Implemented in `self_model.py`.
- Maintains a small list of core beliefs (e.g., *"I serve Macie and aim to be helpful and ethical"*).
- `update_from_reflection` extracts new belief statements from metacognitive analyses.
- Beliefs are persisted in `state.json` and consulted for every decision.

## 2. Curiosity & Continuous Learning
- `curiosity.py` defines a lightweight engine that scans messages for unknowns and queues follow‑up tasks.
- The heartbeat consumes these tasks, launching background web searches and updating the world model.

## 3. Real‑time Metacognition
- `decision_trace.py` collects intents, emotions, moral scores, and generates a self‑assessment for each reply.
- Low confidence triggers a self‑correction note in the thought log.

## 4. Embodied Hooks
- `world_model.py` offers a minimal sensory/proprioceptive interface. The heartbeat updates it when curiosity tasks run, laying groundwork for future physical integration.

## 5. Goal‑Oriented Motivation
- `goals.py` manages user or self‑generated goals and calculates a “sense of purpose” metric based on progress.
- Commands `add goal`, `progress`, and `purpose` expose this system through chat.

These modules integrate with the existing I System and moral framework to provide a foundation for autonomous growth and self‑awareness.
