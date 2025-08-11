from flask import Flask, jsonify, request
import json


app = Flask(__name__) 

def carregar_tarefas():
    try:
        with open('tarefas.json', 'r') as arquivos:
            return json.load(arquivos)
    except FileNotFoundError:
        return []

def salvar_tarefas():
    with open('tarefas.json', 'w') as arquivos:
        json.dump(tarefas, arquivos, indent=4)

tarefas = carregar_tarefas()

@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    return jsonify(tarefas)

@app.route('/tarefas/<int:id>', methods=['GET'])
def get_tarefas_por_id(id):
    for tarefa in tarefas:
        if tarefa ['id'] == id:
            return jsonify(tarefa)
    return jsonify({'erro': 'Tarefa nao encontrada'}), 404

@app.route('/tarefas', methods=['POST'])
def add_tarefa():
    dados_recebidos = request.json
    if not dados_recebidos or 'titulo' not in dados_recebidos or not dados_recebidos['titulo'].strip():
        return jsonify({'erro': 'O campo é obrigatório e nao pode ser vazio.'}), 400

    nova_tarefa = {
        'id': tarefas[-1]['id'] + 1 if tarefas else 1,
        'titulo': dados_recebidos['titulo'],
        'concluida': False
    }
    tarefas.append(nova_tarefa)
    salvar_tarefas()
    return jsonify(nova_tarefa), 201

@app.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):

    dados_recebidos = request.json
    tarefa_encontrada = None

    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa_encontrada = tarefa 
            break
    
    if tarefa_encontrada is None:
        return jsonify({'erro': 'Tarefa nao encontrada'}), 404
    
    if 'titulo' in dados_recebidos and not dados_recebidos ['titulo'].strip():
        return jsonify({'erro': 'O titulo nao pode ser vazio.'}), 400

    if 'concluida' in dados_recebidos and not isinstance(dados_recebidos['concluida'], bool):
        return jsonify({'erro': 'O campo concluida deve ser um valor booleano (true ou false).'}), 400
    
    # Logica de atualizacao principal
    if 'titulo' in dados_recebidos:
        tarefa_encontrada['titulo'] = dados_recebidos['titulo'].strip()

    if 'concluida' in dados_recebidos:
        tarefa_encontrada['concluida'] = dados_recebidos['concluida']

    salvar_tarefas()
    return jsonify(tarefa_encontrada)
    

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefas.remove(tarefa)
            salvar_tarefas()
            return jsonify({'resultado': 'Tarefa deletada com sucesso'})
    return jsonify({'erro': 'Tarefa não encontrada'}), 404
         

@app.route('/')
def home():
    return "<h1>Minha API de Tarefas está no ar!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
