from django.db import models


class RiskField:

    '''
    RiskField wraps the allowed form fields types.
    '''
    choices = [
        ('date', 'Date'),
        ('number', 'Number'),
        ('text', 'Text'),
        ('enum', 'Predefined Choices'),
    ]


class Title(models.Model):

    '''
    Title is an abstract Model class
    to define a common 'title' field which is used by other
    models
    '''
    title = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        abstract = True


class RiskType(Title):

    '''
    RiskType defines the main structure of the 'Risk' entry
    which it is a Title and possibliy a many generic fields.
    models
    '''
    opts = models.ManyToManyField('FieldType')


class FieldType(Title):

    '''
    FieldType defines the individual Field type,
    which is a Title and a widget.
    '''
    widget = models.CharField(
        max_length=10,
        choices=RiskField.choices,
    )

    class Meta:
        ordering = ('id', 'title')


class FieldTypeOption(Title):

    '''
    FieldTypeOption defines a single value of 'enum'
    possible values, it has no use for other field types.
    '''

    field_type = models.ForeignKey(
        'FieldType', related_name='opts', on_delete=models.CASCADE)


class Risk(Title):

    '''
    Risk is Our final data model destination,
    It connects custom data fields to isurer
    '''

    insurer = models.CharField(max_length=50)
    risk_type = models.ForeignKey('RiskType', on_delete=models.CASCADE)


class RiskFieldValue(models.Model):

    '''
    RiskFieldValue represents a single value for
    a custom field of Risk model.
    '''

    risk = models.ForeignKey(
        'Risk',
        related_name='values',
        on_delete=models.CASCADE,
    )
    field = models.ForeignKey('FieldType', on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return self.value

    def __repr__(self):
        return '%s: %s'.format(
            self.field.title,
            self.value,
        )
