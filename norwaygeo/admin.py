from django.contrib.gis import admin
from norwaygeo.models import Kommune


class KommuneAdmin(admin.GeoModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('navn', 'komm', 'shape_len', 'kml', 'geom')
        }),
    )
    readonly_fields = ('kml',)
admin.site.register(Kommune, KommuneAdmin)