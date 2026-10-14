from unittest.mock import MagicMock


def test_index_route(client):
    """Проверка главной страницы и её алиаса."""
    for path in ['/', '/index']:
        response = client.get(path)
        assert response.status_code == 200


def test_static_routes(client):
    """Проверка простых текстовых страниц."""
    assert client.get('/about').status_code == 200
    assert client.get('/page').status_code == 200


def test_game_route_new_game(client, monkeypatch):
    """Проверка инициализации новой игры при пустой сессии."""

    # Функция-имитатор, которая запишет дефолтные значения в сессию при старте
    def fake_start_new_game(sess):
        sess['secret'] = 'СЛОВО'
        sess['mask'] = ['*', '*', '*', '*', '*']
        sess['hint'] = 'Тестовая подсказка'

    monkeypatch.setattr('app.game_logic.start_new_game', fake_start_new_game)

    response = client.get('/game')

    # Теперь Jinja2 получит маску ['*', '*', ...] и не упадет с ошибкой
    assert response.status_code == 200


def test_game_route_existing_game(client, monkeypatch):
    """Проверка отображения текущего прогресса игры."""
    mock_start_game = MagicMock()
    monkeypatch.setattr('app.game_logic.start_new_game', mock_start_game)

    with client.session_transaction() as sess:
        sess['secret'] = 'СЛОВО'
        sess['mask'] = ['*', '*', '*', '*', '*']
        sess['hint'] = 'Подсказка'

    response = client.get('/game')
    assert response.status_code == 200
    mock_start_game.assert_not_called()  # Новая игра не должна запускаться


def test_game_turn_processing(client, monkeypatch):
    """Проверка отправки валидного символа через POST."""
    mock_process_letter = MagicMock()
    monkeypatch.setattr('app.game_logic.process_letter', mock_process_letter)

    response = client.post('/game/turn', data={'letter': 'а'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/game'
    mock_process_letter.assert_called_once()


def test_game_reset_clears_session(client):
    """Проверка сброса состояния игры."""
    with client.session_transaction() as sess:
        sess['secret'] = 'СЛОВО'
        sess['mask'] = ['*']

    response = client.get('/game/reset')
    assert response.status_code == 302

    with client.session_transaction() as sess:
        assert 'secret' not in sess
        assert 'mask' not in sess
