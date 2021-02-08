import string
from re import sub

from django.db.models import Sum
from django.urls import reverse_lazy

from .code import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from School import settings
from .models import *
from django.views import View, generic
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView
from .forms import *

# Create your views here.
context = {}


# assign exam
def insertAssignedExam(request):
    if request.method == "GET":
        for item in request.GET.lists():
            in4 = item[1]
            code = in4[0].split("_")
            classroom_id = code[1]
            subject_id = code[2]
            exam_teacher = in4[1]
            if in4[2] is not None:
                date = in4[2]
            if in4[4] is not None:
                time = in4[4]
            assign_record = AssignedExam.objects.all().filter(classroom_id=classroom_id, subject_id=subject_id)
            if len(assign_record) == 0:
                assign = AssignedExam(classroom_id=classroom_id, subject_id=subject_id, exam_teacher_id=exam_teacher,
                                      date=date, time=time)
                assign.save()
            else:
                assign_record[0].exam_teacher_id = exam_teacher
                assign_record[0].date = date
                assign_record[0].time = time
                assign_record[0].save()

        return render(request, "Student/base.html", context)


# assign teach
def insertAssignedTeach(request):
    if request.method == "GET":
        for item in request.GET.lists():
            if len(item[1]) <= 1:
                main_teacher_id = item[1]
            else:
                in4 = item[1]
                code = in4[0].split("_")
                classroom_id = code[1]
                subject_id = code[2]
                exam_teacher = in4[1]
                if in4[2] is not None:
                    date = in4[2]
                if in4[4] is not None:
                    time = in4[4]
                assign_record = AssignedExam.objects.all().filter(classroom_id=classroom_id, subject_id=subject_id)
                if len(assign_record) == 0:
                    assign = AssignedExam(classroom_id=classroom_id, subject_id=subject_id,
                                          subject_teacher_id=exam_teacher,
                                          date=date, time=time, main_teacher_id=main_teacher_id[0])
                    assign.save()
                else:
                    assign_record[0].exam_teacher_id = exam_teacher
                    assign_record[0].main_teacher_id = main_teacher_id
                    assign_record[0].save()
        return render(request, "Student/base.html", context)


# popup
class Teacher_form(View):
    def get(self, request, row, cel):
        group = Group.objects.exclude(id=5)
        user_list = []
        for item in group:
            user = item.user_set.all()
            for item1 in user:
                user_list.append(item1)
        context['user_list'] = user_list
        context['row'] = row
        context['cel'] = cel
        return render(request, 'Student/teacher_popup.html', context)


class Main_teacher_form(View):
    def get(self, request, row):
        group = Group.objects.get(id=3)
        user_list = group.user_set.all()
        user_lists = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id)
            user_lists.append(users[0])
        context['user_lists'] = user_lists
        context['rows'] = row
        return render(request, 'Student/main_teacher_popup.html', context)


# get test calendar
def getTestCalendar(request):
    if request.method == "GET":
        subject_id = request.GET.get('data')
        plan_test_list = PlanTest.objects.filter(subject_id=subject_id)
        context['plan_test_list'] = plan_test_list
        context['subject_name'] = Subject.objects.get(subject_id=subject_id).subject_name
        return render(request, "Student/planTest.html", context)


