from src.modules.user import User
from src.commons.Database import Database
from src.modules.blog import Blog
from src.modules.post import Post
from flask import Flask,render_template,session,request,make_response

app=Flask(__name__)

app.secret_key='Eliud'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register_user():
    return render_template('register.html')

@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/auth/login',methods=['POST'])
def login_user():
    email=request.form['email']
    password=request.form['password']

    if User.Login_Valid(email,password):
        User.Login(email)
    else:
        session['email']=None

    return render_template('profile.html', email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register():
    email=request.form['email']
    password=request.form['password']

    User.Register(email,password)

    return render_template('profile.html', email=session['email'])



@app.route("/blogs/<string:user_id>")
@app.route("/blogs")

def user_blog(user_id=None):
    if user_id is not None:
        user=User.Get_By_Id(user_id)
    else:
        user=User.Get_By_Email(session['email'])
    blogs=user.Get_Blogs()
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route("/posts/<string:blog_id>")
def user_post(blog_id):
    blog=Blog.from_mongo(blog_id)
    posts=blog.get_post()

    return render_template("posts.html",posts=posts, blog_title=blog.title,blog_id=blog._id)

@app.route("/blogs/new", methods=['GET','POST'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title=request.form['title']
        description=request.form['description']
        user=User.Get_By_Email(session['email'])

        new_blog=Blog(user.email,title,description,user._id)
        new_blog.save_to_mongo()

        return make_response(user_blog(user._id))


@app.route("/post/new/<string:blog_id>",methods=['GET','POST'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html',blog_id=blog_id)
    else:
        content=request.form['content']
        title=request.form['title']
        user=User.Get_By_Email(session['email'])

        new_post=Post(user.email,content,title,blog_id)
        new_post.save_to_mongo()

        return make_response(user_post(blog_id))

app.run(debug=True)
