from django.conf import settings
from django.urls import path, register_converter
from django.conf import settings
from mapentity.registry import registry

from geotrek.common.urls import LangConverter
from geotrek.feedback import models as feedback_models

from .views import (CategoryList, FeedbackOptionsView,
                    SameStatusReportLayer)

register_converter(LangConverter, 'lang')

app_name = 'feedback'
urlpatterns = [
    path('api/<lang:lang>/feedback/categories.json', CategoryList.as_view(), name="categories_json"),
    path('api/<lang:lang>/feedback/options.json', FeedbackOptionsView.as_view(), name="options_json"),
]

urlpatterns += registry.register(feedback_models.Report, menu=settings.REPORT_MODEL_ENABLED)

urlpatterns += [
    path("api/report/report-<slug:status_id>.geojson", SameStatusReportLayer.as_view()),
]
