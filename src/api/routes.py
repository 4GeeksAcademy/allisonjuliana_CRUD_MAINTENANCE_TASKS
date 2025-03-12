"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Room, Maintenance, HouseKeeper, Category, MaintenanceTask
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/categories', methods=['GET'])
def obtener_categories():
    categories = Category.query.all()  # Obtener todas las categorías
    categories_serialize = [category.serialize() for category in categories]  # Serializar cada categoría
    return jsonify(categories_serialize), 200  # Retornar los datos serializados como JSON

@api.route('/maintenance', methods=['GET'])
def get_maintenance():
    maintenance = Maintenance.query.all()
    
    return jsonify([maint.serialize() for maint in maintenance])

@api.route('/housekeepers', methods=['GET'])
def get_housekeepers():
    housekeepers = HouseKeeper.query.all()
    return jsonify([housekeeper.serialize() for housekeeper in housekeepers]), 200

@api.route('/rooms', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    return jsonify([room.serialize() for room in rooms]), 200

@api.route('/maintenancetasks', methods=['GET'])
def get_all_maintenance_tasks():
    """Obtener todas las tareas de mantenimiento"""
    maintenance_tasks = MaintenanceTask.query.all()  # Obtener todas las tareas
    return jsonify([task.serialize() for task in maintenance_tasks]), 200

@api.route('/maintenancetasks/<int:id>', methods=['GET'])
def get_maintenance_task(id):
    """Obtener una tarea de mantenimiento específica por ID"""
    maintenance_task = MaintenanceTask.query.get(id)
    if not maintenance_task:
        return jsonify({"message": "Tarea de mantenimiento no encontrada"}), 404
    return jsonify(maintenance_task.serialize()), 200

@api.route('/maintenancetasks', methods=['POST'])
def create_maintenance_task():
    """Crear una nueva tarea de mantenimiento"""
    data = request.get_json()

    try:
        # Obtener los datos enviados
        nombre = data.get('nombre')
        photo = data.get('photo')
        condition = data.get('condition')
        room_id = data.get('room_id')
        maintenance_id = data.get('maintenance_id')
        housekeeper_id = data.get('housekeeper_id')
        category_id = data.get('category_id')

        # Crear la nueva tarea de mantenimiento
        new_task = MaintenanceTask(
            nombre=nombre,
            photo=photo,
            condition=condition,
            room_id=room_id,
            maintenance_id=maintenance_id,
            housekeeper_id=housekeeper_id,
            category_id=category_id
        )

        # Agregarla a la base de datos
        db.session.add(new_task)
        db.session.commit()

        return jsonify(new_task.serialize()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al crear la tarea de mantenimiento", "error": str(e)}), 400

@api.route('/maintenancetasks/<int:id>', methods=['PUT'])
def update_maintenance_task(id):
    """Actualizar una tarea de mantenimiento existente"""
    maintenance_task = MaintenanceTask.query.get(id)

    if not maintenance_task:
        return jsonify({"message": "Tarea de mantenimiento no encontrada"}), 404

    data = request.get_json()

    try:
        # Actualizar los campos de la tarea de mantenimiento
        maintenance_task.nombre = data.get('nombre', maintenance_task.nombre)
        maintenance_task.photo = data.get('photo', maintenance_task.photo)
        maintenance_task.condition = data.get('condition', maintenance_task.condition)
        maintenance_task.room_id = data.get('room_id', maintenance_task.room_id)
        maintenance_task.maintenance_id = data.get('maintenance_id', maintenance_task.maintenance_id)
        maintenance_task.housekeeper_id = data.get('housekeeper_id', maintenance_task.housekeeper_id)
        maintenance_task.category_id = data.get('category_id', maintenance_task.category_id)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify(maintenance_task.serialize()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al actualizar la tarea de mantenimiento", "error": str(e)}), 400

@api.route('/maintenancetasks/<int:id>', methods=['DELETE'])
def delete_maintenance_task(id):
    """Eliminar una tarea de mantenimiento"""
    maintenance_task = MaintenanceTask.query.get(id)

    if not maintenance_task:
        return jsonify({"message": "Tarea de mantenimiento no encontrada"}), 404

    try:
        # Eliminar la tarea de mantenimiento
        db.session.delete(maintenance_task)
        db.session.commit()
        return jsonify({"message": "Tarea de mantenimiento eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al eliminar la tarea de mantenimiento", "error": str(e)}), 400

