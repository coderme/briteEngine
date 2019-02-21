from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from britecore.risksman.models import (
    RiskField,
    RiskType,
    FieldType,


)

from britecore.risksman.serializers import (
    FieldChoiceSerializer,
    RiskTypeSerializer,
)


class RiskFieldViewTest(TestCase):

    def test_get_fields_types(self):
        client = APIClient()

        response = client.get(
            reverse(
                'fields-types',
            ),
        )

        serialized = FieldChoiceSerializer(
            RiskField,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            serialized.data,
            response.data,
        )


class RiskTypeViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        opts = []
        opts.append(
            FieldType.objects.create(
                title='firstname',
                widget='text',
            ),
        )
        opts.append(
            FieldType.objects.create(
                title='lastname',
                    widget='text',
            ),
        )
        risk_type = RiskType.objects.create(
            title='Exam',
        )
        risk_type.opts.add(*opts)
        risk_type.save()

    def test_get_risk_types(self):
        response = self.client.get(
            reverse(
                'risktype-list',
            ),
        )
        risk_types = RiskType.objects.all()
        serialized = RiskTypeSerializer(risk_types, many=True)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            serialized.data,
            response.data,
        )
