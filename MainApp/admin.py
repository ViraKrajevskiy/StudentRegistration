from django.contrib import admin

from MainApp.modells.MainModel.Students import Applicant
from MainApp.modells.Tests.Test import ExamResult
from MainApp.modells.Topick.Directions import Direction

@admin.register(Direction)

class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'quota')
    search_fields = ('name', 'code')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'total_score')
    readonly_fields = ('total_score',)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone_number', 'direction', 'is_approved', 'registration_date')
    list_filter = ('direction', 'is_approved', 'gender', 'is_graduated')
    search_fields = ('last_name', 'first_name', 'passport_seria', 'phone_number')
    list_editable = ('is_approved',)
    readonly_fields = ('registration_date',)

    fieldsets = (
        ('Shaxsiy Ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 'address')
        }),
        ('Pasport va Aloqa', {
            'fields': ('passport_seria', 'phone_number', 'email')
        }),
        ('Ota-Onasi haqida', {
            'fields': ('parent_first_name', 'parent_last_name', 'parent_phone_number')
        }),
        ('Ta\'lim va Yo\'nalish', {
            'fields': ('school_name', 'is_graduated', 'direction')
        }),
        ('Status', {
            'fields': ('is_approved', 'registration_date')
        }),
    )