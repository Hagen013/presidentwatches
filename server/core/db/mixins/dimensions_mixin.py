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
        dims = [self.height, self.width, self.thickness]
        dims = [str(d) for d in dims if d > 0]
        for i in range(len(dims)):
            if dims[i].endswith('.0'):
                dims[i] = dims[i][:-2]
        if len(dims) == 0:
            return ''
        else:
            dims = ' x '.join(dims)
            dims = 'Габариты ' + dims
            return dims
        

    @property
    def weight(self):
        return '{weight} {measure}'.format(
            self._weight,
            self.measure
        )
    
    @property
    def volume(self):
        return self.height * self.width * self.thickness
