from flask import Blueprint, jsonify, request
from src.tasks.week4.S04E04.drone_models import DroneInstruction, DroneResponse
from src.services.drone_service import DroneNavigator

drone_bp = Blueprint('drone', __name__)
drone_navigator = DroneNavigator()

@drone_bp.route('/drone', methods=['POST'])
def handle_drone():
    try:
        data = DroneInstruction(**request.get_json())
        print(data)
        terrain = drone_navigator.navigate(data.instruction)
        return DroneResponse(description=terrain).model_dump()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500