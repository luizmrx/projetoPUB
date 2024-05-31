from django.contrib import admin
from .models import Student, Discipline, DisciplineDemand

admin.site.register(Student)
admin.site.register(Discipline)
admin.site.register(DisciplineDemand)
