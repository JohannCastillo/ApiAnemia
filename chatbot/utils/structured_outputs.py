from pydantic import BaseModel
from openai import OpenAI
from django.conf import (
    settings,
)  # Para obtener las configuraciones de tu archivo settings.py


client = OpenAI(api_key=settings.OPENAI_API_KEY)

"""
Retorna una respuesta estructurada como una lista de strings
Ejemplo: listar recomendaciones según propmt
{
    "description": "Descripción de la lista",
    "items": ["Elemento 1", "Elemento 2", "Elemento 3"]
}
"""
class List(BaseModel):
    description : str
    items : list[str]    

def get_list_structured_output(messages):
    try :
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=List
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(e)
        pass