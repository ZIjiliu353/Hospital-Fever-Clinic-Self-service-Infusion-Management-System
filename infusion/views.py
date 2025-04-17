from django.shortcuts import render
from django.http import JsonResponse
from .models import Infusion,InfusionSeat
from user.models import Patient,Doctor,Nurse
from appointment.models import Appointment
from medication.models import Medication
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def patient_infusion(request):
    return render(request, 'infusion/patient_infusion.html')


def get_patient_infusion(request):
    if request.method == 'GET':
        # 从数据库中获取符合条件的输液记录
        current_patient_id = request.session.get('user_id')
        # 从数据库中获取符合条件的输液记录，过滤预约ID对应的数据并且包含了病人ID的
        infusions = Infusion.objects.filter(appointment__patient_id=current_patient_id).order_by('-id')


        # 构建输液记录的列表
        infusion_data = []
        for infusion in infusions:
            infusion_id = infusion.id

            # 获取护士信息
            try:
                nurse_name = Nurse.objects.get(nurse_id=infusion.nurse_id).name
            except Nurse.DoesNotExist:
                nurse_name = None

            # 获取座位号信息，如果不存在则设为 None
            try:
                seat_number = infusion.seat_id
            except AttributeError:
                seat_number = None

            appointment_id = infusion.appointment_id
            # 获取预约对象
            appointment = Appointment.objects.get(id=appointment_id)
            doctor_name = Doctor.objects.get(doctor_id=appointment.doctor_id).name
            patient_name = Patient.objects.get(patient_id=appointment.patient_id).name
            appointment_date = appointment.date
            appointment_time = appointment.hour
            medication = appointment.medication.name
            dosage = appointment.dose
            check_in_status = '未报到' if not infusion.check_in_status else '已报到'
            sit_down_status = '未坐下' if not infusion.sit_down_status else '已坐下'
            infusion_status = infusion.infusion_status

            # 添加到输液记录列表
            infusion_data.append({
                'infusion_id': infusion_id,
                'doctor_name': doctor_name,
                'nurse_name': nurse_name,
                'patient_name': patient_name,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'seat_number': seat_number,
                'medication': medication,
                'dosage': dosage,
                'check_in_status': check_in_status,
                'sit_down_status': sit_down_status,
                'infusion_status': infusion_status
            })

        return JsonResponse({'infusions': infusion_data})
    else:
        # 如果不是 GET 请求，返回错误信息
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

