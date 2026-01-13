from django.shortcuts import redirect, render
from .forms import RegistrationForm
from django.db.models import Count, Prefetch
from .modells.Topick.Directions import Faculty, Direction
import json
from django.utils import translation

def registration_success(request):
    user_language = request.session.get('_language', 'uz')
    translation.activate(user_language)

    texts = {
        'uz': {
            'success_title': "Muvaffaqiyatli!",
            'success_sub': "Ma'lumotlaringiz qabul qilindi",
            'success_desc': "Ro'yxatdan o'tganingiz uchun rahmat! Sizning anketangiz qabul komissiyasi tizimiga yuborildi.",
            'btn_home': "Bosh sahifaga qaytish"
        },
        'ru': {
            'success_title': "Успешно!",
            'success_sub': "Ваши данные получены",
            'success_desc': "Благодарим за регистрацию! Ваша анкета передана в информационную систему приёмной комиссии.",
            'btn_home': "На главную страницу"
        },
        'en': {
            'success_title': "Success!",
            'success_sub': "Data Received",
            'success_desc': "Thank you for registering! Your application has been submitted to the admissions system.",
            'btn_home': "Back to Home"
        }
    }

    return render(request, 'registration/success.html', {
        't': texts.get(user_language, texts['uz']),
        'lang': user_language
    })

def university_info(request):
    user_language = request.GET.get('lang')
    if user_language not in ['ru', 'uz', 'en']:
        user_language = request.session.get('_language', 'uz')

    translation.activate(user_language)
    request.session['_language'] = user_language

    texts = {
        'uz': {
            'nav_reg': "Ro'yxatdan o'tish",
            'hero_badge': "QABUL 2026/2027",
            'hero_title': "Sizning muvaffaqiyatingiz shu yerdan boshlanadi",
            'hero_sub': "Mamlakatning yetakchi universitetiga yagona onlayn platforma orqali hujjat topshiring.",
            'hero_btn': "Hujjat topshirishni boshlash",
            'stat_online': "ONLAYN QABUL",
            'stat_quota': "KVOTA O'RINLARI",
            'stat_dir': "YO'NALISHLAR",
            'apply_btn': "Hujjat topshirish",
            'left_seats': "Bo'sh joylar",
            'full_msg': "Joylar tugagan",
            'total_quota': "Jami kvota",
            'lang_label': "Ta'lim tili",
            'footer': "© 2026 Onlayn qabul tizimi. Abituriyentlar uchun maxsus tayyorlangan."
        },
        'ru': {
            'nav_reg': "Регистрация",
            'hero_badge': "ПРИЁМ 2026/2027",
            'hero_title': "Твой успех начинается здесь",
            'hero_sub': "Подайте документы в ведущий университет страны через единую онлайн-платформу.",
            'hero_btn': "Начать поступление",
            'stat_online': "ОНЛАЙН ПРИЕМ",
            'stat_quota': "КВОТНЫХ МЕСТ",
            'stat_dir': "НАПРАВЛЕНИЙ",
            'apply_btn': "Подать заявку",
            'left_seats': "Осталось мест",
            'full_msg': "Мест нет",
            'total_quota': "Всего квота",
            'lang_label': "Язык обучения",
            'footer': "© 2026 Система онлайн-приема. Сделано для абитуриентов."
        },
        'en': {
            'nav_reg': "Registration",
            'hero_badge': "ADMISSION 2026/2027",
            'hero_title': "Your success starts here",
            'hero_sub': "Apply to the country's leading university through a single online platform.",
            'hero_btn': "Start Application",
            'stat_online': "ONLINE ADMISSION",
            'stat_quota': "QUOTA SEATS",
            'stat_dir': "DIRECTIONS",
            'apply_btn': "Apply Now",
            'left_seats': "Seats left",
            'full_msg': "Full",
            'total_quota': "Total quota",
            'lang_label': "Instruction language",
            'footer': "© 2026 Online Admission System. Built for applicants."
        }
    }

    faculties = Faculty.objects.prefetch_related(
        Prefetch(
            'directions',
            queryset=Direction.objects.annotate(registered_count=Count('applicants'))
        )
    ).all()

    return render(request, 'Infopage/MainInfo.html', {
        'faculties': faculties,
        't': texts.get(user_language, texts['uz']),
        'lang': user_language
    })

