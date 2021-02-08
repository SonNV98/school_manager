from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *
from tinymce import TinyMCE


# Register your models here.
class UsersInline(admin.StackedInline):
    fieldsets = [
        ('Thông tin cơ bản', {'fields': ['date_of_birth', 'gender', 'number_phone', 'job','technique']}),
        ('Quê quán, chỗ ở hiện tại và địa chỉ', {'fields': ['address', 'stay_now', 'national',
                                                            'province', 'district', 'ward']}),
        ('Dân tộc và tôn giáo', {'fields': ['folk', 'religion']}),
        ('Thông tin về chứng minh thư', {'fields': ['cmtnd', 'cmtnd_day_create', 'cmnt_area']}),
        ('Thông tin về tài khoản ngân hàng', {'fields': ['bank_number', 'bank_name']}),
        ('Thông tin về sổ bảo hiểm, đối tượng miễn giảm và ưu tiên', {'fields': ['code_of_health',
                                                                                 'priority_subject',
                                                                                 'subject_of_reduction']}),
        ('Thông tin liên hệ(Bố, Mẹ, Chị/Anh/Em gái, Vợ/Chồng, Người giám hộ)',
         {'fields': ['dad_name', 'dad_birthday', 'dad_number_phone', 'dad_job'
             , 'dad_address', 'mom_name', 'mom_birthday',
                     'mom_number_phone', 'mom_job'
             , 'mom_address', 'sis_bro','my_son_daughter','wife_husband_name', 'wife_husband_birthday', 'wife_husband_number_phone', 'wife_husband_job'
             , 'wife_husband_address','tutor_name', 'tutor_birthday', 'tutor_number_phone', 'tutor_job'
             , 'tutor_address',]}),
        ('Bằng cấp', {'fields': ['certificate']}),
        ('Lớp học', {'fields': ['classroom']}),
        ('Trạng thái hoạt động và ngày tạo', {'fields': ['on_delete_flag', 'published']}),
    ]

    model = Users
    can_delete = False
    verbose_name_plural = 'Thông tin chi tiết về tài khoản đăng kí'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)


# Category
class SubCategoryTabularInLine(admin.TabularInline):
    model = SubCategory
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Icon và tên danh mục', {'fields': ['icon', 'category_name']}),
        ('Nhóm tài khoản', {'fields': ['group']}),
        ('Trạng thái hoạt động và ngày tạo', {'fields': ['on_delete_flag', 'sub_category_flag', 'published']})
    ]
    inlines = [SubCategoryTabularInLine]
    list_display = ('icon', 'category_name', 'group', 'on_delete_flag', 'sub_category_flag', 'published')


# News
class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Vấn đề và tiêu đề', {'fields': ['subject', 'title']}),
        ('Nhóm tài khoản', {'fields': ['group']}),
        ('Nộ dụng và ngày tạo', {'fields': ['content', 'published']}),
        ('File', {'fields': ['file']}),
        ('Trạng thái hoạt động', {'fields': ['on_delete_flag']}),
    ]
    list_display = ('subject', 'title', 'group', 'content', 'published', 'file', 'on_delete_flag')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


# Class
class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Mã và tên lớp học', {'fields': ['classroom_id', 'classroom_name']}),
        ('Sĩ số lớp học', {'fields': ['quantity']}),
        ('Trạng thái hoạt động và ngày tạo', {'fields': ['on_delete_flag', 'published']}),
    ]
    list_display = ('classroom_id', 'classroom_name', 'quantity', 'on_delete_flag', 'published')


# News
class ShareNewsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Vấn đề và tiêu đề', {'fields': ['subject', 'title']}),
        ('Lớp', {'fields': ['classroom']}),
        ('Nộ dụng và ngày tạo', {'fields': ['content', 'published']}),
        ('File', {'fields': ['file']}),
        ('Trạng thái hoạt động', {'fields': ['on_delete_flag','share_school_flag']}),
    ]
    list_display = ('subject', 'title', 'classroom', 'content', 'published', 'file', 'on_delete_flag','share_school_flag')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Classroom, ClassAdmin)
admin.site.register(Subject)
admin.site.register(Calendar)
admin.site.register(ShareNews, ShareNewsAdmin)
admin.site.register(Score)
admin.site.register(PlanTest)
admin.site.register(AssignedExam)