# update student's information
def updateStudentIn4(request):
    if request.method == "GET":
        authUser = User.objects.all().filter(username=context['username'])
        studentUser = Users.objects.get(user_id=authUser.values()[0].get('id'))
        if request.GET.get('data[national]') is not None:
            studentUser.national = request.GET.get('data[national]')
        if request.GET.get('data[folk]') is not None:
            studentUser.folk = request.GET.get('data[folk]')
        if request.GET.get('data[religion]') is not None:
            studentUser.religion = request.GET.get('data[religion]')
        if request.GET.get('data[priority_subject]') is not None:
            studentUser.priority_subject = request.GET.get('data[priority_subject]')
        if request.GET.get('data[subject_of_reduction]') is not None:
            studentUser.subject_of_reduction = request.GET.get('data[subject_of_reduction]')
        if request.GET.get('data[cmtnd]') is not None:
            studentUser.cmtnd = request.GET.get('data[cmtnd]')
        if request.GET.get('data[cmnt_area]') is not None:
            studentUser.cmnt_area = request.GET.get('data[cmnt_area]')
        if request.GET.get('data[bank_name]') is not None:
            studentUser.bank_name = request.GET.get('data[bank_name]')
        if request.GET.get('data[bank_number]') is not None:
            studentUser.bank_number = request.GET.get('data[bank_number]')
        if request.GET.get('data[code_of_health]') is not None:
            studentUser.code_of_health = request.GET.get('data[code_of_health]')
        if request.GET.get('data[province]') is not None:
            studentUser.province_id = request.GET.get('data[province]')
        if request.GET.get('data[district]') is not None:
            studentUser.district_id = request.GET.get('data[district]')
        if request.GET.get('data[ward]') is not None:
            studentUser.ward_id = request.GET.get('data[ward]')
        if request.GET.get('data[cmtnd_day_create]') is not None:
            studentUser.cmtnd_day_create = request.GET.get('data[cmtnd_day_create]')

        if request.GET.get('data[dad_name]') is not None:
            studentUser.dad_name = request.GET.get('data[dad_name]')
        if request.GET.get('data[dad_birthday]') is not None:
            studentUser.dad_birthday = request.GET.get('data[dad_birthday]')
        if request.GET.get('data[dad_job]') is not None:
            studentUser.dad_job = request.GET.get('data[dad_job]')
        if request.GET.get('data[dad_address]') is not None:
            studentUser.dad_address = request.GET.get('data[dad_address]')
        if request.GET.get('data[dad_number_phone]') is not None:
            studentUser.dad_number_phone = request.GET.get('data[dad_number_phone]')
        if request.GET.get('data[mom_name]') is not None:
            studentUser.mom_name = request.GET.get('data[mom_name]')
        if request.GET.get('data[mom_address]') is not None:
            studentUser.mom_address = request.GET.get('data[mom_address]')
        if request.GET.get('data[mom_birthday]') is not None:
            studentUser.mom_birthday = request.GET.get('data[mom_birthday]')
        if request.GET.get('data[mom_job]') is not None:
            studentUser.mom_job = request.GET.get('data[mom_job]')
        if request.GET.get('data[mom_number_phone]') is not None:
            studentUser.mom_number_phone = request.GET.get('data[mom_number_phone]')
        if request.GET.get('data[tutor_name]') is not None:
            studentUser.tutor_name = request.GET.get('data[tutor_name]')
        if request.GET.get('data[tutor_address]') is not None:
            studentUser.tutor_address = request.GET.get('data[tutor_address]')
        if request.GET.get('data[tutor_birthday]') is not None:
            studentUser.tutor_birthday = request.GET.get('data[tutor_birthday]')
        if request.GET.get('data[tutor_job]') is not None:
            studentUser.tutor_job = request.GET.get('data[tutor_job]')
        if request.GET.get('data[tutor_number_phone]') is not None:
            studentUser.tutor_number_phone = request.GET.get('data[tutor_number_phone]')
        if request.GET.get('data[wife_husband_address]') is not None:
            studentUser.wife_husband_address = request.GET.get('data[wife_husband_address]')
        if request.GET.get('data[wife_husband_birthday]') is not None:
            studentUser.wife_husband_birthday = request.GET.get('data[wife_husband_birthday]')
        if request.GET.get('data[wife_husband_job]') is not None:
            studentUser.wife_husband_job = request.GET.get('data[wife_husband_job]')
        if request.GET.get('data[wife_husband_name]') is not None:
            studentUser.wife_husband_name = request.GET.get('data[wife_husband_name]')
        if request.GET.get('data[wife_husband_number_phone]') is not None:
            studentUser.wife_husband_number_phone = request.GET.get('data[wife_husband_number_phone]')
        if request.GET.get('data[my_son_daughter]') is not None:
            studentUser.my_son_daughter = request.GET.get('data[my_son_daughter]')
        if request.GET.get('data[sis_bro]') is not None:
            studentUser.sis_bro = request.GET.get('data[sis_bro]')
        if request.GET.get('data[stay_now]') is not None:
            studentUser.stay_now = request.GET.get('data[stay_now]')
        if request.GET.get('data[email]') is not None:
            studentUser.user.email = request.GET.get('data[email]')
        if request.GET.get('data[number_phone]') is not None:
            studentUser.number_phone = request.GET.get('data[number_phone]')

        studentUser.save()
        return render(request, "Student/base.html", context)


