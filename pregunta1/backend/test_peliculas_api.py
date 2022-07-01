import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from server import create_app
from models import setup_db, Pelicula

class TestPeliculasApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'peliculasdb_test'
        self.database_path = "postgresql+psycopg2://{}@{}/{}".format('postgres:1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_pelicula = {
            'nombre':'new pelicula',
            'duracion': 30,
            'calificacion':5,
            'idioma':'ingles'
        }
        self.new_sala = {
            'numero':1,
            'capacidad':10
        }
        self.new_funcion = {
            'sala_id':1,
            'pelicula_id':1,
            'dia':"Lunes",
            'hora':'20:00'
        }
        self.new_entrada = {
            'funcion_id':1,
            'precio':50.39,
            'fecha':'01/12/2017',
            'hora':'20:00'
        }

    #---------------Peliculas---------------

    def test_create_pelicula_success(self):
        res = self.client().post('/peliculas', json=self.new_pelicula)
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['peliculas']))
        self.assertTrue(data['total'])

    def test_create_pelicula_failed(self):
        res = self.client().post('/peliculas', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_peliculas_success(self):
        res0 = self.client().post('/peliculas', json=self.new_pelicula)
        data0= json.loads(res0.data)

        res = self.client().get('/peliculas')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['peliculas']))
        
    def test_get_peliculas_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/peliculas?page=-1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_peliculas_by_nombre(self):
        res0 = self.client().post('/peliculas', json=self.new_pelicula)

        res = self.client().post('/peliculas', json={'search':'pelicula'})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])

    def test_update_pelicula_success(self):
        res0 = self.client().post('/peliculas', json=self.new_pelicula)
        data0= json.loads(res0.data)
        updated_id = data0['created']
        res = self.client().patch(f'/peliculas/{updated_id}', json={'nombre':'updated test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_update_pelicula_failed(self):
        res = self.client().patch('/peliculas/-1', json={'nombre':'update failed test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_pelicula_success(self):
        resalt = self.client().post('/peliculas', json=self.new_pelicula)

        res0 = self.client().post('/peliculas', json=self.new_pelicula)
        data0= json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/peliculas/'+str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['peliculas'])
        self.assertTrue(data['total'])
        self.assertEqual(data['deleted'], str(deleted_id))

    def test_delete_pelicula_failed(self):
        res = self.client().delete('/peliculas/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
 
    #---------------Sala---------------
    def test_create_sala_success(self):
        res = self.client().post('/salas', json=self.new_sala)
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['salas']))
        self.assertTrue(data['total'])

    def test_create_sala_failed(self):
        res = self.client().post('/salas', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_salas_success(self):
        res0 = self.client().post('/salas', json=self.new_sala)
        data0= json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().get('/salas')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['salas']))

    def test_get_salas_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/salas?page=-1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_sala_by_numero_de_sala(self):
        res0 = self.client().post('/salas', json=self.new_sala)

        res = self.client().post('/salas', json={'search':1})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])

    def test_update_sala_success(self):
        res0 = self.client().post('/salas', json=self.new_sala)
        data0= json.loads(res0.data)
        updated_id = data0['created']
        res = self.client().patch(f'/salas/{updated_id}', json={'numero':100})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
    

    def test_update_sala_failed(self):
        res = self.client().patch('/salas/-1', json={'numero':1000})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_sala_success(self):
        resalt = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/salas', json=self.new_sala)
        data0= json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/salas/'+str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['salas'])
        self.assertTrue(data['total'])
        self.assertEqual(data['deleted'], str(deleted_id))

    def test_delete_sala_failed(self):
        res = self.client().delete('/salas/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    

    #---------------Funcion---------------
    def test_create_funcion_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res = self.client().post('/funciones', json=self.new_funcion)
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['funciones']))
        self.assertTrue(data['total'])

    def test_create_funcion_failed(self):
        res = self.client().post('/funciones', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_funciones_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/funciones', json=self.new_funcion)
        data0= json.loads(res0.data)

        res = self.client().get('/funciones')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['funciones']))

    def test_get_funciones_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/funciones?page=-1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_funciones_by_dia(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/funciones', json=self.new_funcion)

        res = self.client().post('/funciones', json={'search':'Lunes'})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])

    def test_update_funcion_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/funciones', json=self.new_funcion)
        data0= json.loads(res0.data)
        updated_id = data0['created']
        res = self.client().patch(f'/funciones/{updated_id}', json={'dia':'Martes'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_update_funcion_failed(self):
        res = self.client().patch('/funciones/-1', json={'dia':'Domingo'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_funcion_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        resalt = self.client().post('/funciones', json=self.new_funcion)

        res0 = self.client().post('/funciones', json=self.new_funcion)
        data0= json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/funciones/'+str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['funciones'])
        self.assertTrue(data['total'])
        self.assertEqual(data['deleted'], str(deleted_id))

    def test_delete_funcion_failed(self):
        res = self.client().delete('/funciones/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])    
 
    #---------------Entrada---------------

    def test_create_entrada_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/funciones', json=self.new_funcion)

        res = self.client().post('/entradas', json=self.new_entrada)
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['entradas']))
        self.assertTrue(data['total'])

    def test_create_entrada_failed(self):
        res = self.client().post('/entradas', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_entradas_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)

        res0 = self.client().post('/funciones', json=self.new_funcion)
        re = self.client().post('/entradas', json=self.new_entrada)

        res = self.client().get('/entradas')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['entradas']))

    def test_get_entradas_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/entradas?page=-1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_entradas_by_fecha(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)
        res_funcion = self.client().post('/funciones', json=self.new_funcion)

        res0 = self.client().post('/entradas', json=self.new_entrada)

        res = self.client().post('/entradas', json={'search':'01/12/2017'})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])

    def test_update_entrada_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)
        res_funcion = self.client().post('/funciones', json=self.new_funcion)

        res0 = self.client().post('/entradas', json=self.new_entrada)
        data0= json.loads(res0.data)
        updated_id = data0['created']
        res = self.client().patch(f'/entradas/{updated_id}', json={'fecha':'05/02/2000'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])    

    def test_update_entrada_failed(self):
        res = self.client().patch('/entradas/-1', json={'fecha':'05/02/2000'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_entrada_success(self):
        res_pelicula = self.client().post('/peliculas', json=self.new_pelicula)
        res_sala = self.client().post('/salas', json=self.new_sala)
        res_funcion = self.client().post('/funciones', json=self.new_funcion)
        resalt = self.client().post('/entradas', json=self.new_entrada)

        res0 = self.client().post('/entradas', json=self.new_entrada)
        data0= json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/entradas/'+str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['entradas'])
        self.assertTrue(data['total'])
        self.assertEqual(data['deleted'], str(deleted_id))


    def test_delete_entrada_failed(self):
        res = self.client().delete('/entradas/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])  

    def tearDown(self):
        pass
