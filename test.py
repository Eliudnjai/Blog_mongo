from src.modules.post import Post
from src.modules.blog import Blog
from src.modules.user import User
from src.commons.Database import Database


Database.initialize()

blog=Blog(author="Eliudnjai",
          title="Another-nother test",
          description="hope this shit works",
          author_id=User.Get_By_Id(id))
blog.save_to_mongo()
