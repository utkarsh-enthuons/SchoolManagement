from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .decorators import unauthorized_required
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserPasswordChange, UserPasswordReset, UserSetPasswordForm

urlpatterns = [
    path('', views.home, name="homepage"),
    path('login/', views.custom_login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='change-password.html', form_class=UserPasswordChange, success_url='/passwodchangedone/'), name='passwordchange'),
    path('password-reset/', unauthorized_required(redirect_to='homepage')(auth_view.PasswordResetView.as_view(template_name='password-reset.html', form_class=UserPasswordReset)), name='password_reset'),
    path('password-reset/done/', unauthorized_required(redirect_to='homepage')(auth_view.PasswordResetDoneView.as_view(template_name='password-reset-done.html')), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', unauthorized_required(redirect_to='homepage')(auth_view.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html', form_class=UserSetPasswordForm)), name='password_reset_confirm'),
    path('password-reset-complete/', unauthorized_required(redirect_to='homepage')(auth_view.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html',)), name='password_reset_complete'),
    path('groups/', views.group, name='groups'),
    path('group-edit/<int:id>', views.group_edit, name='group_edit'),
    path('group-add/', views.group_add_view.as_view(), name='group_add'),
    path('group-delete/', views.group_delete, name='group_delete'),
    path("subjects/", views.SubjectView.as_view(), name="subject"),
    path('subject-delete/', views.subject_delete, name='subject_delete'),
    path('subject-edit/', views.subject_edit, name='subject edit'),
    path('subject-update/', views.subject_update, name='subject update'),
    path('teachers/', views.TeacherList, name='teachers'),
    path('teacher-add/', views.TeacherAdd.as_view(), name='teacher add'),
    path('teacher/view/<int:id>/', views.TeacherDetails, name='teacher_detail'),
    path('teacher/edit/<int:id>', views.TeacherEdit.as_view(), name='teacher edit'),
    path('teacher-delete/', views.TeacherDelete, name='teacher_delete'),
    path('classes/', views.StudentClassView.as_view(), name='classes'),
    path('class-delete/', views.StudentClassDelete, name='class_delete'),
    path('class-edit/', views.StudentClassEdit, name='class_edit'),
    path('class-update/', views.StudentClassUpdate, name='class_update'),
    path('students/', views.StudentList, name='students'),
    path('student-add/', views.StudentAdd.as_view(), name='student add'),
    path('student/edit/<int:id>/', views.StudentEdit.as_view(), name='student edit'),
    path('student/view/<int:id>/', views.StudentDetails, name='student_detail'),
    path('student-delete/', views.StudentDelete, name='student_delete'),
    path('student-search/', views.StudentSearchFilter, name='student search'),
    path('fee-structure/', views.FeeStructureList, name='fee structure list'),
    path('fee-structure-add/', views.FeeStructureAdd.as_view(), name='fee structure add'),
    path('fee-structure/edit/<int:fee_id>', views.FeeStructureEdit.as_view(), name='fee structure edit'),
    path('fee-structure-delete/', views.FeeStructureDelete, name='fee structure delete'),
    path('fee-payment-student-list/', views.FeeStudentList, name='fee payment student list'),
    path('fee-payment/<int:id>/', views.FeeStudentPay.as_view(), name='fee payment'),
    path('transaction-history/', views.TransactionHistoryList, name='transaction history'),
    path('transaction-history/detail/<int:id>/', views.TransactionHistoryDetail, name='transaction history detail'),
    path('fee-register/', views.FeeRegister, name='fee register'),
    path('change-password/', auth_view.PasswordChangeView.as_view(template_name='change-password.html', form_class=UserPasswordChange), name='change_password'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
