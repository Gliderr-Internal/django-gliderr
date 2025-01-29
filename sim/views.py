import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .models import User

@csrf_exempt
def sign_in(request):
    if request.user.is_authenticated:
        redirect("chat:index")

    context = {
        "google_client_id" : settings.GOOGLE_OAUTH_CLIENT_ID
    }

    return render(request, "sim/sign_in.html", context)


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
        email = user_data['email']
        google_id = user_data['sub']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'google_id': google_id,
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', '')
            }
        )

        login(request, user)
        return redirect("chat:index")


    except ValueError:
        return HttpResponse(status=403)


def sign_out(request):
    logout(request)
    return redirect("sim:sign_in")
