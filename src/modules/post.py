import datetime
import uuid
from src.commons.Database import Database


class Post(object):
    def __init__(self,author,content,title,blog_id,date=datetime.datetime.utcnow(),_id=None):
        self.blog_id = blog_id
        self.author=author
        self.content=content
        self.title=title
        self.date=date
        self._id=uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())


    def json(self):
        return {
           "author":self.author,
            "content":self.content,
            "title":self.title,
            "blog_id":self.blog_id,
            "date":self.date,
            "_id":self._id
        }

    @classmethod
    def from_mongo(cls,id):
        post_data=Database.find_one(collection='posts',
                                    query={"_id":id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={"blog_id":id})]
    #blog_id