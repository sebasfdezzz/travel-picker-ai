def getCity(text):
    return ['New York','Amsterdam','Rome','London','Madrid']









from flask import Flask, render_template, request, jsonify
import sys
import json
from openai import OpenAI
import requests
import random 

app = Flask(__name__)
client = None

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="My API Key",
)
gloabl_input=[""]

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
        gloabl_input[0] = input_text

        result = getCity(input_text)

        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/get_image/<city>')
def get_unsplash_image(city):
    temp_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/310px-Placeholder_view_vector.svg.png'
    return jsonify({'image_url': temp_url}) #comment for prodcution
    access_key = '7iU8pHx9ol-FJexwDVFIgdhMpO-wxKVNk9tbKovW8PU'
    base_url = 'https://api.unsplash.com/search/photos/'
    params = {
        'query': city,
        'client_id': access_key,
    }

    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and 'results' in data and data['results']:
                random_index = random.randint(0, len(data['results']) - 1)

                image_url = data['results'][random_index]['urls']['small']
                return jsonify({'image_url': image_url})
            else:
                return jsonify({'error': 'No results found'}), 404
        else:
            return jsonify({'error': f'Request failed with status code {response.status_code}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/reason-to-go/', methods=['POST'])
def get_gpt_reason():
    try:
        data = request.get_json()
        input_text = gloabl_input[0]
        city = data.get('city', '')

        if not input_text or not city:
            return jsonify({'error': 'Both "input" and "city" parameters are required.'}), 400

        prompt = f'Tell me why {city} is a good place to go given a person is looking for a place to vacation and this is their input: {input_text}'

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=100
        )
        #print(chat_completion)
        print(chat_completion)
        generated_reason = chat_completion['choices'][0]['message']['content']

        return jsonify({'generated_reason': generated_reason})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python app.py <key_file_path>")
        sys.exit(1)

    key_file_path = sys.argv[1]

    try:
        with open(key_file_path, 'r') as key_file:
            openai_key = key_file.read().strip()
            client = OpenAI(
                api_key=openai_key,
            )
    except FileNotFoundError:
        print(f"Error: Key file not found at {key_file_path}")
        sys.exit(1)

    # Use the openai_key as needed in your application
    print(f"Using OpenAI key from {key_file_path}: {openai_key}")
    app.run(host='0.0.0.0',port=3003)