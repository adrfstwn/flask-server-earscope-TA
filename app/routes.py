from flask import Blueprint, jsonify
from .database import test_db_connection

bp = Blueprint('main', __name__)

@bp.route('/test-db', methods=['GET'])
def test_db():
    result = test_db_connection()
    if isinstance(result, dict):
        return jsonify(result), 500
    return jsonify({"message": result}), 200