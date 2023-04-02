from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


def get_or_create_session(request):
    try:
        session_key = request.session["session_key"]
    except KeyError:
        session_store = SessionStore()
        session_store.create()
        session_key = session_store.session_key
        request.session["session_key"] = session_key
    obj = Session.objects.get(pk=session_key)
    return obj, request
