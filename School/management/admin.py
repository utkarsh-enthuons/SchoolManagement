from django.contrib import admin

from .models import CustomUser, Teacher, Students, Subject, StudentClass, FeeStructure, FeePayment, TransactionHistory


# Register your models here.

@admin.register(CustomUser)
class UserList(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'username')


@admin.register(Teacher)
class TeacherList(admin.ModelAdmin):
    list_display = ('teacher_id', 'first_name', 'last_name', 'joining_date', 'is_active')


@admin.register(Students)
class StudentList(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'admission_class', 'father_name', 'mother_name', 'admission_class', 'phone_number', 'is_active')


@admin.register(Subject)
class SubjectList(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name', 'subject_code', 'is_active')


@admin.register(StudentClass)
class StudnetClasstList(admin.ModelAdmin):
    list_display = ('class_id', 'class_name', 'assigning_teacher', 'is_active')


@admin.register(FeeStructure)
class FeeStructureList(admin.ModelAdmin):
    list_display = ('fee_id', 'class_id', 'monthly_fee', 'first_quarter_exam_fee', 'half_year_exam_fee', 'second_quarter_exam_fee', 'annual_exam_fee')


@admin.register(FeePayment)
class FeePaymentList(admin.ModelAdmin):
    list_display = ('fee_id', 'student_id', 'class_id', 'phone_number', 'monthly_fee', 'first_quarter_exam_fee', 'half_year_exam_fee', 'second_quarter_exam_fee', 'annual_exam_fee')


@admin.register(TransactionHistory)
class TransactionHistoryList(admin.ModelAdmin):
    list_display = ('transaction_id', 'student_id', 'transaction_date', 'transaction_type', 'payment_mode', 'amount_paid', 'reference_no', 'remarks')
