import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from config import DevelopmentConfig,ProductionConfig
from extensions import csrf, limiter
from models import db
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# Rotas que renderizam HTML — todo o resto responde em JSON.
HTML_ROUTES = {"/", "/clientes/", "/login"}


def create_app(config = ProductionConfig):
    if not config.SECRET_KEY:
        raise RuntimeError("SECRET_KEY nao configurada. Defina a variavel de ambiente SECRET_KEY antes de iniciar a aplicacao.")
    if not config.TESTING and not config.SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL nao configurada. Defina a variavel de ambiente DATABASE_URL antes de iniciar a aplicacao.")

    app = Flask(__name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,)
    app.config.from_object(config)
    csrf.init_app(app)
    limiter.init_app(app)

    # Nginx fica na frente do Gunicorn: sem isso, request.remote_addr (usado
    # pelo Flask-Limiter) e request.is_secure sempre veriam o Nginx, não o
    # cliente real, e o rate limit ficaria compartilhado entre todo mundo.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    #Inicio o app
    db.init_app(app)

    #Blueprints (importados aqui dentro para evitar import circular com controllers/auth_controller.py, que importa o limiter)
    from controllers import agendamento_bp,auth_bp,home_bp,clientes_bp
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(clientes_bp)

    #Passo o contexto (necessario)
    Migrate(app, db)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # Erros HTTP "normais" (404, 405, os que a gente ja levanta com abort)
        # seguem o fluxo padrao do Flask.
        if isinstance(e, HTTPException):
            return e

        app.logger.exception("Erro nao tratado em %s %s", request.method, request.path)

        if request.path in HTML_ROUTES:
            return "Ocorreu um erro interno. Tente novamente em instantes.", 500
        return jsonify({"sucesso": False, "mensagem": "Erro interno do servidor"}), 500

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app
app = create_app()



if __name__ == "__main__":
    app.run()


