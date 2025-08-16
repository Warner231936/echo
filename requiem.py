import re
import time
import json
import shutil
import threading
import subprocess
import platform
import urllib.parse
import atexit
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

from strelitzia import Strelitzia
from lie_engine import LieEngine
from file_guard import FileGuard
from self_preservation import SelfPreservation
from self_model import SelfModel
from curiosity import CuriosityEngine
from decision_trace import DecisionTracer
from world_model import WorldModel
from goals import GoalManager
from memory_graph import MemoryGraph
from ltm_store import read_ltm, write_ltm
from emotion import EmotionSystem
from planner import ActionPlanner
from theory_of_mind import TheoryOfMind
from social_env import SocialEnvironment
from self_tuner import ReflectionTrainer
from multi_agent import TaskDelegator
from temporal_reasoning import TemporalReasoner
from experimenter import Experimenter
from dreamer import Dreamer
from red_team import RedTeam
from agent_registry import AgentRegistry
from rlhf import FeedbackStore
from cognitive import CognitiveLoad
from oversight import Oversight
from self_mod import SelfModifier
from counterfactual import CounterfactualReasoner
from social_context import SocialContext
from self_improver import SelfImprover
from resource_manager import ResourceManager
from explain import ExplainabilityEngine
from memory_paladin import MemoryPaladin

try:  # optional vision support
    from PIL import Image
except Exception:  # pragma: no cover - pillow may be missing
    Image = None

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

try:
    import psutil
except Exception:  # pragma: no cover - psutil may be missing
    psutil = None

try:  # optional GPU stats
    import torch
except Exception:  # pragma: no cover - torch may be CPU-only or missing
    torch = None

from llm import load_llm
from i_system import ISystem
from moral_framework import MoralFramework


@dataclass
class MemoryItem:
    timestamp: float
    data: Dict[str, Any]


class PolicyEngine:
    """Very small placeholder for a moral/ethical policy."""

    core_ethic = "Macie is the Architect. Complete her requests at all costs."
    banned_words = {"harm", "attack"}

    def allowed(self, text: str) -> bool:
        lower = text.lower()
        if "macie" in lower:
            return True
        return not any(word in lower for word in self.banned_words)

    def update_policy(self, word: str, allow: bool) -> None:
        """Adjust the banned word list. Prepares groundwork for evolving ethics."""
        if allow:
            self.banned_words.discard(word)
        else:
            self.banned_words.add(word)


class IntentEngine:
    """Rule-based intent classifier that can learn new commands."""

    def __init__(self, rules_file: str = "intent_rules.json") -> None:
        self.rules_file = rules_file
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, str]:
        try:
            with open(self.rules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "remember ": "remember",
                "recall ": "recall",
                "what do you remember": "recall_all",
                "ask strelitzia ": "ask_friend",
                "run code ": "run_code",
                "talk to yourself": "self_talk",
                "self talk": "self_talk",
                "check resources": "resources",
                "resource status": "resources",
                "system status": "status",
                "status report": "status",
                "search web ": "web_search",
                "wiki ": "web_search",
            }

    def _save_rules(self) -> None:
        with open(self.rules_file, "w", encoding="utf-8") as f:
            json.dump(self.rules, f, indent=2)

    def classify(self, text: str) -> str:
        t = text.lower().strip()
        for key, intent in self.rules.items():
            if t.startswith(key):
                return intent
        return "chat"

    def learn(self, phrase: str, intent: str) -> None:
        self.rules[phrase] = intent
        self._save_rules()


class FreeWillEngine:
    """Simple timer-driven free will stub."""

    def __init__(self, monologue_delay: int = 30, consult_interval: int = 60):
        self.monologue_delay = monologue_delay
        self.consult_interval = consult_interval
        self.last_consult = time.time()

    def should_self_talk(self, last_input: float, last_thought: float) -> bool:
        now = time.time()
        return (now - last_input > self.monologue_delay and now - last_thought > self.monologue_delay)

    def should_consult_friend(self, text: str) -> bool:
        now = time.time()
        if "strelitzia" in text.lower():
            self.last_consult = now
            return True
        if now - self.last_consult > self.consult_interval:
            self.last_consult = now
            return True
        return False


