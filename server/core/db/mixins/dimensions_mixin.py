from django.db import models


class DimensionsMixin(models.Model):
    """
    Миксин для работы с объектами, имеющими габариты в мм.:
        - длину
        - ширину
        - толщину
    а также вес
    """

    class Meta:
        abstract = True

    dimensions_measure = 'мм'
    weight_measure = 'гр'

    height = models.FloatField(
        default=0,
    )

    width = models.FloatField(
        default=0
    )

    thickness = models.FloatField(
        default=0
    )

    _weight = models.FloatField(
        default=0
    )

    @property
    def dimensions(self):
        dims = [('Д', fields.get('height')), ('Ш', fields.get('width')), ('Ш', fields.get('thickness'))]
        dims = [d for d in dims if d[1]>0]
        dims_labels = [d[0] for d in dims]
        dims_values = [d[1] for d in dims]
        title = 'Габариты {dimensions}'.format(
            dimensions='x'.join(dims_labels)
        )
        value = '{value} {measure}'.format(
            value=' x '.join(dims_values),
            measure=self.dimensions_measure
        )
        return {
            'title': title,
            'value': value
        }
        

    @property
    def weight(self):
        return '{weight} {measure}'.format(
            self._weight,
            self.measure
        )
    
    @property
    def volume(self):
        return self.height * self.width * self.thickness
