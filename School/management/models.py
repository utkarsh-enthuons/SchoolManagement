from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.core.validators import MinValueValidator

# Create your models here.
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
phone_pattern = r'^[6-9]\d{9}$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
pan_card = '^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
# Define choices for districts in Uttar Pradesh
DISTRICT_CHOICES = [
    ('', 'Select District'),
    ('Agra', 'Agra'),
    ('Aligarh', 'Aligarh'),
    ('Ambedkar Nagar', 'Ambedkar Nagar'),
    ('Amethi (Chatrapati Sahuji Mahraj Nagar)', 'Amethi (Chatrapati Sahuji Mahraj Nagar)'),
    ('Amroha (J.P. Nagar)', 'Amroha (J.P. Nagar)'),
    ('Auraiya', 'Auraiya'),
    ('Ayodhya (Faizabad)', 'Ayodhya (Faizabad)'),
    ('Azamgarh', 'Azamgarh'),
    ('Badaun', 'Badaun'),
    ('Baghpat', 'Baghpat'),
    ('Bahraich', 'Bahraich'),
    ('Ballia', 'Ballia'),
    ('Balrampur', 'Balrampur'),
    ('Banda', 'Banda'),
    ('Barabanki', 'Barabanki'),
    ('Bareilly', 'Bareilly'),
    ('Basti', 'Basti'),
    ('Bhadohi (Sant Ravidas Nagar)', 'Bhadohi (Sant Ravidas Nagar)'),
    ('Bijnor', 'Bijnor'),
    ('Budaun', 'Budaun'),
    ('Bulandshahr', 'Bulandshahr'),
    ('Chandauli', 'Chandauli'),
    ('Chitrakoot', 'Chitrakoot'),
    ('Deoria', 'Deoria'),
    ('Etah', 'Etah'),
    ('Etawah', 'Etawah'),
    ('Farrukhabad', 'Farrukhabad'),
    ('Fatehpur', 'Fatehpur'),
    ('Firozabad', 'Firozabad'),
    ('Gautam Buddh Nagar (Noida)', 'Gautam Buddh Nagar (Noida)'),
    ('Ghaziabad', 'Ghaziabad'),
    ('Ghazipur', 'Ghazipur'),
    ('Gonda', 'Gonda'),
    ('Gorakhpur', 'Gorakhpur'),
    ('Hamirpur', 'Hamirpur'),
    ('Hapur (Panchsheel Nagar)', 'Hapur (Panchsheel Nagar)'),
    ('Hardoi', 'Hardoi'),
    ('Hathras (Mahamaya Nagar)', 'Hathras (Mahamaya Nagar)'),
    ('Jalaun (Orai)', 'Jalaun (Orai)'),
    ('Jaunpur', 'Jaunpur'),
    ('Jhansi', 'Jhansi'),
    ('Kannauj', 'Kannauj'),
    ('Kanpur Dehat (Rama Bai Nagar)', 'Kanpur Dehat (Rama Bai Nagar)'),
    ('Kanpur Nagar', 'Kanpur Nagar'),
    ('Kasganj', 'Kasganj'),
    ('Kaushambi', 'Kaushambi'),
    ('Kheri (Lakhimpur Kheri)', 'Kheri (Lakhimpur Kheri)'),
    ('Kushinagar (Padrauna)', 'Kushinagar (Padrauna)'),
    ('Lalitpur', 'Lalitpur'),
    ('Lucknow', 'Lucknow'),
    ('Maharajganj', 'Maharajganj'),
    ('Mahoba', 'Mahoba'),
    ('Mainpuri', 'Mainpuri'),
    ('Mathura', 'Mathura'),
    ('Mau', 'Mau'),
    ('Meerut', 'Meerut'),
    ('Mirzapur', 'Mirzapur'),
    ('Moradabad', 'Moradabad'),
    ('Muzaffarnagar', 'Muzaffarnagar'),
    ('Pilibhit', 'Pilibhit'),
    ('Pratapgarh', 'Pratapgarh'),
    ('Prayagraj (Allahabad)', 'Prayagraj (Allahabad)'),
    ('Raebareli', 'Raebareli'),
    ('Rampur', 'Rampur'),
    ('Saharanpur', 'Saharanpur'),
    ('Sambhal (Bhim Nagar)', 'Sambhal (Bhim Nagar)'),
    ('Sant Kabir Nagar', 'Sant Kabir Nagar'),
    ('Shahjahanpur', 'Shahjahanpur'),
    ('Shamli (Prabuddh Nagar)', 'Shamli (Prabuddh Nagar)'),
    ('Shrawasti', 'Shrawasti'),
    ('Siddharthnagar', 'Siddharthnagar'),
    ('Sitapur', 'Sitapur'),
    ('Sonbhadra', 'Sonbhadra'),
    ('Sultanpur', 'Sultanpur'),
    ('Unnao', 'Unnao'),
    ('Varanasi', 'Varanasi')
]
GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]
RELIGION_CHOICES = [
    ('Hinduism', 'Hinduism'),
    ('Islam', 'Islam'),
    ('Christianity', 'Christianity'),
    ('Sikhism', 'Sikhism'),
    ('Buddhism', 'Buddhism'),
    ('Jainism', 'Jainism'),
    ('Zoroastrianism', 'Zoroastrianism'),
    ('Judaism', 'Judaism'),
    ('Others', 'Others'),
]
CATEGORY_CHOICES = [
    ('General', 'General'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
]
TRANSACTION_TYPE = [
    ('Fee Pay', 'Fee Payment'),
    ('Vehicle Pay', 'Vehicle Fee'),
    ('Exam Fee', 'Exam Fee'),
    ('Admission Fee', 'Admission Fee'),
]
PAYMENT_MODE = [
    ('Cash', 'Cash'),
    ('Credit Card', 'Credit Card'),
    ('Debit Card', 'Debit Card'),
    ('Net Banking', 'Net Banking'),
    ('UPI', 'UPI')
]


class CustomUser(AbstractUser):
    # email = models.EmailField(unique=True)
    teacher = models.OneToOneField('Teacher', null=True, blank=True, on_delete=models.SET_NULL, related_name='user')
    student = models.OneToOneField('Students', null=True, blank=True, on_delete=models.SET_NULL, related_name='user')
    # staff = models.OneToOneField('Staff', null=True, blank=True, on_delete=models.SET_NULL, related_name='user')
    # admin = models.OneToOneField('Admin', null=True, blank=True, on_delete=models.SET_NULL, related_name='user')
    user_type = models.CharField(max_length=10, choices=[('teacher', 'Teacher'), ('student', 'Student'), ('staff', 'Staff'), ('admin', 'Admin')], blank=False)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True, serialize=False)
    subject_name = models.CharField(max_length=64, validators=[RegexValidator(message='Please enter a valid subject name.',regex=name_pattern)], verbose_name='Subject Name')
    subject_code = models.CharField(max_length=3, unique=True, validators=[RegexValidator(regex='^\d{3}$', message="Please enter a valid 3-digit subject_code.")], verbose_name='Subject Code')
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    def __str__(self):
        return self.subject_name


