from django.urls import path

# Объединяем все нужные импорты в одну строку:
from .views import index, by_rubric, BbCreateView

urlpatterns = [
    # 1. Маршрут для добавления объявления
    path('add/', BbCreateView.as_view(), name='add'),

    # 2. Маршрут для отображения объявлений по рубрике.
    # Используем функцию 'by_rubric', но сохраняем имя 'rubric_bbs' для шаблонов.
    path('<int:rubric_id>/', by_rubric, name='rubric_bbs'),

    # 3. Маршрут для главной страницы (все объявления)
    path('', index, name='index'),
]