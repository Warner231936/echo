#!/usr/bin/env bash
set -e

# Update package list
sudo apt-get update

# Core tools
sudo apt-get install -y curl gnupg

# ---- MongoDB ----
if ! command -v mongod >/dev/null 2>&1; then
  curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
  echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
  sudo apt-get update || true
  sudo apt-get install -y mongodb-org || echo "MongoDB installation failed; repository may not support this Ubuntu version."
fi

# ---- CUDA Toolkit ----
sudo apt-get install -y nvidia-cuda-toolkit || echo "CUDA toolkit installation failed."

# ---- Python Dependencies ----
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python3 -m pip install --upgrade transformers accelerate safetensors sentencepiece
python3 -m pip install autoawq requests pymongo flask psutil

# Fetch instruction-tuned model weights so they are available immediately after
# setup completes.
python3 download_models.py
