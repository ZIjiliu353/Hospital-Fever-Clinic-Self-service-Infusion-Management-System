from django.shortcuts import render
from user.models import Patient,Doctor
from .models import AppointmentBalance,Appointment
from medication.models import Medication
from infusion.models import Infusion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def make_patient_appointment(request):
    # 获取存储在 session 中的当前用户的 ID
    current_patient_id = request.session.get('user_id')
    # 根据用户 ID 获取用户的其他信息，例如用户名
    current_patient = None
    if current_patient_id:
        current_patient = Patient.objects.filter(patient_id=current_patient_id).first()

    # 获取病人姓名，如果当前用户不存在则为 "Unknown"
    patient_name = current_patient.name if current_patient else "Unknown"

    return render(request, 'appointment/patient_appointment.html', {'patientName': patient_name})

def get_doctors(request):
    doctors = Doctor.objects.all()
    doctor_list = [
        {
            'doctor_id': doctor.doctor_id,
            'name': doctor.name,
        }
        for doctor in doctors
    ]
    return JsonResponse(doctor_list, safe=False)

def get_doctor_balance(request):
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')

        appointment_date = request.GET.get('date')

        appointment_hour = request.GET.get('hour')

        try:
            balance = AppointmentBalance.objects.get(doctor_id=doctor_id, date=appointment_date, hour=appointment_hour).remaining_quota
            return JsonResponse({'balance': balance})
        except AppointmentBalance.DoesNotExist:
            return JsonResponse({'error': '无法获取医生余额'}, status=404)


@csrf_exempt
def submit_appointment(request):
    if request.method == 'POST':
        try:
            # 解析JSON格式的请求体数据
            data = json.loads(request.body)

            # 从请求数据中获取相应的字段
            patient_name = data.get('patientName')
            doctor_id = data.get('doctor')
            appointment_date = data.get('appointmentDate')
            appointment_hour = data.get('appointmentHour')
            reason = data.get('reason')

            #获取当前病人id
            current_patient_id = request.session.get('user_id')
            print("当前病人ID:",current_patient_id)

            # 创建一个新的预约实例并保存
            appointment = Appointment.objects.create(
                patient_id=current_patient_id,
                doctor_id=doctor_id,
                date=appointment_date,
                hour=appointment_hour,
                reason=reason
            )

            # 更新医生的预约余额
            try:
                # 找到医生的预约余额记录
                balance = AppointmentBalance.objects.get(doctor_id=doctor_id, date=appointment_date, hour=appointment_hour)
                # 减去一个预约名额
                balance.remaining_quota -= 1
                # 保存更新后的记录
                balance.save()
            except AppointmentBalance.DoesNotExist:
                # 如果没有找到医生的预约余额记录，可以抛出异常或者记录日志
                print("医生的预约余额记录不存在！")

            # 返回JSON响应，表示收到信息
            return JsonResponse({'message': '收到预约信息！'})
        except json.JSONDecodeError as e:
            # 如果解析失败，返回错误响应
            return JsonResponse({'error': 'JSON数据解析失败：' + str(e)}, status=400)

    # 如果不是POST请求，返回错误响应
    return JsonResponse({'error': '只接受POST请求！'}, status=400)

def view_appointment_history(request):
    return render(request, 'appointment/view_appointment_history.html')


def get_appointment_data(request):
    if request.method == 'GET':
        print("Received GET request")  # 添加调试语句，输出收到 GET 请求

        # 获取当前病人的 ID
        current_patient_id = request.session.get('user_id')
        print("Current patient ID:", current_patient_id)  # 添加调试语句，输出当前病人的 ID

        try:
            # 根据当前病人的 id 获取预约记录
            appointments = Appointment.objects.filter(patient_id=current_patient_id).order_by('-id')

            # 逐个替换病人 ID 和医生 ID 为姓名
            appointments_json = []
            for appointment in appointments:
                patient_name = Patient.objects.get(patient_id=appointment.patient_id).name
                doctor_name = Doctor.objects.get(doctor_id=appointment.doctor_id).name
                appointment_data = {
                    'patient_name': patient_name,
                    'doctor_name': doctor_name,
                    'appointment_date': appointment.date,
                    'appointment_time': appointment.hour,
                    'infusion_reason': appointment.reason,
                    'medication': appointment.medication.name if appointment.medication else None,
                    'dosage': appointment.dose,
                    'status': appointment.status,
                }
                print("Appointment data:", appointment_data)  # 添加调试语句，输出每条预约记录的数据
                appointments_json.append(appointment_data)

            # 返回 JSON 响应
            return JsonResponse({'appointments': appointments_json})

        except Appointment.DoesNotExist:
            # 如果找不到预约记录，返回空的 JSON 响应
            return JsonResponse({'appointments': []})

    else:
        return JsonResponse({'message': 'Unsupported request method'}, status=405)

