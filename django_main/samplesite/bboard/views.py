# from django.shortcuts import render
# from .models import Bb
# from .models import Rubric
# from django.views.generic.edit import CreateView
# from .forms import BbForm
# from django.urls import reverse_lazy
#
# class BbCreateView(CreateView):
#     template_name = 'bboard/bb_create.html'
#     form_class = BbForm
#     success_url = '/bboard/'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         success_url = reverse_lazy('index')
#         context['rubrics'] = Rubric.objects.all()
#         return context
#
# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return render(request, 'bboard/index.html', context)
#
#
# def rubric_bbs(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)
#
# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {
#         'bbs': bbs,
#         'rubrics': rubrics,
#         'current_rubric': current_rubric
#     }
#     return render(request, 'bboard/by_rubric.html', context)

# bboard/views.py

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Импорт моделей для использования в ORM
from .models import Bb, Rubric, Tag, BbRating, ProjectUser
# Импорт для вычислений и агрегации (средний рейтинг)
from django.db.models import Avg, Count
# Импорт формы
from .forms import BbForm


# ----------------------------------------------------------------------
# 1. Представление для создания нового объявления
# ----------------------------------------------------------------------

class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    success_url = '/bboard/'  # Или reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Этот код, вероятно, лишний, так как рубрики должны быть в форме
        # Если рубрики нужны в контексте, оставьте:
        context['rubrics'] = Rubric.objects.all()
        return context


# ----------------------------------------------------------------------
# 2. Представление для отображения всех объявлений (Главная страница)
# ----------------------------------------------------------------------

def index(request):
    # Оптимизированный запрос:
    # 1. select_related('rubric'): Избегает N+1 запросов для рубрики
    # 2. prefetch_related('tags'): Избегает N+1 запросов для тегов (М2М)
    # 3. annotate(...): Вычисляет средний рейтинг и количество голосов
    bbs = Bb.objects.all().select_related('rubric', 'bbdetail').prefetch_related('tags').annotate(
        average_rating=Avg('bbrating__rating_value'),
        rating_count=Count('bbrating')
    ).order_by('-published')  # Сортировка по дате публикации

    rubrics = Rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


# ----------------------------------------------------------------------
# 3. Представление для отображения объявлений по рубрике
# (Объединяет вашу логику rubric_bbs и by_rubric)
# ----------------------------------------------------------------------

def by_rubric(request, rubric_id):
    # Получаем текущую рубрику
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # Оптимизированный запрос с фильтром по рубрике:
    bbs = Bb.objects.filter(rubric=rubric_id).select_related('rubric', 'bbdetail').prefetch_related('tags').annotate(
        average_rating=Avg('bbrating__rating_value'),
        rating_count=Count('bbrating')
    ).order_by('-published')

    rubrics = Rubric.objects.all()  # Получаем все рубрики для навигации

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric
    }
    return render(request, 'bboard/by_rubric.html', context)

# ----------------------------------------------------------------------
# * Ваше представление 'rubric_bbs' дублирует 'by_rubric'.
# Рекомендуется использовать только одно из них (например, 'by_rubric')
# и удалить дубликат из urls.py
# ----------------------------------------------------------------------

# def rubric_bbs(request, rubric_id):
#     # Этот код идентичен 'by_rubric', поэтому его можно удалить,
#     # если он не нужен для обратной совместимости URL.
#     pass