class PersonBase(models.Model):
    profile_photo = models.ImageField(
        verbose_name=_('Profile Image'),
        upload_to='profile/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=False,
        default=''
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name='First Name',
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid first name.")],
        blank=False
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name='Last Name',
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid last name.")],
        blank=False
    )
    phone_number = models.CharField(
        max_length=10,
        unique=False,
        validators=[RegexValidator(regex=phone_pattern, message="Please enter a valid mobile number.")],
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=64,
        unique=False,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=email_pattern, message="Please enter a valid email address.")]
    )
    aadhar_number = models.CharField(
        max_length=12,
        verbose_name=_('Aadhar Card'),
        unique=True,
        blank=False,
        null=False,
        default='',
        validators=[RegexValidator(regex='^\d{12}$', message="Please enter a valid 12-digit aadhar card number.")]
    )
    mother_name = models.CharField(
        max_length=64,
        verbose_name='Mother Name',
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid mother name.")],
        blank=False,
        db_default=''
    )
    father_name = models.CharField(
        max_length=64,
        verbose_name='Father Name',
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid father name.")],
        blank=False,
        db_default=''
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        verbose_name=_('Gender'),
        blank=False,
        default='M'
    )
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        verbose_name=_('Category'),
        blank=False,
        default='General'
    )
    religion = models.CharField(
        max_length=15,
        choices=RELIGION_CHOICES,
        verbose_name=_('Religion'),
        blank=False,
        default='Hinduism'
    )
    per_house_no = models.CharField(
        max_length=20,
        verbose_name=_('House No'),
        blank=True,
    )
    per_landmark = models.CharField(
        max_length=100,
        verbose_name=_('Landmark'),
        blank=True,  # Optional
    )
    per_city_or_village = models.CharField(
        max_length=64,
        verbose_name=_('City/Village'),
        blank=False
    )
    per_pincode = models.CharField(
        max_length=6,
        verbose_name=_('Pincode'),
        blank=False,
        validators=[RegexValidator(regex='^\d{6}$', message="Please enter a valid 6-digit pincode.")],
        default=''
    )
    per_district = models.CharField(
        max_length=50,
        verbose_name=_('District'),
        choices=DISTRICT_CHOICES,
        blank=False,
        default=''
    )
    per_state = models.CharField(
        max_length=50,
        verbose_name=_('State'),
        blank=False,
        default="Uttar Pradesh",
        editable=False
    )
    cor_house_no = models.CharField(
        max_length=20,
        verbose_name=_('House No'),
        blank=True,
    )
    cor_landmark = models.CharField(
        max_length=100,
        verbose_name=_('Landmark'),
        blank=True,  # Optional
    )
    cor_city_or_village = models.CharField(
        max_length=64,
        verbose_name=_('City/Village'),
        blank=False,
        default=''
    )
    cor_pincode = models.CharField(
        max_length=6,
        verbose_name=_('Pincode'),
        blank=False,
        validators=[RegexValidator(regex='^\d{6}$', message="Please enter a valid 6-digit pincode.")],
        default=''
    )
    cor_district = models.CharField(
        max_length=50,
        verbose_name=_('District'),
        choices=DISTRICT_CHOICES,
        blank=False,
        default=''
    )
    cor_state = models.CharField(
        max_length=50,
        verbose_name=_('State'),
        blank=False,
        default="Uttar Pradesh",
        editable=False
    )
    nationality = models.CharField(
        max_length=50,
        verbose_name=_('Nationality'),
        blank=False,
        default='INDIAN'
    )

    class Meta:
        abstract = True  # This ensures no table is created for this model

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(PersonBase):
    teacher_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_('Teacher ID')
    )
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        max_length=64,
        unique=True,
        blank=False,
        null=False,
    )
    joining_date = models.DateField(
        verbose_name=_('Joining Date'),
        default=date.today,
        blank=False
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    pan_card = models.CharField(
        max_length=10,
        verbose_name=_('Pan Card'),
        unique=True,
        blank=False,
        validators=[RegexValidator(regex=pan_card, message="Please enter a valid pan card number. The pancard number should be in capital letters.")],
        help_text='The pancard should be in capital letters.',
        db_default=''
    )
    bank_name = models.CharField(
        max_length=64,
        verbose_name=_("Bank Name"),
        blank=False,
        validators=[RegexValidator(regex=name_pattern, message="Please enter a valid back name.")],
        db_default=''
    )
    bank_account_no = models.CharField(
        max_length=20,
        verbose_name=_("Account No."),
        blank=False,
        validators=[RegexValidator(regex="^\d+$", message="Please enter a valid account number.")],
        db_default=''
    )
    ifsc_code = models.CharField(
        max_length=11,
        verbose_name=_("IFSC Code"),
        blank=False,
        help_text='The IFSC Card should be in capital letters.',
        validators=[RegexValidator(regex='^[A-Z]{4}0[A-Z0-9]{6}$', message="Please enter a valid IFSC code. The IFSC code should be in capital letters.")],
        db_default=''
    )
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)  # Save the teacher and assign primary key (PK)

        if not self.teacher_id:
            today = date.today()
            current_year = today.strftime("%Y")
            current_month = today.strftime("%m")
            current_day = today.strftime("%d")
            daily_count = Teacher.objects.filter(joining_date=today).count() + 1
            self.teacher_id = f"teacher_{current_year}{current_month}{current_day}{daily_count}{self.phone_number}"
            super().save(update_fields=['teacher_id'])

        # Create a related CustomUser if not already existing
        if not hasattr(self, 'user'):  # Check if the CustomUser is already created
            custom_user = CustomUser.objects.create_user(
                username=self.teacher_id,
                phone_number=self.phone_number,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                is_staff=True,
                password='Teacher@123',  # Default password
                user_type='teacher',  # Set the user type
                teacher=self  # Link to this teacher
            )
            teacher_group, created = Group.objects.get_or_create(name='Teacher')
            custom_user.groups.add(teacher_group)

        super().save(*args, **kwargs)  # Final save

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class StudentClass(models.Model):
    class_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_('Class ID'),
        primary_key=True
    )
    class_name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("Class Name"),
        default=""
    )
    assigning_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    def save(self, *args, **kwargs):
        # Check if the assigned teacher is inactive
        if self.assigning_teacher and not self.assigning_teacher.is_active:
            # If teacher is inactive, remove them from the class
            self.assigning_teacher = None

        # Automatically generate class_id based on class_name if it is not set
        if not self.class_id:
            self.class_id = f"{self.class_name}_class"

        # Call the parent class's save method to save the model
        super(StudentClass, self).save(*args, **kwargs)

    def __str__(self):
        return self.class_name


