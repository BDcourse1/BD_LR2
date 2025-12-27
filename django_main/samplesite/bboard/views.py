from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Импорт моделей для использования в ORM
from .models import Bb, Rubric, Tag, BbRating, ProjectUser
# Импорт для вычислений и агрегации (средний рейтинг)
from django.db.models import Avg, Count
# Импорт формы
from .forms import BbForm

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Bb
from .forms import BbForm, FeatureFormSet  # Импортируем наш формсет


# ----------------------------------------------------------------------
# 1. Представление для создания нового объявления
# ----------------------------------------------------------------------

class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    success_url = '/bboard/'  # Или reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Если страница отправлена (POST), заполняем формсет данными из запроса
            context['features'] = FeatureFormSet(self.request.POST)
        else:
            # Если страница только открылась (GET), создаем пустой формсет
            context['features'] = FeatureFormSet()
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        features = context['features']

        # Проверяем на валидность и основную форму, и все формы в наборе
        if form.is_valid() and features.is_valid():
            # 1. Сохраняем товар, но пока только в памяти (commit=False не нужен, если сразу сохраняем)
            self.object = form.save()

            # 2. Связываем характеристики с только что созданным товаром
            features.instance = self.object

            # 3. Сохраняем все характеристики в базу данных
            features.save()

            return redirect(self.get_success_url())
        else:
            # Если что-то не так, заново отрисовываем страницу с ошибками
            return self.render_to_response(self.get_context_data(form=form))


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