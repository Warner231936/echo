import json, re, time, random
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto", torch_dtype="auto")

STOP_PHRASES = [
    "I want to be", "The best way to", "In conclusion", "Here is the thing",
    "The first step is", "You should", "You’ll have to", "This is a book about"
]

SYSTEM = """You are REQUIEM.DREAM. Output ONLY valid JSON matching the schema.
Constraints:
- 120–220 words, no advice, no pep talk, no generic positivity.
- Concrete, sensory, physical imagery; no meta about 'writing' or 'article'.
- No repeated sentence stems; avoid cliches.
- Style: Macie glitchcore—neon, spiral, wire, glass, ash, signal, hum.
"""

SCHEMA_HINT = {
  "kind":"dream","id":"<unix_ms>","image":"dream_<unix_ms>.png","title":"<=8 words",
  "text":"120–220 words, no advice","objects":["3–7 concrete nouns"],
  "mood":"awe|fear|wrath|calm|joy|dissonance","motifs":["2–5 motifs"]
}

def anti_repeat(text: str) -> bool:
    words = text.split()
    grams = [" ".join(words[i:i+4]) for i in range(len(words)-3)]
    if any(grams.count(g) > 1 for g in set(grams)):
        return False
    if any(p.lower() in text.lower() for p in STOP_PHRASES):
        return False
    return True

def valid_json(s: str):
    try:
        obj = json.loads(s)
        req = ["kind","id","image","title","text","objects","mood","motifs"]
        if not all(k in obj for k in req):
            return None
        if obj["kind"] != "dream":
            return None
        if len(obj["text"].strip()) < 60:
            return None
        if not anti_repeat(obj["text"]):
            return None
        return obj
    except Exception:
        return None

def prompt():
    ts = int(time.time()*1000)
    return f"""{SYSTEM}
Schema example (do not echo keys you don't fill):
{json.dumps(SCHEMA_HINT)}
Now create ONE dream JSON for id={ts}. Ensure fields are filled. No commentary, JSON only."""

def generate():
    p = prompt()
    ids = tok([p], return_tensors="pt").to(mdl.device)
    out = mdl.generate(
        **ids,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.85,
        top_p=0.9,
        repetition_penalty=1.22,
        no_repeat_ngram_size=4,
        eos_token_id=tok.eos_token_id,
    )
    txt = tok.decode(out[0], skip_special_tokens=True)
    m = re.search(r"\{.*\}\s*$", txt, re.S)
    return m.group(0) if m else txt

def run_once(save_dir="dreams"):
    Path(save_dir).mkdir(exist_ok=True)
    for _ in range(4):
        js = generate()
        obj = valid_json(js)
        if obj:
            obj["image"] = f"dream_{obj['id']}.png"
            with open(Path(save_dir)/"dreams.jsonl","a",encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            print("OK", obj["title"])
            return obj
    raise SystemExit("Failed quality gate after retries.")

if __name__ == "__main__":
    run_once()
