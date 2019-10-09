from django.utils import timezone


def form_validate_and_save(form, request):
    if form.is_valid():
        result = form.save(commit=False)
        result.author = request.user
        result.published_date = timezone.now()
        result.save()
        return result
    else:
        return None