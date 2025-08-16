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
  document.getElementById('status').innerHTML = Object.entries(status).map(([k,v]) => `<div>${k}: ${v}</div>`).join('');
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
  <style>
    body { background:#000; color:#0f0; font-family:monospace; height:100vh; margin:0; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; }
    pre { margin-top:0; margin-bottom:auto; text-align:center; color:#0f0; }
    form { margin-bottom:10%; display:flex; flex-direction:column; align-items:center; }
    input { margin:0.5em; padding:0.5em; background:#111; border:1px solid #0f0; color:#0f0; border-radius:4px; }
    button { padding:0.5em 1em; background:#0f0; color:#000; border:none; border-radius:4px; cursor:pointer; }
  </style>
</head>
<body>
<pre>
 ____                  _                  ____            _        _
|  _ \ ___  __ _ _   _(_) ___ _ __ ___   |  _ \ ___  _ __| |_ __ _| |
| |_) / _ \/ _` | | | | |/ _ \ '_ ` _ \  | |_) / _ \| '__| __/ _` | |
|  _ <  __/ (_| | |_| | |  __/ | | | | | |  __/ (_) | |  | || (_| | |
|_| \_\___|\__, |\__,_|_|\___|_| |_| |_| |_|   \___/|_|   \__\__,_|_|
              |_|                                                    
</pre>
<form method="post">
  <input name="username" placeholder="username" />
  <input type="password" name="password" placeholder="password" />
  <button type="submit">Login</button>
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
