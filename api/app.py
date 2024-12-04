import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Cria ou conecta ao banco de dados
def init_db():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        ''')
    conn.commit()

# Rota principal para exibir o estoque
@app.route('/')
def index():
    with sqlite3.connect(os.path.join(os.path.dirname(__file__), '../estoque.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, quantidade, preco FROM estoque')
        estoque = cursor.fetchall()
    return render_template('index.html', estoque=estoque)

# Rota para adicionar item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        with sqlite3.connect('estoque.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO estoque (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')

# Rota para excluir item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
