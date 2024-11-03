from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.template import loader
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
import logging
from .forms import CustomLoginForm, TeacherForm, SubjectForm, StudentClassForm, StudentSearchForm, StudentForm, \
    GroupPermissionForm, FeeStructureForm, FeePaymentForm, TransactionHistoryForm
from .models import CustomUser, Teacher, Subject, StudentClass, Students, FeeStructure, FeePayment, TransactionHistory

logger = logging.getLogger(__name__)


def home(request):
    data = {
        # 'sdfsfd': sdfsf
    }
    return render(request, 'dashboard.html', data)



def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user, username, password)
            if user is not None:
                auth_login(request, user)
                return redirect('homepage')  # Redirect to a desired page after login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomLoginForm()
        print(form.errors)

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def group(request):
    groups = Group.objects.all()
    data = {
        'group': groups
    }
    # for group in groups:
    #     print(f"Group ID: {group.id} | Group Name: {group.name}")
    return render(request, 'group-list.html', data)


class group_add_view(View):
    def get(self, request):
        form = GroupPermissionForm()
        data = {'form': form}
        return render(request, 'group-add.html', data)

    def post(self, request):
        form = GroupPermissionForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New group has been created.")
            return redirect('groups')
        else:
            print("Form is not valid. Errors:", form.errors)

        data = {'form': form}
        return render(request, 'group-add.html', data)


def group_edit(request, id):
    group = get_object_or_404(Group, pk=id)
    if request.method == 'POST':
        form = GroupPermissionForm(request.POST, instance=group, group=group)
        if form.is_valid():
            form.save()  # Save the changes to the group name and permissions
            messages.success(request, "Group Permission has been updated.")
        else:
            # If form is not valid, display error messages
            messages.error(request, "There was an error updating the group. Please check the form.")
    else:
        form = GroupPermissionForm(instance=group, group=group)  # For GET requests, display the form with current values

    return render(request, 'group-edit.html', {'form': form, 'group': group})


@require_POST
def group_delete(request):
    group_id = request.POST.get('item_id')
    if group_id:
        try:
            group_item = get_object_or_404(Group, id=group_id)
            group_item.delete()
            return JsonResponse({'success': True})  # Return a success response
        except Exception as e:
            print("Exception section worked...")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response
    return JsonResponse({'success': False, 'error': 'Invalid group ID'}, status=400)


