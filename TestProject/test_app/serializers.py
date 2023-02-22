from rest_framework import serializers
from .models import Project, WTG
from django.db.models import Sum
from datetime import datetime


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer class for Project Model"""
    WTG_numbers = serializers.SerializerMethodField('get_wtg_numbers')
    total_kW = serializers.SerializerMethodField('get_total_kw')
    months_acquired = serializers.SerializerMethodField('get_months_acquired')

    @staticmethod
    def _get_associated_wtg(proj_obj):
        return WTG.objects.filter(project_id=proj_obj.id)

    def get_wtg_numbers(self, obj):
        associated_wtg = self._get_associated_wtg(obj)
        return ','.join([str(item.WTG_number) for item in associated_wtg])

    def get_total_kw(self, obj):
        associated_wtg = self._get_associated_wtg(obj)
        return associated_wtg.aggregate(Sum('kW'))['kW__sum']

    @staticmethod
    def get_months_acquired(obj):
        if obj.acquisition_date:
            now = datetime.now()
            return (now.year - obj.acquisition_date.year) * 12 + now.month - obj.acquisition_date.month
        return None

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_number', 'acquisition_date',
                  'number_3l_code', 'project_deal_type_id', 'project_group_id',
                  'project_status_id', 'company_id', 'WTG_numbers', 'total_kW',
                  'months_acquired']
        read_only_fields = []
