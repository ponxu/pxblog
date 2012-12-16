from bottle import Bottle, run, template
app = Bottle()

@app.route('/hello/:name')
def hello(name):
    return "Hello, %s" % name

if __name__ == "__main__":
    run(app, host = 'localhost', port = 8080, reloader = True)