def register_view(request):
    # 1. Определяем язык
    user_language = request.GET.get('lang')
    if user_language not in ['ru', 'uz', 'en']:
        user_language = request.session.get('_language', 'uz')

    translation.activate(user_language)
    request.session['_language'] = user_language

    # 2. Тексты переводов (ДОБАВЛЕНЫ СЕКЦИЯ 3 и ФАКУЛЬТЕТ)
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
            # Секция 3
            'parent_title': "Ota-ona ma'lumotlari",
            'contact_person': "Kim orqali bog'lanish",
            'parent_last_name': "Familiyasi",
            'parent_first_name': "Ismi",
            'parent_phone': "Telefon raqami",
            # Секция 4
            'edu_title': "TA'LIM VA YO'NALISH",
            'school_name': "Bitirgan maktabingiz nomi",
            'faculty_label': "Fakultet",
            'direction_label': "Yo'nalish",
            'edu_lang': "Ta'lim tili (Imtihon tili)",
            'btn': "RO'YXATDAN O'TISH",
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
            # Секция 3
            'parent_title': "Данные родителей",
            'contact_person': "Контактное лицо",
            'parent_last_name': "Фамилия",
            'parent_first_name': "Имя",
            'parent_phone': "Номер телефона",
            # Секция 4
            'edu_title': "ОБРАЗОВАНИЕ И НАПРАВЛЕНИЕ",
            'school_name': "Название учебного заведения",
            'faculty_label': "Факультет",
            'direction_label': "Направление",
            'edu_lang': "Язык обучения (экзамена)",
            'btn': "ЗАРЕГИСТРИРОВАТЬСЯ",
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
            # Секция 3
            'parent_title': "Parent Information",
            'contact_person': "Contact Person",
            'parent_last_name': "Last Name",
            'parent_first_name': "First Name",
            'parent_phone': "Phone Number",
            # Секция 4
            'edu_title': "EDUCATION & DIRECTION",
            'school_name': "School/College Name",
            'faculty_label': "Faculty",
            'direction_label': "Direction",
            'edu_lang': "Language of Education",
            'btn': "REGISTER NOW",
        }
    }
    current_text = texts.get(user_language, texts['uz'])

    # 3. Подготовка данных для JS (с учетом языка имен из БД)
    faculties = Faculty.objects.all()
    faculty_map = {}

    for f in faculties:
        # Пытаемся взять имя на текущем языке, если нет - обычное name
        f_name = getattr(f, f'name_{user_language}', f.name)

        directions_data = []
        for d in f.directions.all():
            d_name = getattr(d, f'name_{user_language}', d.name)
            directions_data.append({'id': d.id, 'name': d_name})

        faculty_map[str(f.id)] = directions_data

    langs_config = {str(d.id): d.get_available_languages() for d in Direction.objects.all()}

    # 4. Логика предвыбора
    selected_dir_id = request.GET.get('direction_id')
    selected_faculty_id = ""
    if selected_dir_id:
        try:
            direction_obj = Direction.objects.get(id=selected_dir_id)
            selected_faculty_id = direction_obj.faculty.id
        except: pass

    # 5. Обработка формы
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES, language=user_language)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        initial = {'direction': selected_dir_id} if selected_dir_id else {}
        form = RegistrationForm(language=user_language, initial=initial)

    return render(request, 'registration/register.html', {
        'form': form,
        't': current_text,
        'faculties_list': faculties, # Для первичной загрузки селекта
        'faculty_map': json.dumps(faculty_map),
        'langs_config': json.dumps(langs_config),
        'selected_faculty_id': selected_faculty_id,
        'lang': user_language
    })