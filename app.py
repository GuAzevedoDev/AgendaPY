from flask import Flask
from config import DevelopmentConfig,ProductionConfig
from controllers import agendamento_bp,auth_bp,home_bp,clientes_bp
from models import db
from flask_migrate import Migrate

def create_app(config = ProductionConfig):
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
    migrate = Migrate(app, db)
        
    return app
app = create_app()



if __name__ == "__main__":
    app.run()


