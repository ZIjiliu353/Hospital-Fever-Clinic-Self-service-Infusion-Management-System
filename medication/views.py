from django.shortcuts import render
from django.http import JsonResponse
from .models import Medication
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



@csrf_exempt
def medication_list(request):
    if request.method == 'GET':


        # 检查请求是否为 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("This is an AJAX request")
            medications = Medication.objects.all()
            return JsonResponse({'medications': list(medications.values())})
        else:
            print("This is not an AJAX request")
            medications = Medication.objects.all()
            return render(request, 'medication/medication_list.html', {'medications': medications})
    else:
        return JsonResponse({'message': '请求方法不支持'}, status=405)


@csrf_exempt
def add_medication_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        expiration_date = data.get('expiration_date')
        current_quantity = data.get('current_quantity')
        print("Received data:", data)  # 添加这行用于调试，打印接收到的数据

        # 检查是否已存在具有相同名称和到期日期的药物
        existing_medication = Medication.objects.filter(name=name, expiration_date=expiration_date).first()
        if existing_medication:
            return JsonResponse({'message': '具有相同名称和到期日期的药物已存在，拒绝添加'}, status=400)
        else:
            Medication.objects.create(name=name, expiration_date=expiration_date, current_quantity=current_quantity)
            return JsonResponse({'message': '药物添加成功'})
    else:
        return JsonResponse({'message': '请求方法不支持'}, status=405)


@csrf_exempt
def edit_medication(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        medication_id = data.get('id')  # 从编辑表单中获取药物的 ID
        print(medication_id)
        name = data.get('name')
        print(name)
        expiration_date = data.get('expiration_date')
        print(expiration_date)
        quantity = data.get('current_quantity')
        print(quantity)
        try:
            medication = Medication.objects.get(medication_id=medication_id)
            medication.name = name
            medication.expiration_date = expiration_date
            medication.current_quantity = quantity
            medication.save()
            return JsonResponse({'message': '药物更新成功'})
        except Medication.DoesNotExist:
            return JsonResponse({'message': '药物不存在'}, status=404)
    else:
        return JsonResponse({'message': '请求方法不支持'}, status=405)


@csrf_exempt
def delete_medication(request, medication_id):
    if request.method == 'DELETE':
        try:
            # 根据药物 ID 查询数据库中的药物记录
            medication = Medication.objects.get(medication_id=medication_id)
            print(medication_id)
            # 删除药物记录
            medication.delete()
            # 返回成功的响应
            return JsonResponse({'message': '药物删除成功'}, status=200)
        except Medication.DoesNotExist:
            # 如果药物不存在，返回错误的响应
            return JsonResponse({'error': '指定的药物不存在'}, status=404)
        except Exception as e:
            # 处理其他异常情况
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # 如果请求方法不是DELETE，返回405 Method Not Allowed
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
