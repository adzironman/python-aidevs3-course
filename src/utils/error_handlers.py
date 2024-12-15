from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({
            "error": e.description,
            "status_code": e.code
        }), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status_code": 500
        }), 500