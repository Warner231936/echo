# Requiem Setup

This repository contains a prototype AI core.

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

> **Note:** These scripts attempt to install optional components and may require adjustments for your specific environment.

## LLMs

Model clients live in the `llm/` directory. By default Requiem falls back to
an echo model, but it can use providers such as Mistral when configured. To
enable Mistral install the `mistralai` package and provide an API key via the
`MISTRAL_API_KEY` environment variable:

```bash
export MISTRAL_API_KEY="your-key"
pip install mistralai
```

Without a key the assistant uses the echo model.

## Usage

Launch a simple chat loop:

```bash
python requiem.py
```

While chatting you can ask it to remember notes:

- `remember the sky is blue`
- `what do you remember?`

Mention "time" in a message to get the current time. Type `exit` to quit.
