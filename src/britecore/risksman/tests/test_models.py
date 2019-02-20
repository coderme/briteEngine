from django.test import TestCase
from britecore.risksman.models import (
    FieldType,
    RiskType,
    FieldTypeOption,
    Risk,
    RiskFieldValue,
)


class FieldTypeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        FieldType.objects.create(title='first name', widget='text')

    def test_title_label(self):
        field_type = FieldType.objects.get(pk=1)
        field_label = field_type._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        field_type = FieldType.objects.get(pk=1)
        field_max_length = field_type._meta.get_field('title').max_length
        self.assertEquals(field_max_length, 50)

    def test_widget_label(self):
        field_type = FieldType.objects.get(pk=1)
        field_label = field_type._meta.get_field('widget').verbose_name
        self.assertEquals(field_label, 'widget')

    def test_widget_max_length(self):
        field_type = FieldType.objects.get(pk=1)
        field_max_length = field_type._meta.get_field('widget').max_length
        self.assertEquals(field_max_length, 10)


class FieldTypeOptionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        field_type = FieldType.objects.create(
            title='fruit',
            widget='enum',
        )

        FieldTypeOption.objects.create(
            title='apple',
            field_type=field_type,
        )

    def test_title_label(self):
        field_type_option = FieldTypeOption.objects.get(pk=1)
        field_label = field_type_option._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        field_type_option = FieldTypeOption.objects.get(pk=1)
        field_max_length = field_type_option._meta.get_field(
            'title').max_length
        self.assertEquals(field_max_length, 50)

    def test_field_type_foreignkey(self):
        field_type = FieldType.objects.get(pk=1)
        field_type_option = FieldTypeOption.objects.get(pk=1)
        self.assertEquals(field_type, field_type_option.field_type)


class RiskTypeOptionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        field_types = []
        field_types.append(
            FieldType.objects.create(
                title='model',
                widget='enum',
            ),
        )

        field_types.append(
            FieldType.objects.create(
                title='made',
                widget='number',
            ),
        )

        field_types.append(
            FieldType.objects.create(
                title='type',
                widget='text',
            ),
        )

        risk_type = RiskType.objects.create(
            title='apple',
        )
        risk_type.opts.add(*field_types)
        risk_type.save()

    def test_title_label(self):
        risk_type = RiskType.objects.get(pk=1)
        field_label = risk_type._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        risk_type = RiskType.objects.get(pk=1)
        field_max_length = risk_type._meta.get_field(
            'title').max_length
        self.assertEquals(field_max_length, 50)

    def test_opts_many2many(self):
        risk_type = RiskType.objects.get(pk=1)
        field_types = FieldType.objects.all()

        for field in field_types:
            self.assertTrue(field in risk_type.opts.all())
