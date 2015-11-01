import utils
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
@app.route("/")
def intro():
    return render_template("home.html")

@app.route("/login", methods = ["POST"])
def login():
    if str(request.form["button"]) == "Log in!":
        username = str(request.form["username"])
        if utils.pwordAuth(username, str(request.form["password"])):
            return redirect('/feed/' + username)
        else:
            return render_template("/home.html", text = "Username/Password does not match")
    else:
        return render_template("/register.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if str(request.form["button"]) == "Register!":
        if utils.unameAuth(str(request.form["username"])) != True:
            utils.addAccount(str(request.form["username"]), str(request.form["password"]), str(request.form["firstname"]), str(request.form["lastname"]), str(request.form["paragraph_text"]))
            utils.editInfo(str(request.form["username"]), str(request.form["paragraph_text"]))
            return redirect('/feed/' + str(request.form["username"]))
        else:
            return render_template("/register.html", text = "this username already exists")
    else:
        return render_template("/home.html")
@app.route("/home")
@app.route("/home/<username>", methods = ["GET", "POST"])
def home(username):
    print("hello")
    if request.method == "POST":
        print("2")
        if(str(request.form["post"]) == "finding"):
            utils.addFriend(username, str(request.form["search_for"]))
        elif (str(request.form["post"])) == "commenting":
            print("1")
            print(str(request.form["id"]))
            print("3")
            utils.addComment(str(request.form["id"]), username, str(request.form["comments"]))
    return render_template("allfriends.html", theposts = utils.showFriendPosts(username), username = username, friendslist = utils.friendList(username), comments = utils.showAllComments())

@app.route("/settings")
@app.route("/settings/<username>", methods = ["GET", "POST"])
def settings(username):
    print("1")
    if request.method == "POST":
        print("2")
        if (str(request.form["post"]) == "change"):
            print("3")
            the_response = utils.changePword(str(request.form["user"]), str(request.form["oldpass"]), str(request.form["pass1"]), str(request.form["pass2"]))
            return render_template("settings.html", username = username, the_response = the_response, friendslist = utils.friendList(username))
        elif (str(request.form["post"]) == "finding"):
            print("4")
            utils.addFriend(username, str(request.form["search_for"]))
            return render_template("settings.html", username = username, friendslist = utils.friendList(username))
    else:
        return render_template("settings.html", username = username, friendslist = utils.friendList(username))
                  

@app.route("/feed")
@app.route("/feed/<username>", methods = ["GET", "POST"])
def feed(username):
    print(request.method == "POST")
    if request.method == "POST":
        print("5")
        if str(request.form["post"]) == "posted":
            print("2")
            utils.addPost(username, str(request.form["title"]), "sub", str(request.form["paragraph_text"]))
        elif (str(request.form["post"])) == "finding":
            print(str(request.form["search_for"]))
            print("3")
            utils.addFriend(username, str(request.form["search_for"]))
            print(utils.isFriend(username, str(request.form["search_for"])))
        elif (str(request.form["post"])) == "commenting":
            utils.addComment(str(request.form["id"]), username, str(request.form["comments"]))
    return render_template("feed.html", comments = utils.showAllComments(), username = username, compareto = username,  posts = utils.showPosts(username), name = utils.findName(username), info = utils.showInfo(username), friendslist = utils.friendList(username))
'''
@app.route("/<username>")
@app.route("/<username>/<user2>", methods = ["GET", "POST"])
def viewing(username, user2):
    return render_template("feed.html", username = username, compareto = user2, posts = utils.showPosts(user2), name = utils.findName(user2), info = utils.showInfo(user2), friendslist = utils.friendList(username))
'''
if __name__ == "__main__":
    app.debug = True
    app.run()
    
