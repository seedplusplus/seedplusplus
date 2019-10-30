from django.utils import timezone
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import User
import django.forms
import django.http.request
import django.db.models


def form_validate_and_save(form: django.forms.Form, request: django.http.request.HttpRequest, edit: bool = False,
                           **kwargs):
    if form.is_valid():
        result = form.save(commit=False)
        result.owner = request.user
        if not edit:
            result.published_date = timezone.now()
            result.created_on = result.published_date
        result.last_modified = timezone.now()
        for key, value in kwargs.items():
            result.__setitem__(key, value)
        result.save()
        form.save_m2m()
        return result
    else:
        return None


def has_perm(user: User, obj: django.db.models.Model, perm: str):
    # wrapper for guardian.user.has_perm
    if hasattr(obj, 'owner') and obj.owner == user:
        return True
    else:
        return user.has_perm(perm, obj)


def set_perm(user: User, obj: django.db.models.Model, perm: str, value: bool = True):
    if value:
        assign_perm(perm, user, obj)
    else:
        remove_perm(perm, user, obj)
