from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('suffix', models.CharField(blank=True, max_length=20, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True)),
                ('civil_status', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed'), ('separated', 'Separated')], max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=150, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'members', 'ordering': ['last_name', 'first_name']},
        ),
        migrations.CreateModel(
            name='Sacrament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sacrament_type', models.CharField(choices=[('baptism', 'Baptism'), ('confirmation', 'Confirmation'), ('communion', 'First Holy Communion'), ('marriage', 'Marriage'), ('last_rites', 'Last Rites')], max_length=20)),
                ('date_received', models.DateField()),
                ('officiant_name', models.CharField(blank=True, max_length=150, null=True)),
                ('place', models.CharField(blank=True, max_length=150, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sacraments', to='registry.member')),
            ],
            options={'db_table': 'sacraments'},
        ),
        migrations.CreateModel(
            name='SacramentParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('role', models.CharField(choices=[('godfather', 'Godfather'), ('godmother', 'Godmother'), ('sponsor', 'Sponsor'), ('witness', 'Witness')], max_length=20)),
                ('sacrament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='registry.sacrament')),
            ],
            options={'db_table': 'sacrament_participants'},
        ),
        migrations.CreateModel(
            name='BaptismDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(blank=True, max_length=150, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sacrament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='baptism_detail', to='registry.sacrament')),
            ],
            options={'db_table': 'baptism_details'},
        ),
        migrations.CreateModel(
            name='CommunionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('sacrament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='communion_detail', to='registry.sacrament')),
            ],
            options={'db_table': 'communion_details'},
        ),
        migrations.CreateModel(
            name='ConfirmationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sacrament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_detail', to='registry.sacrament')),
            ],
            options={'db_table': 'confirmation_details'},
        ),
        migrations.CreateModel(
            name='MarriageDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spouse_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sacrament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='marriage_detail', to='registry.sacrament')),
            ],
            options={'db_table': 'marriage_details'},
        ),
        migrations.CreateModel(
            name='LastRitesDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_notes', models.TextField(blank=True, null=True)),
                ('family_contact', models.CharField(blank=True, max_length=150, null=True)),
                ('sacrament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='last_rites_detail', to='registry.sacrament')),
            ],
            options={'db_table': 'last_rites_details'},
        ),
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount_pledged', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('unpaid', 'Unpaid'), ('partial', 'Partially Paid'), ('paid', 'Fully Paid')], default='unpaid', max_length=10)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pledges', to='registry.member')),
            ],
            options={'db_table': 'pledges', 'ordering': ['-date_created']},
        ),
        migrations.CreateModel(
            name='PledgePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='registry.pledge')),
            ],
            options={'db_table': 'payments', 'ordering': ['-payment_date']},
        ),
    ]
