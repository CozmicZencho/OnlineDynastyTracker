from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/counter')
def counter():
    count = int(request.args.get('n', 0))
    return render_template('partials/_counter.html', count=count)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
