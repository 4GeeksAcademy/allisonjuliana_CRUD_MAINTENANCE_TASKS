from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Maintenance {self.nombre}>'
      
    def serialize(self):
      return {
          "id": self.id,
          "nombre": self.nombre,
          "email": self.email,
          "password": self.password,
        }
    
class HouseKeeper(db.Model):
    __tablename__ = 'housekeeper'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<HouseKeeper {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
        }
    
class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Room {self.nombre}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Category {self.nombre}>'
            # do not serialize the password, its a security breach
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

class MaintenanceTask(db.Model):
    __tablename__ = 'maintenancetask'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    condition = db.Column(db.String(120), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id'), nullable=False)
    housekeeper_id = db.Column(db.Integer, db.ForeignKey('housekeeper.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # Relaciones
    room = db.relationship('Room')
    maintenance = db.relationship('Maintenance')
    housekeeper = db.relationship('HouseKeeper')
    category = db.relationship('Category')

    def __repr__(self):
        return f'<MaintenanceTask {self.nombre}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "photo": self.photo,
            "condition": self.condition,
            "room": self.room.serialize() if self.room else None,  # Detalles de la habitación
            "maintenance": self.maintenance.serialize() if self.maintenance else None,  # Detalles del mantenimiento
            "housekeeper": self.housekeeper.serialize() if self.housekeeper else None,  # Detalles del housekeeper
            "category": self.category.serialize() if self.category else None,  # Detalles de la categoría
        }

