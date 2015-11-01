from pymongo import MongoClient

connection = MongoClient()

#+=====++ Setup ++=====+#
'''
def setup():
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE accounts (uname text, pword text, first text, last text, info text, piclink text, friends text)")
    c.execute("CREATE TABLE posts (id integer, uname text, title text, sub text, post text, time text)")
    c.execute("CREATE TABLE comments (id integer, uname text, comment text, time text)")
    c.execute("CREATE TABLE likes (id integer, uname text)")
    conn.commit()
'''

def setup():
    db = connection['Data']
    collection = db['accounts']
    accounts.insert({
        'uname': '',
        'pword':'',
        'first':'',
        'last':'',
        'info':'',
        'piclink':'',
        'friends':''
    })
    collection = db['posts']
    posts.insert({
        'id':'',
        'uname':'',
        'title':'',
        'sub':'',
        'post':'',
        'time':''
    })
    collection = db['comments']
    comments.insert({
        'id':'',
        'uname':'',
        'comment':'',
        'time':''
    })
    collection = db['likes']
    likes.insert({
        'id':'',
        'uname':''
    })

#+=====++ Apostrophes ++=====+#
def replaceAp(s):
    return s.replace("'", "&#8217")
def unreplace(s):
    return s.replace("&#8217", "'")
def listRep(l):
    n = []
    for s in l:
        n.append(unreplace(s))
    return n
#+=====++ Accounts ++=====+#
'''
def unameAuth(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    accounts = c.execute("SELECT uname FROM accounts")
    for r in accounts:
        if r[0] == uname:
            return True
    return False
'''


def unameAuth(username):
    db = connection['Data']
    accounts = db.accounts.find({'uname':username}) 
    print accounts.count() 

    if accounts.count() == 0:
        return False
    return True

'''
def pwordAuth(uname, pword):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    p = c.execute("SELECT pword FROM accounts WHERE uname = '"+uname+"';")
    for r in p:
        return r[0] == pword
    return False
'''

def pwordAuth(username, password):
    db = connection['Data']
    #print db.accounts.find_one({'uname':username})
    result = db.accounts.find_one({'uname':username})
    if len(result) == 0:
	    return False
    p = result['pword']
    return p == password
    
"""
def addAccount(uname, pword, first, last):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    if uname.find(",") != -1: # it can't have a comma in it
        return "This account name has a character that is not allowed (',')"
    if uname.find("'") != -1: # it can't have an apostrophe in it
        return "This account name has a character that is not allowed (''')"
    accounts = c.execute("SELECT uname FROM accounts")
    for r in accounts:
        if r[0] == uname:
            return "This account name already exists"
    c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?);", (replaceAp(uname), replaceAp(pword), replaceAp(first), replaceAp(last), "", "", ""))
    conn.commit()
"""

def addAccount(username, password, first, last):
    db = connection['Data']
    if username.find(",") != -1:
        return "This account name has a character that is not allowed (',')"
    if username.find("'") != -1:
        return "This account name has a character that is not allowed (''')"
    accountnames = db.accounts.find({'uname':'username'})
    for r in accountnames:
        if r['uname'] == username:
            return "This account name already exists"
    db.accounts.insert_one({
        'uname':replaceAp(username),
        'pword':replaceAp(password),
        'first':replaceAp(first),
        'last':replaceAp(last)
    })

"""
def changePword(uname, oldP, newP, cNewP):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    p = c.execute("SELECT pword FROM accounts WHERE uname = '"+uname+"';")
    for r in p:
        result = r[0]
    if result != oldP:
        return "The password you input was incorrect."
    if newP != cNewP:
        return "The confirmed new password did not match."
    else:
        c.execute("UPDATE accounts SET pword = '"+replaceAp(newP)+"' WHERE uname = '"+uname+"';")
        conn.commit()        
        return "Password successfully updated"
"""
def changePword(username, oldP, newP, cNewP):
    db = connection['Data']
    p = db.accounts.find({'uname':'username'}, {'pword':1})
    for r in p:
        result = r[0]['pword']
    if result != oldP:
        return "The password you input was incorrect."
    if newP != cNewP:
        return "The confirmed new password did not match."
    else:
        db.accounts.update_one({
            {'uname':'username'},
            {
                '$set': {
                    'pword':'replaceAp(newP)'
                }
            }
        })
        return "Password successfully updated"
