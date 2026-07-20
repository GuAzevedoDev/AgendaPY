from services.services import AgendamentosService, ServicosService,Funcionario,Cliente
from flask import Flask
from config import DevelopmentConfig
from controllers import agendamento_bp,auth_bp,home_bp,clientes_bp
from models import db
import os

servicos_service = ServicosService()
agendamento_service = AgendamentosService()
funcionario_service = Funcionario()
cliente_service = Cliente()

def create_app(config = DevelopmentConfig):
    app = Flask(__name__,
        template_folder="views/templates",
        static_folder="views/static",)
    app.config.from_object(config)
    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta,"banco.db"
    )
    
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


