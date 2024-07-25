def decode_output(cod_prediccion, label_encoders):
    return label_encoders.get('Dx_anemia').classes_[cod_prediccion]


def encode_input(input, label_encoders):
    for caracteristica, le in label_encoders.items():
        for code, value in enumerate(le.classes_):
            if caracteristica in input and input[caracteristica] == value:
                input[caracteristica] = code
    return input

def predict(modelo, input_data):
  model, scaler = modelo
  # Escalar entrada
  input_data_scaled = scaler.transform([input_data])
  # Predecir
  prediction = model.predict(input_data_scaled)+1
  return prediction[0]