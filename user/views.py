from django.shortcuts import render, redirect
from .forms import DoctorLoginForm,PatientLoginForm,NurseLoginForm
from .forms import DoctorRegistrationForm,PatientRegistrationForm,NurseRegistrationForm
from .models import Doctor,Patient,Nurse
from .backends import DoctorBackend,PatientBackend,NurseBackend
from django.http import HttpResponseNotFound,HttpResponseBadRequest

def home(request):
    return render(request, "user/login_home.html")


def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            contact_number = form.cleaned_data['doctor_contact_number']
            password = form.cleaned_data['doctor_password']

            # 使用自定义的医生身份验证后端进行身份验证
            user = DoctorBackend().authenticate(request, contact_number=contact_number, password=password)
            if user is not None:
                # 登录成功后的操作
                request.session['user_id'] = user.pk
                return redirect('doctor_dashboard')
            else:
                # 登录失败时，添加错误消息
                form.add_error(None, '医生账号或密码错误')
    else:
        form = DoctorLoginForm()

    return render(request, 'user/doctor_login.html', {'form': form})

def patient_login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            contact_number = form.cleaned_data['patient_contact_number']
            password = form.cleaned_data['patient_password']

            # 使用自定义的病人身份验证后端进行身份验证
            user = PatientBackend().authenticate(request, contact_number=contact_number, password=password)
            if user is not None:
                # 登录成功后的操作
                request.session['user_id'] = user.pk
                return redirect('patient_dashboard')
            else:
                # 登录失败时，添加错误消息
                form.add_error(None, '病人账号或密码错误')
    else:
        form = PatientLoginForm()

    return render(request, 'user/patient_login.html', {'form': form})

def nurse_login(request):
    if request.method == 'POST':
        form = NurseLoginForm(request.POST)
        if form.is_valid():
            contact_number = form.cleaned_data['nurse_contact_number']
            password = form.cleaned_data['nurse_password']

            # 使用自定义的护士身份验证后端进行身份验证
            user = NurseBackend().authenticate(request, contact_number=contact_number, password=password)
            if user is not None:
                # 登录成功后的操作
                request.session['user_id'] = user.pk
                return redirect('nurse_dashboard')
            else:
                # 登录失败时，添加错误消息
                form.add_error(None, '护士账号或密码错误')
    else:
        form = NurseLoginForm()

    return render(request, 'user/nurse_login.html', {'form': form})


def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            # 检查是否存在相同账号的医生
            if Doctor.objects.filter(contact_number=form.cleaned_data['contact_number']).exists():
                return render(request, 'user/doctor_register.html', {'form': form, 'error_message': '该账号已经存在，请选择其他账号。'})
            else:
                # 保存表单数据到数据库
                form.save()
                # 在注册成功时，你可以添加一些提示信息
                return render(request, 'user/doctor_register.html', {'form': form, 'success_message': '注册成功！'})
    else:
        form = DoctorRegistrationForm()

    return render(request, 'user/doctor_register.html', {'form': form})

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # 检查是否存在相同账号的病人
            if Patient.objects.filter(contact_number=form.cleaned_data['contact_number']).exists():
                form.add_error('contact_number', '该账号已经存在，请选择其他账号。')
            else:
                # 保存表单数据到数据库
                form.save()
                # 在注册成功时，你可以添加一些提示信息

                return render(request, 'user/patient_register.html', {'form': form, 'success_message': '注册成功！'})
    else:
        form = PatientRegistrationForm()

    return render(request, 'user/patient_register.html', {'form': form})
def nurse_register(request):
    if request.method == 'POST':
        form = NurseRegistrationForm(request.POST)
        if form.is_valid():
            # 检查是否存在相同账号的护士
            if Nurse.objects.filter(contact_number=form.cleaned_data['contact_number']).exists():
                form.add_error('contact_number', '该账号已经存在，请选择其他账号。')
            else:
                # 保存表单数据到数据库
                form.save()
                # 在注册成功时，你可以添加一些提示信息
                return render(request, 'user/nurse_register.html', {'form': form, 'success_message': '注册成功！'})
    else:
        form = NurseRegistrationForm()

    return render(request, 'user/nurse_register.html', {'form': form})

def doctor_dashboard(request):
    return render(request, 'user/doctor_dashboard.html')

def patient_dashboard(request):
    return render(request, 'user/patient_dashboard.html')

def nurse_dashboard(request):
    return render(request, 'user/nurse_dashboard.html')

def doctor_profile(request):
    # 获取当前登录的医生
    current_doctor_id = request.session.get('user_id')
    current_doctor = Doctor.objects.get(pk=current_doctor_id)

    context = {
        'doctor': current_doctor
    }

    return render(request, 'user/doctor_profile.html', context)


