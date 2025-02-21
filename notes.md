# Projeto Lista de Supermercado

Quase todos os comandos executados usam o terminal, então evite fechá-lo...

## Verifiacr se tudo está instalado:
- Python: caso não tenha instalado, considere acessar [python org](https://www.python.org/downloads/) e seguir o tutorial.

Abra um terminal e execute para verificar a versão do python instalada.:
```sh
    python --version
    python3 --version
```
- pip: caso não tenha instalado, considere acessar [pip](https://pip.pypa.io/en/stable/installation/) e seguir o tutorial.

Verifique a versão do pip

```sh
    pip --version
    pip3 --version
```

- Vscode: Instale-o [aqui](https://code.visualstudio.com/). (Se você já tiver o vscode instalado, desconsidere esse tópico).

### Instalar PostgreSql

- PostgreSql: Instale no site oficial [postgresql](https://www.postgresql.org/download/)


## Criar Banco de dados (PostgreSQL)
- linux: ``` sudo -u postgre psql ```

```sql
    CREATE DATABASE db_name;
    CREATE USER user WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE db_name TO user;
```
> **db_name**: Nome do seu banco de dados.
> **user**: nome do seu usuário.
> **password**: Substitua por uma senha. Dica: Se for usar caractere especial nela, evite usar @.

- windows
Acesse o terminal do PostgreSql e crie seguindo os comandos acima.


### Criar a pasta do projeto
- Navegue até o diretório que vc quer criar o projeto e digite no terminal/cmd:

Dica: Use `cd nome_do_diretório` para navega pelos arquivos...

```sh
    mkdir marketlist
    cd marketlist
```

### Ative o ambiente virtual python para instalar as dependências:

```sh
    python -m venv venv
```

### Ativar o ambiente

- Lunux/macOs
```sh
    source venv/bin/activate
```

- Winderson
```sh
    venv\Scripts\activate
```

### Instalar o flask no venv.

- Linux
```sh
    install flask flask-sqlalchemy psycopg2-binary
```

> flask: Framework que cria a API
> flask-sqlalchemy: Permite SQL e um ORM básico na aplicação
> psycopg2-binary: Faz a conexão com o banco de dados

- Windows

## Estrutura do projeto

Vamos criar a seguinte estrutura no projeto:

```
marketlist/
|--src/
|  |--config/
|  |  |--config.py
|  |--models/
|  |  |--item.py
|  |--routes/
|  |  |--item.py 
|  |--app.py
|--venv
```

### Criando a aplicação

A Aplicação `app` será o 'coração' da API. É nela onde tudo é configurado e interligado para funcionar.

No diretório principal `src/`, crie um arquivo `app.py` com o código abaixo:

```python
    from flask import Flask, Blueprint, request, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from config.config import Config
    from models.item import db
    from routes.item import item_bp

    app = Flask(__name__)

    # configurando o banco
    app.config.from_object(Config)

    # iniciando a aplicação
    db.init_app(app)

    # Migrando as tabelas.
    migrate= Migrate(app, db)

    with app.app_context():
        db.create_all()

    # Registrando as rotas
    app.register_blueprint(item_bp)

    # Rota teste

    # Start
    if __name__ == "__main__":
        app.run(debug=True)
```

Neste momento, nosso API já pode retornar alguma coisa, que tal testar?

Logo abaixo do comentário `# Rota teste` adicione a seguinte linha de código:

```python
    @app.route('/hello')
    def hello():
        return jsonify({
            'message': 'Hello World!'
        })
```

No terminal, inicie a aplicação digitando `python app.py`. Agora, vá no navegador e acesse a `http://localhost:5000/hello` e veja o que acontece.

> Tente mudar a mensagem e atualize a página.

> Dado que você testou tudo, encerre a aplicação apertando `Ctrl + C` no terminal.

### Criando arquivo de configuração

Este arquivo permitirá se conectar com o banco de dados que criamos.

Substitua os campos `user`, `password` e `database_name` pelos **mesmos valores** quando criamos nosso banco de dados `PostgreSql` acima.

```python
    class Config:
        SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/database_name"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Criando o model

O model é a definição do dado, com seus campos.

No diretório `src/models/`, crie um arquivo chamado `item.py` e ditige o código abaixo:

```python
    from flask_sqlalchemy import SQLAlchemy

    # Criando um objeto SQLAlchemy que possibilita criar comandos SQL mais fácil (com o ORM do SQLAlchemy).
    db = SQLAlchemy()

    # Definindo o escopo dos dados.
    class Item(db.Model):
        id = db.Column( db.Integer, primary_key = True, autoincrement = True )
        nome = db.Column( db.String(100), nullable = False )
        descricao = db.Column( db.String(200), nullable = True )
        comprado = db.Column( db.Boolean, default=False )

        def json(self):
            return {
                'id': self.id,
                'nome': self.nome,
                'descricao': self.descricao,
                'comprado': self.comprado
        }
```

### Rotas

Nesta etapa, vamos construir as principais rotas para o CRUD dos itens.

No diretório `src/routes/`, crie um arquivo chamado `item.py`, e escreva o código:

```python
    from flask import Blueprint, request, jsonify
    from models.item import db, Item

    item_bp = Blueprint('item_bp', __name__)
```

Vamos criar cada rota separadamente, seguindo cada operação HTTP. Adicione cada código das rotas abaixo no mesmo arquivo.

#### GET
Nessa operação, vamos recuperar os itens da nossa aplicação.

- GET/: Recuperando todos os itens `Item.query.all()`
```python
    @item_bp.route('/item', methods=['GET'])
    def listar_itens():
        itens = Item.query.all()
        itens_json = [ item.json() for item in itens ]
        
        return jsonify({
            'count': len( itens_json ),
            'itens': itens_json
        })
```

- GET/id/: Buscar item pelo ID.
```python
    @item_bp.route('/item/<int:id>', methods=['GET'])
    def buscar_item(id):
        item = Item.query.get(id)
        
        if not item:
            return jsonify({
                "erro": "Item não encontrado"
            }), 404
        
        return jsonify({
            'item': item.json()
        })
```

#### POST
Esta operação permitirá criar itens no nosso banco de dados.

```python
    @item_bp.route('/item', methods=['POST'])
    def criar_item():
        data = request.json # Capturando os dados enviados na requisição 

        # Criando um item a partir do objeto enviado
        item_novo = Item(
            nome = data['nome'],
            descricao = data['descricao'],
            comprado = data['comprado']
        )

        # Adiciona o item ao banco de dados
        db.session.add( item_novo )

        # Salva as alterações
        db.session.commit() 

        return jsonify({
            'message': 'Item criado com sucesso!',
            'item': item_novo.json()
        }), 201
```

#### PUT
Esta operação permite editar os campos de um item (com exceção do ID).

```python
    @item_bp.route('/item/<int:id>', methods=['PUT'])
    def atualizar_item(id):
        item = Item.query.get(id)
        
        if not item:
            return jsonify({
                "erro": "Item não encontrado"
            }), 404
        
        data = request.json

        item.nome = data.get("nome", item.nome)
        item.descricao = data.get("descricao", item.descricao)
        item.comprado = data.get("comprado", item.comprado)

        db.session.commit()

        return jsonify({
            'item': item.json(),
            "mensagem": "Item atualizado!"
        })
```

#### PATCH
Essa operação permite fazer uma alteração parcial nos dados de um item.

```python
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
```

#### DELETE
Por último, nossa operação de deletar um item.

```python
    @item_bp.route('/item/<int:id>', methods=['DELETE'])
    def deletar_item(id):
        item = Item.query.get(id)

        if not item:
            return jsonify({
                "erro": "Item não encontrado"
            }), 404
        
        db.session.delete( item )
        db.session.commit()
        
        return jsonify({
            "mensagem": f"Item com ID {item.id} deletado!"
        })
```

~**ENTÃO SE EU FOR NO NAVEGADOR AGORA MESMO E DIGITAR http://localhost:5000/item EU JÁ CONSIGO CRIAR E FAZER TUDO NOS ITENS?????**

~**NÃO. Ainda.**

### Migrations

Antes de testar tudo, temos que criar as migrações, que nada mais são do que as modificações que fizemos na(s) tabela(s) da nossa aplicação.

No terminal, na raiz do projeto `src/`, digite:
```sh
    flask db init
```

Esse comando provavelmente vai criar uma pasta chamada `migrations` que servem para armazenar os arquivos de controle das alterações realizadas no banco. Por hora, não é tão importante então só desconsidere. (Mas faça o comando).

- Criar um arquivo de migração (com base nos modelos do SQLAlchemy)

```sh
    flask db migrate -m "Criação das tabelas iniciais"
```

- Aplicar as migrações no banco (atualizar)
```sh
    flask db upgrade
```

**NADA FUNCIONOU**
Se nenhuma comando acima funcionou, tente esses:
```sh
    python -m flask db init
    python -m flask db migrate -m "Criação das tabelas"
    python -m flask db upgrade
```

> Se ainda não funcionou. Tenter procurar pelo erro na internet.


## LETS TEST
Agora que configuramos tudo, podemos testar.

Inicie a aplicação
```python
    python app.py
```

Teste cada operação no [postman](https://www.postman.com/) ou algum outro App de fazer requisições. Tente **inserir**, **editar** e **deletar** itens no banco de dados.

Veja a magia acontecer


### Testando com a ferramenta cURL

- GET: Pegar todos os itens
```sh
    curl -X GET http://127.0.0.1:5000/item
```

- GET: Pegar o item do ID = 2
```sh
    curl -X GET http://127.0.0.1:5000/item/1
```

- POST: Criar um item
```sh
    curl -X POST http://127.0.0.1:5000/item -H "Content-type: application/json" -d '{"nome":"Abóbora", "descricao":"abobora", "comprado":"False"}'
```

- PATCH: Editar um item (alterar para comprado = True)
```sh
    curl -X PATCH http://127.0.0.1:5000/item -H "Content-type: application/json" -d '{"comprado":"True"}'
```

- DELETE: Deletar o item de ID = 2
```sh
    curl -X DELETE http://127.0.0.1:5000/item/2
```