from flask import render_template, request, redirect, url_for, session
from app import app
from app import game_logic  # Импортируем нашу вынесенную логику


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Якубович'}
    return render_template('index.html', title='Home', user=user)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/page')
def page():
    return render_template('page.html')


# Обновленный роут вашей игры
@app.route('/game')
def game():
    # Если игра еще не создана в текущей сессии браузера, стартуем её
    if 'secret' not in session:
        game_logic.start_new_game(session)

    is_victory = '*' not in session.get('mask', [])

    return render_template(
        'game.html',
        title="Game",
        hint=session.get('hint'),
        mask=session.get('mask'),
        is_victory=is_victory,
        secret=session.get('secret')
    )


# Новый роут для обработки отправленной посетителем буквы (POST из формы)
@app.route('/game/turn', methods=['POST'])
def game_turn():
    letter = request.form.get('letter', '').strip()
    if letter:
        game_logic.process_letter(session, letter)
    return redirect(url_for('game'))


# Новый роут для перезапуска игры (кнопка "Играть снова")
@app.route('/game/reset')
def game_reset():
    session.pop('secret', None)
    session.pop('mask', None)
    session.pop('hint', None)
    return redirect(url_for('game'))
