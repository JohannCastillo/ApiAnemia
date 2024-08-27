from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_image, name="generate_image"),
    path("dieta/<int:dieta_id>", views.gen_dieta, name="generate_image"),
    path("predict/<int:diag_id>", views.gen_predict, name="generate_image"),
]
