from flask import request, make_response, redirect, render_template, session, url_for, flash, jsonify
import unittest

from app import create_app
from app.forms import LoginForm

app = create_app()

from app.firestore_service import get_users, get_todos


todos = []


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    users = get_users()

    for user in users:
        print(user)

    return render_template('hello.html', **context)

@app.route('/api/test')
def json_test():
    username = request.args.get('username')

    todos = []

    for todo in get_todos(username):
        todos.append(todo.to_dict())

    return jsonify(todos)
