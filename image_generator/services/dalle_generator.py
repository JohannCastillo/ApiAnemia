from .base_generator import BaseImageGenerator
from openai import OpenAI
from django.conf import settings


class DalleGenerator(BaseImageGenerator):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_image(self, prompt, size="1024x1024", quality="standard", n=1):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )
        return response.data[0].url
