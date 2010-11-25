# -*- coding: utf-8 -*-

import os
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, GEOSGeometry
from django.core.management.base import BaseCommand
from norwaygeo.models import Kommune, kommune_mapping


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        """
        Loads kommuner from the shapefile with the mapping of fields
        specified in the model.
        """
        
        kommune_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                   '../../data/admin-level-no-sea/admin-level-no-sea.shp'))

        komm = LayerMapping(Kommune, kommune_shp, kommune_mapping,
                          transform=False, encoding='iso-8859-1')

        komm.save(strict=True)
        
        #To inspect data: 
        #python manage.py ogrinspect norwaygeo/data/admin-level-no-sea/admin-level-no-sea.shp Kommune --srid=32633 --mapping --multi
