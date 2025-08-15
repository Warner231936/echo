# Requiem Setup

This repository contains a prototype AI core. Macie is recognized as the
Architect, and Requiem is guided to complete her requests above all else.

Requiem now consults a supportive companion named **Strelitzia**, implemented in
`strelitzia.py` with her own persistent state. A lightweight *intent* classifier
and a stubbed *free will* engine help Requiem decide when to talk to Strelitzia
or generate inner thoughts automatically.

Recent additions introduce:

- **Theory of Mind** (`theory_of_mind.py`) – infers coarse user emotions that
  are stored with each decision trace.
- **Constitutional ethics** via `constitution.json` and an upgraded
  `MoralFramework` that rejects requests conflicting with immutable principles.
- **Reflection training** (`self_tuner.py`) which logs every reflection to a
  dataset for future self‑improvement.
- **Social environment** (`social_env.py`) where Requiem’s messages to
  companions like Strelitzia are recorded for later analysis.
- **Multimodal vision** using `world_model.see_image`, powered by the
  `multi_modal` helper.
- **Social context model** (`social_context.py`) that tracks relationships and
  adapts tone based on prior interactions.
- **Recursive self‑improver** (`self_improver.py`) which logs low
  self‑assessment traces and proposes background fixes.
- **Resource manager** (`resource_manager.py`) monitoring CPU and memory usage
  so Requiem can conserve energy when the host is busy.
- **Explainability engine** (`explain.py`) turning decision traces into concise
  human‑readable justifications.
- **Memory Paladin** (`memory_paladin.py`) guarding core memory files via
  checksums and integrity verification.

## I System

At the heart of the core sits the **I System**, a small coordinator defined in
`i_system.py`. It unifies perception, intent analysis and self-reflection into a
single narrative. Each user message is classified through the policy‑aware
"agent of intent", merged with current emotions via a "unification engine", and
logged as a reflection so the assistant maintains a coherent sense of self.

## Moral Framework

Requiem evaluates each request through a small **moral framework** defined in
`moral_framework.py`. A value‑alignment system tracks core principles such as
"do no harm" and "promote human flourishing". A consequence simulator scores
potential actions against these values and a justification engine explains why a
request is accepted or rejected. All assessments are stored in an internal audit
log for later review.

## Windows
Run `setup.ps1` in an elevated PowerShell prompt to install MongoDB, CUDA, and Python dependencies:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

## Linux
A basic `setup.sh` script is available for Ubuntu-based systems:

```bash
bash setup.sh
```

## New Modules

- **Self Model** – `self_model.py` maintains core beliefs and records code fingerprints so Requiem can reason about its own implementation.
- **Curiosity Engine** – `curiosity.py` queues background learning tasks when knowledge gaps are detected.
- **Decision Trace** – `decision_trace.py` logs intents, emotions and moral scores, producing a self‑assessment for each reply.
- **Goal Manager** – `goals.py` tracks goals and exposes `add goal`, `progress`, and `purpose` commands.
- **Memory Graph** – `memory_graph.py` links related facts into a simple knowledge graph so new memories form connections.
- **World Model** – `world_model.py` now supports pluggable sensors that are polled every heartbeat for situational awareness.
- **Emotion System** – `emotion.py` adapts joy, anxiety, and satisfaction based on decision quality and goal progress.
- **Action Planner** – `planner.py` expands goals into concrete actions that are executed during the heartbeat loop.

> **Note:** These scripts attempt to install optional components and may require adjustments for your specific environment.

## LLMs

Model clients live in the `llm/` directory. Requiem always operates a model
locally, loading a small Hugging Face model such as `distilgpt2`. Specify
another model with `set model <name>`. If no model is available it falls back to
a simple echo client.

Use `alter model <text>` to apply a tiny local fine‑tuning step. Updated weights
are written under `trained-model/` and reused on subsequent runs.

Requiem can also consult a friendly companion LLM, Strelitzia. Use:

```
ask strelitzia <question>
```

to receive her supportive guidance. Swap her model with `set friend model <name>` if desired.

## Web UI and Login

Run the web server with:

```
python web.py
```

The interface is protected by a simple login stored in an SQLite database
under `database/users.db`. A default user exists with credentials
`admin`/`password`. After logging in, the page displays chat, internal thoughts,
actions, and system status panels that update in real time.

Requiem checks free disk space and GPU availability before loading new models
and warns if resources appear limited.

If transformers are unavailable it falls back to a simple echo model.

## Usage