def doctor_edit_profile(request):
    if request.method == 'POST':
        # 处理表单提交逻辑
        current_doctor_id = request.session.get('user_id')
        try:
            current_doctor = Doctor.objects.get(pk=current_doctor_id)
        except Doctor.DoesNotExist:
            # 处理医生不存在的情况
            return HttpResponseNotFound("Doctor not found")

        # 更新医生个人信息
        current_doctor.name = request.POST.get('name')
        current_doctor.gender = request.POST.get('gender')
        current_doctor.age = request.POST.get('age')
        current_doctor.department = request.POST.get('department')
        current_doctor.title = request.POST.get('title')
        current_doctor.info = request.POST.get('info')
        current_doctor.contact_number = request.POST.get('contact_number')
        current_doctor.save()

        # 重定向到医生个人信息页面或其他页面
        return redirect('doctor_profile')

    else:
        # 处理 GET 请求，获取当前登录医生的ID并从数据库中获取医生信息
        current_doctor_id = request.session.get('user_id')
        try:
            current_doctor = Doctor.objects.get(pk=current_doctor_id)
        except Doctor.DoesNotExist:
            # 处理医生不存在的情况
            return HttpResponseNotFound("Doctor not found")

        # 将医生信息传递给模板并渲染表单页面
        context = {'doctor': current_doctor}
        return render(request, 'user/doctor_edit_profile.html', context)

def patient_profile(request):
    # 获取当前登录的病人
    current_patient_id = request.session.get('user_id')
    current_patient = Patient.objects.get(pk=current_patient_id)

    context = {
        'patient': current_patient
    }

    return render(request, 'user/patient_profile.html', context)

def patient_edit_profile(request):
    if request.method == 'POST':
        # 处理表单提交逻辑
        current_patient_id = request.session.get('user_id')
        try:
            current_patient = Patient.objects.get(pk=current_patient_id)
        except Patient.DoesNotExist:
            # 处理病人不存在的情况
            return HttpResponseNotFound("Patient not found")

        # 更新病人个人信息
        current_patient.name = request.POST.get('name')
        current_patient.gender = request.POST.get('gender')
        current_patient.age = request.POST.get('age')
        current_patient.address = request.POST.get('address')
        current_patient.info = request.POST.get('info')
        current_patient.contact_number = request.POST.get('contact_number')
        current_patient.save()

        # 重定向到病人个人信息页面或其他页面
        return redirect('patient_profile')

    else:
        # 处理 GET 请求，获取当前登录病人的ID并从数据库中获取病人信息
        current_patient_id = request.session.get('user_id')
        try:
            current_patient = Patient.objects.get(pk=current_patient_id)
        except Patient.DoesNotExist:
            # 处理病人不存在的情况
            return HttpResponseNotFound("Patient not found")

        # 将病人信息传递给模板并渲染表单页面
        context = {'patient': current_patient}
        return render(request, 'user/patient_edit_profile.html', context)

def nurse_profile(request):
    # 获取当前登录的护士
    current_nurse_id = request.session.get('user_id')
    current_nurse = Nurse.objects.get(pk=current_nurse_id)

    context = {
        'nurse': current_nurse
    }

    return render(request, 'user/nurse_profile.html', context)

def nurse_edit_profile(request):
    if request.method == 'POST':
        # 处理表单提交逻辑
        current_nurse_id = request.session.get('user_id')
        try:
            current_nurse = Nurse.objects.get(pk=current_nurse_id)
        except Nurse.DoesNotExist:
            # 处理护士不存在的情况
            return HttpResponseNotFound("Nurse not found")

        # 更新护士个人信息
        current_nurse.name = request.POST.get('name')
        current_nurse.gender = request.POST.get('gender')
        current_nurse.age = request.POST.get('age')
        current_nurse.department = request.POST.get('department')
        current_nurse.title = request.POST.get('title')
        current_nurse.info = request.POST.get('info')
        current_nurse.contact_number = request.POST.get('contact_number')
        current_nurse.save()

        # 重定向到护士个人信息页面或其他页面
        return redirect('nurse_profile')

    else:
        # 处理 GET 请求，获取当前登录护士的ID并从数据库中获取护士信息
        current_nurse_id = request.session.get('user_id')
        try:
            current_nurse = Nurse.objects.get(pk=current_nurse_id)
        except Nurse.DoesNotExist:
            # 处理护士不存在的情况
            return HttpResponseNotFound("Nurse not found")

        # 将护士信息传递给模板并渲染表单页面
        context = {'nurse': current_nurse}
        return render(request, 'user/nurse_edit_profile.html', context)


def patient_doctor_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'user/patient_doctor_list.html', context)


def doctor_detail(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        # 处理医生不存在的情况
        return HttpResponseNotFound("Doctor not found")

    context = {'doctor': doctor}
    return render(request, 'user/doctor_detail.html', context)