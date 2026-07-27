from functools import wraps
from flask import session, jsonify,redirect, url_for

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "funcionario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def funcionario_required(*ids_permitidos):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("funcionario_id") not in ids_permitidos:
                return jsonify({"sucesso": False, "mensagem": "Acesso nao autorizado"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator