from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework import generics as g
from rest_framework import viewsets
from rest_framework.views import APIView


from .models import (
    RiskField,
    RiskType,
    FieldType,
    Risk,
)

from .serializers import (
    FieldChoiceSerializer,
    RiskTypeSerializer,
    FieldTypeSerializer,
    RiskSerializer,
    ExtendedRiskTypeSerializer,
)


class HomeView(TemplateView):

    '''
     HomeView displays the static template
     "templates/home.html"
     the main page
    '''
    template_name = 'home.html'


class RiskFieldView(APIView):

    '''
     RiskFieldView [GET] endpoint,
     Exposes the supported form input types for
     constructing Custom Risk options types.
    '''

    def get(self, request, format=None):
        serializer = FieldChoiceSerializer(RiskField)
        return Response(serializer.data)


class RiskTypeView(viewsets.ModelViewSet):

    '''
     RiskTypeView [GET,POST,DELETE] endpoints,
     Handles creating, retrieving, deleting of
     RiskType.
    '''

    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer


class SingleRiskTypeView(g.RetrieveAPIView):

    '''
     SingleRiskTypeView [GET] endpoint,
     Handles retrieving of RiskType using
     the ExtendedRiskTypeSerializer.
    '''

    queryset = RiskType.objects.all()
    serializer_class = ExtendedRiskTypeSerializer


class FieldTypeView(viewsets.ModelViewSet):

    '''
     FieldTypeView [GET,POST,DELETE] REST endpoints,
     Handles creating, retrieving and deleting of custom
     form inputs based on allowed Fieldtype.
    '''

    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer


class RiskView(viewsets.ModelViewSet):

    '''
     RiskView [GET] REST endpoint,
     Displays the form of adding new Risk,
     entry based on RiskType custom fields.
    '''

    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
1
