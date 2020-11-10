from django.shortcuts import render


def register_view(request):
    context = {}
    return render(request, "users/register.html", context)
