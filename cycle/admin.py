from django.contrib import admin
from cycle.models import Cycle, Client, Objectives, Procedures


class CycleAdmin(admin.ModelAdmin):
    pass


class ClientAdmin(admin.ModelAdmin):
    pass


class ObjectivesAdmin(admin.ModelAdmin):
    pass


class ProceduresAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cycle, CycleAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Objectives, ObjectivesAdmin)
admin.site.register(Procedures, ProceduresAdmin)
