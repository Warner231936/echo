"""Utility to fetch open source LLM weights for offline use."""
from huggingface_hub import snapshot_download

MODELS = {
    "openllm": "openlm-research/open_llama_3b",
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
