from django.contrib import admin
import member.models as mem
# Register your models here.
admin.site.register(mem.Profile)
admin.site.register(mem.Organizations)
admin.site.register(mem.Companies)
admin.site.register(mem.Position)
admin.site.register(mem.Cell_Carriers)
admin.site.register(mem.Organization_Involvement)
admin.site.register(mem.Job_History)
admin.site.register(mem.Position_History)

