from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import time
import pymongo

def getCollectionObject(collectionName):
    connection = pymongo.MongoClient("ds127044.mlab.com", 27044)
    db = connection['adaptive_web']
    status = db.authenticate(username, password)
    if status == True:
        return db[collectionName]
    else:
        print("Authentication Error!")
        return 

def validateLogin(userName, password):
    userLoginDetails = getCollectionObject('userLoginDetails')
    userData = userLoginDetails.find_one({'username': userName})
    if userData is None:
        return "Username doesn't exist, it seems!"
    if password == userData['password']:
        return "Logged In"
    return "Incorrect Login"
 
def createUserLogin(userName, password, rePassword):
    if password != rePassword:
        return "No Match"
    userLoginDetails = getCollectionObject('userLoginDetails')
    checkData = userLoginDetails.find_one({'username': userName})
    if checkData is None:        
        userData = {'username': userName, 'password': password}
        userLoginDetails.insert_one(userData)
        return "Account Created"
    else:
        return "Username Exists"
    return

def getCurrentTime():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

app = Flask(__name__, template_folder = 'templates')
app.secret_key = 'NoSoupForYou!'

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('user', userName = session['username']))
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    userName = request.form['userName']
    password = request.form['password']
    status = validateLogin(userName, password)
    if status == 'Logged In':
        timestamp = getCurrentTime()
        session['username'] = userName
        print(session['username'])
        userLog = getCollectionObject('userLog')
        logData = {'Username': userName, 'Timestamp': timestamp, 'Action': 'Login'}
        userLog.insert_one(logData)
        return redirect(url_for('user', userName = userName))
    else:
        return status

@app.route('/register', methods = ['POST'])
def register():
    userName = request.form['newUserName']
    password = request.form['newPassword']
    rePassword = request.form['reNewPassword']
    status = createUserLogin(userName, password, rePassword)
    if status == 'Username Exists':
        return status
    if status == 'No Match':
        return "Passwords do not match!"
    session['username'] = userName
    timestamp = getCurrentTime()
    userLog = getCollectionObject('userLog')
    logData = {'Username': userName, 'Timestamp': timestamp, 'Action': 'Register'}
    userLog.insert_one(logData)
    return redirect(url_for('user', userName = userName))

@app.route('/user/logout')
def logout():
    timestamp = getCurrentTime()
    userName = session['username']
    userLog = getCollectionObject('userLog')
    logData = {'Username': userName, 'Timestamp': timestamp, 'Action': 'Logout'}
    userLog.insert_one(logData)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<userName>')
def user(userName):
    userLog = getCollectionObject('userLog')
    cursor = userLog.find()
    df = pd.DataFrame(list(cursor))
    df = df[df['Username'] == userName]
    df = df[['Action', 'Timestamp']]
    df = df.to_html(classes = "table is-bordered has-text-centered", index = False)
    return render_template('userProfile.html', userName = userName, userlog = df)

@app.route('/user/<userName>/clicks', methods = ['POST'])
def userClicks(userName):
    clickDetails = request.form['clickDetails'];
    print(session['username'])
    print(clickDetails)
    return redirect(url_for('user', userName = userName))

@app.route('/user/stackoverflow/tags', methods = ['POST'])
def pageTags():
    if 'username' not in session:
        return redirect(url_for('index'))
    tags = request.form['tags']
    if tags is None or tags == '':
        tags = "NA"
    url = request.form['url']
    timestamp = request.form['timeStamp']
    print(tags)
    username = session['username']
    tagsLog = getCollectionObject('tagsLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp, 'tags': tags}
    tagsLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/searchBox', methods = ['POST'])
def searchField():
    if 'username' not in session:
        return redirect(url_for('index'))
    url = request.form['url']
    timestamp = request.form['timeStamp']
    print("search" + url)
    username = session['username']
    searchLog = getCollectionObject('searchLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp}
    searchLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/scroll', methods = ['POST'])
def scrollEvent():
    if 'username' not in session:
        return redirect(url_for('index'))    
    url = request.form['url']
    scrollRatio = request.form['scrollRatio']
    timestamp = request.form['timeStamp']
    username = session['username']
    print(scrollRatio)
    row = username + "," + url + "," + timestamp + "," + scrollRatio + "\n"
    scrollLog = getCollectionObject('scrollLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp, 'scrollRatio': scrollRatio}
    scrollLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/idleTime', methods = ['POST'])
def idleEvent():
    if 'username' not in session:
        return redirect(url_for('index'))  
    url = request.form['url']
    timestamp = request.form['timeStamp']
    print("Idle" + url)
    username = session['username']
    row = username + "," + url + "," + timestamp + "\n"
    idleLog = getCollectionObject('idleLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp}
    idleLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/clicks', methods = ['POST'])
def clicks():
    if 'username' not in session:
        return redirect(url_for('index'))    
    url = request.form['url']
    targetClass = request.form['targetClass']
    timestamp = request.form['timeStamp']
    username = session['username']
    row = username + "," + url + "," + timestamp + "," + targetClass + "\n"
    clicksLog = getCollectionObject('clicksLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp, 'targetClass': targetClass}
    clicksLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/copiedElement', methods = ['POST'])
def copiedElement():
    if 'username' not in session:
        return redirect(url_for('index'))    
    url = request.form['url']
    timestamp = request.form['timeStamp']
    copiedClass = request.form['elementClass']
    copiedText = request.form['elementText']
    print(copiedClass)
    username = session['username']
    copyLog = getCollectionObject('copyLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp, 'copiedClass': copiedClass, 'copiedText': copiedText}
    copyLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

@app.route('/user/stackoverflow/submitButton', methods = ['POST'])
def submitButton():
    if 'username' not in session:
        return redirect(url_for('index'))
    url = request.form['url']
    timestamp = request.form['timeStamp']
    username = session['username']
    submitLog = getCollectionObject('submitLog')
    logData = {'username': username, 'url': url, 'timestamp': timestamp}
    submitLog.insert_one(logData)
    return redirect(url_for('user', userName = session['username']))

if __name__ == '__main__':
    app.run()