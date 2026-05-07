from app import create_app


def test_autorization():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get('/autorization')
    assert response.status_code == 200, 'Ожидается 200'
    answer = response.get_data(as_text = True)
    assert 'У вас нет доступа' in answer
