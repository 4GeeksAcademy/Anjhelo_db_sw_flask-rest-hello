from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favoritos = db.relationship("Favorite", back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favoritos": [favorite.serialize() for favorite in self.favoritos]
            # do not serialize the password, it's a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gravity = db.Column(db.String(5), nullable=False)
    population = db.Column(db.String(10), nullable=False)
    terrain = db.Column(db.String(20), nullable=False)
    id_people = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)
    favoritos = db.relationship('Favorite', back_populates='planet')

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    birth_year = db.Column(db.String(20), nullable=False)
    mass = db.Column(db.String(4), nullable=False)
    vehicles = db.relationship("Vehicles", backref="piloto")
    planets = db.relationship("Planets", backref="planeta_origen")
    favoritos = db.relationship("Favorite", back_populates='people')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "mass": self.mass
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(30), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    cost_in_credits = db.Column(db.String(15), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)
    favoritos = db.relationship('Favorite', back_populates='vehicle')

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)

    user = db.relationship('User', back_populates='favoritos')
    people = db.relationship('People', back_populates='favoritos')
    planet = db.relationship('Planets', back_populates='favoritos')
    vehicle = db.relationship('Vehicles', back_populates='favoritos')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }