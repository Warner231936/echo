"""Utility to fetch open source, instruction-tuned LLM weights for offline use."""
from huggingface_hub import snapshot_download

# Map of instruction-following model aliases to their HuggingFace repositories.
# Only models that are explicitly instruction-tuned are listed here so that the
# system does not accidentally download base models.
MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
    "gaia": "gaianet/gemma-3-270m-it-GGUF",
}


def fetch_all() -> None:
    for name, repo in MODELS.items():
        try:
            snapshot_download(repo, local_dir=f"models/{name}", local_dir_use_symlinks=False)
            print(f"Downloaded {repo} to models/{name}")
        except Exception as exc:
            print(f"Failed to download {repo}: {exc}")


if __name__ == "__main__":
    fetch_all()
