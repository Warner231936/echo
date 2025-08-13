diff --git a//dev/null b/README.md
index 0000000000000000000000000000000000000000..a1666db99d466c8c9952263403029e8bad94f9f5 100644
--- a//dev/null
+++ b/README.md
@@ -0,0 +1,34 @@
+# Requiem Setup
+
+This repository contains a prototype AI core.
+
+## Windows
+Run `setup.ps1` in an elevated PowerShell prompt to install MongoDB, CUDA, and Python dependencies:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File .\setup.ps1
+```
+
+## Linux
+A basic `setup.sh` script is available for Ubuntu-based systems:
+
+```bash
+bash setup.sh
+```
+
+> **Note:** These scripts attempt to install optional components and may require adjustments for your specific environment.
+
+## Usage
+
+Launch a simple chat loop:
+
+```bash
+python requiem.py
+```
+
+While chatting you can ask it to remember notes:
+
+- `remember the sky is blue`
+- `what do you remember?`
+
+Mention "time" in a message to get the current time. Type `exit` to quit.
