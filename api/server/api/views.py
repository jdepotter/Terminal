from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from api.models import Schedule
from api.serializers import ScheduleSerializer
from rest_framework.decorators import api_view
from datetime import datetime
import calendar
import json

from django.core import serializers 


@api_view(['GET'])
def schedule_list(request):
    if request.method == 'GET':
        schedules = Schedule.objects.all()

        schedule_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedule_serializer.data, safe=False)


@api_view(['GET'])
def y_schedule_list(request, year):
    if request.method == 'GET':
        schedules = Schedule.objects.filter(date__year = year)

        schedule_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedule_serializer.data, safe=False)


@api_view(['GET'])
def y_m_schedule_list(request, year, month):
    if request.method == 'GET':
        iyear = int(year)
        imonth = int(month)
        start = datetime(iyear, imonth, 1)
        days_in_month = calendar.monthrange(iyear, imonth)[1]
        end = datetime(iyear, imonth, days_in_month)

        schedules = Schedule.objects.mongo_find({'date': {'$gte': start, '$lt': end }})

        schedule_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedule_serializer.data, safe=False)


@api_view(['GET'])
def y_m_d_schedule_list(request, year, month, day):
    if request.method == 'GET':
        iyear = int(year)
        imonth = int(month)
        iday = int(day)
        start = datetime(iyear, imonth, iday)
        days_in_month = calendar.monthrange(iyear, imonth)[1]
        end = datetime(iyear, imonth, iday+1)

        schedules = Schedule.objects.mongo_find({'date': {'$gte': start, '$lt': end }})

        schedule_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedule_serializer.data, safe=False)