# load district follow province
def loadDistrict(request):
    if request.method == "GET":
        province_id = request.GET.get('province')
        district_list = District.objects.filter(province_id=province_id).order_by('name')
        context['district_list'] = district_list
        return render(request, "Student/district_list.html", context)


# load ward follow province
def loadWard(request):
    if request.method == "GET":
        district_id = request.GET.get('district')
        ward_list = Ward.objects.filter(district_id=district_id).order_by('name')
        context['ward_list'] = ward_list
        return render(request, "Student/ward_list.html", context)


# insert share information for class
def insertShareNewsForClass(request):
    if request.method == "GET":
        authUser = User.objects.all().filter(username=context['username'])
        studentUser = Users.objects.all().filter(user_id=authUser.values()[0].get('id'))
        shareNews = ShareNews(content=request.GET.get('data'),
                              classroom_id=studentUser.values()[0].get('classroom_id'))
        shareNews.save()
        return render(request, "Student/base.html", context)


# insert share information for school
def insertShareNewsForSchool(request):
    if request.method == "GET":
        authUser = User.objects.all().filter(username=context['username'])
        studentUser = Users.objects.all().filter(user_id=authUser.values()[0].get('id'))
        shareNews = ShareNews(content=request.GET.get('data'), share_school_flag=1,
                              classroom_id=studentUser.values()[0].get('classroom_id'))
        shareNews.save()
        return render(request, "Student/base.html", context)


# update number phone
def updateNumberPhone(request):
    if request.method == "GET":
        for item in request.GET:
            array = request.GET[item].split("-")
            userId = array[0]
            numberPhone = array[1]
            userNumberPhone = Users.objects.get(user_id=userId)
            userNumberPhone.number_phone = numberPhone
            userNumberPhone.save()
        return render(request, "Student/base.html", context)


# logout account
def logout_request(request):
    logout(request)
    return redirect("Student:login")


# login account
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                context['fullname'] = request.user.get_full_name()
                context['username'] = username
                context['group'] = request.user.groups.all()
                return redirect("Student:home")
            else:
                context['errorLogin'] = "You have entered the wrong account and password. Please enter the " \
                                        "information again! "
        else:
            context['errorLogin'] = "You have entered the wrong account and password. Please enter the " \
                                    "information again! "
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, "Student/login.html", context)


