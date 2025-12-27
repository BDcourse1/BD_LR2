from django.contrib import admin
from .models import (
    Bb,
    Rubric,
    BbDetail,
    Tag,
    ProjectUser,
    BbRating,
    BbFeature,  # Добавляем новую модель характеристик
    # BbImage   # Раскомментируйте, если создавали модель для фото
)


# 1. Настройка Inline для характеристик
# Это позволит добавлять/редактировать параметры прямо внутри объявления
class BbFeatureInline(admin.TabularInline):
    model = BbFeature
    extra = 1  # Количество пустых полей для новых параметров


# 2. Настройка Inline для фото (опционально)
# class BbImageInline(admin.TabularInline):
#     model = BbImage
#     extra = 1

# 3. Настройка основной модели Bb (Объявления)
class BbAdmin(admin.ModelAdmin):
    # Что отображать в общем списке
    list_display = ('rubric', 'title', 'content', 'price', 'published')
    # Что будет ссылкой на редактирование
    list_display_links = ('title', 'content')
    # По каким полям искать
    search_fields = ('title', 'content')

    # ПОДКЛЮЧАЕМ ДИНАМИЧЕСКИЕ СПИСКИ (Характеристики)
    inlines = [BbFeatureInline]  # Добавьте сюда BbImageInline, если нужно


# 4. Настройка для модели BbRating
class BbRatingAdmin(admin.ModelAdmin):
    list_display = ('bb', 'user', 'rating_value', 'rated_at')
    list_filter = ('rating_value', 'rated_at')
    search_fields = ('bb__title', 'user__username')


# РЕГИСТРАЦИЯ ВСЕХ МОДЕЛЕЙ

admin.site.register(Rubric)
admin.site.register(Bb, BbAdmin)  # Используем расширенную настройку с Inline
admin.site.register(BbDetail)
admin.site.register(Tag)
admin.site.register(ProjectUser)
admin.site.register(BbRating, BbRatingAdmin)

# Регистрируем характеристики отдельно (на случай, если захотите смотреть их общим списком)
admin.site.register(BbFeature)
# admin.site.register(BbImage)