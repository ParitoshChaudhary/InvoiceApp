from django.shortcuts import render


def home_screen_view(request):
    context = {}
    user = request.user
    if user:
        user_id = user.id
        context['id'] = user_id
    return render(request, "base.html", context)
