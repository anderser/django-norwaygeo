# -*- coding: utf-8 -*-

import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import add_postgis_srs

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        """ 
        Adds the necessary SRS 32633 (UTM 33N) and 4326 (WGS84) to
        the postgis DB
        """
        add_postgis_srs(32633)
        add_postgis_srs(4326)
        
