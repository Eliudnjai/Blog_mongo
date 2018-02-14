from src.commons.Database import Database
import uuid
import datetime
from src.modules.blog import Blog
from flask import session

class User(object):
    def __init__(self,email,password,_id=None):
        self.email=email
        self.password=password
        self._id=uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "email":self.email,
            "password":self.password,
            "_id":self._id
        }

    def Save_To_Mongo(self):
        Database.insert(collection='users',
                        data=self.json())

    @classmethod
    def Get_By_Email(cls,email):
        email_data=Database.find_one(collection='users',
                                     query={"email":email})
        if email_data is not None:
            return cls(**email_data)
        else:
            return None

    @classmethod
    def Get_By_Id(cls,_id):
        id_data=Database.find_one(collection='users',
                                  query={'_id':_id})
        if id_data is not None:
            return cls(**id_data)

    @classmethod
    def Login_Valid(cls,email,password):
        user=cls.Get_By_Email(email)
        if user.password == password:
            return True
        else:
            return None

    @classmethod
    def Register(cls,email,password):
        user=cls.Get_By_Email(email)
        if user is None:
            new_user=cls(email,password)
            new_user.Save_To_Mongo()
            session['email']=email
            return True
        else:
            return False

    @staticmethod
    def Login(user_email):
        session['email']=user_email

    @staticmethod
    def logout():
        session['email']=None


    def Get_Blogs(self):
        return Blog.Find_By_Author(self._id)

    def New_Blog(self,title,description):
        blog=Blog(author=self.email,
                  title=title,
                  description=description,
                  author_id=self._id)
        blog.save_to_mongo()

    def New_Post(blog_id,title,content,date=datetime.datetime.utcnow()):
        blog=Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)




