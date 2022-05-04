"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from labs import views as lab_views
from grants import views as grant_views
from tools import views as tool_views
from users import views as user_views

urlpatterns = [
    path(
        "api/",
        include(
            [
                path(
                    "labs/",
                    include(
                        [
                            path("", lab_views.LabsList.as_view()),
                            path("<uuid:id>", lab_views.LabDetail.as_view()),
                        ]
                    ),
                ),
                path(
                    "grants/",
                    include(
                        [
                            path("", grant_views.GrantsList.as_view()),
                            path("<uuid:id>", grant_views.GrantDetail.as_view()),
                        ]
                    ),
                ),
                path(
                    "tools/",
                    include(
                        [
                            path("", tool_views.ToolsList.as_view()),
                            path("<uuid:id>", tool_views.ToolDetail.as_view()),
                        ]
                    ),
                ),
                path(
                    "users/",
                    include(
                        [
                            path("", user_views.UsersList.as_view()),
                            path("<uuid:id>", user_views.UserDetail.as_view()),
                        ]
                    ),
                ),
            ]
        ),
    )
]
