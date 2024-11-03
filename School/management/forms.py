import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm, password_validation
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission

from .models import DISTRICT_CHOICES, Teacher, Subject, StudentClass, Students, FeeStructure, TransactionHistory, \
    FeePayment

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+?1?\d{9,15}$'
password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'


class UserPasswordReset(PasswordResetForm):
    email = forms.EmailField(label=_('Email Address'), max_length=255, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}), validators=[
            RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control', 'autofocus': 'True'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html(), validators=[
            RegexValidator(regex=password_pattern,
                           message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    new_password2 = forms.CharField(label=_('Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))

    def clean_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Passwords do not match")
        return new_password2


class UserSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": _("The confirm password doesn't match with new password."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class GroupPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-control"}),
        required=False,
        label="Permissions",
        help_text="Select the permissions for the group.",
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group and isinstance(group, Group):  # Ensure 'group' is a Group instance
            self.fields['permissions'].initial = group.permissions.all()


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class TeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field in ['profile_photo', 'first_name', 'last_name', 'phone_number', 'email', 'aadhar_number', 'father_name', 'mother_name', 'gender', 'religion', 'per_city_or_village', 'per_pincode', 'per_district', 'cor_city_or_village', 'cor_pincode', 'cor_district', 'nationality', 'joining_date', 'pan_card','bank_name', 'bank_account_no', 'ifsc_code']:
            self.fields[field].required = True

        self.fields['cor_district'].choices = DISTRICT_CHOICES
        self.fields['per_district'].choices = DISTRICT_CHOICES
        self.fields['subject'].empty_label = "Select Subject"
        today = datetime.date.today()
        self.fields['joining_date'].widget.attrs.update({'max': today})
        self.fields['subject'].queryset = Subject.objects.filter(is_active=True)

    class Meta:
        model = Teacher
        fields = "__all__"
        widgets = {
            'profile_photo': forms.FileInput(attrs={'placeholder': 'Profile Photo', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'placeholder': 'Aadhar Card', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'select2'}),
            'religion': forms.Select(attrs={'class': 'select2'}),
            'father_name': forms.TextInput(attrs={'placeholder': 'Father Name', 'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'placeholder': 'Mother Name', 'class': 'form-control'}),
            'per_house_no': forms.TextInput(attrs={'placeholder': 'House Number', 'class': 'form-control'}),
            'per_landmark': forms.TextInput(attrs={'placeholder': 'Landmark', 'class': 'form-control'}),
            'per_city_or_village': forms.TextInput(attrs={'placeholder': 'City/Village', 'class': 'form-control'}),
            'per_pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-control'}),
            'per_district': forms.Select(attrs={'placeholder': 'Select District', 'class': 'select2'}),
            'cor_house_no': forms.TextInput(attrs={'placeholder': 'House Number', 'class': 'form-control'}),
            'cor_landmark': forms.TextInput(attrs={'placeholder': 'Landmark', 'class': 'form-control'}),
            'cor_city_or_village': forms.TextInput(attrs={'placeholder': 'City/Village', 'class': 'form-control'}),
            'cor_pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-control'}),
            'cor_district': forms.Select(attrs={'placeholder': 'Select District', 'class': 'select2'}),
            'subject': forms.Select(attrs={'class': 'select2'}),
            'nationality': forms.TextInput(attrs={'placeholder': 'Nationality', 'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select Joining Date', 'class': 'form-control'}),
            'pan_card': forms.TextInput(attrs={'placeholder': 'Pan Card', 'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'Bank Name', 'class': 'form-control'}),
            'bank_account_no': forms.TextInput(attrs={'placeholder': 'Account No.', 'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'placeholder': 'IFSC Code', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'placeholder': 'Active Status', 'class': 'form-control'}),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if Teacher.objects.filter(email=email).exists():
                raise ValidationError("A teacher with this email already exists.")
            return email

        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if Teacher.objects.filter(phone_number=phone_number).exists():
                raise ValidationError("A teacher with this phone number already exists.")
            return phone_number


class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['subject_name'].required = True
        self.fields['subject_code'].required = True
        self.fields['subject_name'].validators = [RegexValidator(regex=name_pattern, message="Subject name can only contain letters and spaces.")]
        self.fields['subject_code'].validators = [RegexValidator(regex='^\d{3}$', message="Please enter a valid 3-digit subject_code.")]

    class Meta:
        model = Subject
        fields = "__all__"
        widgets = {
            'subject_name': forms.TextInput(attrs={'placeholder': 'Subject name', 'class': 'form-control'}),
            'subject_code': forms.TextInput(attrs={'placeholder': 'Subject code', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'placeholder': 'Active Status', 'class': 'form-control'}),
        }


class StudentClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentClassForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].required = True
        self.fields['assigning_teacher'].required = False

        self.fields['assigning_teacher'].empty_label = "Select Teacher"
        self.fields['assigning_teacher'].queryset = Teacher.objects.filter(is_active=True)
    class Meta:
        model = StudentClass
        fields = "__all__"
        widgets = {
            'class_name': forms.TextInput(attrs={'placeholder': 'Class Name', 'class': 'form-control'}),
            'assigning_teacher': forms.Select(attrs={'class': 'select2'}),
        }


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in ['profile_photo', 'first_name', 'last_name', 'phone_number', 'email', 'aadhar_number', 'DOB', 'father_name', 'mother_name', 'gender', 'religion', 'per_city_or_village', 'per_pincode', 'per_district', 'cor_city_or_village', 'cor_pincode', 'cor_district', 'nationality', 'enrollment_date', 'admission_class', 'profile_photo']:
            self.fields[field].required = True
        self.fields['cor_district'].choices = DISTRICT_CHOICES
        self.fields['per_district'].choices = DISTRICT_CHOICES
        self.fields['admission_class'].empty_label = "Select Class"
        today = datetime.date.today()
        self.fields['enrollment_date'].widget.attrs.update({'max': today})
        self.fields['admission_class'].queryset = StudentClass.objects.filter(is_active=True)

    class Meta:
        model = Students
        fields = "__all__"
        widgets = {
            'profile_photo': forms.FileInput(attrs={'placeholder': 'Profile Photo', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
            'alternative_phone': forms.TextInput(attrs={'placeholder': 'Alternative Phone number', 'class': 'form-control'}),
            'DOB': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth', 'class': 'form-control'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of admission', 'class': 'form-control'}),
            'admission_class': forms.Select(attrs={'class': 'select2'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'placeholder': 'Aadhar Card', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'select2'}),
            'category': forms.Select(attrs={'class': 'select2'}),
            'religion': forms.Select(attrs={'class': 'select2'}),
            'father_name': forms.TextInput(attrs={'placeholder': 'Father Name', 'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'placeholder': 'Mother Name', 'class': 'form-control'}),
            'per_house_no': forms.TextInput(attrs={'placeholder': 'House Number', 'class': 'form-control'}),
            'per_landmark': forms.TextInput(attrs={'placeholder': 'Landmark', 'class': 'form-control'}),
            'per_city_or_village': forms.TextInput(attrs={'placeholder': 'City/Village', 'class': 'form-control'}),
            'per_pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-control'}),
            'per_district': forms.Select(attrs={'placeholder': 'Select District', 'class': 'select2'}),
            'cor_house_no': forms.TextInput(attrs={'placeholder': 'House Number', 'class': 'form-control'}),
            'cor_landmark': forms.TextInput(attrs={'placeholder': 'Landmark', 'class': 'form-control'}),
            'cor_city_or_village': forms.TextInput(attrs={'placeholder': 'City/Village', 'class': 'form-control'}),
            'cor_pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-control'}),
            'cor_district': forms.Select(attrs={'placeholder': 'Select District', 'class': 'select2'}),
            'nationality': forms.TextInput(attrs={'placeholder': 'Nationality', 'class': 'form-control'}),
            'Student_sign': forms.FileInput(attrs={'placeholder': 'Student Signature', 'class': 'form-control'}),
            'mother_sign': forms.FileInput(attrs={'placeholder': 'Mother\'s signature', 'class': 'form-control'}),
            'father_sign': forms.FileInput(attrs={'placeholder': 'Father\'s signature', 'class': 'form-control'}),
            'birth_certificate': forms.FileInput(attrs={'placeholder': 'Birth Certificate', 'class': 'form-control'}),
            'character_certificate': forms.FileInput(attrs={'placeholder': 'Character Certificate', 'class': 'form-control'}),
            'aadhar_card': forms.FileInput(attrs={'placeholder': 'Aadhar Card', 'class': 'form-control'}),
            'caste_certificate': forms.FileInput(attrs={'placeholder': 'Caste Certificate', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'placeholder': 'Active Status', 'class': 'form-control'}),
        }


class StudentSearchForm(forms.Form):
    class_id = forms.ModelChoiceField(
        queryset=StudentClass.objects.filter(is_active=True),  # Only active classes
        required=False, label="Class", empty_label="Select Class",
        widget=forms.Select(attrs={'class': 'select2'})
    )

    phone_number = forms.CharField(
        max_length=15, required=False, label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
        validators=[RegexValidator(regex=phone_pattern, message="Please enter a valid phone number.")])

    name = forms.CharField(
        max_length=100, required=False, label="Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid name.")])


class FeeStructureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeeStructureForm, self).__init__(*args, **kwargs)
        for field in ['monthly_fee', 'admission_fee', 'first_quarter_exam_fee', 'half_year_exam_fee', 'second_quarter_exam_fee', 'annual_exam_fee']:
            self.fields[field].required = True

        self.fields['class_id'].empty_label = "Select Class"

    class Meta:
        model = FeeStructure
        fields = "__all__"
        widgets = {
            'class_id': forms.Select(attrs={'class': 'select2'}),
            'monthly_fee': forms.TextInput(attrs={'placeholder': 'Monthly fee', 'class': 'form-control'}),
            'admission_fee': forms.TextInput(attrs={'placeholder': 'Admission fee', 'class': 'form-control'}),
            'first_quarter_exam_fee': forms.TextInput(attrs={'placeholder': 'First quarter exam fee', 'class': 'form-control'}),
            'half_year_exam_fee': forms.TextInput(attrs={'placeholder': 'Half year exam fee', 'class': 'form-control'}),
            'second_quarter_exam_fee': forms.TextInput(attrs={'placeholder': 'Second quarter exam fee', 'class': 'form-control'}),
            'annual_exam_fee': forms.TextInput(attrs={'placeholder': 'Annual exam fee', 'class': 'form-control'}),
            'board_reg_fee': forms.TextInput(attrs={'placeholder': 'Board registration fee', 'class': 'form-control'}),
            'board_fee': forms.TextInput(attrs={'placeholder': 'Board fee', 'class': 'form-control'}),
            'admit_card_fee': forms.TextInput(attrs={'placeholder': 'Admit card fee', 'class': 'form-control'}),
            'practical_1_fee': forms.TextInput(attrs={'placeholder': 'Practical 1 fee', 'class': 'form-control'}),
            'practical_2_fee': forms.TextInput(attrs={'placeholder': 'Practical 2 fee', 'class': 'form-control'}),
            'practical_3_fee': forms.TextInput(attrs={'placeholder': 'Practical 3 fee', 'class': 'form-control'}),
            'practical_4_fee': forms.TextInput(attrs={'placeholder': 'Practical 4 fee', 'class': 'form-control'}),
        }


class FeePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeePaymentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeePayment
        fields = "__all__"
        widgets = {
            'class_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'monthly_fee': forms.TextInput(attrs={'placeholder': 'Monthly fee', 'class': 'form-control'}),
            'admission_fee': forms.TextInput(attrs={'placeholder': 'Admission fee', 'class': 'form-control'}),
            'first_quarter_exam_fee': forms.TextInput(attrs={'placeholder': 'First quarter exam fee', 'class': 'form-control'}),
            'half_year_exam_fee': forms.TextInput(attrs={'placeholder': 'Half year exam fee', 'class': 'form-control'}),
            'second_quarter_exam_fee': forms.TextInput(attrs={'placeholder': 'Second quarter exam fee', 'class': 'form-control'}),
            'annual_exam_fee': forms.TextInput(attrs={'placeholder': 'Annual exam fee', 'class': 'form-control'}),
            'board_reg_fee': forms.TextInput(attrs={'placeholder': 'Board registration fee', 'class': 'form-control'}),
            'board_fee': forms.TextInput(attrs={'placeholder': 'Board fee', 'class': 'form-control'}),
            'admit_card_fee': forms.TextInput(attrs={'placeholder': 'Admit card fee', 'class': 'form-control'}),
            'practical_1_fee': forms.TextInput(attrs={'placeholder': 'Practical 1 fee', 'class': 'form-control'}),
            'practical_2_fee': forms.TextInput(attrs={'placeholder': 'Practical 2 fee', 'class': 'form-control'}),
            'practical_3_fee': forms.TextInput(attrs={'placeholder': 'Practical 3 fee', 'class': 'form-control'}),
            'practical_4_fee': forms.TextInput(attrs={'placeholder': 'Practical 4 fee', 'class': 'form-control'}),
        }


class TransactionHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionHistoryForm, self).__init__(*args, **kwargs)
        for field in ['transaction_date', 'transaction_type', 'payment_mode', 'amount_paid']:
            self.fields[field].required = True
    class Meta:
        model = TransactionHistory
        exclude = ['transaction_id']
        widgets = {
            'amount_paid': forms.HiddenInput(),
            'transaction_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Transaction Date', 'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'placeholder': 'Transaction Type', 'class': 'form-control'}),
            'payment_mode': forms.Select(attrs={'placeholder': 'Payment Mode', 'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'placeholder': 'Reference Number', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'placeholder': 'Remarks', 'class': 'form-control', 'rows': '5'}),
        }
