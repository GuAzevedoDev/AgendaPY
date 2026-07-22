from flask import Flask
from config import DevelopmentConfig
from controllers import agendamento_bp,auth_bp,home_bp,clientes_bp
from models import db

def create_app(config = DevelopmentConfig):
    app = Flask(__name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,)
    app.config.from_object(config)

    #Inicio o app
    db.init_app(app)

    #Blueprints
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(clientes_bp)

    #Passo o contexto (necessario)
    with app.app_context():
        db.create_all()
        
    return app
app = create_app()



if __name__ == "__main__":
    app.run(debug=True)


