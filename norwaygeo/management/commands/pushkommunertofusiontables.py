# -*- coding: utf-8 -*-

import os
from django.core.management.base import BaseCommand
from placemat import ftclient
from django.conf import settings
from norgeo.models import Kommune

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        """
        Pushes the kommune-table to Google Fusion tables. 
        Requires placemat python client lib for Fusion Tables
        http://code.google.com/p/placemat/
        and your Google login credentials in settings.py or local_settings.py
        """
        
        auth_token = ftclient.GetAuthToken(
                             settings.GOOGLE_FUSION_TABLES_LOGIN['email'], 
                             settings.GOOGLE_FUSION_TABLES_LOGIN['password']
                             )
        
        ft = ftclient.FTClient(auth_token)
        
        
        cols = [
                ['kommnr', 'NUMBER'],
                ['kommune', 'STRING'],
                ['geo', 'LOCATION'],
                
               ]
        
        table_name = 'placemattest2'
        
        tableid = ft.createTable(table_name, cols)
        
        r = 0
        query = ''
        for k in Kommune.objects.all().order_by('komm'):
            #print k.komm, k.navn
            query += "INSERT INTO %s (kommnr, kommune, geo) VALUES (%i,'%s', '%s');" % (tableid, k.komm, k.navn.encode('utf-8'), k.kml())
            
            if r % 5:
                ft.runPostQuery(query)
                print query
                query = ''
                
            r = r+1
            
            
        #print ft.runGetQuery('SHOW TABLES')
