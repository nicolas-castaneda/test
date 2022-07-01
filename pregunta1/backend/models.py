from flask_sqlalchemy import SQLAlchemy

database_name='peliculasdb'
database_path = "postgresql+psycopg2://{}@{}/{}".format('postgres:1234','localhost:5432', database_name)
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    #db.drop_all()
    db.create_all()


class Pelicula(db.Model):
    '''
    propiedades:
    
    PK pelicula id
    nombre pelicula
    duracion
    calificacion
    idioma
    '''
    __tablename__ = 'pelicula'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(), nullable = False)
    duracion = db.Column(db.Float, nullable = False)
    calificacion = db.Column(db.Float, nullable = False)
    idioma = db.Column(db.String(), nullable = False)

    #idpadre=db.Column(db.Integer,db.ForeignKey('modelopadre.id'),nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return{
            'id':self.id,
            'nombre':self.nombre,
            'duracion':self.duracion,
            'calificacion':self.calificacion,
            'idioma':self.idioma
        }
    

class Sala(db.Model):
    '''
    propiedades:

    PK sala id
    capacidad
    numero de sala
    '''
    __tablename__ = 'sala'
    id = db.Column(db.Integer, primary_key = True)
    capacidad = db.Column(db.Integer, nullable = False)
    numero = db.Column(db.Integer, nullable = False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return{
            'id':self.id,
            'capacidad':self.capacidad,
            'numero':self.numero,
        }


class Funcion(db.Model):
    '''
    propiedades:

    PK funcion id
    FK sala id
    FK pelicula id
    dia
    hora
    '''
    __tablename__ = 'funcion'
    id = db.Column(db.Integer, primary_key = True)
    sala_id = db.Column(db.Integer(), db.ForeignKey('sala.id'),nullable = False)
    pelicula_id = db.Column(db.Integer(), db.ForeignKey('pelicula.id'),nullable = False)
    dia = db.Column(db.String(), nullable = False)
    hora = db.Column(db.String(), nullable = False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return{
            'id':self.id,
            'sala_id':self.sala_id,
            'pelicula_id':self.pelicula_id,
            'dia':self.dia,
            'hora':self.hora
        }


class Entrada(db.Model):
    '''
    propiedades:

    PK entrada id
    FK funcion id
    precio
    fecha
    hora
    '''
    __tablename__ = 'entrada'
    id = db.Column(db.Integer, primary_key = True)
    funcion_id = db.Column(db.Integer, db.ForeignKey('funcion.id'),nullable = False)
    precio = db.Column(db.Float, nullable = False)
    fecha = db.Column(db.String(), nullable = False)
    hora = db.Column(db.String(), nullable = False)

    #idpadre=db.Column(db.Integer,db.ForeignKey('modelopadre.id'),nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return{
            'id':self.id,
            'funcion_id':self.funcion_id,
            'precio':self.precio,
            'fecha':self.fecha,
            'hora':self.hora
        }