def appointment_handling(request):
    return render(request, 'appointment/appointment_handling.html')

def doctor_get_appointment_data(request):
    if request.method == 'GET':
        print("Received GET request")  # 添加调试语句，输出收到 GET 请求

        # 获取当前医生的 ID
        current_doctor_id = request.session.get('user_id')
        print("Current doctor ID:", current_doctor_id)  # 添加调试语句，输出当前医生的 ID

        try:
            # 根据当前医生的 id 获取预约记录
            appointments = Appointment.objects.filter(doctor_id=current_doctor_id).order_by('-id')


            # 逐个替换病人 ID 和医生 ID 为姓名
            appointments_json = []
            for appointment in appointments:
                patient_name = Patient.objects.get(patient_id=appointment.patient_id).name
                doctor_name = Doctor.objects.get(doctor_id=appointment.doctor_id).name
                appointment_data = {
                    'patient_name': patient_name,
                    'doctor_name': doctor_name,
                    'patient_id': appointment.patient_id,
                    'appointment_id': appointment.id,
                    'appointment_date': appointment.date,
                    'appointment_time': appointment.hour,
                    'infusion_reason': appointment.reason,
                    'medication': appointment.medication.name if appointment.medication else None,
                    'dosage': appointment.dose,
                    'status': appointment.status,
                }
                print("Appointment data:", appointment_data)  # 添加调试语句，输出每条预约记录的数据
                appointments_json.append(appointment_data)

            # 返回 JSON 响应
            return JsonResponse({'appointments': appointments_json})

        except Appointment.DoesNotExist:
            # 如果找不到预约记录，返回空的 JSON 响应
            return JsonResponse({'appointments': []})

    else:
        return JsonResponse({'message': 'Unsupported request method'}, status=405)


def get_medications(request):
    if request.method == 'GET':
        # 获取数据库中的所有药物数据
        medications = Medication.objects.all()

        # 将药物数据转换为字典列表
        medications_list = [{'id': med.medication_id, 'name': med.name, 'expiration_date': med.expiration_date, 'current_quantity': med.current_quantity} for med in medications]

        # 打印药物数据
        print("Medications:", medications_list)

        # 返回 JSON 响应
        return JsonResponse({'medications': medications_list})
    else:
        # 如果不是 GET 请求，返回错误信息
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)

@csrf_exempt
def doctor_deal_with_appointment(request):
    if request.method == 'POST':
        # 解析JSON格式的请求体数据
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        medication_id = data.get('medication_id')
        dosage = data.get('dosage')

        print('Received appointment ID:', appointment_id)
        print('Received medication ID:', medication_id)
        print('Received dosage:', dosage)


        # 尝试获取并更新Appointment实例
        try:
            appointment = Appointment.objects.get(id=appointment_id)

            # 检查medication_id和dose是否已设置
            if appointment.medication_id and appointment.dose:
                # 如果已设置，先加上之前的剂量到medication的current_quantity
                medication = Medication.objects.get(medication_id=appointment.medication_id)
                medication.current_quantity += appointment.dose
                medication.save()
                print('Previous medication quantity adjusted.')

            # 更新appointment的medication_id和dose
            appointment.medication_id = medication_id
            appointment.dose = dosage
            appointment.status = 'completed'
            appointment.save()
            print('Appointment updated successfully.')

        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Appointment with given ID does not exist.'}, status=404)

        # 尝试获取Medication实例
        try:
            medication = Medication.objects.get(medication_id=medication_id)
            # 减去dosage数量
            medication.current_quantity -= dosage
            # 保存更改
            medication.save()
            print('Medication quantity updated successfully.')
        except Medication.DoesNotExist:
            return JsonResponse({'error': 'Medication with given ID does not exist.'}, status=404)

        # 尝试获取符合条件的输液记录，如果不存在，则创建新记录
        infusion_record, created = Infusion.objects.get_or_create(appointment_id=appointment_id)
        if created:
            print('New infusion record created with appointment ID:', appointment_id)
        else:
            print('Infusion record already exists with appointment ID:', appointment_id)


        return JsonResponse({'message': 'Appointment handled successfully.'})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

def patient_detail(request):
    patient_id = request.GET.get('patient_id')  # 从GET请求中获取patient_id
    if patient_id:
        try:
            # 使用patient_id从数据库获取Patient对象
            patient = Patient.objects.get(pk=patient_id)
            # 准备传递给模板的上下文
            context = {
                'patient': patient
            }
            # 渲染patient_profile.html模板并返回响应
            return render(request, 'appointment/patient_detail.html', context)
        except Patient.DoesNotExist:
            # 处理Patient对象不存在的情况
            return render(request, 'appointment/patient_detail.html', {'error': 'Patient does not exist'})
    else:
        # 处理没有提供patient_id的情况
        return render(request, 'appointment/patient_detail.html', {'error': 'No patient_id provided'})
