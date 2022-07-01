from crypt import methods
import json

from flask import (
    Flask,
    abort,
    jsonify,
    request
)

from flask_cors import CORS
from models import setup_db, Pelicula, Funcion, Sala, Entrada

PELICULAS_PER_PAGE=5

def paginate_peliculas(request, selection, isDescendent):
    if request.args.get('page',1,type=int) <= 0:
        abort(404)
    if isDescendent:
            start = len(selection) - PELICULAS_PER_PAGE
            end = len(selection)
    else:
        page= request.args.get('page',1,type=int)
        start = (page - 1) * PELICULAS_PER_PAGE
        end = start + PELICULAS_PER_PAGE
    info_total = [info.format() for info in selection]
    current_info = info_total[start:end]
    return current_info


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=['http://127.0.0.1:8082'])
    #TODO
    

    @app.after_request
    def after_resquest(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,PATH,DELETE,OPTIONS')
        return response

    # Asserts -> status_code, success o failed || assertTrue
    #---------------Peliculas---------------
    @app.route('/peliculas', methods=['GET'])
    def get_peliculas():
        selection = Pelicula.query.order_by('id').all()

        peliculas = paginate_peliculas(request, selection, False)
        if len(peliculas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'peliculas': peliculas,
            'total':len(peliculas)
        })

    @app.route('/peliculas', methods=['POST'])
    def create_pelicula():
        body=request.get_json()
        nombre=body.get('nombre', None)
        duracion = body.get('duracion', None)
        calificacion = body.get('calificacion', None)
        idioma = body.get('idioma', None)
        search = body.get('search', None)

        if search:
            selection = Pelicula.query.order_by('id').filter(Pelicula.nombre.like('%{}%'.format(search))).all()
            peliculas = paginate_peliculas(request, selection, False)
            return jsonify({
                'success': True,
                'peliculas': peliculas,
                'total': len(selection)
            })

        if nombre is None or duracion is None or calificacion is None or idioma is None:
            abort(422)
        try:
            pelicula=Pelicula(nombre=nombre,duracion=duracion,calificacion=calificacion,idioma=idioma)
            new_id=pelicula.insert()

            selection=Pelicula.query.order_by('id').all()
            peliculas=paginate_peliculas(request, selection, True)

            return jsonify({
                'success':True,
                'created':new_id,
                'peliculas':peliculas,
                'total':len(selection)
            })
        except:
            abort(500)
    
    @app.route('/peliculas/<id>', methods=['PATCH'])
    def update_pelicula(id):
        error_404 = False
        try:
            pelicula=Pelicula.query.filter(Pelicula.id==id).one_or_none()
            if pelicula is None:
                error_404 = True
                abort(404)

            body=request.get_json()
            if 'nombre' in body:
                pelicula.nombre=body.get('nombre')

            pelicula.update()

            return jsonify({
                'success':True,
                'id':id,
                'new_nombre':body.get('nombre')
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/peliculas/<id>', methods=['DELETE'])
    def delete_pelicula_by_id(id):
        error_404 = False
        try:
            pelicula = Pelicula.query.filter(Pelicula.id==id).one_or_none()
            if pelicula is None:
                error_404 = True
                abort(404)

            pelicula.delete()

            selection = Pelicula.query.order_by('id').all()
            peliculas=paginate_peliculas(request, selection, False)

            return jsonify({
                'success':True,
                'deleted':id,
                'peliculas':peliculas,
                'total':len(selection)
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)

    #---------------Sala---------------

    @app.route('/salas', methods=['GET'])
    def get_salas():
        selection = Sala.query.order_by('id').all()
        salas = paginate_peliculas(request, selection, False)
        if len(salas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'salas': salas,
            'total':len(salas)
        })

    @app.route('/salas', methods=['POST'])
    def create_sala():
        body=request.get_json()

        capacidad=body.get('capacidad', None)
        numero = body.get('numero', None)
        search = body.get('search', None)

        if search:
            selection = Sala.query.order_by('id').filter(Sala.numero==search).all()
            salas = paginate_peliculas(request, selection, False)
            return jsonify({
                'success': True,
                'salas': salas,
                'total': len(selection)
            })

        if numero is None or capacidad is None:
            abort(422)
        try:
            sala=Sala(capacidad=capacidad,numero=numero)
            new_id=sala.insert()

            selection=Sala.query.order_by('id').all()
            salas=paginate_peliculas(request, selection, True)

            return jsonify({
                'success':True,
                'created':new_id,
                'salas':salas,
                'total':len(selection)
            })
        except:
            abort(500)

    
    @app.route('/salas/<id>', methods=['PATCH'])
    def update_sala(id):
        error_404 = False
        try:
            sala=Sala.query.filter(Sala.id==id).one_or_none()
            if sala is None:
                error_404 = True
                abort(404)

            body=request.get_json()
            if 'numero' in body:
                sala.numero_de_sala=body.get('numero')

            sala.update()

            return jsonify({
                'success':True,
                'id':id,
                'new_numero':body.get('numero')
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)
        


    @app.route('/salas/<id>', methods=['DELETE'])
    def delete_sala_by_id(id):
        error_404 = False
        try:
            sala = Sala.query.filter(Sala.id==id).one_or_none()
            if sala is None:
                error_404 = True
                abort(404)

            sala.delete()

            selection = Sala.query.order_by('id').all()
            salas=paginate_peliculas(request, selection, False)

            return jsonify({
                'success':True,
                'deleted':id,
                'salas':salas,
                'total':len(selection)
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    #---------------Funcion---------------
    @app.route('/funciones', methods=['GET'])
    def get_funciones():
        selection = Funcion.query.order_by('id').all()
        funciones = paginate_peliculas(request, selection, False)
        if len(funciones) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'funciones': funciones,
            'total':len(funciones)
        })

    @app.route('/funciones', methods=['POST'])
    def create_funciones():
        body=request.get_json()

        sala_id=body.get('sala_id', None)
        pelicula_id = body.get('pelicula_id', None)
        dia = body.get('dia', None)
        hora = body.get('hora', None)
        search = body.get('search', None)

        if search:
            selection = Funcion.query.order_by('id').filter(Funcion.dia.like('%{}%'.format(search))).all()
            funciones = paginate_peliculas(request, selection, False)
            return jsonify({
                'success': True,
                'funciones': funciones,
                'total': len(selection)
            })

        if sala_id is None or pelicula_id is None or dia is None or hora is None:
            abort(422)
        try:
            funcion=Funcion(sala_id=sala_id,pelicula_id=pelicula_id,dia=dia,hora=hora)
            new_id=funcion.insert()

            selection=Funcion.query.order_by('id').all()
            funciones=paginate_peliculas(request, selection, True)

            return jsonify({
                'success':True,
                'created':new_id,
                'funciones':funciones,
                'total':len(selection)
            })
        except:
            abort(500)

    @app.route('/funciones/<id>', methods=['PATCH'])
    def update_funcion(id):
        error_404 = False
        try:
            funcion=Funcion.query.filter(Funcion.id==id).one_or_none()
            if funcion is None:
                error_404 = True
                abort(404)

            body=request.get_json()
            if 'dia' in body:
                funcion.dia=body.get('dia')

            funcion.update()

            return jsonify({
                'success':True,
                'id':id,
                'new_dia':body.get('dia')
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/funciones/<id>', methods=['DELETE'])
    def delete_funcion_by_id(id):
        error_404 = False
        try:
            funcion = Funcion.query.filter(Funcion.id==id).one_or_none()
            if funcion is None:
                error_404 = True
                abort(404)

            funcion.delete()

            selection = Funcion.query.order_by('id').all()
            funciones=paginate_peliculas(request, selection, False)

            return jsonify({
                'success':True,
                'deleted':id,
                'funciones':funciones,
                'total':len(selection)
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)

    #---------------Entrada---------------
    @app.route('/entradas', methods=['GET'])
    def get_entradas():
        selection = Entrada.query.order_by('id').all()
        entradas = paginate_peliculas(request, selection, False)
        if len(entradas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'entradas': entradas,
            'total':len(entradas)
        })

    @app.route('/entradas', methods=['POST'])
    def create_entrada():
        body=request.get_json()

        funcion_id=body.get('funcion_id', None)
        precio = body.get('precio', None)
        fecha = body.get('fecha', None)
        hora = body.get('hora', None)
        search = body.get('search', None)

        if search:
            selection = Entrada.query.order_by('id').filter(Entrada.fecha.like('%{}%'.format(search))).all()
            entradas = paginate_peliculas(request, selection, False)
            return jsonify({
                'success': True,
                'entradas': entradas,
                'total': len(selection)
            })

        if funcion_id is None or precio is None or fecha is None or hora is None:
            abort(422)
        try:
            entrada=Entrada(funcion_id=funcion_id,precio=precio,fecha=fecha,hora=hora)
            new_id=entrada.insert()

            selection=Entrada.query.order_by('id').all()
            entradas=paginate_peliculas(request, selection, True)

            return jsonify({
                'success':True,
                'created':new_id,
                'entradas':entradas,
                'total':len(selection)
            })
        except:
            abort(500)

    
    @app.route('/entradas/<id>', methods=['PATCH'])
    def update_entrada(id):
        error_404 = False
        try:
            entrada=Entrada.query.filter(Entrada.id==id).one_or_none()
            if entrada is None:
                error_404 = True
                abort(404)

            body=request.get_json()
            if 'fecha' in body:
                entrada.fecha=body.get('fecha')

            entrada.update()

            return jsonify({
                'success':True,
                'id':id,
                'new_fecha':body.get('fecha')
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/entradas/<id>', methods=['DELETE'])
    def delete_entrada_by_id(id):
        error_404 = False
        try:
            entrada = Entrada.query.filter(Entrada.id==id).one_or_none()
            if entrada is None:
                error_404 = True
                abort(404)

            entrada.delete()

            selection = Entrada.query.order_by('id').all()
            entradas=paginate_peliculas(request, selection, False)

            return jsonify({
                'success':True,
                'deleted':id,
                'entradas':entradas,
                'total':len(selection)
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "message":'not found',
                "success": False,
                'code':404
            }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
                "message":'method not allowed',
                "success": False,
                'code':405
            }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
                "message":'unprocessable',
                "success": False,
                'code':422
            }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
                "message":'internal server error',
                "success": False,
                'code':500
            }), 500

    return app
# flask run -h localhost -p 8082