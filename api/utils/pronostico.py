"""
Retorna el valor del pronóstico dado una fecha en formato yyyy-MM
"""

def get_pronostico_value_by_date(result_df, date):
    return result_df[result_df['ds'].apply(lambda x: x.strftime("%Y-%m") == date)]["yhat"].values[0]