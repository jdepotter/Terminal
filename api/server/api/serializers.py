from rest_framework import serializers 
from api.models import Item, Line, Schedule


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'status')


class LineSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Line
        fields = ('name', 'items')


class ScheduleSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ('date', 'shift', 'terminal', 'timestamp', 'lines')
