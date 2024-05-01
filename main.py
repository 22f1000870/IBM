from flask import Flask, redirect, render_template, request, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.exceptions import Unauthorized
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login_db.sqlite3"
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

login = LoginManager(app)

app.app_context().push()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('userdash'))
            else:
                return "<h1>Wrong password</h1>"
        else:
            return "<h1>User not found</h1>"

    return render_template('login.html')

@app.route('/dash')
@login_required
def userdash():
    response = make_response(render_template('user.html', user=current_user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate' #learn this
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/logout')
@login_required #sequence matter only after app.route
def logout():
    logout_user()
    return redirect(url_for('loginuser'))

@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return redirect(url_for('loginuser'))
if __name__ == '__main__':
    app.run(debug=True)
