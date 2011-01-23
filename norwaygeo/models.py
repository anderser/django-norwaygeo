#!/usr/bin/python
# -*- coding: utf8 -*-

from django.contrib.gis.db import models
from utils.slugify import unique_slugify

class FylkerNoAreasManager(models.GeoManager):
    def get_query_set(self):
        return super(FylkerNoAreasManager, self).get_query_set().filter(isfylke=True)


class Fylke(models.Model):
    
    """
    Model that holds geographic info on a fylke (county)
    A fylke has several kommuner
    """
    
    fylke_nr = models.IntegerField(unique=True)
    name = models.CharField(max_length=32)
    fylke_ssb_code = models.CharField(max_length=4, blank=True)
    geom = models.MultiPolygonField(srid=32633, blank=True, null=True)
    slug = models.SlugField(editable=True, blank=True)
    
    """Some fylker are actually regions/other areas, """
    isfylke = models.BooleanField(default=True,verbose_name=u"er fylke (dvs ikke annet område)")
    
    objects = FylkerNoAreasManager()
    objects_with_areas = models.GeoManager()
    
    
    class Meta:
        verbose_name_plural = 'fylker'
        ordering = ['fylke_nr',]

    def __unicode__(self):
        return unicode(self.name)
    
    def get_ssb_code(self):
        
        """
        Generates the standard SSB fylke code which is a two char string of digits
        with a leading zero for numbers lower than 10
        """
        
        if self.fylke_nr > 9:
            return "%i" % self.fylke_nr
        else:
            return "0%i" % self.fylke_nr
    
    def geom_type (self):
        
        return self.geom.geom_type
    
    def kml (self):
        
        """
        Returns KML of the geom field in this model. For use in i.e. Google maps. Converted to EPSG 4326
        """
        
        return self.geom.transform(4326, clone=True).kml
    
    def save(self, *args, **kwargs):
        self.komm_ssb_kode = self.get_ssb_code()
        unique_slugify(self, self.name, slug_field_name='slug')
        super(Fylke, self).save(*args, **kwargs) 

class Kommune(models.Model):
    
    """
    Model that holds geographic info on a kommune
    A kommune is part of a fylke.
    """
    
    komm_nr = models.IntegerField(unique=True)
    name = models.CharField(max_length=32)
    komm_ssb_code = models.CharField(max_length=4, blank=True)
    
    geom = models.MultiPolygonField(srid=32633, blank=True)
    
    fylke = models.ForeignKey(Fylke, blank=True, null=True)
    slug = models.SlugField(editable=True, blank=True)
    
    objects = models.GeoManager()
    
    
    class Meta:
        verbose_name_plural = 'kommuner'
        ordering = ['komm_nr',]

    def __unicode__(self):
        
        """
        Some Norwegian kommuner have similar names. When displaying these
        using __unicode__ fylke is added to the tekst returned for kommuner
        that has similar names to other kommuner
        """
        
        duplicates = [u'Os', u'Nes', u'Sande', u'Herøy', u'Våler', u'Bø']
        if self.name in duplicates:
            return self.name + u" (" + unicode(self.fylke) + u")"
        else:
            return self.name
    
    def save(self, *args, **kwargs):
        self.komm_ssb_code = self.get_ssb_code()
        unique_slugify(self, self.name, slug_field_name='slug')
        super(Kommune, self).save(*args, **kwargs) 
        
    def get_ssb_code(self):
        
        """
        Generates the standard SSB kommune code which is a four char string of digits
        with a leading zero for numbers lower than 1000
        """
        
        if self.komm_nr > 999:
            return "%i" % self.komm_nr
        else:
            return "0%i" % self.komm_nr
    
    def get_fylke_from_komm_nr(self):
        
        if self.komm_nr > 99:
            return self.komm_nr // 100
        else:
            return self.komm_nr // 10
    
    def kml (self):
        
        """
        Returns KML of the geom field in this model. For use in i.e. Google maps. Converted to EPSG 4326
        """
        
        return self.geom.transform(4326, clone=True).kml
    
    def adjacent_kommuner(self):
        
        """
        Returns kommuner that has polygon which touches this kommune's polygon
        """
        
        return Kommune.objects.filter(geom__touches=self.geom)

        
# Auto-generated `LayerMapping` dictionary for Kommune model
kommune_mapping = {
                   
    'id': 'KOMM',
    'name' : 'NAVN',
    'komm_nr' : 'KOMM',
    'geom' : 'MULTIPOLYGON',
}
