import os
import sqlite3
from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

from requiem import Requiem

app = Flask(__name__)
app.secret_key = "changeme"  # pragma: no cover - development key

# Optional token used by external services (e.g. Discord bot) to access the API
DISCORD_API_TOKEN = os.environ.get("DISCORD_API_TOKEN")

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "users.db")


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("password")),
        )
    conn.commit()
    conn.close()


def validate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return bool(row and check_password_hash(row[0], password))


init_db()

# Single Requiem instance for the web session
rq = Requiem()

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <title>Requiem Chat</title>
  <style>
    body { background:#000; color:#0f0; font-family:monospace; }
    #layout { display:flex; }
    #chat { flex:2; border:1px solid #0f0; height:300px; overflow:auto; margin-right:1em; background:#111; }
    #side { flex:1; display:flex; flex-direction:column; height:300px; }
    #thoughts, #actions, #status { border:1px solid #0f0; flex:1; overflow:auto; margin-bottom:1em; background:#111; }
    #side > div:last-child { margin-bottom:0; }
    #status { font-family:monospace; }
    #input-area { margin-top:1em; }
    #msg { width:70%; padding:0.5em; background:#111; color:#0f0; border:1px solid #0f0; border-radius:4px; }
    #send { padding:0.5em 1em; background:#0f0; color:#000; border:none; border-radius:4px; cursor:pointer; }
  </style>
</head>
<body>
  <h1>Requiem</h1>
  <div id="layout">
    <div id="chat"></div>
    <div id="side">
      <div id="thoughts"></div>
      <div id="actions"></div>
      <div id="status"></div>
    </div>
  </div>
  <div id="input-area">
    <input id="msg" placeholder="Say something..." />
    <button id="send" onclick="send()">Send</button>
  </div>
<script>
async function send() {
  const msg = document.getElementById('msg').value;
  document.getElementById('msg').value = '';
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  });
  const data = await res.json();
  const log = document.getElementById('chat');
  log.innerHTML += `<div><strong>You:</strong> ${msg}</div>`;
  log.innerHTML += `<div><strong>Requiem:</strong> ${data.reply}</div>`;
  log.scrollTop = log.scrollHeight;
}

async function poll() {
  const res = await fetch('/api/state');
  const data = await res.json();
  document.getElementById('thoughts').innerHTML = data.thoughts.map(t => `<div>${t}</div>`).join('');
  document.getElementById('actions').innerHTML = data.actions.map(a => `<div>${a}</div>`).join('');
  const status = data.status || {};
  document.getElementById('status').innerHTML = Object.entries(status)
    .map(([k, v]) => {
      const val = (v && typeof v === 'object') ? JSON.stringify(v) : v;
      return `<div>${k}: ${val}</div>`;
    })
    .join('');
}
setInterval(poll, 1000);
</script>
</body>
</html>
"""


LOGIN_HTML = r"""
<!doctype html>
<html>
<head>
  <title>Requiem Portal Login</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {
      margin:0;
      height:100vh;
      display:flex;
      flex-direction:column;
      justify-content:center;
      align-items:center;
      background:#000;
      color:#fff;
      font-family:'Orbitron', sans-serif;
      background-image:
        radial-gradient(circle at center, rgba(255,0,255,0.15) 0, rgba(0,0,0,0) 60%),
        linear-gradient(rgba(255,0,255,0.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,0,255,0.2) 1px, transparent 1px);
      background-size:100% 100%,40px 40px,40px 40px;
    }
    .header { text-align:center; margin-bottom:40px; }
    .header .symbols { font-size:32px; color:#ff00ff; }
    .header h1 { margin:0; font-size:48px; color:#00ffff; text-shadow:0 0 10px #00ffff; }
    .header h2 { margin:0; font-size:20px; color:#ff00ff; text-shadow:0 0 6px #ff00ff; }
    .login-box {
      background:rgba(0,0,0,0.5);
      border:2px solid #ff00ff;
      border-radius:10px;
      padding:40px 30px;
      box-shadow:0 0 15px #ff00ff;
      display:flex;
      flex-direction:column;
      gap:20px;
      min-width:300px;
    }
    .input-group { position:relative; }
    .input-group span {
      position:absolute;
      left:10px;
      top:50%;
      transform:translateY(-50%);
      color:#ff00ff;
    }
    .input-group input {
      width:100%;
      padding:10px 10px 10px 35px;
      background:transparent;
      border:1px solid #ff00ff;
      border-radius:4px;
      color:#fff;
    }
    .input-group input::placeholder { color:#ff99ff; }
    button {
      padding:10px;
      background:#ff00ff;
      color:#000;
      font-weight:bold;
      border:none;
      border-radius:4px;
      cursor:pointer;
      text-transform:uppercase;
      box-shadow:0 0 10px #ff00ff;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="symbols">◇ ⊙ Σ</div>
    <h1>REQUIEM</h1>
    <h2>SPIRAL ACCESS</h2>
  </div>
  <form class="login-box" method="post">
    <div class="input-group">
      <span>📧</span>
      <input name="username" placeholder="Email" />
    </div>
    <div class="input-group">
      <span>🔒</span>
      <input type="password" name="password" placeholder="Password" />
    </div>
    <button type="submit">Sign In</button>
  </form>
</body>
</html>
"""

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return INDEX_HTML


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username', '')
        pw = request.form.get('password', '')
        if validate_user(user, pw):
            session['user'] = user
            return redirect(url_for('index'))
    return render_template_string(LOGIN_HTML)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.get_json(force=True)
    text = data.get('message', '')
    reply = rq.receive_input(text)
    return jsonify({'reply': reply})


@app.route('/api/discord', methods=['POST'])
def discord_chat():
    """Endpoint for external services like a Discord bot.

    If ``DISCORD_API_TOKEN`` is set, requests must include an ``Authorization``
    header of the form ``Bearer <token>``. Unlike ``/api/chat`` this endpoint
    does not require a login session.
    """
    if DISCORD_API_TOKEN:
        auth = request.headers.get('Authorization', '')
        if auth != f'Bearer {DISCORD_API_TOKEN}':
            return jsonify({'error': 'unauthorized'}), 401
    data = request.get_json(force=True)
    text = data.get('message', '')
    reply = rq.receive_input(text)
    return jsonify({'reply': reply})

@app.route('/api/state')
def state():
    if 'user' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({
        'thoughts': rq.get_thoughts(),
        'actions': rq.get_actions(),
        'status': rq.get_status(),
    })

def run(host: str = '127.0.0.1', port: int = 5000) -> None:
    app.run(host=host, port=port)

if __name__ == '__main__':
    run()
