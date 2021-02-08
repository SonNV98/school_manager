from django.db import models
from datetime import datetime
from tinymce import HTMLField
from django.contrib.auth.models import User, Group


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=1000)
    icon = models.CharField(max_length=1000)
    sub_category_flag = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=1000)
    icon = models.CharField(max_length=1000, null=True, blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.sub_category_name


class News(models.Model):
    subject = models.CharField(null=True, blank=True, max_length=8000)
    title = models.CharField(null=True, blank=True, max_length=8000)
    content = HTMLField('Content', null=True, blank=True)
    file = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.title


class Province(models.Model):
    province_id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False, )
    type = models.CharField(max_length=30, null=False, blank=False, )

    def __str__(self):
        return self.name


class District(models.Model):
    district_id = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False, )
    type = models.CharField(max_length=30, null=False, blank=False, )
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(models.Model):
    ward_id = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=200, unique=True, primary_key=True)
    classroom_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.classroom_name


class Subject(models.Model):
    subject_id = models.CharField(primary_key=True, unique=True, max_length=200)
    subject_name = models.CharField(max_length=200)
    academic_credits = models.IntegerField(default=0)
    classroom = models.ManyToManyField(Classroom)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.subject_name


class Score(models.Model):
    theory_score = models.FloatField(default=0)
    exercise_score = models.FloatField(default=0)
    test_score = models.FloatField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    @property
    def avergateHk(self):
        return ((self.theory_score + self.exercise_score) / 2 + (self.test_score * 2)) / 3


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender_type = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    date_of_birth = models.DateTimeField("birthday", default=datetime.now(),null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_type)
    number_phone = models.CharField(max_length=11, null=True, blank=True)
    job = models.CharField(max_length=500, null=True, blank=True)
    technique = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    stay_now = models.CharField(max_length=500, null=True, blank=True)
    national = models.CharField(max_length=500, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    folk = models.CharField(max_length=500, null=True, blank=True)
    religion = models.CharField(max_length=500, null=True, blank=True)
    cmtnd = models.CharField(max_length=14, null=True, blank=True)
    cmtnd_day_create = models.DateTimeField("CMTND day create", default=datetime.now(), null=True, blank=True)
    cmnt_area = models.CharField(max_length=500, null=True, blank=True)
    bank_number = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=500, null=True, blank=True)
    code_of_health = models.CharField(max_length=100, null=True, blank=True)
    dad_name = models.CharField(max_length=500, null=True, blank=True)
    dad_birthday = models.DateTimeField("dad'birthday", default=datetime.now(),null=True, blank=True)
    dad_number_phone = models.CharField(max_length=14, null=True, blank=True)
    dad_job = models.CharField(max_length=150, null=True, blank=True)
    dad_address = models.CharField(max_length=500, null=True, blank=True)
    mom_name = models.CharField(max_length=500, null=True, blank=True)
    mom_birthday = models.DateTimeField("mom'birthday", default=datetime.now(),null=True,blank=True)
    mom_number_phone = models.CharField(max_length=14, null=True, blank=True)
    mom_job = models.CharField(max_length=150, null=True, blank=True)
    mom_address = models.CharField(max_length=500, null=True, blank=True)
    sis_bro = models.CharField(max_length=500, null=True, blank=True)
    my_son_daughter = models.CharField(max_length=500, null=True, blank=True)
    wife_husband_name = models.CharField(max_length=500, null=True, blank=True)
    wife_husband_birthday = models.DateTimeField("mom'birthday", default=datetime.now(),null=True, blank=True)
    wife_husband_number_phone = models.CharField(max_length=14, null=True, blank=True)
    wife_husband_job = models.CharField(max_length=150, null=True, blank=True)
    wife_husband_address = models.CharField(max_length=500, null=True, blank=True)
    tutor_name = models.CharField(max_length=500, null=True, blank=True)
    tutor_birthday = models.DateTimeField("mom'birthday", default=datetime.now(),null=True,blank=True)
    tutor_number_phone = models.CharField(max_length=14, null=True, blank=True)
    tutor_job = models.CharField(max_length=150, null=True, blank=True)
    tutor_address = models.CharField(max_length=500, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    certificate = models.CharField(max_length=500, null=True, blank=True)
    priority_subject = models.CharField(max_length=500, null=True, blank=True)
    subject_of_reduction = models.CharField(max_length=500, null=True, blank=True)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now(),null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Calendar(models.Model):
    start_date = models.DateTimeField("start date", default=datetime.now())
    end_date = models.DateTimeField("end date", default=datetime.now())
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    day_type = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening')
    )
    day = models.CharField(max_length=15, choices=day_type)
    kind_type = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Wednesday', 'Wednesday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    kind = models.CharField(max_length=20, choices=kind_type)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())


class ShareNews(models.Model):
    subject = models.CharField(null=True, blank=True, max_length=8000)
    title = models.CharField(null=True, blank=True, max_length=8000)
    content = HTMLField('Content', null=True, blank=True)
    file = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    share_school_flag = models.IntegerField(default=0)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())

    def __str__(self):
        return self.title


class PlanTest(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())


class AssignedExam(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    main_teacher = models.ForeignKey(User, related_name="MainTeacher", on_delete=models.CASCADE, null=True, blank=True)
    subject_teacher = models.ForeignKey(User, related_name="SuTeacher", on_delete=models.CASCADE, null=True, blank=True)
    exam_teacher = models.ForeignKey(User, related_name="ExamTeacher", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    on_delete_flag = models.IntegerField(default=0)
    published = models.DateTimeField("date published", default=datetime.now())
