from django import forms
from .modells.MainModel.Students import Applicant
from .modells.Topick.Directions import Direction

class RegistrationForm(forms.ModelForm):
    is_graduated = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'uz')
        super().__init__(*args, **kwargs)

        # 1. Расширяем словарь переводов для всех полей
        labels = {
            'ru': {
                'gender': [('', '---'), ('M', 'Мужчина'), ('F', 'Женщина')],
                'parents': [('', '---'), ('mother', 'Мать'), ('father', 'Отец'), ('other', 'Другое')],
                'addr': "Адрес",
                'grad': "Окончил обучение",
                'photo': "Фото (3x4)",
                'choice_label': "Контактное лицо"
            },
            'en': {
                'gender': [('', '---'), ('M', 'Male'), ('F', 'Female')],
                'parents': [('', '---'), ('mother', 'Mother'), ('father', 'Father'), ('other', 'Other')],
                'addr': "Address",
                'grad': "Graduated",
                'photo': "Photo (3x4)",
                'choice_label': "Contact Person"
            },
            'uz': {
                'gender': [('', '---'), ('M', 'Erkak'), ('F', 'Ayol')],
                'parents': [('', '---'), ('mother', 'Ona'), ('father', 'Ota'), ('other', 'Boshqa')],
                'addr': "Manzil",
                'grad': "Tugatganman",
                'photo': "Rasm (3x4)",
                'choice_label': "Kim orqali bog'lanish"
            }
        }

        txt = labels.get(language, labels['uz'])

        # 2. Применяем переводы к спискам (Choices)
        self.fields['gender'].choices = txt['gender']
        self.fields['choice_field'].choices = txt['parents'] # Тот самый перевод мамы/папы

        # 3. Применяем переводы к лейблам
        self.fields['address'].label = txt['addr']
        self.fields['is_graduated'].label = txt['grad']
        self.fields['photo'].label = txt['photo']
        self.fields['choice_field'].label = txt['choice_label']

        # 4. Перевод направлений из БД (если есть поля name_ru, name_uz)
        if 'direction' in self.fields:
            self.fields['direction'].queryset = Direction.objects.all()
            # Пытаемся взять имя на нужном языке, если поле существует в модели Direction
            self.fields['direction'].label_from_instance = lambda obj: getattr(obj, f'name_{language}', obj.name)

    class Meta:
        model = Applicant
        fields = [
            'photo', 'first_name', 'last_name', 'middle_name', 'birth_date', 'gender',
            'passport_seria', 'phone_number', 'email', 'address', 'choice_field',
            'parent_first_name', 'parent_last_name', 'parent_phone_number',
            'school_name', 'is_graduated', 'direction', 'education_language'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }