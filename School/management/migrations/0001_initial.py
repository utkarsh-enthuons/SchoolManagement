# Generated by Django 5.1.2 on 2024-10-23 00:09

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('teacher_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('student_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('staff_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_staff_member', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(default='', upload_to='profile/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], verbose_name='Profile Image')),
                ('first_name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='Please enter a valid first name.', regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$')], verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='Please enter a valid last name.', regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$')], verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=64, null=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid email address.', regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')])),
                ('aadhar_number', models.CharField(default='', max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid 12-digit aadhar card number.', regex='^\\d{12}$')], verbose_name='Aadhar Card')),
                ('mother_name', models.CharField(db_default='', max_length=64, validators=[django.core.validators.RegexValidator(message='Please enter a valid mother name.', regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$')], verbose_name='Mother Name')),
                ('father_name', models.CharField(db_default='', max_length=64, validators=[django.core.validators.RegexValidator(message='Please enter a valid father name.', regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$')], verbose_name='Father Name')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='M', max_length=6, verbose_name='Gender')),
                ('category', models.CharField(choices=[('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], default='General', max_length=15, verbose_name='Category')),
                ('religion', models.CharField(choices=[('Hinduism', 'Hinduism'), ('Islam', 'Islam'), ('Christianity', 'Christianity'), ('Sikhism', 'Sikhism'), ('Buddhism', 'Buddhism'), ('Jainism', 'Jainism'), ('Zoroastrianism', 'Zoroastrianism'), ('Judaism', 'Judaism'), ('Others', 'Others')], default='Hinduism', max_length=15, verbose_name='Religion')),
                ('per_house_no', models.CharField(blank=True, max_length=20, verbose_name='House No')),
                ('per_landmark', models.CharField(blank=True, max_length=100, verbose_name='Landmark')),
                ('per_city_or_village', models.CharField(max_length=64, verbose_name='City/Village')),
                ('per_pincode', models.CharField(default='', max_length=6, validators=[django.core.validators.RegexValidator(message='Please enter a valid 6-digit pincode.', regex='^\\d{6}$')], verbose_name='Pincode')),
                ('per_district', models.CharField(choices=[('', 'Select District'), ('Agra', 'Agra'), ('Aligarh', 'Aligarh'), ('Ambedkar Nagar', 'Ambedkar Nagar'), ('Amethi (Chatrapati Sahuji Mahraj Nagar)', 'Amethi (Chatrapati Sahuji Mahraj Nagar)'), ('Amroha (J.P. Nagar)', 'Amroha (J.P. Nagar)'), ('Auraiya', 'Auraiya'), ('Ayodhya (Faizabad)', 'Ayodhya (Faizabad)'), ('Azamgarh', 'Azamgarh'), ('Badaun', 'Badaun'), ('Baghpat', 'Baghpat'), ('Bahraich', 'Bahraich'), ('Ballia', 'Ballia'), ('Balrampur', 'Balrampur'), ('Banda', 'Banda'), ('Barabanki', 'Barabanki'), ('Bareilly', 'Bareilly'), ('Basti', 'Basti'), ('Bhadohi (Sant Ravidas Nagar)', 'Bhadohi (Sant Ravidas Nagar)'), ('Bijnor', 'Bijnor'), ('Budaun', 'Budaun'), ('Bulandshahr', 'Bulandshahr'), ('Chandauli', 'Chandauli'), ('Chitrakoot', 'Chitrakoot'), ('Deoria', 'Deoria'), ('Etah', 'Etah'), ('Etawah', 'Etawah'), ('Farrukhabad', 'Farrukhabad'), ('Fatehpur', 'Fatehpur'), ('Firozabad', 'Firozabad'), ('Gautam Buddh Nagar (Noida)', 'Gautam Buddh Nagar (Noida)'), ('Ghaziabad', 'Ghaziabad'), ('Ghazipur', 'Ghazipur'), ('Gonda', 'Gonda'), ('Gorakhpur', 'Gorakhpur'), ('Hamirpur', 'Hamirpur'), ('Hapur (Panchsheel Nagar)', 'Hapur (Panchsheel Nagar)'), ('Hardoi', 'Hardoi'), ('Hathras (Mahamaya Nagar)', 'Hathras (Mahamaya Nagar)'), ('Jalaun (Orai)', 'Jalaun (Orai)'), ('Jaunpur', 'Jaunpur'), ('Jhansi', 'Jhansi'), ('Kannauj', 'Kannauj'), ('Kanpur Dehat (Rama Bai Nagar)', 'Kanpur Dehat (Rama Bai Nagar)'), ('Kanpur Nagar', 'Kanpur Nagar'), ('Kasganj', 'Kasganj'), ('Kaushambi', 'Kaushambi'), ('Kheri (Lakhimpur Kheri)', 'Kheri (Lakhimpur Kheri)'), ('Kushinagar (Padrauna)', 'Kushinagar (Padrauna)'), ('Lalitpur', 'Lalitpur'), ('Lucknow', 'Lucknow'), ('Maharajganj', 'Maharajganj'), ('Mahoba', 'Mahoba'), ('Mainpuri', 'Mainpuri'), ('Mathura', 'Mathura'), ('Mau', 'Mau'), ('Meerut', 'Meerut'), ('Mirzapur', 'Mirzapur'), ('Moradabad', 'Moradabad'), ('Muzaffarnagar', 'Muzaffarnagar'), ('Pilibhit', 'Pilibhit'), ('Pratapgarh', 'Pratapgarh'), ('Prayagraj (Allahabad)', 'Prayagraj (Allahabad)'), ('Raebareli', 'Raebareli'), ('Rampur', 'Rampur'), ('Saharanpur', 'Saharanpur'), ('Sambhal (Bhim Nagar)', 'Sambhal (Bhim Nagar)'), ('Sant Kabir Nagar', 'Sant Kabir Nagar'), ('Shahjahanpur', 'Shahjahanpur'), ('Shamli (Prabuddh Nagar)', 'Shamli (Prabuddh Nagar)'), ('Shrawasti', 'Shrawasti'), ('Siddharthnagar', 'Siddharthnagar'), ('Sitapur', 'Sitapur'), ('Sonbhadra', 'Sonbhadra'), ('Sultanpur', 'Sultanpur'), ('Unnao', 'Unnao'), ('Varanasi', 'Varanasi')], default='', max_length=50, verbose_name='District')),
                ('per_state', models.CharField(default='Uttar Pradesh', editable=False, max_length=50, verbose_name='State')),
                ('cor_house_no', models.CharField(blank=True, max_length=20, verbose_name='House No')),
                ('cor_landmark', models.CharField(blank=True, max_length=100, verbose_name='Landmark')),
                ('cor_city_or_village', models.CharField(default='', max_length=64, verbose_name='City/Village')),
                ('cor_pincode', models.CharField(default='', max_length=6, validators=[django.core.validators.RegexValidator(message='Please enter a valid 6-digit pincode.', regex='^\\d{6}$')], verbose_name='Pincode')),
                ('cor_district', models.CharField(choices=[('', 'Select District'), ('Agra', 'Agra'), ('Aligarh', 'Aligarh'), ('Ambedkar Nagar', 'Ambedkar Nagar'), ('Amethi (Chatrapati Sahuji Mahraj Nagar)', 'Amethi (Chatrapati Sahuji Mahraj Nagar)'), ('Amroha (J.P. Nagar)', 'Amroha (J.P. Nagar)'), ('Auraiya', 'Auraiya'), ('Ayodhya (Faizabad)', 'Ayodhya (Faizabad)'), ('Azamgarh', 'Azamgarh'), ('Badaun', 'Badaun'), ('Baghpat', 'Baghpat'), ('Bahraich', 'Bahraich'), ('Ballia', 'Ballia'), ('Balrampur', 'Balrampur'), ('Banda', 'Banda'), ('Barabanki', 'Barabanki'), ('Bareilly', 'Bareilly'), ('Basti', 'Basti'), ('Bhadohi (Sant Ravidas Nagar)', 'Bhadohi (Sant Ravidas Nagar)'), ('Bijnor', 'Bijnor'), ('Budaun', 'Budaun'), ('Bulandshahr', 'Bulandshahr'), ('Chandauli', 'Chandauli'), ('Chitrakoot', 'Chitrakoot'), ('Deoria', 'Deoria'), ('Etah', 'Etah'), ('Etawah', 'Etawah'), ('Farrukhabad', 'Farrukhabad'), ('Fatehpur', 'Fatehpur'), ('Firozabad', 'Firozabad'), ('Gautam Buddh Nagar (Noida)', 'Gautam Buddh Nagar (Noida)'), ('Ghaziabad', 'Ghaziabad'), ('Ghazipur', 'Ghazipur'), ('Gonda', 'Gonda'), ('Gorakhpur', 'Gorakhpur'), ('Hamirpur', 'Hamirpur'), ('Hapur (Panchsheel Nagar)', 'Hapur (Panchsheel Nagar)'), ('Hardoi', 'Hardoi'), ('Hathras (Mahamaya Nagar)', 'Hathras (Mahamaya Nagar)'), ('Jalaun (Orai)', 'Jalaun (Orai)'), ('Jaunpur', 'Jaunpur'), ('Jhansi', 'Jhansi'), ('Kannauj', 'Kannauj'), ('Kanpur Dehat (Rama Bai Nagar)', 'Kanpur Dehat (Rama Bai Nagar)'), ('Kanpur Nagar', 'Kanpur Nagar'), ('Kasganj', 'Kasganj'), ('Kaushambi', 'Kaushambi'), ('Kheri (Lakhimpur Kheri)', 'Kheri (Lakhimpur Kheri)'), ('Kushinagar (Padrauna)', 'Kushinagar (Padrauna)'), ('Lalitpur', 'Lalitpur'), ('Lucknow', 'Lucknow'), ('Maharajganj', 'Maharajganj'), ('Mahoba', 'Mahoba'), ('Mainpuri', 'Mainpuri'), ('Mathura', 'Mathura'), ('Mau', 'Mau'), ('Meerut', 'Meerut'), ('Mirzapur', 'Mirzapur'), ('Moradabad', 'Moradabad'), ('Muzaffarnagar', 'Muzaffarnagar'), ('Pilibhit', 'Pilibhit'), ('Pratapgarh', 'Pratapgarh'), ('Prayagraj (Allahabad)', 'Prayagraj (Allahabad)'), ('Raebareli', 'Raebareli'), ('Rampur', 'Rampur'), ('Saharanpur', 'Saharanpur'), ('Sambhal (Bhim Nagar)', 'Sambhal (Bhim Nagar)'), ('Sant Kabir Nagar', 'Sant Kabir Nagar'), ('Shahjahanpur', 'Shahjahanpur'), ('Shamli (Prabuddh Nagar)', 'Shamli (Prabuddh Nagar)'), ('Shrawasti', 'Shrawasti'), ('Siddharthnagar', 'Siddharthnagar'), ('Sitapur', 'Sitapur'), ('Sonbhadra', 'Sonbhadra'), ('Sultanpur', 'Sultanpur'), ('Unnao', 'Unnao'), ('Varanasi', 'Varanasi')], default='', max_length=50, verbose_name='District')),
                ('cor_state', models.CharField(default='Uttar Pradesh', editable=False, max_length=50, verbose_name='State')),
                ('nationality', models.CharField(default='INDIAN', max_length=50, verbose_name='Nationality')),
                ('teacher_id', models.CharField(editable=False, max_length=50, unique=True, verbose_name='Teacher ID')),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('joining_date', models.DateField(default=datetime.date.today, verbose_name='Joining Date')),
                ('pan_card', models.CharField(db_default='', help_text='The pancard should be in capital letters.', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid pan card number. The pancard number should be in capital letters.', regex='^[A-Z]{5}[0-9]{4}[A-Z]{1}$')], verbose_name='Pan Card')),
                ('bank_name', models.CharField(db_default='', max_length=64, validators=[django.core.validators.RegexValidator(message='Please enter a valid back name.', regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$')], verbose_name='Bank Name')),
                ('bank_account_no', models.CharField(db_default='', max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter a valid account number.', regex='^\\d+$')], verbose_name='Account No.')),
                ('ifsc_code', models.CharField(db_default='', help_text='The IFSC Card should be in capital letters.', max_length=11, validators=[django.core.validators.RegexValidator(message='Please enter a valid IFSC code. The IFSC code should be in capital letters.', regex='^[A-Z]{4}0[A-Z0-9]{6}$')], verbose_name='IFSC Code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
    ]
