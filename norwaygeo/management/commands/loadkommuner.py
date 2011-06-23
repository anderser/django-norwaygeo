# -*- coding: utf-8 -*-

import os
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, GEOSGeometry
from django.core.management.base import BaseCommand
from norwaygeo.models import Kommune, kommune_mapping, Fylke


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        """
        Loads kommuner from the shapefile with the mapping of fields
        specified in the model.
        """
        
        print "Deleting kommuner"
        Kommune.objects.all().delete()
        
        print "Loading kommuner shape data"
        kommune_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                   '../../data/statens-kartverk-n5000/administrativ-flate-uten-hav-AGE.shp'))

        komm = LayerMapping(Kommune, kommune_shp, kommune_mapping,
                          transform=False, encoding='iso-8859-1')

        komm.save(strict=True)
        
        print "Attaching kommuner to fylke"
        #Set fylke for each kommune by going through komm_nr
        for k in Kommune.objects.all():
            k.fylke = Fylke.objects.get(fylke_nr=k.get_fylke_from_komm_nr())
            k.save()
        
        #Fill fylke geom field based on union of kommuner in fylke
        print "Aggregating fylke geom from kommuner"
        for f in Fylke.objects.all():
            kommuner = Kommune.objects.filter(fylke=f)
            agg = kommuner.unionagg()
            
            #Dirty hack to covnvert polygons to multipolygon to avoid using geometryfield
            #and use multipolygonfield instead
            
            if agg.geom_type == "Polygon":
                wkt = agg.wkt
                srid = agg.srid
                
                area = "%s)" % agg.wkt.replace('POLYGON (', 'MULTIPOLYGON ((')
                
            else:
                area = agg
            
            #End of dirty hack
            
            f.geom = area
            f.save()
        
        #To inspect data: 
        #python manage.py ogrinspect norwaygeo/data/admin-level-no-sea/admin-level-no-sea.shp Kommune --srid=32633 --mapping --multi