class SubjectView(View):
    def get(self, request):
        # Handle GET request
        subjects = Subject.objects.all()
        form = SubjectForm()
        context = {
            'subjects': subjects,
            'form': form
        }
        return render(request, 'subject.html', context)

    def post(self, request):
        subjects = Subject.objects.all()
        form = SubjectForm(data=request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.is_active = True
            subject.save()
            messages.success(request, "New subject has been created.")
            return redirect('subject')
        else:
            print("Form is not valid. Errors:", form.errors)
        context = {
            'subjects': subjects,
            'form': form
        }
        return render(request, 'subject.html', context)


@require_POST
def subject_delete(request):
    subject_id = request.POST.get('item_id')
    subject_item2 = get_object_or_404(Subject, subject_id=subject_id)
    print(subject_item2)
    if subject_id:
        try:
            subject_item = get_object_or_404(Subject, subject_id=subject_id)
            subject_item.delete()
            return JsonResponse({'success': True})  # Return a success response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response
    return JsonResponse({'success': False, 'error': 'Invalid subject ID'}, status=400)


def subject_edit(request):
    subject_id = request.GET.get('subject_id')
    if subject_id:
        try:
            # Use the correct model name "Subject"
            subject_data = get_object_or_404(Subject, subject_id=subject_id)
            return JsonResponse({
                'subject_id': subject_data.subject_id,
                'subject_name': subject_data.subject_name,
                'subject_code': subject_data.subject_code,
                'subject_status': subject_data.is_active
            })
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Subject not found'}, status=404)
    return JsonResponse({'error': 'Invalid Subject ID'}, status=400)

@require_POST
def subject_update(request):
    try:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')

        # Convert subject_status to a boolean value
        subject_status = request.POST.get('subject_status') == 'true'

        print(subject_code, subject_name, subject_id)

        if not subject_id or not subject_name or not subject_code:
            return JsonResponse({'success': False, 'message': 'All fields are required'}, status=400)

        try:
            subject = Subject.objects.get(subject_id=subject_id)
            # Update the subject fields
            subject.subject_name = subject_name
            subject.subject_code = subject_code
            subject.is_active = subject_status
            subject.save()

            return JsonResponse({
                'success': True,
                'message': 'Subject updated successfully',
                'subject_id': subject.subject_id,
                'subject_name': subject.subject_name,
                'subject_code': subject.subject_code,
                'subject_status': subject.is_active
            })

        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Subject not found'}, status=404)

    except Exception as e:
        logger.error(f'Error updating subject: {e}', exc_info=True)
        return JsonResponse({'success': False, 'message': 'An error occurred'}, status=500)


def TeacherList(request):
    TeacherData = Teacher.objects.all
    return render(request, 'teacher-list.html', {'Teachers': TeacherData})


class TeacherAdd(View):
    def get(self, request):
        form = TeacherForm()
        return render(request, 'teacher-add.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = TeacherForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_active = True
            teacher.save()

            # Create a CustomUser for login if required
            custom_user = CustomUser.objects.create_user(
                username=teacher.teacher_id,
                password='Teacher@123',
                user_type='teacher',
                email=teacher.email,
                phone_number=teacher.phone_number
            )
            messages.success(request, "New teacher has been created, and the user account is ready.")
            return redirect('teachers')
        else:
            print("Form is not valid. Errors:", form.errors)
        return render(request, 'teacher-add.html', {'form': form})


def TeacherDetails(request, id):
    teacher_id = get_object_or_404(Teacher, pk=id)
    return render(request, 'teacher-view.html', {'teacher_det': teacher_id})


class TeacherEdit(View):
    def get(self, request, id):
        teacher = get_object_or_404(Teacher, pk=id)
        form = TeacherForm(instance=teacher)
        return render(request, 'teacher-edit.html', {'form': form})

    @transaction.atomic
    def post(self, request, id):
        teacher = get_object_or_404(Teacher, pk=id)
        form = TeacherForm(data=request.POST, files=request.FILES, instance=teacher)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Update the teacher and CustomUser
                    teacher = form.save()

                    custom_user = teacher.user
                    custom_user.email = teacher.email
                    custom_user.phone_number = teacher.phone_number
                    custom_user.save()

                    messages.success(request, "Teacher details have been updated.")
                    return redirect('teachers')
            except Exception as e:
                form.add_error(None, f"Error saving CustomUser data: {e}")
        else:
            print("Form is not valid. Errors:", form.errors)
        return render(request, 'teacher-edit.html', {'form': form})


@require_POST
def TeacherDelete(request):
    teacher_id = request.POST.get('item_id')
    print(teacher_id)
    if teacher_id:
        try:
            teacher_item = get_object_or_404(Teacher, id=teacher_id)
            teacher_item.delete()
            return JsonResponse({'success': True})  # Return a success response
        except Exception as e:
            print("Exception section worked...")
            print(str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response
    return JsonResponse({'success': False, 'error': 'Invalid teacher ID'}, status=400)


class StudentClassView(View):
    def get(self, request):
        classes = StudentClass.objects.all().order_by('class_name')
        form = StudentClassForm()
        context = {
            'class_list': classes,
            'form': form
        }
        return render(request, 'class.html', context)

    def post(self, request):
        classes = StudentClass.objects.all()
        form = StudentClassForm(data=request.POST)
        if form.is_valid():
            classes_form = form.save(commit=False)
            classes_form.is_active = True
            classes_form.save()
            messages.success(request, "New class has been created.")
            return redirect('classes')
        else:
            print("Form is not valid. Errors:", form.errors)
        context = {
            'class_list': classes,
            'form': form
        }
        return render(request, 'class.html', context)


@require_POST
def StudentClassDelete(request):
    class_id = request.POST.get('item_id')
    class_item2 = get_object_or_404(StudentClass, class_id=class_id)
    print(class_item2)
    if class_id:
        try:
            class_item = get_object_or_404(StudentClass, class_id=class_id)
            class_item.delete()
            return JsonResponse({'success': True})  # Return a success response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response
    return JsonResponse({'success': False, 'error': 'Invalid subject ID'}, status=400)


def StudentClassEdit(request):
    class_id = request.GET.get('class_id')
    if class_id:
        try:
            class_data = get_object_or_404(StudentClass, class_id=class_id)
            assigning_teacher_id = class_data.assigning_teacher.id if class_data.assigning_teacher else ""

            return JsonResponse({
                'class_id': class_data.class_id,
                'class_name': class_data.class_name,
                'assigning_teacher': assigning_teacher_id,
                'class_status': class_data.is_active
            })
        except StudentClass.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
    return JsonResponse({'error': 'Invalid Class ID'}, status=400)


@require_POST
def StudentClassUpdate(request):
    try:
        class_id = request.POST.get('class_id')
        class_name = request.POST.get('class_name')
        assigning_teacher_id = request.POST.get('assigning_teacher')  # This is the ID
        class_status = request.POST.get('class_status') == 'true'
        print(assigning_teacher_id, class_name, class_id, class_status)

        if not class_id or not class_name or not assigning_teacher_id:
            return JsonResponse({'success': False, 'message': 'All fields are required'}, status=400)

        try:
            currentClass = StudentClass.objects.get(class_id=class_id)
            assigning_teacher = Teacher.objects.get(id=assigning_teacher_id)
            currentClass.class_name = class_name
            currentClass.assigning_teacher = assigning_teacher
            currentClass.is_active = class_status
            currentClass.save()
            return JsonResponse({
                'success': True,
                'message': 'Class updated successfully',
                'class_id': currentClass.class_id,
                'class_name': currentClass.class_name,
                'assigning_teacher': f"{assigning_teacher.first_name} {assigning_teacher.last_name}",
                'class_status': currentClass.is_active
            })

        except StudentClass.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Class not found'}, status=404)
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Teacher not found'}, status=404)

    except Exception as e:
        logger.error(f'Error updating class: {e}', exc_info=True)
        return JsonResponse({'success': False, 'message': 'An error occurred'}, status=500)


def StudentList(request):
    form = StudentSearchForm()
    StudentData = Students.objects.all
    return render(request, 'student-list.html', {'students': StudentData, 'form': form})


class StudentAdd(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'student-add.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = StudentForm(data=request.POST, files=request.FILES)
        student_data = Students.objects.all()
        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save(commit=False)
                    student.is_active = True
                    student.save()

                    messages.success(request, "New student has been created.")
                    for Student in student_data:
                        print(Student.id)
                    return redirect('students')
            except IntegrityError as e:
                if "Duplicate entry" in str(e):
                    messages.error(request, "A student with this username already exists. Please choose a unique username.")
                else:
                    messages.error(request, f"An error occurred while saving the student: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
        else:
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
        return render(request, 'student-add.html', {'form': form})


class StudentEdit(View):
    def get(self, request, id):
        student = get_object_or_404(Students, pk=id)
        form = StudentForm(instance=student)
        return render(request, 'student-edit.html', {'form': form})

    @transaction.atomic
    def post(self, request, id):
        student = get_object_or_404(Students, pk=id)
        form = StudentForm(data=request.POST, files=request.FILES, instance=student)
        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save()
                    custom_user = student.user
                    custom_user.first_name = student.first_name
                    custom_user.last_name = student.last_name
                    custom_user.save()

                    messages.success(request, "Student details have been updated.")
                    return redirect('students')
            except Exception as e:
                form.add_error(None, f"Error saving CustomUser data: {e}")
        else:
            print("Form is not valid. Errors:", form.errors)
        return render(request, 'student-edit.html', {'form': form})


def StudentDetails(request, id):
    student_id = get_object_or_404(Students, pk=id)
    return render(request, 'student-view.html', {'student_det': student_id})


@require_POST
@transaction.atomic
def StudentDelete(request):
    student_id = request.POST.get('item_id')
    if student_id:
        try:
            student_item = get_object_or_404(Students, id=student_id)
            custom_user = CustomUser.objects.filter(username=student_item.student_id).first()
            custom_user.delete()
            student_item.delete()
            return JsonResponse({'success': True})  # Return a success response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response
    return JsonResponse({'success': False, 'error': 'Invalid student ID'}, status=400)


def StudentSearchFilter(request):
    form = StudentSearchForm(request.GET or None)
    students = Students.objects.all()

    if form.is_valid():
        class_id = form.cleaned_data.get('class_id')
        phone_number = form.cleaned_data.get('phone_number')
        name = form.cleaned_data.get('name')

        query = Q()
        if class_id:
            query &= Q(admission_class_id=class_id.class_id)
        if phone_number:
            query &= Q(phone_number__icontains=phone_number)
        if name:
            students = students.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            query &= (Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(full_name__icontains=name))

        students = students.filter(query)
    student_data = list(students.values(
        'first_name', 'last_name', 'father_name', 'mother_name', 'id',
        'aadhar_number', 'admission_class__class_name', 'DOB', 'is_active'
    ))

    return JsonResponse({'students': student_data}, status=200)


def FeeStructureList(request):
    fee_structure_list = FeeStructure.objects.all
    return render(request, 'fee-structure-list.html', {'fee_structure_list': fee_structure_list})


class FeeStructureAdd(View):
    def get(self, request):
        form = FeeStructureForm()
        return render(request, 'fee-structure-add.html', {'form': form})

    def post(self, request):
        form = FeeStructureForm(data=request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.is_active = True
            form_data.save()
            messages.success(request, "New fee structure has been created.")
            return redirect('fee structure list')
        else:
            print("Form is not valid. Errors:", form.errors)
        return render(request, 'fee-structure-add.html', {'form': form})


class FeeStructureEdit(View):
    def get(self, request, fee_id):
        fee_structure_id = get_object_or_404(FeeStructure, pk=fee_id)
        form = FeeStructureForm(instance=fee_structure_id)
        return render(request, 'fee-structure-edit.html', {'form': form})

    def post(self, request, fee_id):
        fee_structure_id = get_object_or_404(FeeStructure, pk=fee_id)
        form = FeeStructureForm(data=request.POST, instance=fee_structure_id)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee Structure has been Updated.")
            return redirect('fee structure list')
        else:
            print("Form is not valid. Errors:", form.errors)
        return render(request, 'fee-structure-edit.html', {'form': form})


@require_POST
def FeeStructureDelete(request):
    fee_structure_id = request.POST.get('item_id')
    if fee_structure_id:
        try:
            fee_structure_item = get_object_or_404(FeeStructure, fee_id=fee_structure_id)
            fee_structure_item.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            print("Exception section worked...")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid fee structure ID'}, status=400)


def FeeStudentList(request):
    form = StudentSearchForm()
    StudentData = Students.objects.all
    return render(request, 'fee-payment-student-list.html', {'students': StudentData, 'form': form})


def FeeRegister(request):
    form = StudentSearchForm()
    payment_details = FeePayment.objects.all()
    fee_status_dict = {}
    months_range = range(1, 13)
    for payment in payment_details:
        fee_structure = FeeStructure.objects.get(class_id=payment.class_id)
        fee_status = {}
        fee_status['admission_fee_status'] = calculate_fee_status(int(payment.admission_fee or 0), int(fee_structure.admission_fee or 0))
        fee_status['first_quarter_exam_fee_status'] = calculate_fee_status(int(payment.first_quarter_exam_fee or 0), int(fee_structure.first_quarter_exam_fee or 0))
        fee_status['half_year_exam_fee_status'] = calculate_fee_status(int(payment.half_year_exam_fee or 0), int(fee_structure.half_year_exam_fee or 0))
        fee_status['second_quarter_exam_fee_status'] = calculate_fee_status(int(payment.second_quarter_exam_fee or 0), int(fee_structure.second_quarter_exam_fee or 0))
        fee_status['annual_exam_fee_status'] = calculate_fee_status(int(payment.annual_exam_fee or 0), int(fee_structure.annual_exam_fee or 0))
        fee_status['board_reg_fee_status'] = calculate_fee_status(int(payment.board_reg_fee or 0), int(fee_structure.board_reg_fee or 0))
        fee_status['board_fee_status'] = calculate_fee_status(int(payment.board_fee or 0), int(fee_structure.board_fee or 0))
        fee_status['admit_card_fee_status'] = calculate_fee_status(int(payment.admit_card_fee or 0), int(fee_structure.admit_card_fee or 0))
        fee_status['practical_1_fee_status'] = calculate_fee_status(int(payment.practical_1_fee or 0), int(fee_structure.practical_1_fee or 0))
        fee_status['practical_2_fee_status'] = calculate_fee_status(int(payment.practical_2_fee or 0), int(fee_structure.practical_2_fee or 0))
        fee_status['practical_3_fee_status'] = calculate_fee_status(int(payment.practical_3_fee or 0), int(fee_structure.practical_3_fee or 0))
        fee_status['practical_4_fee_status'] = calculate_fee_status(int(payment.practical_4_fee or 0), int(fee_structure.practical_4_fee or 0))
        fee_status['monthly_fee_status'] = calculate_monthly_fee_status(int(payment.monthly_fee or 0), int(fee_structure.monthly_fee or 0))
        fee_status_dict[payment.fee_id] = fee_status
    return render(request, 'fee-register.html', {'payment_details': payment_details, 'fee_status_dict': fee_status_dict, 'form': form,  'months_range': months_range})


def calculate_monthly_fee_status(total_deposited, total_monthly_fee):
    # if total_deposited is 0:
    #     total_deposited = 1
    monthly_fee = total_monthly_fee // 12
    months_paid = total_deposited // monthly_fee
    remaining_amount = total_deposited % monthly_fee
    if remaining_amount != 0:
        remaining_amount = monthly_fee - remaining_amount
    return {
        'months_paid': months_paid,
        'remaining_amount': str(remaining_amount)
    }


def calculate_fee_status(paid_amount, due_amount):
    if paid_amount == 0 and due_amount == 0:
        return ''
    elif paid_amount == due_amount:
        return "<span class='text-success font-bold'>PAID</span>"
    elif paid_amount < due_amount:
        remaining = due_amount - paid_amount
        return f"<span class='text-danger font-bold'>{remaining}</span>"
    else:
        extra_paid = paid_amount - due_amount
        return f"<span class='text-warning font-bold'>Extra paid: {extra_paid}</span>"



class FeeStudentPay(View):
    def get(self, request, id):
        FeeData = FeePayment.objects.get(fee_id=id)
        print(FeeData)
        form = FeePaymentForm()
        form_tra = TransactionHistoryForm()
        return render(request, 'fee-payment.html', {'form': form, 'form_tra': form_tra, 'FeeData': FeeData})

    def post(self, request, id):
        FeeData = FeePayment.objects.get(fee_id=id)
        try:
            existing_fee_payment = FeePayment.objects.get(fee_id=id)
        except FeePayment.DoesNotExist:
            existing_fee_payment = None

        form = FeePaymentForm(data=request.POST)
        form_tra = TransactionHistoryForm(data=request.POST)

        if form.is_valid() and form_tra.is_valid():
            fee_fields = [
                'monthly_fee', 'admission_fee', 'first_quarter_exam_fee', 'half_year_exam_fee',
                'second_quarter_exam_fee', 'annual_exam_fee', 'board_reg_fee', 'board_fee',
                'admit_card_fee', 'practical_1_fee', 'practical_2_fee', 'practical_3_fee', 'practical_4_fee'
            ]
            amount_paid = int(form_tra.cleaned_data.get('amount_paid'))
            if amount_paid <= 0:
                messages.error(request, "The total amount of fee can not be blank.")
                return render(request, 'fee-payment.html', {'form': form, 'form_tra': form_tra, 'FeeData': FeeData})
            print(amount_paid, type(amount_paid))
            if existing_fee_payment:
                for field in fee_fields:
                    current_fee = int(getattr(existing_fee_payment, field) or 0)  # Ensure it's an int
                    new_fee = int(form.cleaned_data.get(field) or 0)  # Convert to int
                    setattr(existing_fee_payment, field, current_fee + new_fee)
                existing_fee_payment.save()
            else:
                new_fee_payment = form.save(commit=False)
                for field in fee_fields:
                    new_fee = int(form.cleaned_data.get(field) or 0)  # Convert to int
                    setattr(new_fee_payment, field, new_fee)
                new_fee_payment.student = student
                new_fee_payment.save()

            transaction = form_tra.save(commit=False)
            transaction.student_id = student
            transaction.save()

            return redirect('fee payment student list')

        else:
            messages.error(request, "There was an error with the form.")
            print("Form is not valid. Errors:", form.errors, form_tra.errors)

        return render(request, 'fee-payment.html', {'form': form, 'form_tra': form_tra, 'FeeData': FeeData})


def TransactionHistoryList(request):
    TransactionData = TransactionHistory.objects.all
    return render(request, 'transactionHistory-list.html', {'TransactionDatas': TransactionData})


def TransactionHistoryDetail(request, id):
    TransactionData = get_object_or_404(TransactionHistory, transaction_id=id)
    return render(request, 'transactionHistory-detail.html', {'TransactionData': TransactionData})