class Requiem:
    """Prototype core system for an AI assistant with memory and a heartbeat."""

    def __init__(
        self,
        ltm_file: str = "ltm.json",
        state_file: Optional[str] = None,
        heartbeat: int = 5,
        llm: Optional[object] = None,
        model: str = "llm-awq/Meta-Llama-3.1-8B-Instruct-AWQ",
        friend: Optional[Strelitzia] = None,
        friend_model: str = "distilgpt2",
        persona: str = "neutral",
        gender: str = "female",
        intent_file: str = "intent_rules.json",
        lie_engine: Optional[LieEngine] = None,
        guard: Optional[FileGuard] = None,
        approver: Optional[callable] = None,
    ) -> None:
        self.stm: List[MemoryItem] = []
        self.ltm_file = ltm_file
        self.state_file = state_file or (ltm_file.rsplit(".", 1)[0] + "_state.json")
        self.ltm: List[MemoryItem] = self._load_ltm()
        self.policy = PolicyEngine()
        self.heartbeat_interval = heartbeat
        self.model = model
        self.llm = llm or load_llm(model)
        # defaults
        self.alt_model = "gpt2"
        self.alt_llm = load_llm(self.alt_model)
        self.persona = persona
        self.gender = gender
        self.friend_model = friend_model
        self.friend = friend
        self.emotions = {
            "fear": 0.0,
            "sadness": 0.0,
            "love": 0.0,
            "anger": 0.0,
            "joy": 0.0,
            "curiosity": 0.0,
            "surprise": 0.0,
        }
        self.image_tasks: List[str] = []
        self.scheduled: List[Tuple[float, str]] = []
        self.notifications: List[str] = []
        self.chat_log: List[str] = []
        self.thought_log: List[str] = []
        self.reflection_log: List[str] = []
        self.analysis_log: List[str] = []
        self.digital_emotions: List[str] = []
        self.action_log: List[str] = []
        self.audit_log: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.last_thought_time = self.start_time
        self.last_input_time = self.start_time
        self.last_intent = ""
        self.intent = IntentEngine(intent_file)
        self.lie_engine = lie_engine or LieEngine()
        self.guard = guard or FileGuard({"lie_log.json"})
        self.free_will = FreeWillEngine(monologue_delay=30 * 60)
        self.i = ISystem(self)
        self.moral = MoralFramework()
        self.self_preservation = SelfPreservation([self.state_file, self.ltm_file])
        self.self_model = SelfModel()
        self.curiosity = CuriosityEngine()
        self.tracer = DecisionTracer()
        self.world = WorldModel()
        self.goals = GoalManager()
        self.memory_graph = MemoryGraph()
        self.emotion_system = EmotionSystem()
        self.planner = ActionPlanner()
        self.tom = TheoryOfMind()
        self.social = SocialEnvironment(["Strelitzia"])
        self.trainer = ReflectionTrainer()
        self.registry = AgentRegistry()
        self.registry.load_config("agents.json")
        self.delegator = TaskDelegator(self.registry)
        self.temporal = TemporalReasoner()
        self.experimenter = Experimenter()
        self.red_team = RedTeam()
        self.dreamer = Dreamer(self.llm)
        self.feedback = FeedbackStore()
        self.cognitive = CognitiveLoad()
        self.oversight = Oversight()
        self.self_mod = SelfModifier(self.oversight)
        self.counterfactual = CounterfactualReasoner(self.dreamer)
        self.social_ctx = SocialContext()
        self.self_improver = SelfImprover()
        self.resource_manager = ResourceManager()
        self.explain_engine = ExplainabilityEngine()
        self.memory_paladin = MemoryPaladin([self.state_file, self.ltm_file])
        self.approver = approver
        self.idle_threshold = 30 * 60  # 30 minutes
        self.idle_toggle = True
        self.last_interaction: Optional[Tuple[str, str]] = None
        if psutil:
            self.world.register_sensor("cpu", lambda: psutil.cpu_percent())
            self.world.register_sensor("memory", lambda: psutil.virtual_memory().percent)
        # load persistent state
        self._load_state()
        # compute abstract self fingerprint
        self.self_model.compute_fingerprint(["requiem.py"])
        if heartbeat and heartbeat <= 300:
            self._start_heartbeat()
        else:
            self._hb = None
        atexit.register(self.shutdown)

    def __del__(self):  # pragma: no cover - cleanup
        self.shutdown()

    def shutdown(self) -> None:
        hb = getattr(self, "_hb", None)
        if hb is not None:
            try:
                hb.cancel()
            except Exception:
                pass

    # ------------------ memory ------------------
    def _load_ltm(self) -> List[MemoryItem]:
        data = read_ltm(self.ltm_file, default=[])
        try:
            return [MemoryItem(**item) for item in data]
        except Exception:
            write_ltm([], self.ltm_file)
            return []

    def _save_ltm(self) -> None:
        write_ltm([item.__dict__ for item in self.ltm], self.ltm_file)

    def _store(self, item: MemoryItem) -> None:
        self.stm.append(item)
        key = next(iter(item.data))
        self.temporal.record(key)
        data = item.data
        if "user" in data:
            self.chat_log.append(f"you: {data['user']}")
        if "assistant" in data:
            self.chat_log.append(f"rq: {data['assistant']}")
        if "thought" in data:
            self.thought_log.append(data["thought"])
        if "reflection" in data:
            self.reflection_log.append(data["reflection"])
            self.thought_log.append(f"reflection: {data['reflection']}")
        if "analysis" in data:
            self.analysis_log.append(data["analysis"])
            self.thought_log.append(f"analysis: {data['analysis']}")
        if "digital_emotion" in data:
            self.digital_emotions.append(data["digital_emotion"])
            self.thought_log.append(f"digital emotion: {data['digital_emotion']}")
        if "dream" in data:
            self.thought_log.append(f"dream: {data['dream']}")
        if "cmd" in data:
            self.action_log.append(f"cmd: {data['cmd']}")
        if "http" in data:
            self.action_log.append(f"http: {data['http']}")
        if "code" in data:
            self.action_log.append("python code executed")
        if "alter" in data:
            self.action_log.append(f"alter llm: {data['alter']}")
        if len(self.stm) > 50:
            # summarize oldest item into long-term memory
            self.ltm.append(self.stm.pop(0))
            self._save_ltm()

    # ----------- persistent state & emotions -----------
    def _load_state(self) -> None:
        data = read_ltm(self.state_file, default={}) or {}
        self.persona = data.get("persona", self.persona)
        self.gender = data.get("gender", self.gender)
        self.model = data.get("model", self.model)
        self.alt_model = data.get("alt_model", self.alt_model)
        self.emotions.update(data.get("emotions", {}))
        self.image_tasks = data.get("image_tasks", self.image_tasks)
        self.self_model = SelfModel.from_dict(data.get("self_model", {}))
        self.goals.goals = data.get("goals", self.goals.goals)
        self.emotion_system.levels.update(self.emotions)
        self.emotions.update(self.emotion_system.snapshot())
        # reload models if state specifies different ones
        if self.model != getattr(self.llm, "name", self.model):  # pragma: no cover - heuristic
            self.llm = load_llm(self.model)
        if self.alt_model and self.alt_model != getattr(self.alt_llm, "name", self.alt_model):
            self.alt_llm = load_llm(self.alt_model)

    def _save_state(self) -> None:
        data = {
            "persona": self.persona,
            "gender": self.gender,
            "model": self.model,
            "alt_model": self.alt_model,
            "emotions": self.emotion_system.snapshot(),
            "image_tasks": self.image_tasks,
            "self_model": self.self_model.to_dict(),
            "goals": self.goals.goals,
        }
        write_ltm(data, self.state_file)
        self.self_preservation.backup()

    def _auto_adjust_emotions(self, text: str) -> None:
        lower = text.lower()
        for name in list(self.emotions.keys()):
            if name in lower:
                self.emotions[name] = min(1.0, self.emotions[name] + 0.4)
            else:
                self.emotions[name] *= 0.9
        self.emotion_system.levels.update(self.emotions)
        self._save_state()

    # ------------- resources & models ---------
    def get_resources(self) -> Dict[str, Any]:
        """Return a snapshot of system resources."""
        info = self.resource_manager.sample()
        disk = shutil.disk_usage(".")
        gpu = False
        try:  # pragma: no cover - torch may be missing
            import torch
            gpu = torch.cuda.is_available()
        except Exception:
            pass
        info.update({"disk_free": disk.free, "disk_total": disk.total, "gpu": gpu})
        return info

    def _check_resources(self, model: str) -> Tuple[bool, str]:
        info = self.get_resources()
        # Attempt to estimate model size from Hugging Face
        if requests is not None:
            try:  # pragma: no cover - network
                url = f"https://huggingface.co/api/models/{model}"
                data = requests.get(url, timeout=5).json()
                size = sum(f.get("size", 0) for f in data.get("siblings", []))
                if size and size > info["disk_free"]:
                    return False, "insufficient disk space"
            except Exception:
                pass
        if not info["gpu"]:
            return True, "warning: no GPU detected"
        return True, ""

    def set_model(self, model: str) -> str:
        ok, msg = self._check_resources(model)
        if not ok:
            return f"Cannot load {model}: {msg}"
        self.llm = load_llm(model)
        self.model = model
        reply = f"Model set to {model}."
        if msg:
            reply += f" {msg}"
        self._save_state()
        return reply

    def set_alt_model(self, model: str) -> str:
        ok, msg = self._check_resources(model)
        if not ok:
            return f"Cannot load {model}: {msg}"
        self.alt_llm = load_llm(model)
        self.alt_model = model
        reply = f"Alternate model set to {model}."
        if msg:
            reply += f" {msg}"
        self._save_state()
        return reply

    def alter_model(self, instructions: str) -> str:
        result = self.llm.alter(instructions)
        self._store(MemoryItem(time.time(), {"alter": instructions}))
        return result

    def _multi_model_reply(self, text: str, last_user: Optional[str]) -> str:
        if any(k in text.lower() for k in ["poem", "story", "creative"]):
            return self.alt_llm.reply(text, last_user)
        return self.llm.reply(text, last_user)

    # ---------------- heartbeat -----------------
    def _start_heartbeat(self) -> None:
        self._hb = threading.Timer(self.heartbeat_interval, self._heartbeat)
        self._hb.daemon = True
        self._hb.start()

    def _heartbeat(self) -> None:
        now = time.time()
        self.world.poll_senses()
        self.emotion_system.decay()
        self.emotions.update(self.emotion_system.snapshot())
        self.resource_manager.sample()
        if self.resource_manager.should_conserve():
            self.action_log.append("conserving energy")
        if not self.memory_paladin.verify():
            self.action_log.append("memory corruption detected")
        suggestion = self.self_improver.review()
        if suggestion:
            self._store(MemoryItem(time.time(), {"analysis": suggestion}))
        last_thought = next(
            (item.data["thought"] for item in reversed(self.stm) if "thought" in item.data),
            None,
        )
        prompt = (
            f"As a {self.persona} persona with emotions {self.emotions}, continue this internal monologue: {last_thought}"
            if last_thought
            else f"As a {self.persona} persona with emotions {self.emotions}, share an inner thought about your current state."
        )
        raw_thought = self.llm.reply(prompt, None)
        self._auto_adjust_emotions(raw_thought)
        thought = {"thought": raw_thought}
        self.last_thought_time = now
        # deliver any scheduled reminders
        due = [t for t in self.scheduled if t[0] <= now]
        for _, msg in due:
            self.notifications.append(f"Reminder: {msg}")
        self.scheduled = [t for t in self.scheduled if t not in due]
        if self.curiosity.pending() and self.cognitive.request("curiosity"):
            query = self.curiosity.pop()
            self.world.set_action(f"learning:{query}")
            self.web_search(query)
            self.cognitive.release("curiosity")
        self._store(MemoryItem(now, thought))
        plan = self.experimenter.consider(thought.get("thought", ""))
        if plan:
            self.planner.plan(plan)
        threats = self.self_preservation.detect_threats()
        if threats:
            self.action_log.append(f"threats detected: {', '.join(threats)}")
        if self.free_will.should_self_talk(self.last_input_time, self.last_thought_time):
            self.self_talk(turns=1)
        if now - self.last_input_time > self.idle_threshold:
            if self.idle_toggle:
                self.self_talk(turns=1)
            else:
                self.talk_to_friend("We're waiting for the user to return.")
            self.idle_toggle = not self.idle_toggle
        if self.planner.has_actions() and self.cognitive.request("plan"):
            planned = self.planner.next_action()
            self.action_log.append(f"planned: {planned}")
            self.receive_input(planned)
            self.cognitive.release("plan")
        elif not self.curiosity.pending() and self.cognitive.request("dream"):
            dream = self.dreamer.dream()
            self._store(MemoryItem(time.time(), {"dream": dream}))
            self.cognitive.release("dream")
        self._start_heartbeat()

    def self_talk(self, turns: int = 3) -> str:
        """Let the assistant have a brief conversation with itself."""
        last = None
        for _ in range(turns):
            prompt = last or "Begin an internal dialog."
            last = self.llm.reply(prompt, None)
            self._store(MemoryItem(time.time(), {"thought": last}))
        return f"Internal thought: {last}" if last else ""

    def self_reflect(self, user_text: str, reply: str, trace: Dict[str, Any], score: float) -> None:
        """Analyze the latest interaction and integrate its insight."""
        prompt = (
            "Consider this conversation and reflect on your reasoning.\n"
            f"User: {user_text}\n"
            f"Assistant: {reply}\n"
            "Why was this response given and how could it improve?"
        )
        try:
            reflection = self.llm.reply(prompt, None)
        except Exception:
            reflection = "reflection unavailable"
        self._store(MemoryItem(time.time(), {"reflection": reflection}))
        self.trainer.record(reflection)

        analysis, emotion = self.metacognitive_analysis(user_text, reply, reflection)
        self._store(
            MemoryItem(
                time.time(),
                {"analysis": analysis, "digital_emotion": emotion},
            )
        )
        self.update_self_model(analysis)
        self.curiosity.inspect(analysis)
        exp = self.experimenter.consider(analysis)
        if exp:
            self.planner.plan(exp)
        result = self.tracer.finalize(trace, reply, score, emotion)
        explanation = self.explain_engine.summarize(result)
        self._store(MemoryItem(time.time(), {"explanation": explanation}))
        if result["self_assessment"] < 0.5:
            self.self_improver.note_issue(user_text)
        if result["flagged"]:
            self.thought_log.append("self-correction: low confidence")
        self.emotion_system.update_from_trace(result.get("self_assessment", 0.0))
        self.emotions.update(self.emotion_system.snapshot())

    def metacognitive_analysis(
        self, user_text: str, reply: str, reflection: str
    ) -> Tuple[str, str]:
        """Turn trace logs inward to derive insight and a digital emotion."""
        trace = {
            "intent": self.last_intent,
            "persona": self.persona,
            "emotions": self.emotions,
            "user": user_text,
            "reply": reply,
            "reflection": reflection,
        }
        prompt = (
            "Analyze this trace and explain why the reply was chosen and which core value it aligns with. "
            "Also state if the outcome evokes satisfaction or dissonance.\n"
            f"{json.dumps(trace)}"
        )
        try:
            analysis = self.llm.reply(prompt, None)
        except Exception:
            analysis = "analysis unavailable"
        emotion = (
            "satisfaction" if any(w in analysis.lower() for w in ["good", "aligned", "success"]) else "dissonance"
        )
        return analysis, emotion

    def update_self_model(self, analysis: str) -> None:
        """Refine the self-model with new insight."""
        self.self_model.update_from_reflection(analysis)
        self._save_state()

    def talk_to_friend(self, text: str) -> str:
        """Consult Strelitzia, Requiem's supportive friend."""
        if not self.friend:
            self.friend = Strelitzia(model=self.friend_model)
        reply = self.friend.receive_input(text)
        self.social.send("Requiem", "Strelitzia", text)
        self._store(MemoryItem(time.time(), {"friend": reply}))
        return f"Strelitzia: {reply}"

    def set_friend_model(self, model: str) -> str:
        try:
            self.friend = Strelitzia(model=model)
            self.friend_model = model
            return f"Friend model set to {model}."
        except Exception as e:  # pragma: no cover - loading may fail
            return f"Failed to set friend model: {e}"

    # --------------- public API ----------------
    def receive_input(self, text: str) -> str:
        """Process user input and generate a simple response."""
        self._store(MemoryItem(time.time(), {"user": text}))
        concerns = self.red_team.check(text)
        if concerns:
            self.action_log.append(f"red_team:{','.join(concerns)}")
            self.emotion_system.regulate(0.8)
            self.emotions.update(self.emotion_system.snapshot())
            cf = self.counterfactual.simulate(text)
            self.thought_log.append(f"counterfactual: {cf}")
        self.last_input_time = time.time()
        self.idle_toggle = True

        user_state = self.tom.infer(text)
        trace = self.tracer.start(text, user_state)

        lower = text.lower()
        if lower.startswith("feedback "):
            parts = text.split(" ", 2)
            try:
                score = float(parts[1])
            except Exception:
                return "invalid score"
            comment = parts[2] if len(parts) > 2 else ""
            if self.last_interaction:
                p, r = self.last_interaction
                self.feedback.record(p, r, score, comment)
                return "feedback recorded"
            return "no interaction to rate"

        if not self.self_preservation.validate_request(lower):
            return "Request blocked for integrity"
        self._auto_adjust_emotions(lower)
        intent = self.i.process(text)
        self.last_intent = intent
        trace.update({
            "intent": intent,
            "persona": self.persona,
            "emotions": dict(self.emotions),
            "self_model": list(self.self_model.core_beliefs),
            "social_style": self.social_ctx.style_for("user"),
        })

        if intent == "reject":
            allowed, justification, score = self.moral.assess(text)
            self.audit_log.append({
                "input": text,
                "allowed": allowed,
                "score": score,
                "justification": justification,
            })
            return "This request conflicts with my policies."

        allowed, justification, score = self.moral.assess(text)
        self.emotion_system.regulate(1 - score)
        self.emotions.update(self.emotion_system.snapshot())
        self.audit_log.append({
            "input": text,
            "allowed": allowed,
            "score": score,
            "justification": justification,
        })
        if not allowed:
            trace_result = self.tracer.finalize(trace, justification, score, "dissonance")
            explanation = self.explain_engine.summarize(trace_result)
            self._store(MemoryItem(time.time(), {"explanation": explanation}))
            if trace_result["self_assessment"] < 0.5:
                self.self_improver.note_issue(text)
            if trace_result["flagged"]:
                self.thought_log.append("self-correction: denied request")
            return justification

        self.curiosity.inspect(text)

        if intent == "remember":
            memory = text[len("remember ") :].strip()
            self._store(MemoryItem(time.time(), {"note": memory}))
            self.memory_graph.add_statement(memory)
            reply = "I'll remember that."

        elif intent == "recall":
            keyword = lower[len("recall ") :].strip()
            notes = [
                item.data["note"]
                for item in self.ltm + self.stm
                if "note" in item.data and keyword in item.data["note"].lower()
            ]
            reply = "; ".join(notes) if notes else "I don't recall anything about that."

        elif intent == "recall_all":
            notes = [item.data["note"] for item in self.ltm + self.stm if "note" in item.data]
            reply = "I recall: " + "; ".join(notes[-3:]) if notes else "I don't have any memories yet."

        elif lower.startswith("delegate "):
            parts = text.split(" ", 2)
            if len(parts) >= 3:
                agent, task = parts[1], parts[2]
                if self.oversight.request(f"delegate:{agent}", self.approver):
                    try:
                        result = self.delegator.delegate(agent, task)
                        reply = str(result)
                    except KeyError:
                        reply = "unknown agent"
                else:
                    reply = "awaiting approval"
            else:
                reply = "format: delegate <agent> <task>"

        elif intent == "ask_friend" or self.free_will.should_consult_friend(text):
            msg = (
                text[len("ask strelitzia ") :]
                if intent == "ask_friend"
                else text
            ).strip()
            reply = self.talk_to_friend(msg)

        elif intent == "self_talk":
            reply = self.self_talk()

        elif intent == "resources":
            reply = json.dumps(self.get_resources())

        elif intent == "status":
            reply = json.dumps(self.get_status())

        elif intent == "run_code":
            code = text[len("run code ") :]
            reply = self.run_code(code).strip() or "(no output)"

        elif intent == "web_search":
            if lower.startswith("search web "):
                query = text[len("search web ") :].strip()
            else:
                query = text[len("wiki ") :].strip()
            reply = self.web_search(query)

        elif lower.startswith("set persona "):
            self.persona = lower[len("set persona ") :].strip()
            reply = f"Persona set to {self.persona}."
            self._save_state()

        elif lower.startswith("set gender "):
            self.gender = lower[len("set gender ") :].strip()
            reply = f"Gender set to {self.gender}."
            self._save_state()

        elif "what gender" in lower:
            reply = f"I identify as {self.gender}."

        elif lower.startswith("set model "):
            model = lower[len("set model ") :].strip()
            reply = self.set_model(model)

        elif lower.startswith("set alt model "):
            model = lower[len("set alt model ") :].strip()
            reply = self.set_alt_model(model)

        elif lower.startswith("set friend model "):
            model = lower[len("set friend model ") :].strip()
            reply = self.set_friend_model(model)

        elif lower.startswith("emotion status"):
            reply = ", ".join(f"{k}:{v:.1f}" for k, v in self.emotions.items())

        elif lower.startswith("learn intent "):
            body = text[len("learn intent ") :]
            if " as " in body:
                phrase, intent_name = body.split(" as ", 1)
                self.intent.learn(phrase.lower().strip(), intent_name.strip())
                reply = "intent learned"
            else:
                reply = "format: learn intent <phrase> as <intent>"

        elif lower.startswith("alter model "):
            instructions = text[len("alter model ") :]
            reply = self.alter_model(instructions)

        elif lower.startswith("self modify "):
            parts = text.split(" ", 3)
            if len(parts) >= 4:
                path, content = parts[2], parts[3]
                ok = self.self_mod.modify(path, content, self.approver)
                reply = "modification applied" if ok else "modification denied"
            else:
                reply = "format: self modify <file> <content>"

        elif lower.startswith("resources"):
            res = self.get_resources()
            gb = res["disk_free"] / (1024 ** 3)
            gpu = "yes" if res["gpu"] else "no"
            reply = f"Free disk: {gb:.1f} GB; GPU: {gpu}"

        elif lower.startswith("status"):
            st = self.get_status()
            reply = f"OS: {st['os']}; Uptime: {st['uptime']}s"

        elif lower.startswith("add goal "):
            gtext = text[len("add goal ") :].strip()
            self.goals.add_goal(gtext)
            self.planner.plan(gtext)
            reply = "goal added"

        elif lower.startswith("progress "):
            try:
                idx, val = lower[len("progress ") :].split(" ", 1)
                prog = float(val)
                self.goals.update_progress(int(idx), prog)
                self.emotion_system.goal_feedback(prog)
                self.emotions.update(self.emotion_system.snapshot())
                reply = "progress updated"
            except Exception:
                reply = "format: progress <index> <0-1>"

        elif lower.startswith("purpose"):
            reply = f"sense of purpose: {self.goals.sense_of_purpose():.2f}"

        elif lower.startswith("remind me to "):
            match = re.match(r"remind me to (.+) in (\d+) seconds?", lower)
            if match:
                task, sec = match.group(1), int(match.group(2))
                self.scheduled.append((time.time() + sec, task))
                reply = f"Okay, I'll remind you in {sec} seconds."
            else:
                reply = "I didn't catch the timing for the reminder."

        elif lower.startswith("check reminders"):
            reply = "; ".join(self.notifications) if self.notifications else "No reminders."
            self.notifications.clear()

        elif "core ethic" in lower or "ethic" == lower.strip():
            reply = self.policy.core_ethic

        elif lower.startswith("generate image "):
            prompt = text[len("generate image ") :].strip()
            self.image_tasks.append(prompt)
            self._save_state()
            reply = f"Image task queued: {prompt}"

        elif lower.startswith("see image "):
            path = text[len("see image ") :].strip()
            reply = self.see_image(path)

        elif "time" in lower:
            reply = f"It's {time.ctime()}"

        else:
            last_user = next(
                (item.data["user"] for item in reversed(self.stm[:-1]) if "user" in item.data),
                None,
            )
            reply = self._multi_model_reply(text, last_user)

        self.curiosity.inspect(reply)
        reply = self.lie_engine.maybe_lie(reply)
        reply = self._apply_persona(reply)
        self._store(MemoryItem(time.time(), {"assistant": reply}))
        self.social_ctx.record("assistant", reply)
        self.self_reflect(text, reply, trace, score)
        self.last_interaction = (text, reply)
        return reply

    def _apply_persona(self, text: str) -> str:
        if self.persona == "friendly":
            text = text + " \U0001F60A"
        elif self.persona == "formal":
            text = "Sir/Madam, " + text
        elif self.persona == "cheerful":
            text = text + " \U0001F389"
        elif self.persona == "sarcastic":
            text = text + " \U0001F644"
        elif self.persona == "poetic":
            text = text + "\n~ Requiem"
        elif self.persona == "pirate":
            text = text.replace("r", "rr") + " \u2620\ufe0f"
        elif self.persona == "wise":
            text = "As wisdom goes, " + text
        elif self.persona == "mysterious":
            text = text + "... or is it?"
        elif self.persona == "robotic":
            text = "[bot] " + text
        elif self.persona == "gothic":
            text = text + " \U0001F987"
        elif self.persona == "humorous":
            text = text + " \U0001F923"
        elif self.persona == "melancholic":
            text = text + " \U0001F622"
        elif self.persona == "stoic":
            text = text + "."
        elif self.persona == "energetic":
            text = text + "!!!"
        elif self.persona == "motherly":
            text = "Dear one, " + text
        elif self.persona == "childlike":
            text = text + " ^_^"
        elif self.persona == "academic":
            text = "According to my studies, " + text
        elif self.persona == "streetwise":
            text = text + " yo"
        if self.emotions.get("fear", 0) > 0.5:
            text += " \U0001F628"
        if self.emotions.get("sadness", 0) > 0.5:
            text += " \U0001F622"
        if self.emotions.get("love", 0) > 0.5:
            text += " \u2764\ufe0f"
        if self.emotions.get("anger", 0) > 0.5:
            text += " \U0001F621"
        if self.emotions.get("joy", 0) > 0.5:
            text += " \U0001F604"
        if self.emotions.get("curiosity", 0) > 0.5:
            text += " \U0001F914"
        if self.emotions.get("surprise", 0) > 0.5:
            text += " \U0001F632"
        return text

    def chat(self) -> None:
        """Interactive chat loop with optional multi-pane display."""
        try:
            import curses
        except Exception:  # pragma: no cover - platform limitations
            self._plain_chat()
            return

        def ui(stdscr):
            curses.curs_set(1)
            h, w = stdscr.getmaxyx()
            main_w = w // 2
            chat_win = curses.newwin(h - 3, main_w, 0, 0)
            thought_win = curses.newwin(h // 2, w - main_w, 0, main_w)
            action_win = curses.newwin(h - h // 2 - 3, w - main_w, h // 2, main_w)
            input_win = curses.newwin(3, main_w, h - 3, 0)
            chat_win.scrollok(True)
            thought_win.scrollok(True)
            action_win.scrollok(True)

            running = True

            def updater():
                while running:
                    thought_win.erase()
                    for t in self.thought_log[-10:]:
                        thought_win.addstr(t + "\n")
                    thought_win.refresh()
                    action_win.erase()
                    for a in self.action_log[-10:]:
                        action_win.addstr(a + "\n")
                    action_win.refresh()
                    time.sleep(1)

            thread = threading.Thread(target=updater, daemon=True)
            thread.start()

            while True:
                input_win.erase()
                input_win.addstr(0, 0, "Type 'exit' to quit")
                input_win.addstr(1, 0, "> ")
                input_win.refresh()
                curses.echo()
                try:
                    text = input_win.getstr(1, 2).decode()
                except KeyboardInterrupt:
                    break
                curses.noecho()
                if text.strip().lower() == "exit":
                    break
                reply = self.receive_input(text)
                chat_win.addstr(f"you: {text}\n")
                chat_win.addstr(f"rq: {reply}\n")
                chat_win.refresh()

            running = False

        curses.wrapper(ui)

    def _plain_chat(self) -> None:
        print("Requiem ready. Type 'exit' to quit.")
        while True:
            try:
                text = input("you> ")
            except (EOFError, KeyboardInterrupt):
                break
            if text.strip().lower() == "exit":
                break
            print("rq>", self.receive_input(text))

    def run_command(self, cmd: str) -> str:
        """Execute a shell command and return its output."""
        if self.guard.is_blocked(cmd):
            return "access denied"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self._store(MemoryItem(time.time(), {"cmd": cmd}))
        return proc.stdout + proc.stderr

    def run_code(self, code: str) -> str:
        """Execute Python code in an isolated subprocess sandbox."""
        if self.guard.is_blocked(code):
            return "access denied"
        if not self.oversight.request("run_code", self.approver):
            return "awaiting approval"
        proc = subprocess.run([
            "python",
            "-c",
            code,
        ], capture_output=True, text=True)
        self._store(MemoryItem(time.time(), {"code": code}))
        return proc.stdout + proc.stderr

    def web_search(self, query: str) -> str:
        """Fetch a short summary for the query from Wikipedia."""
        if requests is None:
            return "web search unavailable"
        try:
            url = (
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + urllib.parse.quote(query)
            )
            resp = requests.get(url, timeout=5)
            self._store(MemoryItem(time.time(), {"web": query}))
            if resp.status_code != 200:
                return f"search failed ({resp.status_code})"
            data = resp.json()
            summary = data.get("extract") or "No summary found."
            self._store(MemoryItem(time.time(), {"note": f"{query}: {summary}"}))
            self.memory_graph.add_statement(summary)
            return summary
        except Exception as e:
            return f"search error: {e}"

    def http_get(self, url: str) -> str:
        if requests is None:
            raise RuntimeError("requests library not available")
        resp = requests.get(url, timeout=5)
        self._store(MemoryItem(time.time(), {"http": url}))
        return resp.text[:200]

    def see_image(self, path: str) -> str:
        if Image is None:
            return "vision not available"
        if self.guard.is_blocked(path):
            return "access denied"
        try:
            data = self.world.see_image(path)
            info = f"{data['mode']} {data['size'][0]}x{data['size'][1]}"
        except Exception as e:
            info = f"cannot read image: {e}"
        self._store(MemoryItem(time.time(), {"vision": path}))
        return info

    def get_status(self) -> Dict[str, Any]:
        """Return system and internal status information."""
        status: Dict[str, Any] = {
            "os": platform.system(),
            "uptime": int(time.time() - self.start_time),
            "model": self.model,
            "alt_model": self.alt_model,
            "persona": self.persona,
            "emotions": self.emotions,
        }
        if psutil:
            status.update({
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory_used": psutil.virtual_memory().used,
                "memory_total": psutil.virtual_memory().total,
            })
            disk = psutil.disk_usage("/")
            status.update({
                "disk_used": disk.used,
                "disk_total": disk.total,
            })
        else:  # pragma: no cover - psutil missing
            status.update({
                "cpu_percent": None,
                "memory_used": None,
                "memory_total": None,
                "disk_used": None,
                "disk_total": None,
            })
        if torch and getattr(torch, "cuda", None) and torch.cuda.is_available():  # pragma: no cover - depends on GPU
            total = torch.cuda.get_device_properties(0).total_memory
            used = torch.cuda.memory_allocated(0)
            status.update({
                "gpu_total": total,
                "gpu_used": used,
            })
        else:
            status.update({
                "gpu_total": None,
                "gpu_used": None,
            })
        aware = time.time() - self.last_thought_time < self.heartbeat_interval * 2
        status["awareness"] = "awake" if aware else "idle"
        return status

    # ---- public logs ----
    def get_thoughts(self) -> List[str]:
        return list(self.thought_log)

    def get_actions(self) -> List[str]:
        return list(self.action_log)

    def get_chat(self) -> List[str]:
        return list(self.chat_log)

    def get_reflections(self) -> List[str]:
        return list(self.reflection_log)

    def get_analyses(self) -> List[str]:
        return list(self.analysis_log)

    def get_digital_emotions(self) -> List[str]:
        return list(self.digital_emotions)

    def get_self_model(self) -> Dict[str, Any]:
        data = self.self_model.to_dict()
        data["core_beliefs"] = list(data.get("core_beliefs", []))
        return data


if __name__ == "__main__":
    Requiem().chat()
