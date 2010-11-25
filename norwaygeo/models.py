from django.contrib.gis.db import models

class Kommune(models.Model):
    
    """
    Model that holds geographic info on a kommune
    """
    
    objectid = models.IntegerField()
    subtypekod = models.IntegerField()
    objtype = models.CharField(max_length=32)
    ftema = models.IntegerField()
    operator = models.CharField(max_length=6)
    navn = models.CharField(max_length=32)
    komm = models.IntegerField()
    oppdaterin = models.CharField(max_length=10)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=32633)
    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'kommuner'
        ordering = ['komm',]

    def __unicode__(self):
        return unicode(self.navn)
    
    def kml (self):
        """ Returns KML of the geom field in this model. For use in i.e. Google maps"""
        return self.geom.transform(4326, clone=True).kml


# Auto-generated `LayerMapping` dictionary for Kommune model
kommune_mapping = {
    'objectid' : 'OBJECTID',
    'subtypekod' : 'SUBTYPEKOD',
    'objtype' : 'OBJTYPE',
    'ftema' : 'FTEMA',
    'operator' : 'OPERATOR',
    'navn' : 'NAVN',
    'komm' : 'KOMM',
    'oppdaterin' : 'OPPDATERIN',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'MULTIPOLYGON',
}
