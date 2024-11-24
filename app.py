from flask import Flask, request, session, redirect, url_for, render_template
app = Flask(__name__)
users_list = []
user_series = {}
app.secret_key = 'password'



@app.route('/')
def lista_series():
    username = session.get('username')
    me_gustaria_ver = []
    estoy_viendo = []
    vistas = []
    if username and username in user_series:
        series = user_series[username]
        me_gustaria_ver = [serie for serie in series if serie['categoria'] == 'Me gustaría ver']
        estoy_viendo = [serie for serie in series if serie['categoria'] == 'Estoy viendo']
        vistas = [serie for serie in series if serie['categoria'] == 'Vistas']

    else:
        series = []
    return render_template('lista_series.html', logged_in = session.get('logged_in', False),
                           me_gustaria_ver = me_gustaria_ver,
                           estoy_viendo = estoy_viendo,
                           vistas = vistas)

@app.route('/login', methods=['GET', 'POST'])
def login_function():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users_list if user['username'] == username), None)
        if user and user['password'] == password:
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('lista_series'))
        else:
            error_login = 'Invalid username or password'
            return render_template('login.html', error=error_login)

    return render_template('login.html')



@app.route('/logout')
def logout_function():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login_function'))

@app.route('/register', methods=['GET', 'POST'])
def register_function():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if any(user['username'] == username for user in users_list):
            error = 'Username already registered'
            return render_template('register.html', error=error)
        else:
            users_list.append({'username': username, 'password': password})
            return redirect(url_for('login_function'))
    else:
        return render_template('register.html')

@app.route('/agregar_serie', methods=['GET', 'POST'])
def agregar_serie():
    if not session.get('logged_in', False):
        return redirect(url_for('login_function'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        sinopsis = request.form['sinopsis']
        puntuacion = request.form['puntuacion']
        genero = request.form['genero']
        fecha_estreno = request.form['fecha_estreno']
        num_capitulos = request.form['num_capitulos']
        duracion = request.form['duracion']
        categoria = request.form['categoria']

        username = session.get('username')
        if username not in user_series:
            user_series[username] = []

        nueva_serie = {
            'nombre': nombre,
            'sinopsis': sinopsis,
            'puntuacion': puntuacion,
            'genero': genero,
            'fecha_estreno': fecha_estreno,
            'num_capitulos': num_capitulos,
            'duracion': duracion,
            'categoria': categoria,
        }
        user_series[username].append(nueva_serie)
        return redirect(url_for('lista_series'))

    return render_template('agregar_serie.html', logged_in = session.get('logged_in', False))


if __name__ == '__main__':
    app.run()