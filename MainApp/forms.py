from django import forms
from datetime import date
from django.utils import translation
from MainApp.modells.MainModel.Students import Applicant
from MainApp.modells.Topick.Directions import Direction

class RegistrationForm(forms.ModelForm):
    is_graduated = forms.BooleanField(
        required=True,
        # Label зададим в __init__ для поддержки перевода
    )

    def __init__(self, *args, **kwargs):
        # Получаем язык из views.py
        language = kwargs.pop('language', 'uz')
        super().__init__(*args, **kwargs)

        # 1. ПЕРЕВОД ГЕНДЕРА И АДРЕСА
        if language == 'ru':
            gender_choices = [('', '---------'), ('M', 'Мужчина'), ('F', 'Женщина')]
            address_label = "Адрес проживания"
            graduated_label = "Я полностью окончил школу/колледж"
            school_label = "Название учебного заведения"
        elif language == 'en':
            gender_choices = [('', '---------'), ('M', 'Male'), ('F', 'Female')]
            address_label = "Residential Address"
            graduated_label = "I have graduated from school/college"
            school_label = "School/College Name"
        else:
            gender_choices = [('', '---------'), ('M', 'Erkak'), ('F', 'Ayol')]
            address_label = "Yashash manzili"
            graduated_label = "Men maktabni/kollejni to'liq tugatganman"
            school_label = "Bitirgan maktabingiz nomi"

        # Принудительно ставим переведенные метки (Labels)
        self.fields['gender'].choices = gender_choices
        self.fields['address'].label = address_label
        self.fields['is_graduated'].label = graduated_label
        self.fields['school_name'].label = school_label

        # 2. НАПРАВЛЕНИЯ (используем @property name из модели)
        if 'direction' in self.fields:
            self.fields['direction'].queryset = Direction.objects.all()
            self.fields['direction'].label_from_instance = lambda obj: obj.name

    class Meta:
        model = Applicant
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender',
            'passport_seria', 'phone_number', 'email', 'address',
            'parent_first_name', 'parent_last_name', 'parent_phone_number',
            'school_name', 'is_graduated', 'direction', 'education_language'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                # В идеале здесь тоже нужен перевод через gettext_lazy
                raise forms.ValidationError("Yoshingiz 18 dan kichik!")
        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        direction = cleaned_data.get('direction')
        edu_lang = cleaned_data.get('education_language')
        if direction and edu_lang:
            is_available = False
            if edu_lang == 'uz' and direction.lang_uz: is_available = True
            elif edu_lang == 'ru' and direction.lang_ru: is_available = True
            elif edu_lang == 'en' and direction.lang_en: is_available = True
            if not is_available:
                raise forms.ValidationError("Bu yo'nalishda tanlangan til mavjud emas!")
        return cleaned_data