from apiflask import APIFlask

app = APIFlask(__name__, static_folder='./static', static_url_path="")

@app.route('/')
def index():
    return app.send_static_file('index.html')
