from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from AI import Gemini, openAI  
from datetime import timedelta
import DB

app = Flask(__name__)
app.secret_key = 'Th!$1$@S3cr3tK3y'
app.permanent_session_lifetime = timedelta(days=10)
DB.init_db()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def homePage():
    if 'user' in session:
        return redirect(url_for('chatPage'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = DB.validate_login(email, password)

        if user:
            session['user'] = {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
            flash(f"Welcome back, {user[1]}! ✅", "success")
            return redirect(url_for('chatPage'))
        else:
            flash("Invalid email or password", "error")
            return redirect('/login')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if 'user' in session:
        return redirect(url_for('chatPage'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        mobile = request.form.get('mobile')

        success = DB.register_user(username, email, password, gender, mobile)
        if success:
            flash(f"Hello {username}, your registration was successful! 🎉", "success")
            return redirect('/login')
        else:
            flash("Email already exists. Try logging in.", "error")
            return redirect('/register')

    return render_template('register.html')


@app.route('/chat')
def chatPage():
    if 'user' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('homePage'))
    return render_template('chat.html', username=session['user']['name'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('homePage'))


@app.route('/ask', methods=['POST'])
def ask():
    if 'user' not in session:
        return jsonify({'reply': "Session expired. Please log in again."})
    user_message = request.json.get('message')
    response = Gemini(user_message)
    return jsonify({'reply': response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)