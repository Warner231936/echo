@echo off
REM Start the Requiem web UI with the local Mistral 7B model.
REM Downloads the model on first run if missing.

setlocal

if not exist "models\mistral" (
    echo Mistral model not found. Downloading...
    python download_models.py
)

set "LLM_MODEL=models\mistral"
python web.py %*

endlocal
