from flask import Blueprint, request, jsonify
from models.item import db, Item

item_bp = Blueprint('item_bp', __name__)

@item_bp.route('/item', methods=['GET'])
def listar_itens():
    itens = Item.query.all()
    itens_json = [ item.json() for item in itens ]
    
    return jsonify({
        'count': len( itens_json ),
        'itens': itens_json
    })

@item_bp.route('/item/<int:id>', methods=['GET'])
def buscar_item(id):
    item = Item.query.get(id)
    
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    
    return jsonify({
        'item': item.json()
    })

@item_bp.route('/item', methods=['POST'])
def criar_item():
    data = request.json # Capturando os dados enviados na requisição 

    # Criando um item a partir do objeto enviado
    item_novo = Item(
        nome = data['nome'],
        descricao = data['descricao'],
        comprado = data['comprado']
    )

    db.session.add( item_novo ) # Adiciona o item ao banco de dados

    db.session.commit() # Salva as alterações

    return jsonify({
        'message': 'Item criado com sucesso!',
        'item': item_novo.json()
    }), 201

@item_bp.route('/item/<int:id>', methods=['PUT'])
def atualizar_item(id):
    item = Item.query.get(id)
    
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    
    data = request.json
    item.nome = data.get("nome", item.nome)
    item.descricao = data.get("descricao", item.descricao)
    item.comprado = data.get("comprado", item.comprado)

    db.session.commit()

    return jsonify({
        'item': item.json(),
        "mensagem": "Item atualizado!"
    })

@item_bp.route('/item/<int:id>', methods=['PATCH'])
def atualizar_item_parcial(id):
    item = Item.query.get(id)

    if not item:
        return jsonify({
            "erro": "Item não encontrado"
        }), 404
    
    data= request.json

    item.nome = data.get("nome", item.nome)
    item.descricao = data.get("descricao", item.descricao)
    item.comprado = data.get("comprado", item.comprado)

    db.session.commit()

    # 200 é o código de status HTTP para sucesso na requisição
    return jsonify({
        'message': 'Item atualizado com sucesso!',
        'item': item.json() 
    }), 200

@item_bp.route('/item/<int:id>', methods=['DELETE'])
def deletar_item(id):
    item = Item.query.get(id)

    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    
    db.session.delete( item )
    db.session.commit()
    
    return jsonify({
        "mensagem": f"Item com ID {item.id} deletado!"
    })