class Students(PersonBase):
    student_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_('Student ID')
    )
    phone_number = models.CharField(
        max_length=10,
        unique=False,
        blank=False
    )
    email = models.EmailField(
        max_length=64,
        unique=False,
        blank=False,
    )
    DOB = models.DateField(
        max_length=10,
        verbose_name=_("Date of Birth"),
        blank=False,
        default=''
    )
    enrollment_date = models.DateField(
        max_length=10,
        verbose_name=_("Admission Date"),
        blank=False,
        default=date.today,
    )
    admission_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    alternative_phone = models.CharField(
        max_length=10,
        unique=False,
        validators=[RegexValidator(regex=phone_pattern, message="Please enter a valid mobile number.")],
        blank=True,
        null=True
    )
    profile_photo = models.ImageField(
        verbose_name=_('Student Photo'),
        upload_to='profile/student/photo/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=False,
        default='profile/student/photo/user.png'
    )
    Student_sign = models.ImageField(
        verbose_name=_('Student Signature'),
        upload_to='profile/student/signature/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    mother_sign = models.ImageField(
        verbose_name=_('Mother Signature'),
        upload_to='profile/student/parent_signature/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    father_sign = models.ImageField(
        verbose_name=_('Father Signature'),
        upload_to='profile/student/parent_signature/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    birth_certificate = models.ImageField(
        verbose_name=_('Birth Certificate'),
        upload_to='profile/student/certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    character_certificate = models.ImageField(
        verbose_name=_('Character Certificate'),
        upload_to='profile/student/certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    aadhar_card = models.ImageField(
        verbose_name=_('Aadhar Card'),
        upload_to='profile/student/certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    caste_certificate = models.ImageField(
        verbose_name=_('Caste Certificate'),
        upload_to='profile/student/certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        default=''
    )
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)  # Save the teacher and assign primary key (PK)

        if not self.student_id:
            today = date.today()
            current_year = today.strftime("%Y")
            current_month = today.strftime("%m")
            current_day = today.strftime("%d")
            daily_count = Students.objects.filter(enrollment_date=today).count() + 1
            self.student_id = f"student_{current_year}{current_month}{current_day}{daily_count}{self.phone_number}"
            super().save(update_fields=['student_id'])

        # Create a related CustomUser if not already existing
        if not hasattr(self, 'user'):  # Check if the CustomUser is already created
            custom_user = CustomUser.objects.create_user(
                username=self.student_id,
                first_name=self.first_name,
                last_name=self.last_name,
                is_staff=True,
                password='Student@123',  # Default password
                user_type='student',  # Set the user type
                student=self  # Link to this teacher
            )
            student_group, created = Group.objects.get_or_create(name='Student')
            custom_user.groups.add(student_group)

        super().save(*args, **kwargs)  # Final save

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class FeeStructure(models.Model):
    fee_id = models.AutoField(primary_key=True, serialize=True)
    class_id = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    monthly_fee = models.CharField(
        max_length=5,
        verbose_name=_('Total Monthly Fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    admission_fee = models.CharField(
        max_length=5,
        verbose_name=_('Admission Fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    first_quarter_exam_fee = models.CharField(
        max_length=5,
        verbose_name=_('First quarter exam fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    half_year_exam_fee = models.CharField(
        max_length=5,
        verbose_name=_('Half year exam fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    second_quarter_exam_fee = models.CharField(
        max_length=5,
        verbose_name=_('Second quarter exam fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    annual_exam_fee = models.CharField(
        max_length=5,
        verbose_name=_('Annual year exam fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    board_reg_fee = models.CharField(
        max_length=5,
        verbose_name=_('Board registration fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    board_fee = models.CharField(
        max_length=5,
        verbose_name=_('Board fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    admit_card_fee = models.CharField(
        max_length=5,
        verbose_name=_('Admit card fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    practical_1_fee = models.CharField(
        max_length=5,
        verbose_name=_('Practical 1 fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    practical_2_fee = models.CharField(
        max_length=5,
        verbose_name=_('Practical 2 fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    practical_3_fee = models.CharField(
        max_length=5,
        verbose_name=_('Practical 3 fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    practical_4_fee = models.CharField(
        max_length=5,
        verbose_name=_('Practical 4 fee'),
        validators=[RegexValidator(regex='^\d+$', message="Please enter a valid fee amount.")],
        blank=True,
    )
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    def __str__(self):
        return self.class_id
    class Meta:
        verbose_name = 'Fee Structure Detail'
        verbose_name_plural = 'Fee Structure Details'


class FeePayment(models.Model):
    fee_id = models.AutoField(primary_key=True, serialize=True)
    student_id = models.ForeignKey(Students, on_delete=models.PROTECT)
    class_id = models.ForeignKey(StudentClass, on_delete=models.CASCADE)

    phone_number = models.CharField(
        max_length=10,
        verbose_name=_('Phone Number'),
        validators=[RegexValidator(regex=phone_pattern, message="Please enter a valid phone number.")],
        blank=True,
        default='0'
    )

    monthly_fee = models.IntegerField(
        verbose_name=_('Monthly Fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    admission_fee = models.IntegerField(
        verbose_name=_('Admission Fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    first_quarter_exam_fee = models.IntegerField(
        verbose_name=_('First quarter exam fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    half_year_exam_fee = models.IntegerField(
        verbose_name=_('Half year exam fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    second_quarter_exam_fee = models.IntegerField(
        verbose_name=_('Second quarter exam fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    annual_exam_fee = models.IntegerField(
        verbose_name=_('Annual year exam fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    board_reg_fee = models.IntegerField(
        verbose_name=_('Board registration fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    board_fee = models.IntegerField(
        verbose_name=_('Board fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    admit_card_fee = models.IntegerField(
        verbose_name=_('Admit card fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    practical_1_fee = models.IntegerField(
        verbose_name=_('Practical 1 fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    practical_2_fee = models.IntegerField(
        verbose_name=_('Practical 2 fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    practical_3_fee = models.IntegerField(
        verbose_name=_('Practical 3 fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    practical_4_fee = models.IntegerField(
        verbose_name=_('Practical 4 fee'),
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return f"{self.student_id.first_name} {self.student_id.last_name}"

    class Meta:
        verbose_name = 'Fee Payment Detail'
        verbose_name_plural = 'Fee Payment Details'


class TransactionHistory(models.Model):
    transaction_id = models.CharField(
        max_length=20,
        primary_key=True,
        unique=True,
        serialize=True,
        blank=False
    )
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(verbose_name=_('Transaction Date'), blank=False, default=timezone.now)
    transaction_type = models.CharField(
        max_length=50,
        verbose_name=_('Transaction Type'),
        choices=TRANSACTION_TYPE,
        blank=False,
        default='Fee Pay'
    )
    payment_mode = models.CharField(
        max_length=50,
        verbose_name=_('Payment Mode'),
        choices=PAYMENT_MODE,
        blank=False,
        default='Cash'
    )
    amount_paid = models.CharField(
        max_length=50,
        verbose_name=_('Paid Amount'),
        blank=False,
        default=0,
    )
    reference_no = models.CharField(
        max_length= 10,
        verbose_name=_('Reference Number'),
        blank=True,
        default=''
    )
    remarks = models.TextField(
        verbose_name=_('Remarks'),
        blank=True,
        default=''
    )
    def __str__(self):
        return f"{self.student_id.first_name} {self.student_id.last_name}"

    class Meta:
        verbose_name = 'Transaction History'
        verbose_name_plural = 'Transaction Histories'

    def generate_fee_id(self):
        current_date = timezone.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        today_fees_count = TransactionHistory.objects.filter(
            transaction_date__year=year,
            transaction_date__month=month,
            transaction_date__day=day
        ).count() + 1
        fee_id = f'{year}{month:02d}{day:02d}{today_fees_count:03d}'
        return fee_id

    def save(self, *args, **kwargs):
        if not self.transaction_id:  # Generate transaction_id only if not present
            self.transaction_id = self.generate_fee_id()
        super().save(*args, **kwargs)
