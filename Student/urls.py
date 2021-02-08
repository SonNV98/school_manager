from django.urls import path
from .views import *
from School import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


app_name = 'Student'

urlpatterns = [
    path('home/', CategoryView.as_view(), name='home'),
    path('subCategory/<str:subCategoryId>/', SubCategoryView.as_view(), name='subCategory'),
    path('logout/', logout_request, name='logout'),
    path('login/', login_request, name='login'),
    path('updateNumberPhone/', updateNumberPhone, name='updateNumberPhone'),
    path('insertShareNewsForSchool/', insertShareNewsForSchool, name='insertShareNewsForSchool'),
    path('insertShareNewsForClass/', insertShareNewsForClass, name='insertShareNewsForClass'),
    path('loadDistrict/', loadDistrict, name='loadDistrict'),
    path('loadWard/', loadWard, name='loadWard'),
    path('updateStudentIn4/', updateStudentIn4, name='updateStudentIn4'),
    path('getTestCalendar/', getTestCalendar, name='getTestCalendar'),
    path('create/<str:row>/<str:cel>/', Teacher_form.as_view(), name='create_teacher'),
    path('createMainTeacher/<str:row>/', Main_teacher_form.as_view(), name='create_main_teacher'),
    path('assignedExam/', insertAssignedExam, name='insertAssignedExam'),
    path('assignedTeach/', insertAssignedTeach, name='insertAssignedTeach'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
