# Generated by Django 4.0.2 on 2022-05-15 19:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('1', 'HOD'), ('2', 'Agent')], default=1, max_length=50)),
                ('profile_pic', models.ImageField(upload_to='media/profile_pic')),
                ('user_id', models.CharField(blank=True, max_length=12)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
            name='FundDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=10)),
                ('user_id', models.CharField(max_length=10)),
                ('ref_id', models.CharField(blank=True, max_length=50, null=True)),
                ('plot_number', models.CharField(blank=True, max_length=25, null=True)),
                ('Total_amount', models.CharField(blank=True, max_length=25, null=True)),
                ('user_name', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('joinig_date', models.DateTimeField(blank=True, null=True)),
                ('payment_amount', models.BigIntegerField(blank=True, null=True)),
                ('Payable_amout', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fundtransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=300)),
                ('amount', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_id', models.CharField(max_length=300)),
                ('accountname', models.CharField(max_length=25)),
                ('accountno', models.IntegerField(blank=True, null=True)),
                ('IFSCno', models.CharField(blank=True, max_length=25, null=True)),
                ('Pancardno', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuperAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(max_length=25)),
                ('user_id', models.CharField(max_length=300)),
                ('plot_number', models.CharField(max_length=25)),
                ('Payable_amout', models.IntegerField(blank=True, null=True)),
                ('remaining_amount', models.IntegerField(blank=True, null=True)),
                ('payment_amount', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('mobile_no', models.BigIntegerField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.TextField()),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='receipt/')),
                ('joinig_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('plot_size', models.CharField(blank=True, max_length=100, null=True)),
                ('addresss', models.CharField(blank=True, max_length=5000, null=True)),
                ('mail', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=10, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_mobileno', models.BigIntegerField(blank=True, null=True)),
                ('addresss', models.CharField(blank=True, max_length=5000, null=True)),
                ('mail', models.CharField(blank=True, max_length=50, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookPlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(max_length=25)),
                ('user_id', models.CharField(max_length=300)),
                ('plot_number', models.CharField(max_length=25)),
                ('Payable_amout', models.IntegerField(blank=True, null=True)),
                ('payment_amount', models.IntegerField(blank=True, null=True)),
                ('remaining_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('name', models.CharField(max_length=100)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.BigIntegerField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.TextField()),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='receipt/')),
                ('joinig_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('plot_size', models.CharField(blank=True, max_length=100, null=True)),
                ('addresss', models.CharField(blank=True, max_length=5000, null=True)),
                ('mail', models.CharField(blank=True, max_length=50, null=True)),
                ('account_no', models.CharField(blank=True, default=0, max_length=50, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=100, null=True)),
                ('check_no', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddPlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_no', models.CharField(max_length=10)),
                ('plot_size', models.IntegerField(blank=True, null=True)),
                ('plot_rate', models.IntegerField(blank=True, null=True)),
                ('phase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matrixapp.phase')),
            ],
        ),
    ]
