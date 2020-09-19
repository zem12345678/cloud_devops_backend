#coding=utf8
from utils.baseviews import BaseView
from sqlmng.serializers import *
from sqlmng.models import *
from workflow.models import Step
from workflow.serializers import StepSerializer
class StepViewSet(BaseView):
    '''
        工单审批流
    '''
    queryset = Step.objects.all()
    serializer_class = StepSerializer