'''
def findName(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    n = c.execute("SELECT first, last FROM accounts WHERE uname ='"+uname+"';")
    for r in n:
        return unreplace(r[0]+" "+r[1])
'''
def findName(username):
    db = connection['Data']
    r = db.accounts.find_one({'uname':username},{'first':1,'last':1})
    return unreplace(r['first']+" "+r['last'])

'''
def editInfo(uname, info):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("UPDATE accounts SET info = '"+replaceAp(info)+"' WHERE uname = '"+uname+"';")
    conn.commit()
'''

def editInfo(username, info):
    db = connection['Data']
    inform = replaceAp(info)
    db.accounts.update_one(
        {'uname':'username'},
        {
            '$set': {
                'info':'inform'
            }
        }
    )

'''
def showInfo(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    n = c.execute("SELECT info FROM accounts WHERE uname = '"+uname+"';")
    for r in n:
        return unreplace(r[0])
'''

def showInfo(username):
    db = connection['Data']
    r = db.accounts.find_one({'uname':username},{'info':1})
    if 'info' in r: 
        return unreplace(r['info'])
    return "No info"

'''
def newPic(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("UPDATE accounts SET piclink = 'static/"+uname+".png' WHERE uname = '"+uname+"';")
    conn.commit()
'''

def newPic(username):
    db = connection['Data']
    db.accounts.update_one({
        {'uname':username},
        {
            '$set':{
                'piclink':'static/"username".png'
            }
        }
    })

'''
def findPic(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    n = c.execute("SELECT piclink FROM accounts WHERE uname = '"+uname+"';")
    for r in n:
        return r[0]
'''

def findPic(username):
    db = connection['Data']
    n = db.accounts.find({'uname':username},{'picklink':1})[0]
    return r['piclink']

#+=====++ Friends ++=====+#
'''
def friendList(uname): # returns list of friends
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    n = c.execute("SELECT friends FROM accounts WHERE uname = '"+uname+"';")
    for r in n:
        return r[0].split(",") # this is why no commas!
'''

def friendList(username):
    db = connection['Data']
    n = db.accounts.find_one({'uname':username}, {'friends':1})
    if 'friends' in n:
        return n['friends'].split(",")
    return []
        
def isFriend(uname, friend): # returns if uname has friend as friend
    f = friendList(uname)
    if f != None:
        for s in f:
            if s == friend:
                return True
    return False

"""
def addFriend(uname, friend): # adds friend to uname's friends
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    if isFriend(uname, friend):
        return False
    if not unameAuth(friend):
        return False
    if not unameAuth(uname):
        return False
    f = c.execute("SELECT friends FROM accounts WHERE uname = '"+uname+"';")
    friends = ""
    for s in f:
        friends = s[0]
    if friends != "":
        friends += ","
    friends += friend
    c.execute("UPDATE accounts SET friends = '"+friends+"' WHERE uname = '"+uname+"';")
    conn.commit()
    return True
"""

def addFriend(username, friend):
    db = connection['Data']
    if isFriend(username, friend):
        return False
    if not unameAuth(friend):
        return False
    if not unameAuth(username):
        return False
        f = db.accounts.find({'$and': [ {'uname':username}, {'friends':friend} ]},{'friends':1})[0]
    #for s in f:
        #friends = s['friends']
    if friends == "":
        friends += ","
    #friends += friend
    db.accounts.update_one({
        {'uname':'username'},
        {
            '$set': {
                'friends':'+friends+'
            }
        }
    })
    return True

#+=====++ Blog Posts ++=====+#

# posts:
# (id, uname, post, title, sub, time)
# 
# comments:
# (id, uname, comment, time)
#
# likes:
# (id, uname)
'''
def findID():
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    ids = c.execute("SELECT id FROM posts")
    max = 0
    for r in ids:
        id = r[0]
        if (id > max):
            max = id
    return max+1
'''

