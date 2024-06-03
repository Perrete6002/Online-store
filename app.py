from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import createTable, insertRow, get_user_by_username, update_user as db_update_user
from db_shop import insertRow_product, obtener_productos_existentes, get_product_by_id, update_product, delete_product_from_db

app = Flask(__name__)

# Configuración de la clave secreta
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    logged_in = session.get('logged_in', False)
    return render_template('index.html', logged_in=logged_in)

@app.route('/home')
def home_redirect():
    return redirect(url_for('home'))

@app.route('/login-register')
def login_register():
    logged_in = session.get('logged_in', False)
    return render_template('login_register.html', logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user[2] == password:
            flash('Login successful!', 'success')
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    logged_in = session.get('logged_in', False)
    return render_template('login.html', logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_username(username)
        if user:
            flash('Username already exists', 'danger')
        else:
            insertRow(username, email, password)
            flash('Registration successful!', 'success')
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('home')) 
    logged_in = session.get('logged_in', False)
    return render_template('register.html', logged_in=logged_in)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        username = session['username']
        user = get_user_by_username(username)
        if request.method == 'POST':
            new_username = request.form['new_username']
            new_email = request.form['new_email']
            new_password = request.form['new_password']
            db_update_user(username, new_username, new_email, new_password)
            flash('User information updated successfully!', 'success')
            
            if new_username != username:
                session['username'] = new_username
            
            return redirect(url_for('user'))
        
        logged_in = session.get('logged_in', False)
        return render_template('user.html', user=user, logged_in=logged_in)
    return redirect(url_for('login_register'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login_register'))

@app.route('/galery')
def gallery():
    logged_in = session.get('logged_in', False)
    return render_template('gallery.html', logged_in=logged_in)

@app.route('/gallery_view')
def gallery_view():
    logged_in = session.get('logged_in', False)
    return render_template('gallery_view.html', logged_in=logged_in)

@app.route('/shop')
def shop():
    logged_in = session.get('logged_in', False)
    productos = obtener_productos_existentes()
    return render_template('shop.html', logged_in=logged_in, productos=productos)



# Ruta para administrar productos
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        tag = request.form['tag']
        ID = request.form['id']
        
        insertRow_product(name, description, price, tag, ID)
        return redirect(url_for('admin'))
    else:
        producto = obtener_productos_existentes()

        return render_template('admin.html', products=producto)

@app.route('/modify/<product_id>', methods=['GET'])
def modify_product(product_id):
    product = get_product_by_id(product_id)
    return render_template('modify_product.html', product=product)

@app.route('/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    delete_product_from_db(product_id)
    return redirect(url_for('admin'))


@app.route('/update/<product_id>', methods=['POST'])
def update_product_route(product_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        tag = request.form['tag']
        
        success = update_product(product_id, name, description, price, tag)
        
        if success:
            return redirect(url_for('admin'))
        else:
            return "Error al actualizar el producto."


if __name__ == '__main__':
    createTable() 
    app.run(debug=True)
