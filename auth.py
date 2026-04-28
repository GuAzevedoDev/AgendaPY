from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "funcionario_id" not in session:
            return jsonify({"mensagem": "Não autorizado"}), 401
        return f(*args, **kwargs)
    return wrapper