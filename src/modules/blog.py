from src.modules.post import Post
import datetime
from src.commons.Database import Database
import uuid

class Blog(object):
    def __init__(self,author,title,description,author_id,_id=None):
        self.author=author
        self.author_id=author_id
        self.title=title
        self.description=description
        self._id=uuid.uuid4().hex if _id is None else _id


    def new_post(self,title,content,date=datetime.datetime.utcnow()):

        post=Post(blog_id=self._id,
                  author=self.author,
                  title=title,
                  content=content,
                  date=date)

        post.save_to_mongo()


    def json(self):
        return {
        "title":self.title,
        "author":self.author,
        "author_id":self.author_id,
        "description":self.description,
        "_id":self._id
        }


    def save_to_mongo(self):
        Database.insert(collection="blogs",
                               data=self.json())

    def get_post(self):
        return Post.from_blog(self._id)



    @classmethod
    def from_mongo(cls,id):
        blog_data=Database.find_one(collection="blogs",
                          query={"_id":id})

        return cls(**blog_data)


    @classmethod
    def Find_By_Author(cls,author_id):
        blogs=Database.find(collection='blogs',
                                    query={'author_id':author_id})
        return [cls(**blog) for blog in blogs]
