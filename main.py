from flask import Flask 
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap 
from flask_wtf import Form 
from wtforms import StringField, SubmitField 
from wtforms.validators import Required
from flask import url_for
from flask import session, flash


class NameForm(Form):
    name = StringField("What is your name?", validators=[Required()])
    submit = SubmitField("Submit")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)





@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
        session['name'] = form.name.data 
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h1>Hello, %s</h1>' % user.name



if __name__ == '__main__':
    manager.run()