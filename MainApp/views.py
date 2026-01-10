from django.shortcuts import render, redirect
from django.utils import translation
from django.core.mail import send_mail
from .forms import RegistrationForm

def registration_success(request):
    return render(request, 'registration/success.html')

def register_view(request):
    # 1. ОПРЕДЕЛЕНИЕ ЯЗЫКА
    user_language = request.GET.get('lang')
    if user_language not in ['ru', 'uz', 'en']:
        user_language = request.session.get('_language', 'uz')

    translation.activate(user_language)
    request.session['_language'] = user_language

    # 2. СЛОВАРЬ ПЕРЕВОДОВ (для заголовков HTML)
    texts = {
        'uz': {
            'title': "Onlayn Qabul — 2026",
            'subtitle': "Barcha maydonlarni diqqat bilan to'ldiring",
            'personal_title': "SHAXSIY MA'LUMOTLAR",
            'first_name': "Ism",
            'last_name': "Familiya",
            'middle_name': "Otasining ismi",
            'birth_date': "Tug'ilgan sana",
            'gender': "Jins",
            'passport_title': "PASPORT VA ALOQA",
            'passport_seria': "Pasport seriya va raqam",
            'phone_number': "Telefon raqamingiz",
            'email': "Email (Pochta)",
            'address': "Yashash manzili",
            'parents_title': "OTA-ONA MA'LUMOTLARI",
            'p_first_name': "Ismi",
            'p_last_name': "Familiyasi",
            'p_phone': "Telefoni",
            'edu_title': "TA'LIM VA YO'NALISH",
            'school_name': "Bitirgan maktabingiz nomi",
            'graduated_label': "Men maktabni/kollejni to'liq tugatganman",
            'direction': "Fakultet / Yo'nalish",
            'edu_lang': "Ta'lim tili (Imtihon tili)",
            'btn': "RO'YXATDAN O'TISH",
            'all_rights': "Barcha huquqlar himoyalangan"
        },
        'ru': {
            'title': "Онлайн Прием — 2026",
            'subtitle': "Заполните все поля внимательно",
            'personal_title': "ЛИЧНЫЕ ДАННЫЕ",
            'first_name': "Имя",
            'last_name': "Фамилия",
            'middle_name': "Отчество",
            'birth_date': "Дата рождения",
            'gender': "Пол",
            'passport_title': "ПАСПОРТ И СВЯЗЬ",
            'passport_seria': "Серия и номер паспорта",
            'phone_number': "Ваш номер телефона",
            'email': "Email (Почта)",
            'address': "Адрес проживания",
            'parents_title': "ДАННЫЕ РОДИТЕЛЕЙ",
            'p_first_name': "Имя",
            'p_last_name': "Фамилия",
            'p_phone': "Телефон",
            'edu_title': "ОБРАЗОВАНИЕ И НАПРАВЛЕНИЕ",
            'school_name': "Название учебного заведения",
            'graduated_label': "Я полностью окончил школу/колледж",
            'direction': "Факультет / Направление",
            'edu_lang': "Язык обучения (экзамена)",
            'btn': "ЗАРЕГИСТРИРОВАТЬСЯ",
            'all_rights': "Все права защищены"
        },
        'en': {
            'title': "Online Admission — 2026",
            'subtitle': "Please fill in all fields carefully",
            'personal_title': "PERSONAL INFORMATION",
            'first_name': "First Name",
            'last_name': "Last Name",
            'middle_name': "Middle Name",
            'birth_date': "Birth Date",
            'gender': "Gender",
            'passport_title': "PASSPORT & CONTACT",
            'passport_seria': "Passport Serial & Number",
            'phone_number': "Your Phone Number",
            'email': "Email Address",
            'address': "Residential Address",
            'parents_title': "PARENT INFORMATION",
            'p_first_name': "First Name",
            'p_last_name': "Last Name",
            'p_phone': "Phone Number",
            'edu_title': "EDUCATION & DIRECTION",
            'school_name': "School/College Name",
            'graduated_label': "I have graduated from school/college",
            'direction': "Faculty / Direction",
            'edu_lang': "Language of Education",
            'btn': "REGISTER NOW",
            'all_rights': "All rights reserved"
        }
    }

    current_text = texts.get(user_language, texts['uz'])

    # 3. ОБРАБОТКА ФОРМЫ
    if request.method == 'POST':
        # ПЕРЕДАЕМ language=user_language, чтобы форма знала, как перевести пол
        form = RegistrationForm(request.POST, language=user_language)
        if form.is_valid():
            applicant = form.save()
            try:
                send_mail(
                    "Заявка принята",
                    f"Здравствуйте {applicant.first_name}, ваша заявка получена.",
                    'admin@university.uz',
                    [applicant.email]
                )
            except Exception as e:
                print(f"Mail error: {e}")
            return redirect('registration_success')
    else:
        # ПЕРЕДАЕМ language=user_language для GET запроса (отображение пустой формы)
        form = RegistrationForm(language=user_language)

    return render(request, 'registration/register.html', {
        'form': form,
        't': current_text,
        'lang': user_language
    })