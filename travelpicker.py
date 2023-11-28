# Importamos las librerías de pandas y Sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import numpy
import tensorflow
import random
import json

with open('parte_slop.json', encoding='utf-8') as file:
    Paises = json.load(file)

city_names = list(Paises.keys())  # Extract city names into a list
descriptions = list(Paises.values())  # Extract descriptions into a list

print(city_names)
print(descriptions)

nltk.download('stopwords')
stopwords_list = list(set(stopwords.words('english')))
CV = CountVectorizer(stop_words=stopwords_list)
# Inicializar el vectorizador
#CV = CountVectorizer() #connvierte una loista en una descripcion numerica
# Convertir el arreglo de descripciones en un modelo de Textos Vs Vocabulario
#Toma la lista y la vuelve en una matriz numerica y los valores de la matriz indican la frecuencia de cada palabra
VectorPalabras = CV.fit_transform(descriptions)

# Forma del vector resultante (Textos, Vocabulario)
print("Forma del vector(Textos, Vocabulario) = " + str(VectorPalabras.shape))

# Creamos un transformador de nuestro vector
tfidf_transformer = TfidfTransformer(use_idf=True) #instancia de un transformador que le decimos que va a usar idf
tfidf_transformer.fit(VectorPalabras)#saca el idf (mide exclusividad) y tf (mide frecuencia)

# Insertamos los valores en un DataSet
df_idf = pd.DataFrame(tfidf_transformer.idf_, index = CV.get_feature_names_out(), columns = ["Pesos-IDF"])
# Ordenams los valores del de menor relevancia hasta el de mayor relevancia
df_idf.sort_values(by=['Pesos-IDF'])

# Creamos el "count vector" el cuál indica la cantidad de
# veces que se repite cada token único
count_vector = CV.transform(descriptions)

# Cálculo de los valores para tf-idf, es decir le da la relevancia a cada palabra
tf_idf_vector = tfidf_transformer.transform(count_vector)

# Generamos un DataFrame con los valores tf-idf de cada token
# para cada texto
df = pd.DataFrame(tf_idf_vector.T.todense(),
                  index = CV.get_feature_names_out(),
                  columns = city_names)
# Ordenamos el Dataset por valores (Descendente)
df.sort_values(by=city_names[0],ascending=False)

#Sacar los valores mas relevantes de cada columna y almacenarlos en un diccionario
top_words_by_city = {}

for city in city_names:
    # Sort the DataFrame column (city) by TF-IDF values to get top words
    top_words_by_city[city] = df[city].nlargest(100).index.tolist()

# Display or further process the top words for each city
for city, top_words in top_words_by_city.items():
    print(f"Top words for {city}: {', '.join(top_words)}")

num_examples = 10# Number of example sentences to generate for each city
#words_per_example = 100
examples_by_city ={}

for city, top_words in top_words_by_city.items():
    print(f"Examples for {city}:")
    examples = []
    for _ in range(num_examples):
        # Randomly select a few words from the top words list for the city
        num_words_in_sentence = random.randint(99, 100)  # Randomly select sentence length
        selected_words = random.sample(top_words, num_words_in_sentence)

        # Create an example sentence using the selected words
        example_sentence = ' '.join(selected_words)
        examples.append(example_sentence.capitalize())
    examples_by_city[city] = examples
    #print(f"Generated {num_examples} examples for {city}.")
    print(examples_by_city['Bangkok'])

Y_Examples = list()

for clase, lista_textos in examples_by_city.items():
    for text in lista_textos:
        Y_Examples.append(list(examples_by_city.keys()).index(clase))
print("Vector de salidas Y para Examples by city")
print(Y_Examples)

X_Examples = list()
for lista in examples_by_city.values():
    for texto in lista:
        X_Examples.append(texto)
print(X_Examples)

