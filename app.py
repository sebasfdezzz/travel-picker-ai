from flask import Flask, render_template, request, jsonify
import sys
import json
from openai import OpenAI
import requests
import random
import time 

#list of cities to link the neuron number to city
def getCities(text):
    #load pickle
    #predict with model with text
    #get top 5 neurons
    #create result_list with cities_list[neuron1,neuron2,neuron3,neuron4,neuron5]
    #return result_list

    return ['New York','Amsterdam','Rome','London','Madrid']

app = Flask(__name__)
client = None
client = OpenAI(
    api_key="My API Key",
)
gloabl_input=[""]

time_entities = {
    "season": {
      "summer": "2024-06-21",
      "winter": "2023-12-21",
      "spring": "2024-03-21",
      "fall": "2024-09-24"
    },
    "month": {
      "january": "2024-01-01",
      "february": "2024-02-01",
      "march": "2024-03-01",
      "april": "2024-04-01",
      "may": "2024-05-01",
      "june": "2024-06-01",
      "july": "2024-07-01",
      "august": "2024-08-01",
      "september": "2024-09-01",
      "october": "2024-10-01",
      "november": "2024-11-01",
      "december": "2023-12-01"
    },
    "holiday": {
      "spring break": "2024-03-15",
      "summer break": "2024-06-15",
      "spring vacation": "2024-03-15",
      "summer vacation": "2024-06-15",
      "christmas": "2023-12-25",
      "new year": "2024-01-01",
      "easter": "2024-04-15",
      "thanksgiving": "2024-11-23",
      "halloween": "2024-10-31",
      "independence day": "2024-07-04",
      "labor day": "2024-09-04",
      "memorial day": "2024-05-29",
      "hanukkah": "2023-12-13",
      "diwali": "2024-11-06",
      "eid al-fitr": "2024-05-27",
      "eid al-adha": "2024-07-20",
      "valentine's day": "2024-02-14",
      "mother's day": "2024-05-14",
      "father's day": "2024-06-18",
    }
  }

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

        result = getCities(input_text)

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
    temp =  "sd asndjafskn akjf skndf dnf dsdn fdskn fdskn fkf dskf dsnf dsknf dsknf dsfk sknds fkdsf sknf sdknf dsnf dsknf dskf dsfknds flsd fns fkds fdsknf dskfn dsfknds fkds fkdsnf dskf dsknfds fks fdsknf dsknf dsknf dskf dskf dsknf fkds fks frekg trkn hknyt hkyth ylj yl jytpkhrkgepf wfow dqk dad 2o3 43kr f f foe flkf el feb grv ekv eovfe voefvke v e."
    time.sleep(5) #comment for production
    return jsonify({'generated_reason': temp}) #comment for production
    try:
        data = request.get_json()
        input_text = gloabl_input[0]
        city = data.get('city', '')

        if not input_text or not city:
            return jsonify({'error': 'Both "input" and "city" parameters are required.'}), 400

        prompt = f'In a maximum of 60 words tell me why {city} is a good place to go given a person is looking for a place to vacation and this is their input: {input_text}'

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
        generated_reason = chat_completion.choices[0].message.content

        return jsonify({'generated_reason': generated_reason})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-date', methods=['GET'])
def getDate(): #Reconocimiento de entidades de tiempo para fechas de vuelos
    try:
        if global_input:
            input_text = global_input[0].lower()
            for entity_type, entities in time_entities.items():
                for entity in entities:
                    if entity in input_text:
                        return time_entities[entity_type][entity]
        return "2024-01-01"
    except Exception as e:
        return "2024-01-01"



    
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

    