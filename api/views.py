import datetime
import json
import os
import pickle
import shutil

import Orange
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from patient.models import Device
from device.models import Rawdata, TouchStatus, Acceleration, Gyroscope, Rotation, Unit
from device.serializers import RawdataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.staticfiles.storage import staticfiles_storage

from fallingdetection.settings import STATIC_ROOT


# Create your views here.

class FollowUpView(View):
    def get(self, request):
        return render(request, 'patient_follow-up.html')

@csrf_exempt
@api_view(['POST'])
def ResponesData(request):
    data = request.data
    try:
        device = Device.objects.get(uuid=data['UUID'])
    except Device.DoesNotExist:
        device = Device.objects.create(uuid=data['UUID'], description='unknown device')

    try:
        touch = TouchStatus.objects.get(status_name=data['Touch'])
    except TouchStatus.NotExists:
        touch = TouchStatus.objects.create(status_name=data['Touch'], description='unknown device')

    acceleration = data['data'][0]
    gyroscope = data['data'][1]
    rotation = data['data'][2]

    acceleration_sensor = Acceleration.objects.create(
        valueX=acceleration['valueX'],
        valueY=acceleration['valueY'],
        valueZ=acceleration['valueZ'],
        unit=Unit.objects.get(pk=1)
    )
    gyroscope_sensor = Gyroscope.objects.create(
        valueX=gyroscope['valueX'],
        valueY=gyroscope['valueY'],
        valueZ=gyroscope['valueZ'],
        unit=Unit.objects.get(pk=2)
    )
    rotation_sensor = Rotation.objects.create(
        rotationX=rotation['rotationX'],
        rotationY=rotation['rotationY'],
        rotationZ=rotation['rotationZ'],
        unit=Unit.objects.get(pk=3)
    )

    #create new rawdata

    date = datetime.datetime.now()

    rawdata = Rawdata.objects.create(
        date=date,
        device=device,
        touch_status=touch,
        acceleration=acceleration_sensor,
        gyroscope=gyroscope_sensor,
        rotation=rotation_sensor
    )

    serializer = RawdataSerializer(rawdata)
    data =JSONRenderer().render(serializer.data)

    modlue = pickle.load(open(os.path.join(STATIC_ROOT, 'modules/walking_aid.pkcls'), 'rb'))

    shutil.copy(os.path.join(STATIC_ROOT, 'modules/template.tab'), os.path.join(STATIC_ROOT, 'modules/temp.tab'))
    with open(os.path.join(STATIC_ROOT, 'modules/temp.tab'), "a") as myfile:
        myfile.write("\t2\t3\t4\t5\t6\t7")

    pre = Orange.data.Table(os.path.join(STATIC_ROOT, 'modules/temp.tab'))

    os.remove(os.path.join(STATIC_ROOT, 'modules/temp.tab'))

    print(modlue(pre))

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'sensor_consumer_group', {
            'type': 'send_rawdata',
            'value': json.loads(data),
        }
    )


    # connection.open()
    # send_mail(
    #     'Reply mess!!',
    #     json_string,
    #     settings.EMAIL_HOST_USER,
    #     ['ntdang_20th@student.agu.edu.vn', 'eliane.schroeter@gmail.com'],
    #     connection=connection,
    # )
    # connection.close()
    return Response(json.loads(data))

