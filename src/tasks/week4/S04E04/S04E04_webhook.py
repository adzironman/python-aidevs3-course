# src/tasks/week4/S04E04/S04E04_webhook.py
from flask import Flask
from flask_cors import CORS
from src.tasks.week4.S04E04.config import Config
from src.tasks.week4.S04E04.drone_routes import drone_bp
from src.utils.error_handlers import register_error_handlers
from src.tasks.base_task import BaseTask

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(drone_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

class Webhook(BaseTask):
    def __init__(self):
        super().__init__(task_name="webhook")
        self.port = Config.PORT
        self.app = create_app()
        
    def start_flask(self):
        self.app.run(
            host='0.0.0.0', 
            port=self.port,
            debug=True
        )

    def process(self) -> str:
        self.start_flask()