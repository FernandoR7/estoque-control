from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates", static_folder="static")

# Lista volátil para armazenar os itens
estoque = []

# Rota principal para exibir o estoque
@app.route('/')
def index():
    return render_template('index.html', estoque=estoque)

# Rota para adicionar item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            quantidade = int(request.form['quantidade'])
            preco = float(request.form['preco'])
            # Adiciona o item à lista volátil
            item_id = len(estoque) + 1  # Gera um ID incremental
            estoque.append({'id': item_id, 'nome': nome, 'quantidade': quantidade, 'preco': preco})
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao adicionar item: {e}")
            return "Erro ao adicionar item", 500
    return render_template('add_item.html')

# Rota para excluir item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    global estoque
    # Remove o item da lista pelo ID
    estoque = [item for item in estoque if item['id'] != item_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