#Generar la matriz de entrada
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
maxlen = 100
tokenizer_Examples = Tokenizer(num_words=5000)
tokenizer_Examples.fit_on_texts(X_Examples)
X_Examples_Tok = tokenizer_Examples.texts_to_sequences(X_Examples)
X_Examples_train = pad_sequences(X_Examples_Tok, padding='post', maxlen=maxlen)
print("Matriz de entrada para Examples:")
print(X_Examples_train)

# Declaración de librerías para manejo de arreglos (Numpy)
from numpy import asarray
from numpy import zeros

# Lectura del archivo de embeddings
embeddings_dictionary = dict()
Embeddings_file = open('Word2Vect_Spanish.txt', encoding="utf8")

# Extraemos las características del archivo de embeddings
# y las agregamos a un diccionario (Cada elemento es un vextor)
for linea in Embeddings_file:
    caracts = linea.split()
    palabra = caracts[0]
    vector = asarray(caracts[1:], dtype='float32')
    embeddings_dictionary [palabra] = vector
Embeddings_file.close()

# Asignamos los embeddings correspondientes a cada matriz
# con la que se entrenarán los modelos por medio de un método
def Asignar_Embeddings(tokenizer, vocab_size):
    # Generamos la matriz de embeddings (Con 300 Características)
    embedding_matrix = zeros((vocab_size, 300))
    for word, index in tokenizer.word_index.items():
        # Extraemos el vector de embedding para cada palabra
        embedding_vector = embeddings_dictionary.get(word)
        # Si la palbra si existía en el vocabulario
        # agregamos su vector de embeddings en la matriz
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector
    return embedding_matrix

vocab_size_Examples = len(tokenizer_Examples.word_index) + 1
embedding_matrix_Examples = Asignar_Embeddings(tokenizer_Examples, vocab_size_Examples)

# Declaración de modelo Secuencial que usaremos para todos los casos
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers import DNN
from keras.layers import Embedding

# Definición del método para tener la arquitectura de los modelos para cada nivel contextual
def Definir_Modelos(vocab_size, embedding_matrix, X_train, labels):
    model = Sequential()
    embedding_layer = Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=X_train.shape[1], trainable=False)
    model.add(embedding_layer)
    #model.add(DNN(20, dropout=0.2, recurrent_dropout=0.2))
    model.add(Flatten())
    model.add(Dense(len(labels), activation='softmax'))  # Change 'relu' to 'softmax' for classification

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    print(model.summary())
    print("\nPalabras en el vocabulario:")
    print(vocab_size)
    return model

# Generamos la arquitectura para el modelo de N1
model_Examples = Definir_Modelos(vocab_size_Examples, embedding_matrix_Examples, X_Examples_train, examples_by_city.keys())

# Declaramos el método para entrenar cada modelo
#from tensorflow.keras.utils import to_categorical #COLLLAB
from keras.utils.np_utils import to_categorical

def Entrenar_Modelos(X_train, Y, model, labels):
    # Declaramos librería para convertir la salida en un vector
    # de X elementos con activación en la columna correspondiente
    # a su categoría
    train_labels = to_categorical(Y, num_classes=len(labels))
    print('Matriz de salidas')
    print(train_labels)


    # Ajuste de los datos de entrenamiento al modelo creado
    history = model.fit(X_train, train_labels, epochs=30,  batch_size=1, verbose=1)

    # Cálculo de los procentajes de Eficiencia y pérdida
    score = model.evaluate(X_train, train_labels, verbose=1)
    print("\nTest Loss:", score[0])
    print("Test Accuracy:", score[1])
    return history

# Entrenamos el modelo del nivel NI y obtenemos el historial de las épocas para realizar su gráfica
history_Examples = Entrenar_Modelos(X_Examples_train, Y_Examples, model_Examples, examples_by_city.keys())

import pickle
# Load the model
with open('lstm_model.pkl', 'wb') as f:
    pickle.dump(model_Examples, f)

# Now you can use `loaded_model` for predictions or further training