def findID():
    db = connection['Data']
    ids = db.posts.find()
    print ids
    return ids.count()

'''
def addPost(uname, title, sub, post):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?);", (findID(), uname, replaceAp(title), replaceAp(sub), replaceAp(post), displayDate()))
    conn.commit()
'''
def addPost(username, title, sub, post):
    db = connection['Data']
    db.posts.insert({'id':findID(), 'uname':username, 'title':replaceAp(title), 'sub':replaceAp(sub), 'post':replaceAp(post), 'time':displayDate()})
'''
def showPosts(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    posts = c.execute("SELECT id, title, sub, post, time FROM posts WHERE uname = '"+uname+"';")
    list = []
    for r in posts:
        list.append(r)# ID, title, sub, post, stamp
    return list
'''
def showPosts(username):
    db = connection['Data']
    posts = db.posts.find({'uname':'username'},{'_id':0})
    l = []
    for r in posts:
        l.append(r)
    return l
'''
def showFriendPosts(uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    posts = c.execute("SELECT id, uname, title, sub, post, time FROM posts")
    friendPosts = []
    for r in posts:
        if isFriend(uname, r[1]):
            friendPosts.append(r)# note that everything after id is +1 in index
    return friendPosts
'''
def showFriendPosts(username):
    db = connection['Data']
    posts = db.posts.find({'username':username})
    friendPosts = []
    for r in posts:
        if isFriend(username, r[1]):
            friendPosts.append(r)
    return friendPosts
'''
def showPost(ID):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    post = c.execute("SELECT post FROM posts WHERE id = "+str(ID)+";")
    for r in post:
        return unreplace(r[0])
'''
def showPost(ID):
    db = connection['Data']
    post = db.posts.find({'id':str(ID)}, {post:1,_id:0})
    for r in post:
        return unreplace(r[0])
'''
def addComment(ID, uname, comment):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("INSERT INTO comments VALUES (?, ?, ?, ?);", (ID, uname, replaceAp(comment), displayDate()))
    conn.commit()
'''
def addComment(ID, username, comment):
    db = connection['Data']
    db.comments.upsert({'id':ID,'uname':username,'comment':replaceAp(comment), 'time':displayDate()})
'''
def showComments(ID):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    comments = c.execute("SELECT uname, comment, time FROM comments WHERE id = "+str(ID)+";")
    list = []
    for r in comments:
        list.append(r)# uname, comment, time
    return list
'''
def showComments(ID):
    db = connection['Data']
    comments = db.comments.find({'id':str(ID)},{'uname':1,'comment':1,'time':1,_id:0})
    l = []
    for r in comments:
        l.append(r)
    return l
'''
def showAllComments():
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    comments = c.execute("SELECT id, uname, comment, time FROM comments;")
    list = []
    for r in comments:
        list.append(r)# id, uname, comment, time
    return list
'''
def showAllComments():
    db = connection['Data']
    comments = db.comments.find({'_id':0})
    l = []
    for r in comments:
        l.append(r)
    return l
'''
def addLike(ID, uname):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("INSERT INTO likes VALUES (?, ?);", (ID, uname))
    conn.commit()
'''
def addLike(ID, username):
    db = connection['Data']
    db.likes.upsert({'id':ID, 'uname':username})
'''
def showLikes(ID):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    likes = c.execute("SELECT uname FROM likes WHERE id = "+str(ID)+";")
    list = []
    for r in likes:
        list.append(r[0])# uname
    return list
'''
def showLikes(ID):
    db = connection['Data']
    likes = db.likes.find({'id':str(ID)}, {'uname':1,'_id':0})
    l = []
    for r in likes:
        l.append(r[0])
    return l

def displayDate():
    import datetime
    d = str(datetime.datetime.now())
    d = d.split(" ")
    date = ""

    time = d[1].split(":")
    day = d[0].split("-")
    
    date += day[1]+"/"+day[2]+"/"+day[0]+" at "
    date += time[0]+":"+time[1]
    return date
