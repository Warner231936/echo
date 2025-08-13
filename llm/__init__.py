+import os
+from typing import Optional
+
+from .base import BaseLLM
+
+
+class EchoLLM(BaseLLM):
+    """Fallback model that simply echoes the user input."""
+
+    def reply(self, text: str, last_user: Optional[str]) -> str:
+        prefix = f"Previously you said '{last_user}'. " if last_user else ""
+        return f"{prefix}Echo: {text}"
+
+
+def load_llm(model: str = "mistral-tiny") -> BaseLLM:
+    """Return an available language model client or an echo fallback."""
+    api_key = os.environ.get("MISTRAL_API_KEY")
+    if api_key:
+        try:
+            from .mistral import MistralLLM
+            return MistralLLM(api_key, model)
+        except Exception:  # pragma: no cover - network/import issues
+            pass
+    return EchoLLM()
