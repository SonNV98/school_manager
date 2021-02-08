from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.db import models


class TeacherForm(BSModalForm):
    class Meta:
        model = Users
        fields = ['user', 'technique']