@csrf_exempt
def updateCheckInStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        try:
            infusion = Infusion.objects.get(id=infusion_id)
            # check_in_status的字段用于表示报到状态，这里设置为True表示已报到
            infusion.check_in_status = True
            infusion.save()

            # 调用seat_assignment函数分配座位
            seat_number = seat_assignment()
            print("seat_number:",seat_number)
            if seat_number:
                infusion.seat_id = seat_number
                infusion.save()

            return JsonResponse({'status': 'success', 'message': 'Check-in status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
    else:
        # 对于非PATCH请求，返回405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)

def seat_assignment():
    # 查找第一个未占用的座位
    try:
        unoccupied_seat = InfusionSeat.objects.filter(is_occupied=False).order_by('seat_number').first()
        if unoccupied_seat:
            # 标记座位为已占用
            unoccupied_seat.is_occupied = True
            unoccupied_seat.save()
            # 返回座位号
            return unoccupied_seat.seat_number
    except InfusionSeat.DoesNotExist:
        pass  # 如果没有可用座位，则不执行任何操作
    return None  # 如果没有可用座位，则返回None

@csrf_exempt
def updateSitDownStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        try:
            infusion = Infusion.objects.get(id=infusion_id)
            # sit_down_status的字段用于表示坐下状态，这里设置为True表示已坐下
            infusion.sit_down_status = True
            infusion.save()

            return JsonResponse({'status': 'success', 'message': 'Sit-down status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
    else:
        # 对于非PATCH请求，返回405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)

@csrf_exempt
def patient_updateCancelStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        try:
            infusion = Infusion.objects.get(id=infusion_id)
            # 更新输液状态为已取消
            infusion.infusion_status = 'cancelled'
            infusion.save()

            if infusion.seat_id:
                seat = InfusionSeat.objects.get(seat_number=infusion.seat_id)
                seat.is_occupied = False
                seat.save()

            # 更新药物当前数量
            appointment = infusion.appointment
            medication = Medication.objects.get(medication_id=appointment.medication_id)
            medication.current_quantity += appointment.dose
            medication.save()

            return JsonResponse({'status': 'success', 'message': 'Cancel status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
        except InfusionSeat.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion seat associated with the provided ID does not exist'})
        except Medication.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Medication with the provided ID does not exist'})
    else:
        # For non-PATCH requests, return 405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)


def nurse_infusion(request):
    return render(request, 'infusion/nurse_infusion.html')

def get_nurse_infusion(request):
    if request.method == 'GET':
        # 从数据库中获取符合条件的输液记录
        current_nurse_id = request.session.get('user_id')
        # 从数据库中获取符合条件的输液记录，过滤护士ID对应的数据以及护士ID为空的数据,且病人坐下，输液状态不为已完成和已取消
        infusions = Infusion.objects.filter(
            Q(nurse_id=current_nurse_id) | Q(nurse_id__isnull=True),
            ~Q(infusion_status='completed'),
            ~Q(infusion_status='cancelled'),
            sit_down_status=True

        ).order_by('-id')

        # 构建输液记录的列表
        infusion_data = []
        for infusion in infusions:
            infusion_id = infusion.id

            # 获取护士信息
            try:
                nurse_name = Nurse.objects.get(nurse_id=infusion.nurse_id).name
            except Nurse.DoesNotExist:
                nurse_name = None

            # 获取座位号信息，如果不存在则设为 None
            try:
                seat_number = infusion.seat_id
            except AttributeError:
                seat_number = None

            appointment_id = infusion.appointment_id
            # 获取预约对象
            appointment = Appointment.objects.get(id=appointment_id)
            doctor_name = Doctor.objects.get(doctor_id=appointment.doctor_id).name
            patient_name = Patient.objects.get(patient_id=appointment.patient_id).name
            appointment_date = appointment.date
            appointment_time = appointment.hour
            medication = appointment.medication.name
            dosage = appointment.dose
            check_in_status = '未报到' if not infusion.check_in_status else '已报到'
            sit_down_status = '未坐下' if not infusion.sit_down_status else '已坐下'
            infusion_status = infusion.infusion_status

            # 添加到输液记录列表
            infusion_data.append({
                'infusion_id': infusion_id,
                'doctor_name': doctor_name,
                'nurse_name': nurse_name,
                'patient_name': patient_name,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'seat_number': seat_number,
                'medication': medication,
                'dosage': dosage,
                'check_in_status': check_in_status,
                'sit_down_status': sit_down_status,
                'infusion_status': infusion_status
            })

        return JsonResponse({'infusions': infusion_data})
    else:
        # 如果不是 GET 请求，返回错误信息
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

@csrf_exempt
def updateGetMedicationAndInfusionStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        current_nurse_id = request.session.get('user_id')

        try:
            infusion = Infusion.objects.get(id=infusion_id)

            # 检查是否已存在 nurse_id
            if infusion.nurse_id:
                return JsonResponse({'status': 'error', 'message': '该数据已被其他护士处理'})

            # 更新输液状态为 "infusing"
            infusion.nurse_id = current_nurse_id
            infusion.infusion_status = "infusing"
            infusion.save()

            return JsonResponse({'status': 'success', 'message': 'Get medication and infusion status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
    else:
        # 对于非PATCH请求，返回405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)

@csrf_exempt
def updateCompleteStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        try:
            infusion = Infusion.objects.get(id=infusion_id)
            # 更新输液状态为待拔针
            infusion.infusion_status = 'waiting_for_removal'
            infusion.save()

            return JsonResponse({'status': 'success', 'message': 'Infusion completion status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
    else:
        # 对于非PATCH请求，返回405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)

@csrf_exempt
def updateRemoveNeedleStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        try:
            infusion = Infusion.objects.get(id=infusion_id)
            # 更新输液状态为已完成
            infusion.infusion_status = 'completed'
            infusion.save()


            if infusion.seat_id:
                seat = InfusionSeat.objects.get(seat_number=infusion.seat_id)
                seat.is_occupied = False
                seat.save()

            return JsonResponse({'status': 'success', 'message': 'Remove needle status updated successfully'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion with the provided ID does not exist'})
        except InfusionSeat.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Infusion seat associated with the provided ID does not exist'})
    else:
        # For non-PATCH requests, return 405 Method Not Allowed
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)

def nurse_infusion_history(request):
    return render(request, 'infusion/nurse_infusion_history.html')


def get_nurse_infusion_history(request):
    if request.method == 'GET':
        # 从 session 中获取当前护士的 ID
        current_nurse_id = request.session.get('user_id')

        # 从数据库中获取符合条件的输液记录
        infusions = Infusion.objects.filter(
            nurse_id=current_nurse_id
        ).order_by('-id')

        # 构建输液记录的列表
        infusion_data = []
        for infusion in infusions:
            infusion_id = infusion.id

            # 获取护士信息
            nurse_name = infusion.nurse.name if infusion.nurse else None

            # 获取座位号信息
            seat_number = infusion.seat_id

            appointment_id = infusion.appointment_id
            # 获取预约对象
            appointment = Appointment.objects.get(id=appointment_id)
            doctor_name = appointment.doctor.name
            patient_name = appointment.patient.name
            appointment_date = appointment.date
            appointment_time = appointment.hour
            medication = appointment.medication.name
            dosage = appointment.dose
            check_in_status = '未报到' if not infusion.check_in_status else '已报到'
            sit_down_status = '未坐下' if not infusion.sit_down_status else '已坐下'
            infusion_status = infusion.infusion_status

            # 添加到输液记录列表
            infusion_data.append({
                'infusion_id': infusion_id,
                'doctor_name': doctor_name,
                'nurse_name': nurse_name,
                'patient_name': patient_name,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'seat_number': seat_number,
                'medication': medication,
                'dosage': dosage,
                'check_in_status': check_in_status,
                'sit_down_status': sit_down_status,
                'infusion_status': infusion_status
            })

        return JsonResponse({'infusions': infusion_data})
    else:
        # 如果不是 GET 请求，返回错误信息
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)


@csrf_exempt
def updateCancelStatus(request, infusion_id):
    if request.method == 'PATCH':  # 只处理PATCH请求
        # 从 session 中获取当前护士的 ID
        current_nurse_id = request.session.get('user_id')
        try:
            infusion = Infusion.objects.get(id=infusion_id)

            # 检查是否已存在 nurse_id
            if infusion.nurse_id:
                return JsonResponse({'status': 'error', 'message': '该数据已被其他护士处理'})

            # 更新输液状态为已取消
            infusion.infusion_status = 'cancelled'
            infusion.nurse_id = current_nurse_id  # 更新护士ID
            infusion.save()

            if infusion.seat_id:
                seat = InfusionSeat.objects.get(seat_number=infusion.seat_id)
                seat.is_occupied = False
                seat.save()

            # 更新药物当前数量
            appointment = infusion.appointment
            medication = Medication.objects.get(medication_id=appointment.medication_id)
            medication.current_quantity += appointment.dose
            medication.save()

            return JsonResponse({'status': 'success', 'message': '取消状态更新成功'})
        except Infusion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '输液数据不存在'})
        except InfusionSeat.DoesNotExist:
            return JsonResponse(
                {'status': 'error', 'message': '输液座位不存在'})
        except Medication.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '药物不存在'})
    else:
        # 对于非 PATCH 请求，返回 405
        return JsonResponse({'status': 'error', 'message': '方法不允许'}, status=405)