#Author: Christopher Whetsel

'''This file is needed to tell the admin page what models to display as edittable'''
from django.contrib import admin
import member.models as mem
# Register your models here.
admin.site.register(mem.Profile)
admin.site.register(mem.Organization)
admin.site.register(mem.Company)
admin.site.register(mem.Position)
admin.site.register(mem.Cell_Carrier)
admin.site.register(mem.Organization_Involvement)
admin.site.register(mem.Job_History)
admin.site.register(mem.Position_History)

