import json, os, tempfile, hashlib, time
import portalocker

PATH = "ltm_state.json"
LOCK_SUFFIX = ".lock"

def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def read_ltm(path: str = PATH, default=None):
    try:
        with open(path, "rb") as f:
            return json.loads(f.read().decode("utf-8"))
    except Exception:
        return default

def write_ltm(obj, path: str = PATH):
    data = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    h = _sha256(data)
    lock_path = path + LOCK_SUFFIX
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(lock_path, "w") as lf, portalocker.Lock(lock_path, timeout=5):
        fd, tmp = tempfile.mkstemp(prefix=".ltm_", dir=os.path.dirname(path) or ".")
        with os.fdopen(fd, "wb") as w:
            w.write(data)
            w.flush()
            os.fsync(w.fileno())
        os.replace(tmp, path)
    return h
