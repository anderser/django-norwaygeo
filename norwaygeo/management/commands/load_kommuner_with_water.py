# -*- coding: utf-8 -*-

import os
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.gdal import *
from django.core.management.base import BaseCommand
from norwaygeo.models import Kommune, Fylke
from django.contrib.gis.db.models import Extent, Union

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        """
        Loads kommuner with water from the shapefile and attach to kommune
        """
        
        print "Loading kommuner shape data with water areas"
        kommune_with_water_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                   '../../data/statens-kartverk-n5000/N5000_AdministrativFlate.shp'))

        ds = DataSource(kommune_with_water_shp)
        
        for feat in ds[0]:
            kommnr = feat.get('KOMM')

            try:
                k = Kommune.objects.get(komm_nr=int(kommnr))
            except Kommune.DoesNotExist:
                print "Could not find kommune %i" %kommnr
            else:
                if feat.geom_type == "Polygon":
                    wkt = feat.geom.wkt
                    srid = feat.geom.srid
                
                    area = "%s)" % feat.geom.wkt.replace('POLYGON (', 'MULTIPOLYGON ((')
                
                else:
                    area = feat.geom
                
                k.geom_with_water = area
                k.save()
        
        #Fill fylke geom field based on union of kommuner in fylke
        print "Aggregating fylke geom with water from kommuner"
        for f in Fylke.objects.all():
            kommuner = Kommune.objects.filter(fylke=f).aggregate(Extent('geom_with_water'), Union('geom_with_water'))
            
            agg = kommuner['geom_with_water__union']
            
            #Dirty hack to covnvert polygons to multipolygon to avoid using geometryfield
            #and use multipolygonfield instead
            
            if agg.geom_type == "Polygon":
                wkt = agg.wkt
                srid = agg.srid
                
                area = "%s)" % agg.wkt.replace('POLYGON (', 'MULTIPOLYGON ((')
                
            else:
                area = agg
            
            #End of dirty hack
            
            f.geom_with_water = area
            f.save()
        