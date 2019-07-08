from flask import Flask
from flask import render_template, jsonify, request, redirect
import requests
import json

app = Flask(__name__)


token = None
base = "https://headhunters-api.herokuapp.com/api/"


@app.route('/')
def init():
    return render_template('login.html')


@app.route('/admin/logout')
def logout():
    global token
    token = None
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    global token, base

    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        uri = base + "users/login"
        headers = {'content-type': 'application/json'}
        payload = {'username': email, 'password': password}

        try:
            uResponse = requests.post(uri, headers = headers, data=json.dumps(payload))
        except requests.ConnectionError:
            return "Conection error"

        Jresponse = uResponse.json()

        if 'token' not in Jresponse:
            return redirect("/")
        else:
            token = Jresponse["token"]
            print(token)

    return redirect("/admin")


@app.route('/admin')
def dashboard():
    global token

    if token is None:
        return redirect('/')

    return render_template('home.html')


@app.route('/admin/album/list')
def listAlbumIndex():
    global token

    if token is None:
        return redirect('/')

    return render_template('admin/album_list.html')


@app.route('/admin/user/list')
def listUserIndex():
    global token

    if token is None:
        return redirect('/')

    return render_template('admin/user_list.html')


@app.route('/admin/album/add')
def addAlbumIndex():
    global token

    if token is None:
        return redirect('/')

    return render_template('admin/album_add.html')


@app.route('/admin/user/add')
def addUserIndex():
    global token

    if token is None:
        return redirect('/')

    return render_template('admin/user_add.html')


@app.route('/admin/album/songs/list/<id>')
def listAlbumSongIndex(id):
    global token, base

    if token is None:
        return redirect('/')

    albumName = ''
    uri = base + "albums"
    params = {'genre': ''}
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.get(uri, headers=headers, params=params)
    except requests.ConnectionError:
        return "Connection error"
    Jresponse = uResponse.json()

    for album in Jresponse:
        if str(album['id']) == str(id):
            albumName = album['title']
            break

    return render_template('admin/song_list.html', albumName=albumName, albumId=id)


@app.route('/admin/song/add')
def addSongIndex():
    global token, base

    if token is None:
        return redirect('/')

    albums = []
    uri = base + "albums"
    params = {'genre': ''}
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.get(uri, headers=headers, params=params)
    except requests.ConnectionError:
        return "Connection error"
    albums = uResponse.json()

    return render_template('admin/song_add.html', albums=albums)


@app.route('/admin/album/delete/<id>')
def deleteAlbum(id):
    global token, base

    if token is None:
        return redirect('/')

    uri = base+"albums/"+str(id)
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.delete(uri, headers=headers)
    except requests.ConnectionError:
        return "Connection error"

    Jresponse =uResponse.text
    if id in Jresponse:
        return redirect('/admin/album/list')
    else:
        return "error"


@app.route('/admin/user/delete/<id>')
def deleteUser(id):
    global token, base

    if token is None:
        return redirect('/')

    uri = base+"users/"+str(id)
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.delete(uri, headers=headers)
    except requests.ConnectionError:
        return "Connection error"

    Jresponse =uResponse.text
    if id in Jresponse:
        return redirect('/admin/user/list')
    else:
        return "error"


@app.route('/albumlist')
def listAlbum():
    global token, base

    if token is None:
        return redirect('/')

    uri = base + "albums"
    params = {'genre':''}
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.get(uri, headers=headers, params=params)
    except requests.ConnectionError:
        return "Connection error"
    Jresponse =uResponse.json()
    n = {'data': Jresponse}

    return jsonify(n)


@app.route('/userlist')
def listUser():
    global token, base

    if token is None:
        return redirect('/')

    uri = base + "users/all"
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.get(uri, headers=headers)
    except requests.ConnectionError:
        return "Connection error"

    Jresponse =uResponse.json()
    n = {'data': Jresponse}

    return jsonify(n)


@app.route('/songlist/<albumId>')
def listSongs(albumId):
    global token, base
    songList = []

    if token is None:
        return redirect('/')

    uri = base + "albums"
    params = {'genre': ''}
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.get(uri, headers=headers, params=params)
    except requests.ConnectionError:
        return "Connection error"
    Jresponse = uResponse.json()

    for album in Jresponse:
        if str(album['id']) == str(albumId):
            songList = album['songList']
            break
    n = {'data': songList}

    return jsonify(n)


@app.route('/albumadd', methods=['POST'])
def addAlbum():
    global token, base

    if token is None:
        return redirect('/')

    title = request.form['title']
    artist = request.form['artist']
    url = request.form['url']
    image = request.form['image']
    thumbnailImage = request.form['thumbnailImage']
    songList = []
    likes = 0
    genre = request.form['genre']
    description = request.form['description']

    payload = {
        'title': title,
        'artist': artist,
        "url": url,
        "image": image,
        "thumbnailImage": thumbnailImage,
        "songList": songList,
        "likes": likes,
        "genre":genre,
        "description": description
    }

    uri = base + "albums"
    headers = {'content-type': 'application/json', 'Authorization': token}
    try:
        uResponse = requests.post(uri, headers=headers, data= json.dumps(payload))
    except requests.ConnectionError:
        return "Connection error"

    Jresponse = uResponse.json()

    if 'id' not in Jresponse:
        return redirect("/admin")
    else:
        return redirect("/admin/album/list")


@app.route('/useradd', methods=['POST'])
def userAdd():
    global token, base

    if token is None:
        return redirect('/')

    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    accountType = request.form['accountType']

    uri = base + "users/register"
    headers = {'content-type': 'application/json'}
    payload = {
        'username': username,
        'password': password,
        'confirmPassword': confirmPassword
    }


    try:
        uResponse = requests.post(uri, headers=headers, data=json.dumps(payload))
    except requests.ConnectionError:
        return "Connection error"

    Jresponse = uResponse.json()
    print(Jresponse)

    if 'id' not in Jresponse:
        return redirect("/admin")
    else:
        return redirect("/admin/user/list")


@app.route('/songadd', methods=['POST'])
def songAdd():
    global token, base

    if token is None:
        return redirect('/')

    albumToEdit = None
    albumId = request.form['album']
    title = str(request.form['title'])
    artist = str(request.form['artist'])
    albumArtUrl = str(request.form['albumArtUrl'])
    audioUrl = str(request.form['audioUrl'])

    song = {
        'title': title,
        'artist': artist,
        'albumArtUrl': albumArtUrl,
        'audioUrl': audioUrl
    }

    uri = base + "albums"
    params = {'genre': ''}
    headers = {'content-type': 'application/json', 'Authorization': token}

    try:
        uResponse = requests.get(uri, headers=headers, params=params)
    except requests.ConnectionError:
        return "Connection error"
    jresponse = uResponse.json()

    for album in jresponse:
        if str(album['id']) == str(albumId):
            albumToEdit = album
            break

    print(albumToEdit['songList'])
    print(song)
    albumToEdit['songList'].append(song)
    print(albumToEdit)

    uri = base + "albums/" + str(albumId)

    try:
        requests.put(uri, headers=headers, data=json.dumps(albumToEdit))
    except requests.ConnectionError:
        return "Connection error"

    return redirect("/admin/album/songs/list/" + str(albumId))


if __name__ == '__main__':
    app.run()