# information of subcategory
def in4ForSubCate(request, subCategoryId):
    authUser = User.objects.all().filter(username=context['username'])
    studentUser = Users.objects.all().filter(user_id=authUser.values()[0].get('id'))
    context['studentUser'] = studentUser[0]
    if studentUser[0].technique_id is not None:
        context['technique'] = Subject.objects.all().filter(subject_id=studentUser[0].technique_id)[0]
    studentClass = Classroom.objects.all().filter(classroom_id=studentUser.values()[0].get('classroom_id'))
    group = Group.objects.get(id=context['group'].values()[0].get('id', "None"))
    userGroupLst = group.user_set.all()
    context['userGroupLst'] = userGroupLst
    if len(studentClass) != 0:
        context['className'] = studentClass.values()[0].get('classroom_name')
        classroom = Classroom.objects.get(classroom_id=studentClass.values()[0].get('classroom_id'))
        userClassLst = classroom.users_set.all()
        subjectList = classroom.subject_set.all()
        context['subjectList'] = subjectList
        context['userClassLst'] = userClassLst

    if subCategoryId == "1":
        newsFromSchool = News.objects.all().filter(group_id=context['group'].values()[0].get('id', "None"),
                                                   on_delete_flag=0)
        paginator = Paginator(newsFromSchool, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    elif subCategoryId == "8":
        province_list = Province.objects.all().order_by('name')
        context['province_list'] = province_list
    elif subCategoryId == "2":
        shareNews = ShareNews.objects.all().filter(classroom_id=studentClass.values()[0].get('classroom_id'),
                                                   on_delete_flag=0)
        paginator2 = Paginator(shareNews, 2)
        page_number2 = request.GET.get('page')
        page_obj2 = paginator2.get_page(page_number2)
        context['page_obj2'] = page_obj2
    elif subCategoryId == "9" or subCategoryId == "24" or subCategoryId == "32":
        form = PasswordChangeForm(request.user)
        context['form'] = form
    elif subCategoryId == "14":
        # TODO
        calendarSubjectT10 = Subject.objects.get(subject_id='T10').calendar_set.all()
        context['calendarSubjectT10'] = calendarSubjectT10[0]
        # TODO
    elif subCategoryId == "17":
        plan_test_list = PlanTest.objects.filter(classroom_id=studentClass.values()[0].get('classroom_id'))
        context['plan_test_list17'] = plan_test_list
    elif subCategoryId == "18" or subCategoryId == "19":
        groupMainTeacher = Group.objects.get(pk=3)
        listMainTeacher = groupMainTeacher.user_set.all()
        for teacher in listMainTeacher:
            for user in userClassLst:
                if teacher.id == user.user_id:
                    context['teacher'] = user
        score = Score.objects.all().filter(user_id=authUser.values()[0].get('id'))
        context['score'] = score
    elif subCategoryId == "25":
        subjectClass = Classroom.objects.all().filter(subject__subject_id=studentUser.values()[0].get('technique_id'))
        context['subjectClass'] = subjectClass
    elif subCategoryId == "26" or subCategoryId == "27" or subCategoryId == "28" or subCategoryId == "29" or subCategoryId == "34":
        group2 = Group.objects.get(id=2)
        userGroupLst2 = group2.user_set.all()
        group1 = Group.objects.get(id=1)
        userGroupLst1 = group1.user_set.all()
        group3 = Group.objects.get(id=3)
        userGroupLst3 = group3.user_set.all()
        group4 = Group.objects.get(id=4)
        userGroupLst4 = group4.user_set.all()
        context['userGroupLst1'] = userGroupLst1
        context['userGroupLst2'] = userGroupLst2
        context['userGroupLst3'] = userGroupLst3
        context['userGroupLst4'] = userGroupLst4
    elif subCategoryId == "52":
        group = Group.objects.get(id=5)
        user_list = group.user_set.all()
        users_list = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id, classroom__classroom_id__startswith='10')
            score = Score.objects.all().filter(user_id=users[0].user_id)
            theory_score = 0
            exercise_score = 0
            test_score = 0
            for item1 in score:
                theory_score += item1.theory_score
                exercise_score += item1.exercise_score
                test_score += item1.test_score

            userCode = User()
            userCode.username = users[0].user.username
            userCode.fullname = users[0].user.first_name + " " + users[0].user.last_name
            userCode.class_name = users[0].classroom.classroom_name
            average = ((theory_score + exercise_score * 2) / 3 + test_score * 2) / 3
            if average >= 8:
                userCode.learning_power = "Giỏi"
            elif average >= 6.5:
                userCode.learning_power = "Khá"
            elif average >= 5:
                userCode.learning_power = "Trung bình"
            else:
                userCode.learning_power = "Yếu"
            users_list.append(userCode)
        context['users_list'] = users_list
    elif subCategoryId == "53":
        group = Group.objects.get(id=5)
        user_list = group.user_set.all()
        users_list = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id, classroom__classroom_id__startswith='11')
            if len(users) != 0:
                score = Score.objects.all().filter(user_id=users[0].user_id)
                theory_score = 0
                exercise_score = 0
                test_score = 0
                for item1 in score:
                    theory_score += item1.theory_score
                    exercise_score += item1.exercise_score
                    test_score += item1.test_score

                userCode = User()
                userCode.username = users[0].user.username
                userCode.fullname = users[0].user.first_name + " " + users[0].user.last_name
                userCode.class_name = users[0].classroom.classroom_name
                average = ((theory_score + exercise_score * 2) / 3 + test_score * 2) / 3
                if average >= 8:
                    userCode.learning_power = "Giỏi"
                elif average >= 6.5:
                    userCode.learning_power = "Khá"
                elif average >= 5:
                    userCode.learning_power = "Trung bình"
                else:
                    userCode.learning_power = "Yếu"
                users_list.append(userCode)
        context['users_list'] = users_list
    elif subCategoryId == "54":
        group = Group.objects.get(id=5)
        user_list = group.user_set.all()
        users_list = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id, classroom__classroom_id__startswith='12')
            if len(users) != 0:
                score = Score.objects.all().filter(user_id=users[0].user_id)
                theory_score = 0
                exercise_score = 0
                test_score = 0
                for item1 in score:
                    theory_score += item1.theory_score
                    exercise_score += item1.exercise_score
                    test_score += item1.test_score

                userCode = User()
                userCode.username = users[0].user.username
                userCode.fullname = users[0].user.first_name + " " + users[0].user.last_name
                userCode.class_name = users[0].classroom.classroom_name
                average = ((theory_score + exercise_score * 2) / 3 + test_score * 2) / 3
                if average >= 8:
                    userCode.learning_power = "Giỏi"
                elif average >= 6.5:
                    userCode.learning_power = "Khá"
                elif average >= 5:
                    userCode.learning_power = "Trung bình"
                else:
                    userCode.learning_power = "Yếu"
                users_list.append(userCode)
        context['users_list'] = users_list
    elif subCategoryId == "55" or subCategoryId == "56":
        classroom = Classroom.objects.all()
        context['classroom'] = classroom
        subject = Subject.objects.all()
        context['subject'] = subject
        context['len_subject'] = len(subject)
        assign = AssignedExam.objects.all()
        context['assign'] = assign
        context['flag'] = False
        main_teacher = AssignedExam.objects.values('classroom__classroom_id', 'main_teacher__first_name',
                                                   'main_teacher__last_name').distinct()
        context['main_teacher'] = main_teacher
    elif subCategoryId == "57":
        group = Group.objects.get(id=2)
        user_list = group.user_set.all()
        user_lists = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id)
            user_lists.append(users[0])
        context['user_list_57'] = user_lists
    elif subCategoryId == "58":
        group = Group.objects.get(id=5)
        user_list = group.user_set.all()
        user_lists = []
        for item in user_list:
            users = Users.objects.all().filter(user_id=item.id)
            user_lists.append(users[0])
        context['user_list_58'] = user_lists


# get category
class CategoryView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        template_name = 'Student/base.html'
        category = Category.objects.all().filter(group_id=context['group'].values()[0].get('id', "None"),
                                                 on_delete_flag=0)
        subCategory = SubCategory.objects.all()
        context['Category'] = category
        context['SubCategory'] = subCategory
        return render(request, template_name, context)


# get sub category
class SubCategoryView(CategoryView):
    login_url = CategoryView.login_url

    def get(self, request, subCategoryId):
        super().get(request)
        url = ("Student/subCate", ".html")
        template_name = subCategoryId.join(url)
        in4ForSubCate(request, subCategoryId)
        return render(request, template_name, context)

    def post(self, request, subCategoryId):
        if subCategoryId == "9":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                context['form'] = form
                return render(request, 'Student/subCate9.html', context)
            else:
                messages.error(request, 'Please correct the error below.')


