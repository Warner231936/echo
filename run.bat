@echo off
REM Launch Requiem chat loop with a local Mistral 7B model.
REM Downloads the model on first run if missing.

setlocal

if not exist "models\mistral" (
    echo Mistral model not found. Downloading...
    python download_models.py
)

set "LLM_MODEL=models\mistral"
python requiem.py %*

endlocal
