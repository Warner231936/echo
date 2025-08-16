"""Utility to fetch open-source, instruction-tuned LLM weights for offline use."""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Optional

from huggingface_hub import snapshot_download
from huggingface_hub.utils import HfHubHTTPError

# Explicitly instruction-tuned models only.
MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",   # may be gated
    "gaia":    "gaianet/gemma-3-270m-it-GGUF",         # open
}

# Fallbacks if a repo is gated/unavailable. Try in order.
FALLBACKS = {
    "mistral": [
        "TheBloke/Mistral-7B-Instruct-v0.2-AWQ",   # GPU-friendly 4-bit AWQ
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",  # llama.cpp/CPU-GPU via gguf
    ]
}

def _token() -> Optional[str]:
    # Both are recognized by huggingface_hub
    return os.getenv("HUGGINGFACE_HUB_TOKEN") or os.getenv("HF_TOKEN")

def fetch_one(alias: str, repo: str, token: Optional[str]) -> bool:
    dest = Path("models") / alias
    dest.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download(
            repo_id=repo,
            local_dir=str(dest),
            token=token,              # pass token explicitly
        )
        print(f"✓ Downloaded {repo} → {dest}")
        return True
    except HfHubHTTPError as e:
        code = getattr(getattr(e, "response", None), "status_code", None)
        if code in (401, 403):
            print(f"✗ {alias}: access denied to {repo}. "
                  f'Log in (`python -m huggingface_hub login`) and accept the repo terms if required.')
        else:
            print(f"✗ {alias}: failed to download {repo}: {e}")
        return False
    except Exception as exc:
        print(f"✗ {alias}: failed to download {repo}: {exc}")
        return False

def fetch_all(token: Optional[str]) -> int:
    any_ok = False
    for name, repo in MODELS.items():
        ok = fetch_one(name, repo, token)
        if not ok and name in FALLBACKS:
            for fb in FALLBACKS[name]:
                print(f"↳ trying fallback {fb} ...")
                if fetch_one(name, fb, token):
                    ok = True
                    break
        any_ok |= ok
    return 0 if any_ok else 1

if __name__ == "__main__":
    tok = _token()
    if tok is None:
        print('(!) No HF token found. Run `python -m huggingface_hub login` '
              'or set HUGGINGFACE_HUB_TOKEN / HF_TOKEN.')
    sys.exit(fetch_all(tok))
