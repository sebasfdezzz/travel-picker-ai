def getCity(text):
    return ['New York','Amsterdam','Rome','London','Madrid']









from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET'])
def result():
    try:
        cities_param = request.args.get('cities')

        cities = json.loads(cities_param)

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

@app.route('/get_image/<city>')
def get_unsplash_image(city):
    # Replace 'YOUR_ACCESS_KEY' with your actual Unsplash API access key
    access_key = '7iU8pHx9ol-FJexwDVFIgdhMpO-wxKVNk9tbKovW8PU'
    base_url = 'https://api.unsplash.com/search/photos/'
    params = {
        'query': 'city of '+ city,
        'client_id': access_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        image_url = data[0]['urls']['small']
        return jsonify({'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3003)