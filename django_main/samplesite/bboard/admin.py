from django.contrib import admin

# Импортируем все модели, включая новые, добавленные для связей
from .models import (
    Bb,
    Rubric,
    BbDetail,
    Tag,
    ProjectUser,
    BbRating
)

# ----------------------------------------------------
# Настройка для модели Rubric
# (Оставлена простой, так как у вас не было кастомной)
# ----------------------------------------------------
admin.site.register(Rubric)


# ----------------------------------------------------
# Настройка для модели Bb (Объявления)
# (Ваша оригинальная настройка)
# ----------------------------------------------------
class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(Bb, BbAdmin)


# ----------------------------------------------------
# Настройка для модели BbRating (Для связи Многие-ко-Многим с доп. данными)
# Добавляем list_display для удобного просмотра
# ----------------------------------------------------
class BbRatingAdmin(admin.ModelAdmin):
    list_display = ('bb', 'user', 'rating_value', 'rated_at')
    list_filter = ('rating_value', 'rated_at')
    search_fields = ('bb__title', 'user__username')


# ----------------------------------------------------
# Регистрация НОВЫХ моделей
# ----------------------------------------------------

# Модель для связи «Один-к-Одному»
admin.site.register(BbDetail)

# Модель для простой связи «Многие-ко-Многим»
admin.site.register(Tag)

# Модель Пользователя для сложной связи «Многие-ко-Многим»
admin.site.register(ProjectUser)

# Промежуточная модель для сложной связи «Многие-ко-Многим»
admin.site.register(BbRating, BbRatingAdmin)