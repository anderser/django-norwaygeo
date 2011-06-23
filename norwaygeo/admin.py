from django.contrib.gis import admin
from norwaygeo.models import Kommune, Fylke

class StatkartGeoAdmin(admin.GeoModelAdmin): 
    wms_url = 'http://opencache.statkart.no/gatekeeper/gk/gk.open?'
    #wms_url =  
    wms_layer = 'topo2graatone' 
    wms_name = 'Statkart WMS-C Topo2' 
    display_srid = 32633 
    map_srid = 32633
    units = "m"
    max_extent = '-2500000, 3500000, 3545984, 9045984'
    max_resolution = 21664 
    num_zoom = 21
    debug = False
    default_zoom = 14
    modifiable = False

class KommuneAdmin(StatkartGeoAdmin):
    fieldsets = (
        (None, {
            'fields': ('komm_nr', 'name', 'komm_ssb_code', 'slug', 'fylke', 'police_district', 'geom',)
        }),
    )
    list_display = ('komm_nr', 'name', 'fylke','police_district')
    
    list_filter = ('police_district',)
    #map is no modifiable
    modifiable = False
    
    readonly_fields = ('komm_nr', 'name', 'komm_ssb_code', 'fylke','slug',)
    
class FylkeAdmin(StatkartGeoAdmin):    
    fieldsets = (
        (None, {
            'fields': ('fylke_nr', 'name', 'fylke_ssb_code', 'slug', 'geom_type', 'geom', )
        }),
    )
    readonly_fields = ('geom_type',)
    is_polygon = True
    is_collection = True
    

admin.site.register(Fylke, FylkeAdmin)
admin.site.register(Kommune, KommuneAdmin)