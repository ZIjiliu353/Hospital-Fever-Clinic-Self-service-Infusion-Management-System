from datetime import datetime, timedelta
from user.models import Doctor
from appointment.models import AppointmentBalance

def create_initial_balances():
    # 获取所有医生
    doctors = Doctor.objects.all()

    # 获取今天和未来两天的日期
    today = datetime.now().date()
    future_dates = [today + timedelta(days=i) for i in range(3)]

    # 删除过去日期的余额数据
    AppointmentBalance.objects.filter(date__lt=today).delete()

    # 指定时间段
    hours = list(range(10, 17))

    # 为每个医生在指定时间段内创建余额数据
    for doctor in doctors:
        for date in future_dates:
            for hour in hours:
                # 创建余额数据
                balance, created = AppointmentBalance.objects.get_or_create(
                    doctor=doctor,
                    date=date,
                    hour=hour,
                    defaults={'remaining_quota': 10}  # 默认每小时剩余名额为 10
                )

# 执行函数来创建初始余额数据
create_initial_balances()