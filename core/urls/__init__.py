from .commands import urlpatterns as command_urls
from .plans import urlpatterns as plan_urls
from .profiles import urlpatterns as profile_urls
from .users import urlpatterns as user_urls

urlpatterns = profile_urls + plan_urls + user_urls + command_urls
