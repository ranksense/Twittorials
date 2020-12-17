import time
from flask import Flask, render_template, request, redirect, send_from_directory, make_response, url_for
from random import randrange

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'user1' and request.authorization.password == 'mypassword':
        return '<h1>You are logged in</h1>'
    return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login Required'})

@app.route('/page')
def webpage():
    page = randrange(10)
    return render_template('webpage.html',page=page)

@app.route('/robots.txt')
def static_from_root():
    def file_modifier(filename = "static/robots.txt"):
        f = open(filename, "r")
        lines = f.readlines()
        new_file = ''
        for i in range(len(lines)):
            if lines[i].startswith('Allow'):
                lines[i] = lines[i].replace('Allow','Disallow')
            elif lines[i].startswith('Disallow'):
                lines[i] = lines[i].replace('Disallow','Allow')
            new_file += lines[i]
        return new_file

    def write_file(new_file, filename = 'static/robots.txt'):
        with open(filename,'w') as f:
            f.write(new_file)

    robots = file_modifier()
    write_file(robots)
    return send_from_directory(app.static_folder,request.path[1:])

@app.route("/redirected")
def new_url():
    return 'Redirected Page!'

@app.route("/middle-redirect")
def middle_url():
    return redirect("/redirected",code=302)

@app.route("/multiple_r/<num>")
def multiple_r(num):
    i = int(num)
    if i < 4:
        return redirect(f"/multiple_r/{i+1}",code=301)
    elif i >= 4:
        return 'error page', 404

@app.route("/redirect-301")
def starting_url():
    return redirect("/middle-redirect",code=301)

@app.route("/redirect-loop")
def redirect_loop():
    return redirect("/looped",code=301)

@app.route("/looped")
def looped():
    return redirect("/redirect-loop",code=301)

@app.route('/canonical')
def canonical():
    return render_template('canonical.html')

@app.route("/canonical-loop")
def canonical_loop():
    return redirect("/canonical",code=301)

@app.route("/timeout")
def timeout():
    time.sleep(15)
    return 'That was long to load'

if __name__ == '__main__':
    app.run(debug=True)