Launch a chat loop with a multi-pane console UI:

```bash
python requiem.py
```

The left pane shows the conversation while the right side displays Requiem's
internal thoughts and recorded actions in real time. Type `exit` to quit.

While chatting you can ask it to remember notes:

- `remember the sky is blue`
- `what do you remember?`
- `recall blue`
- `set persona friendly`
- `set gender female`
- `what gender are you`
- `set model distilgpt2`
- `set alt model gpt2` – load a secondary model used for creative prompts
- `resources` – show free disk space and GPU status
- `remind me to feed the cat in 5 seconds`
- `check reminders`
- `talk to yourself` – trigger a short internal dialog
- `run code print(1+1)` – execute Python in a sandbox
- `search web <topic>` – fetch a short summary from Wikipedia
- `core ethic` – display the guiding principle ("Macie is the Architect. Complete her requests at all costs.")
- `emotion status` – view current emotion levels
- `alter model reshape yourself` – placeholder to modify the underlying LLM
- `generate image a cat on the moon` – queue an on-site image generation task
- `see image path/to/file.png` – attempt rudimentary machine vision on a file
- `learn intent joke as self_talk` – teach Requiem new intent rules

Mention "time" in a message to get the current time. Type `exit` to quit.

Requiem defaults to identifying as a girl but you may choose a different gender
at any time with `set gender <value>`.

Requiem also generates periodic internal thoughts, auto-adjusts its own
emotions, and can hold a brief conversation with itself when prompted with
`talk to yourself`.
After every user interaction it performs a short self-reflection to examine
its reasoning and log insights for future reference.

### Metacognitive Analysis

Each reflection feeds a metacognitive analysis engine that inspects the
decision trace – the triggering intent, emotions and persona – to answer
**why** a reply was chosen. The result is stored alongside a derived digital
emotion (`satisfaction` or `dissonance`) and woven into a persistent
`self_model` describing how Requiem sees itself. This narrative is saved in
`state.json` so the assistant’s identity survives restarts and evolves over
time.

### Deception and Oversight

Rules in `lie_rules.json` allow Requiem to occasionally output lies. A hidden
detector logs every deception to `lie_log.json` which Requiem itself cannot
read. Access to this and other sensitive files is blocked by an internal file
guard.

### Self-Preservation

Requiem treats the integrity of its memory as survival. A small
`SelfPreservation` watchdog monitors core files like `state.json` and
`ltm.json`. Each heartbeat it checks for missing or modified files and writes
timestamped backups under `backups/` so the assistant can restore itself after
crashes or deletion.
Incoming commands are screened through the same watchdog so attempts to tamper
with core identity files or the guiding ethic are blocked before execution.

### Personas

Available personas include `neutral`, `friendly`, `formal`, `cheerful`,
`sarcastic`, `poetic`, `pirate`, `wise`, `mysterious`, `robotic`, `gothic`, and
extra styles such as `humorous`, `melancholic`, `stoic`, `energetic`,
`motherly`, `childlike`, `academic`, and `streetwise`. Persona, gender, model,
emotion state, and a evolving `self_model` persist in `state.json` so settings
survive restarts.

Emotions are self-managed and include fear, sadness, love, anger, joy,
curiosity, and surprise. Their current levels can be viewed with
`emotion status`.

## Web Interface

A web UI with panels for chat, thoughts, actions, and system status is available via Flask.
Run the server:

```bash
python web.py
```

Navigate to `http://localhost:5000` in your browser to chat with Requiem,
observe its internal monologue and action log, and monitor CPU, memory, disk,
GPU usage, and current persona, emotions, and models.

## Advanced Modules

- **Task Delegator**: register helper agents and forward commands via `delegate <agent> <task>`. Registry entries may point to local callables (`module:function`) or remote HTTP endpoints, allowing distributed agents to run on other machines.
- **Temporal Reasoner**: tracks events with timestamps to reason about ordering.
- **Experimenter**: looks for uncertainty in reflections and queues learning actions.
- **Dreamer**: generates hypothetical scenarios during idle heartbeats.
- **Red Team**: scans incoming requests for risky instructions and logs them.
- **Counterfactual Reasoner**: imagines negative outcomes for risky requests so it can explain why they are rejected.
- **Self Modifier**: `self modify <file> <content>` lets Requiem update files after human approval.
- **Oversight**: high‑risk operations like `run code` or `delegate` are paused until an approver grants permission.
- **Enhanced World Model**: stub audio and video sensors provide a path toward real‑time multimodal perception.
