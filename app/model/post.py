from datetime import datetime
from app import db

class Post():
    def __init__(self,title: str, author: str, tags: list[str], content: str) -> None:
        data_list = db.posts.find()
        
        self.id = len(list(data_list)) + 1
        self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.update_at = None
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        