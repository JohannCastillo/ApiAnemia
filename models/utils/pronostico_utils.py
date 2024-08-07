import pandas as pd

def predecir_segun_fechas(prophet, year_start, year_end):
    start_date = f'{year_start}-01-01'
    end_date = f'{year_end}-12-31'
    future_dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    future = pd.DataFrame(future_dates, columns=['ds'])
    forecast = prophet.predict(future)
    forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x: max(0, x))
    forecast['yhat'] = forecast['yhat'].apply(lambda x: max(0, x))
    return forecast

# def generar_imagen(forecast):
#     matplotlib.use('agg')
#     plt.figure(figsize=(14, 8))

#     # Plotear las predicciones
#     plt.plot(forecast['ds'], forecast['yhat'], label='Predicción', color='blue')
#     plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=0.4, label='Intervalo de confianza')

#     # Etiquetas y título
#     plt.xlabel('Fecha')
#     plt.ylabel('Predicción')
#     plt.title('Predicciones con Prophet')
#     plt.legend()

#     # Anotar los valores en cada tick del eje x
#     previous_yhat=-1
#     for x, y in zip(forecast['ds'], forecast['yhat']):
#         if previous_yhat > y:
#             offset = -10
#         else:
#             offset = 10
#         plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, offset), ha='center', fontsize=8)
#         previous_yhat = y

#     # Ajustar la visualización de las fechas en el eje x
#     plt.xticks(rotation=45)
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png', bbox_inches='tight')
#     print("imagen guardada")
#     buffer.seek(0)
#      # Cerrar la figura para liberar memoria
#     plt.close()
#     # Convertir el buffer a una cadena base64
#     img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
#     buffer.close()
#     return img_base64
