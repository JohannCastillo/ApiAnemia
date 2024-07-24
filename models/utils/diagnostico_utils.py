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