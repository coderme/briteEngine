from django.test import TestCase
from britecore.risksman.models import (
    FieldType,
    RiskType,
    FieldTypeOption,
    Risk,
    RiskFieldValue,
)


class FieldTypeModelTest(TestCase):

    '''
     FieldTypeModelTest tests for FieldType

    '''

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


class RiskFieldValueModelTest(TestCase):
    value = '1853'

    @classmethod
    def setUpTestData(cls):

        field_type = FieldType.objects.create(
            title='model',
                widget='number',
        )

        risk_type = RiskType.objects.create(
            title='automobile',
        )

        risk_type.opts.add(field_type)
        risk_type.save()

        risk = Risk.objects.create(
            title='old cars',
            risk_type=risk_type,
        )

        RiskFieldValue.objects.create(
            value=RiskFieldValueModelTest.value,
            risk=risk,
            field=field_type,
        )

    def test_value_label(self):
        risk_field_value = RiskFieldValue.objects.get(pk=1)
        field_label = risk_field_value._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'value')

    def test_method__str__(self):
        risk_field_value = RiskFieldValue.objects.get(pk=1)
        self.assertEquals(
            RiskFieldValueModelTest.value,
            str(risk_field_value),
        )

    def test_method__repr__(self):
        risk_field_value = RiskFieldValue.objects.get(pk=1)
        self.assertEquals(
            '%s: %s'.format(
                risk_field_value.field.title,
                RiskFieldValueModelTest.value,
            ),
            repr(risk_field_value),
        )


class RiskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        std = []
        std.append(
            FieldType.objects.create(
                title='firstname',
                widget='text',
            ),
        )
        std.append(
            FieldType.objects.create(
                title='lastname',
                widget='text',
            ),
        )

        risk_type = RiskType.objects.create(
            title='exam',
        )

        risk_type.opts.add(*std)
        risk_type.save()

        risk = Risk.objects.create(
            title='maths low marks',
            risk_type=risk_type,
        )

    def test_title_label(self):
        risk = Risk.objects.get(pk=1)
        field_label = risk._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        risk = Risk.objects.get(pk=1)
        field_max_length = risk._meta.get_field(
            'title').max_length
        self.assertEquals(field_max_length, 50)

    def test_insurer_label(self):
        risk = Risk.objects.get(pk=1)
        field_label = risk._meta.get_field('insurer').verbose_name
        self.assertEquals(field_label, 'insurer')

    def test_insurer_max_length(self):
        risk = Risk.objects.get(pk=1)
        field_max_length = risk._meta.get_field(
            'insurer').max_length
        self.assertEquals(field_max_length, 50)
