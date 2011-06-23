# -*- coding: utf-8 -*-

import os
from django.core.management.base import BaseCommand
from optparse import OptionParser, make_option
import xlrd
from norwaygeo.utils.excel import ExcelDictReader
from norwaygeo.models import Kommune, PoliceDistrict, Fylke
from django.contrib.gis.db.models import Extent, Union

def to_multi(agg):

    if agg.geom_type == "Polygon":
        wkt = agg.wkt
        srid = agg.srid
    
        area = "%s)" % agg.wkt.replace('POLYGON (', 'MULTIPOLYGON ((')     
    else:
        area = agg
    return area
    

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                                         make_option("-f", "--file", dest="file", default=""),
                                         make_option("-d", "--delete", dest="delete", default=""),
                                         )
    
    def handle(self, *args, **options):
        
        """ 
        Loads mapping of police disctrict to kommune and creates geoms from kommuner agg
        """

        
        if options['delete']:
            PoliceDistrict.objects.all().delete()
        
        if options['file']:
        
            reader = ExcelDictReader(options['file'], 0, 0, 1)
            
            print "Adding police districts and attaching kommuner"
            
            for row in reader:
                
                if row['kommnr']:
                    
                    district,created = PoliceDistrict.objects.get_or_create(district_nr=int(row['poldistriktnr']),
                                                                                    defaults={
                                                                                              'name': row['poldistriktnavn'],
                                                                                              'id': int(row['poldistriktnr']),
                                                                                              },
                                                                                              )
                    try:
                        kommune = Kommune.objects.get(komm_nr=int(row['kommnr']))
                    except Kommune.DoesNotExist:
                        print "No kommune: %i" % int(row['kommnr'])
                    else:
                        kommune.police_district = district
                        kommune.save()
                        
                        
                        
            print "Creating police district polygons"
            
            for p in PoliceDistrict.objects.all():
                
                kommuner = Kommune.objects.filter(police_district=p).aggregate(Extent('geom'), Union('geom'))
                
                kommuner_with_water = Kommune.objects.filter(police_district=p).aggregate(Extent('geom_with_water'), Union('geom_with_water'))
                
                p.geom = to_multi(kommuner['geom__union'])
                p.geom_with_water = to_multi(kommuner_with_water['geom_with_water__union'])
                p.save()
                
                
                
                    
            