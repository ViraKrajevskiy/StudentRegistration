import json
from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe # Для отображения фото

# Импорты всех твоих моделей
from MainApp.modells.MainModel.Students import Applicant
from MainApp.modells.Topick.Directions import Direction, Faculty, Subject
from MainApp.modells.Tests.Test import ExamResult

# 1. Регистрация Факультетов
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')
    search_fields = ('name_uz', 'name_ru', 'name_en')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_uz', 'faculty', 'quota', 'lang_uz', 'lang_ru', 'lang_en')
    list_filter = ('faculty', 'lang_uz', 'lang_ru', 'lang_en')
    search_fields = ('name_uz', 'code')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'total_score')
    readonly_fields = ('total_score',)

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    change_list_template = "admin/applicant_change_list.html"

    list_display = ('get_photo', 'last_name', 'first_name', 'phone_number', 'direction', 'is_approved', 'registration_date')
    list_filter = ('direction', 'is_approved', 'gender', 'is_graduated')
    search_fields = ('last_name', 'first_name', 'passport_seria', 'phone_number')
    list_editable = ('is_approved',)
    readonly_fields = ('registration_date', 'preview_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit:cover; border-radius:5px;">')
        return "Нет фото"
    get_photo.short_description = "Фото"

    def preview_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="200">')
        return "Нет фото"
    preview_photo.short_description = "Просмотр фото"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # Определяем текущий язык для графиков
        from django.utils import translation
        lang = translation.get_language()
        # Выбираем поле в зависимости от языка (name_uz, name_ru или name_en)
        direction_field = f"direction__name_{lang}" if lang in ['ru', 'en'] else "direction__name_uz"

        direction_data = list(qs.values(direction_field).annotate(total=Count("id")).order_by("-total"))
        status_data = list(qs.values("is_approved").annotate(total=Count("id")))

        extra_info = {
            "direction_json": json.dumps([
                {"label": item[direction_field] or "---", "value": item["total"]}
                for item in direction_data
            ]),
            "status_json": json.dumps([
                {"label": "Одобрен" if item["is_approved"] else "В ожидании", "value": item["total"]}
                for item in status_data
            ]),
        }
        response.context_data.update(extra_info)
        return response