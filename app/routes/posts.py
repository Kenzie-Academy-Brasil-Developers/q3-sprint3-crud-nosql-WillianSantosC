from flask import Flask, jsonify, request
from datetime import datetime

from app import db
from app.model.post import Post
from app.controllers.helpers import verify_keys

def posts(app: Flask):

    @app.post('/posts')
    def create_post():
        try:
            new_post = Post(**request.get_json())

            db.posts.insert_one(new_post.__dict__)
            del new_post.__dict__['_id']

            return jsonify(new_post.__dict__), 201

        except TypeError:
            data = request.get_json()
            return {
                    "error": "Chave(s) incorreta(s) ou faltando",
                    "necessárias": [
                    "title",
                    "author",
                    "content",
                    "tags"
                    ],
                    "recebidas": list(data.keys())
                 }, 400
       
    
    @app.delete('/posts/<int:id>')
    def delete_post(id: int):
        try:
            data = db.posts.find_one_and_delete({"id": id})
            del data['_id']
            
            return jsonify(data), 200

        except TypeError:
            return jsonify(error= 'Post não existe no banco de dados'), 404

    @app.get('/posts/<int:id>')
    def read_post_by_id(id: int):
        try:
            post = [post for post in db.posts.find() if post['id'] == id]
            del post[0]['_id']

            return jsonify(post), 200
        except IndexError:
            return jsonify(error= 'Post buscado não existe no banco de dados'), 404
    
    @app.get('/posts')
    def read_posts():
        data_list = db.posts.find()
        new_data_list = []
        print(request.get_json())

        for data in data_list:
            del data['_id']
            new_data_list.append(data)

        return jsonify(new_data_list), 200

    
    @app.patch('/posts/<int:id>')
    def update_post(id: int):
        try: 
            verify_keys()
            update_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            update = {"$set": {**request.get_json(), "update_at": update_at}}
            db.posts.update_one({'id': id}, update)

            post = [post for post in db.posts.find() if post['id'] == id]
            del post[0]['_id']

            return jsonify(post), 200
        except IndexError:
            return jsonify(error= 'Post não existe no banco de dados'), 404
        except KeyError:
            data = request.get_json()
            return {
                    "error": "chave(s) incorreta(s)",
                    "permitidas": [
                    "title",
                    "author",
                    "content",
                    "tags"
                    ],
                    "recebidas": list(data.keys())
                 }, 400