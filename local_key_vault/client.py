from flask import Flask, request, jsonify

from .vault import LocalKeyVault

app = Flask(__name__)
vault = LocalKeyVault()

@app.route('/create_scope', methods=['POST'])
def create_scope():
    data = request.json
    scope_name = data['scope_name']
    password = data['password']
    try:
        vault.create_scope(scope_name, password)
        return jsonify({'message': 'Scope created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/set_secret', methods=['POST'])
def set_secret():
    data = request.json
    scope_name = data['scope_name']
    password = data['password']
    secret_key = data['secret_key']
    secret_value = data['secret_value']
    try:
        scope = vault.get_scope(scope_name, password)
        scope.set_secret(secret_key, secret_value)
        return jsonify({'message': 'Secret set successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/get_secret', methods=['POST'])
def get_secret():
    data = request.json
    scope_name = data['scope_name']
    password = data['password']
    secret_key = data['secret_key']
    try:
        scope = vault.get_scope(scope_name, password)
        secret_value = scope.get_secret(secret_key)
        return jsonify({'secret_value': secret_value}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/list_secrets', methods=['POST'])
def list_secrets():
    data = request.json
    scope_name = data['scope_name']
    password = data['password']
    try:
        scope = vault.get_scope(scope_name, password)
        secrets = scope.list_secrets()
        return jsonify({'secrets': secrets}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/delete_secret', methods=['POST'])
def delete_secret():
    data = request.json
    scope_name = data['scope_name']
    password = data['password']
    secret_key = data['secret_key']
    try:
        scope = vault.get_scope(scope_name, password)
        scope.delete_secret(secret_key)
        return jsonify({'message': 'Secret deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(ssl_context='adhoc')