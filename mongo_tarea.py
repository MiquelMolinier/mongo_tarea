# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:56:11 2020

@author: USER
"""

from pymongo import MongoClient
import datetime
import time
import pprint
#ejecutar mongod antes de ejecutar el script
cliente = MongoClient('localhost')
db = cliente['blog']
noticia = db['noticia']
usuario = db['usuario']
comentario = db['comentario']
noticia.delete_many({})
usuario.delete_many({})
comentario.delete_many({})
def mostrar(coleccion):
    print(f'{coleccion.name:*^64s}')
    for documento in coleccion.find():
        pprint.pprint(documento)
def crear_usuario(id_, nombre, twitter, descripcion, calle=None, 
                  numero=None, puerta=None, ciudad=None, telefonos=None):
    try:
        usuario.insert_one({'_id':id_})
        usuario.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    user = {'_id':id_, 'nombre':nombre, 'twitter':twitter,
            'descripcion':descripcion,
            'calle':calle, 'numero':numero, 'puerta':puerta,
            'ciudad':ciudad, 'telefonos':telefonos,
            'articulos':[]
           }
    usuario.insert_one(user)
def crear_noticia(id_, titulo, cuerpo, id_autor, tags=None):
    try:
        noticia.insert_one({'_id':id_})
        noticia.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    user = usuario.find_one({'_id':id_autor})
    if user is None:
        print('No existe Autor')
        return
    articulo = {'_id':id_, 'titulo':titulo, 'cuerpo':cuerpo,
                'fecha_pub':datetime.datetime.now(),
               'id_autor':id_autor, 'tags':tags,'comentarios':[]}
    noticia.insert_one(articulo)
    usuario.update_one({'_id':id_autor},{'$push':{'articulos':id_}})
def crear_comentario(id_, id_noticia, id_usuario, texto):
    try:
        comentario.insert_one({'_id':id_})
        comentario.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    notice = noticia.find_one({'_id':id_noticia})
    user = usuario.find_one({'_id':id_usuario})
    if notice is None or user is None:
        print('No existe Usuario o Noticia')
        return
    coment = {'_id':id_, 'id_usuario':id_usuario,
              'id_noticia':id_noticia, 'texto':texto,
              'fecha_pub':datetime.datetime.now()}
    comentario.insert_one(coment)
    noticia.update_one({'_id':id_noticia},{'$push':{'comentarios':id_}})
crear_usuario(id_=4,nombre="Damon",twitter="Damon.com",descripcion="Dios")
crear_usuario(id_=7,nombre="USER",twitter="USER.com",descripcion="USER")
crear_usuario(id_=5,nombre="Ian",twitter="Ian.com",descripcion="Muerto")
crear_usuario(id_=94,nombre='Jainy', twitter='Jainy.com',
              descripcion='Milagro retorcido',calle='robles',numero=4,
              puerta=371,ciudad='lima',telefonos=[999123879,271828184,123456789])
crear_usuario(id_=41,nombre='Silvia', twitter='anya.com',
              descripcion='Lacerante culpa',calle='ficus',numero=6,
              puerta=321,ciudad='lima',telefonos=[999123879,271828184,123456789])
crear_usuario(id_=1,nombre='user1', twitter='user1.com',
              descripcion='solamente user1')
crear_usuario(id_=2,nombre='user2', twitter='user2.com',
              descripcion='solamente user2')
crear_usuario(id_=3,nombre='user3', twitter='user3.com',
              descripcion='solamente user3')
crear_noticia(12,"Humanz","Album discotequero mas no simplón",id_autor=4,tags=['musica'])
crear_noticia(13,"Joy division","Banda de postpunk",id_autor=5,tags=["historia","musica"])
crear_noticia(14,"Title1","Description",id_autor=5,tags=["historia","musica","poesía","filosofía"])
crear_noticia(15,"Title2","Description",id_autor=5,tags=["filosofia","musica"])
crear_noticia(16,"Title3","Description",id_autor=5,tags=["estadística","biologia","algebra"])
crear_noticia(17,"Title4","Description",id_autor=5,tags=["algebra","historia"])
crear_noticia(18,"Title5","Description",id_autor=94,tags=["criminología","derecho"])
crear_noticia(19,"Title","Description",id_autor=1,tags=["comics","cultura"])
crear_noticia(20,"Title","Description",id_autor=1,tags=["estadística","machine learning"])
crear_noticia(21,"Title","Description",id_autor=2,tags=["geometría","programación"])
crear_noticia(22,"Title","Description",id_autor=3,tags=["literatura","poesía"])
crear_noticia(id_=55,titulo='Bondad',
              cuerpo='Los niños nacidos en "Un mundo feliz"',
              id_autor=94, tags=['psicologia','etica'])
crear_noticia(id_=66, titulo='Mujeres', cuerpo='Reseña de la novela "Mujeres"',
              id_autor=41,tags=['sexo','literatura'])
crear_comentario(id_=18,id_noticia=13,id_usuario=1,texto="spam")
crear_comentario(id_=19,id_noticia=13,id_usuario=2,texto="spam")
crear_comentario(id_=20,id_noticia=13,id_usuario=2,texto="spam")
crear_comentario(id_=21,id_noticia=12,id_usuario=1,texto="spam")
crear_comentario(id_=22,id_noticia=14,id_usuario=3,texto="spam")
crear_comentario(id_=23,id_noticia=14,id_usuario=3,texto="spam")
crear_comentario(id_=24,id_noticia=17,id_usuario=3,texto="spam")
crear_comentario(id_=25,id_noticia=17,id_usuario=3,texto="spam")
crear_comentario(id_=26,id_noticia=18,id_usuario=3,texto="spam")
crear_comentario(id_=27,id_noticia=16,id_usuario=94,
                 texto="Es imposible no dedicarte unas cuantas palabras aun si estas se autorreferencian")
crear_comentario(id_=15,id_noticia=55, id_usuario=41,
                 texto='Padres e hijos')
crear_comentario(id_=16,id_noticia=55, id_usuario=41,
                 texto='Los Gammas, los Epsilones, los Deltas')
crear_comentario(id_=17,id_noticia=55, id_usuario=41,
                 texto='Los criterios de producción aplicados a la biología')
crear_comentario(id_=14,id_noticia=66, id_usuario=1,
                 texto='spam')
crear_comentario(id_=13,id_noticia=66, id_usuario=2, texto='spam')
crear_comentario(id_=12,id_noticia=66, id_usuario=3, texto='spam')

def consulta_1():
    #1.Muestra los usuarios que comentaron sin repetirlos
    x = db.usuario.find({"_id":{"$in":(db.comentario.distinct("id_usuario"))}})
    print(f'{"Consulta 1":-^80}')
    for i in x:
        pprint.pprint(i)
def consulta_2():
    #2-Mostrar las noticias con comentarios
    x = db.noticia.find({"_id":{"$in":(db.comentario.distinct("id_noticia"))}})
    print(f'{"Consulta 2":-^80}')
    for i in x:
        pprint.pprint(i)
def consulta_3():
    #3-Cantidad de comentarios por autor
    x = db.comentario.aggregate(
        [{"$group":{"_id":{"id_usuario":"$id_usuario",},
                  "Numero de comentarios":{"$sum":1}}},
         {"$sort":{"Numero de comentarios":-1}}])
    print(f'{"Consulta 3":-^80}')
    for i in x:
        pprint.pprint(i)
def consulta_4():
    #4-Cantidad de tags por noticia
    x = db.noticia.aggregate(
        [{"$unwind":"$tags"},{"$group":{"_id":{"id":"$_id","Titulo":"$titulo"},
                                    "Numero de tags":{"$sum":1}}},
         {"$sort":{"Numero de tags":-1}}])
    print(f'{"Consulta 4":-^80}')
    for i in x:
        pprint.pprint(i)
def consulta_5():
    #5-Mostrar el autor, más activo en comentarios, con sus datos personales
    print(f'{"Consulta 5":-^80}')
    x = db.usuario.find_one(
        {"_id":(db.comentario.aggregate(
            [{"$group":{"_id":"$id_usuario","Numero de comentarios":{"$sum":1}}},
             {"$sort":{"Numero de comentarios":-1}}]).next()["_id"])})
    pprint.pprint(x)
def consulta_6():
    #6-Mostrar el autor con más publicaciones
    print(f'{"Consulta 6":-^80}')
    x= db.usuario.find_one(
        {"_id":(db.usuario.aggregate([{"$unwind":"$articulos"},
                                    {"$group":{"_id":"$_id","Articulos":{"$sum":1}}},
                                    {"$sort":{"Articulos":-1}}]).next()["_id"])})
    pprint.pprint(x)
def consulta_7():
    #7-Mostrar el autor menos activo en comentarios con sus datos personales
    print(f'{"Consulta 7":-^80}')
    x = db.usuario.find_one({"_id":(db.comentario.aggregate(
        [{"$group":{"_id":"$id_usuario","Numero de comentarios":{"$sum":1}}},
         {"$sort":{"Numero de comentarios":1}}]).next()["_id"])})
    pprint.pprint(x)
def consulta_8():
    #8-Mostrar el autor con menos publicaciones
    print(f'{"Consulta 8":-^80}')
    x = db.usuario.find_one({"_id":(db.usuario.aggregate(
        [{"$unwind":"$articulos"},{"$group":{"_id":"$_id","Articulos":{"$sum":1}}},
         {"$sort":{"Articulos":1}}]).next()["_id"])})
    pprint.pprint(x)
def consulta_9():
    #9-Mostrar los tags
    print(f'{"Consulta 9":-^80}')
    x = db.noticia.distinct("tags")
    for i in x:
        pprint.pprint(i)
def consulta_10():
    #10-Mostrar la cantidad de tags
    print(f'{"Consulta 10":-^81}')
    x = db.noticia.aggregate(
        [{"$unwind":"$tags"},{"$group":{"_id":"$tags"}},
         {"$count":"numero de tags"}]).next()["numero de tags"]
    print(x)
def consulta_11():
    #11-Mostrar los autores con publicaciones
    print(f'{"Consulta 11":-^81}')
    x = db.usuario.find({"articulos":{"$not":{"$size":0}}})
    for i in x:
        pprint.pprint(i)
def consulta_12():
    #12-Mostrar la cantidad de autores con publicaciones
    print(f'{"Consulta 12":-^81}')
    x = db.usuario.aggregate([
        {"$match":{"articulos":{"$not":{"$size":0}}}},
        {"$count":"Numero de autores"}]).next()["Numero de autores"]
    print(x)
def consulta_13():
    #13-Mostrar cantidad de autores
    print(f'{"Consulta 13":-^81}')
    x = db.usuario.count_documents({})
    print(x)
def consulta_14():
    #14-Mostrar la cantidad de comentarios
    print(f'{"Consulta 14":-^81}')
    x = db.comentario.count_documents({})
    print(x)
def consulta_15():
    #15-Mostrar el numero de comentarios por noticia
    print(f'{"Consulta 15":-^81}')
    x = db.noticia.aggregate([
        {"$unwind":"$comentarios"},
        {"$group":{"_id":{"id":"$comentarios","Titulo":"$titulo"},
                   "Numero de comentarios":{"$sum":1}}}])
    for i in x:
        pprint.pprint(i)

# Para ver los documentos de las colecciones descomentar las siguientes intrucciones
mostrar(usuario)
mostrar(noticia)
mostrar(comentario)
consulta_1()
consulta_2()
consulta_3()
consulta_4()
consulta_5()
consulta_6()
consulta_7()
consulta_8()
consulta_9()
consulta_10()
consulta_11()
consulta_12()
consulta_13()
consulta_14()
consulta_15()
time.sleep(30) 

    
    
    
    
    
    
    
    
    
    
    
    
    