import datetime


"""
    Funciones para codificar y decodificar los datos de entrada y salida del modelo
"""
def decode_output(cod_prediccion, label_encoders):
    return label_encoders.get('Dx_anemia').classes_[cod_prediccion]


def encode_input(input, label_encoders):
    for caracteristica, le in label_encoders.items():
        for code, value in enumerate(le.classes_):
            if caracteristica in input and input[caracteristica] == value:
                input[caracteristica] = code
    return input

def predict(modelo, input_data):
  model, label_encoders, scaler = modelo
  # Codificar entrada 
  list_values = list(encode_input(input_data, label_encoders).values())
  # Escalar entrada
  input_data_scaled = scaler.transform([list_values])
  # Predecir
  prediction = model.predict(input_data_scaled)
  return decode_output(prediction[0], label_encoders=label_encoders)

"""
    Calcular edad en meses a partir de la fecha de nacimiento
"""

def calcular_edad_en_meses(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year
    meses = hoy.month - fecha_nacimiento.month
    edad_meses = edad * 12 + meses
    return edad_meses