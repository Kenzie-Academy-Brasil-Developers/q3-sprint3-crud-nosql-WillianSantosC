from flask import Flask

def init_app(app: Flask):
    from app.routes.posts import posts

    posts(app)