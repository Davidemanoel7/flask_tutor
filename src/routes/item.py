from flask import Blueprint, request, jsonify
from models.item import db, Item
import sys

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
        descricao = data.get('descricao', ''),
        comprado = data.get('comprado', False),
        quantidade = data.get('quantidade', 0)
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
    item.comprado = data.get("comprado", item.comprado )
    item.quantidade = data.get("quantidade", item.quantidade)

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
    item.comprado = data.get("comprado", item.comprado )
    item.quantidade = data.get("quantidade", item.quantidade)

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

@item_bp.route('/itens', methods=['GET'])
def listar_comprados():
    args_str = request.args.get('comprado', default='', type=str )

    args_comprado = parse_bool( args_str )

    if args_comprado is None:
        return jsonify({
            'erro': 'Parâmetro "comprado" inválido. Use true ou false'
            }), 400
    
    itens = Item.query.filter_by( comprado= args_comprado ).all()
    itens_json = [ item.json() for item in itens ]

    return jsonify({
        'count': len( itens_json ),
        'itens': itens_json
    })


def parse_bool(value):
    """Converte strings comuns para booleano"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.strip().lower()
        if value in {"true", "1", "yes", "on"}:
            return True
        elif value in {"false", "0", "no", "off"}:
            return False
        else:
            return False
    return None