from rest_framework import serializers
from .models import (
    RiskField,
    RiskType,
    FieldType,
    FieldTypeOption,
    RiskFieldValue,
    Risk,
)


class FieldChoiceSerializer(serializers.Serializer):

    '''
    FieldChoiceSerializer serializes
    our *static* form fields types.
    '''
    choices = serializers.ChoiceField(RiskField.choices)


class FieldTypeOptionSerializer(serializers.ModelSerializer):

    '''
    FieldTypeOptionSerializer serializes field options,
    enum allowed values
    '''

    class Meta:
        model = FieldTypeOption
        fields = ['id', 'title', 'field_type']
        extra_kwargs = {
            # field_type won't be created yet.
            # so, don't scream about this field now :)
            'field_type': {'required': False}
        }


class FieldTypeSerializer(serializers.ModelSerializer):

    '''
    FieldTypeSerializer serializes FieldType
    as long as its FieldTypeOption,
    '''

    opts = FieldTypeOptionSerializer(many=True)

    def create(self, validated_data):
        opts = validated_data.pop('opts')
        field_type = FieldType.objects.create(**validated_data)
        for opt in opts:
            FieldTypeOption.objects.create(
                title=opt['title'],
                field_type=field_type,
            )
        return field_type

    class Meta:
        model = FieldType
        fields = ('id', 'title', 'widget', 'opts')


class RiskTypeSerializer(serializers.ModelSerializer):

    '''
    FieldTypeSerializer serializes RiskType,
    We don't need FieldTypeSerializer here, since
    we are not creating new FieldType, we use already
    created fields.
    '''

    opts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FieldType.objects.all(),
    )

    def create(self, validated_data):
        opts = validated_data.pop('opts')
        risk_type = RiskType.objects.create(**validated_data)
        risk_type.opts.add(*opts)
        return risk_type

    class Meta:
        model = RiskType
        fields = ('id', 'title', 'opts')


class ExtendedRiskTypeSerializer(RiskTypeSerializer):

    '''
    ExtendedRiskTypeSerializer serializes RiskType and
    *all* its FieldTypeOption values.
    '''

    opts = FieldTypeSerializer(many=True, read_only=True)


class RiskValueSerializer(serializers.ModelSerializer):

    '''
    RiskValueSerializer serializes RiskFieldValue.
    '''

    field = serializers.PrimaryKeyRelatedField(
        queryset=FieldType.objects.all(),
    )

    class Meta:
        model = RiskFieldValue
        fields = ('id', 'risk', 'field', 'value')
        extra_kwargs = {
            'risk': {'required': False}
        }


class RiskSerializer(serializers.ModelSerializer):

    '''
    RiskSerializer serializes Risk with its related
    RiskFieldValue custom values.
    '''

    values = RiskValueSerializer(many=True)
    risk_type = serializers.PrimaryKeyRelatedField(
        queryset=RiskType.objects.all(),
    )

    class Meta:
        model = Risk
        fields = ('id', 'title', 'risk_type', 'values')
