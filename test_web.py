from web import app, rq


def test_web_chat():
    client = app.test_client()
    client.post('/login', data={'username': 'admin', 'password': 'password'})
    resp = client.post('/api/chat', json={'message': 'hello'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'reply' in data
    assert isinstance(data['reply'], str)


def test_state_endpoint():
    rq.run_command('echo hi')
    rq.self_talk(turns=1)
    client = app.test_client()
    client.post('/login', data={'username': 'admin', 'password': 'password'})
    state = client.get('/api/state').get_json()
    assert 'thoughts' in state and 'actions' in state and 'status' in state
    assert any('echo hi' in a for a in state['actions'])
    status = state['status']
    assert 'os' in status and 'model' in status and 'persona' in status
