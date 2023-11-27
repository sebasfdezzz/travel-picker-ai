def getCity(text):
    return ['New York','Amsterdam','Rome','London','Madrid']









from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        data = request.get_json()
        cities = data.get('cities')

        return render_template('result.html', cities=cities)
    except Exception as e:
        return str(e), 400 

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        input_text = data.get('input')

        result = getCity(input_text)

        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3003)