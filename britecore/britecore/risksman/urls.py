from django.urls import path, re_path, include
from django.contrib.staticfiles import views
from rest_framework import routers

from . import views as v

# viewsets make use of the builtin rest_framework routers
router = routers.SimpleRouter()
router.register('api/v1/fields', v.FieldTypeView)
router.register('api/v1/risks-types', v.RiskTypeView)
router.register('api/v1/risks', v.RiskView)


urlpatterns = [
    # rest_framework Generic views need to be registered individually
    # not in the router, otherwise you know what!
    path('api/v1/fields-types/',
         v.RiskFieldView.as_view(), name='fields-types'),
    path('api/v1/risks-type-fields/<int:pk>/',
         v.SingleRiskTypeView.as_view()),
    # this is a dev env so the following seems *ok*
    re_path(r'^static/(?P<path>.*)$', views.serve),
    re_path(r'^$', v.HomeView.as_view(), name='home'),
    path('', include(router.urls)),
]

print(router.urls)
