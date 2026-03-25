from django.db import models


class Member(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    CIVIL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    civil_status = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        name = ' '.join(p for p in parts if p)
        if self.suffix:
            name += f' {self.suffix}'
        return name

    @property
    def full_name(self):
        return str(self)

    @property
    def date_registered(self):
        return self.created_at.date() if self.created_at else None


class Sacrament(models.Model):
    SACRAMENT_TYPES = [
        ('baptism', 'Baptism'),
        ('confirmation', 'Confirmation'),
        ('communion', 'First Holy Communion'),
        ('marriage', 'Marriage'),
        ('last_rites', 'Last Rites'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sacraments')
    sacrament_type = models.CharField(max_length=20, choices=SACRAMENT_TYPES)
    date_received = models.DateField()
    officiant_name = models.CharField(max_length=150, blank=True, null=True)
    place = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sacraments'

    def __str__(self):
        return f"{self.get_sacrament_type_display()} - {self.member}"


class SacramentParticipant(models.Model):
    ROLE_CHOICES = [
        ('godfather', 'Godfather'),
        ('godmother', 'Godmother'),
        ('sponsor', 'Sponsor'),
        ('witness', 'Witness'),
    ]

    sacrament = models.ForeignKey(Sacrament, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'sacrament_participants'

    def __str__(self):
        return f"{self.name} ({self.role})"


class BaptismDetail(models.Model):
    sacrament = models.OneToOneField(Sacrament, on_delete=models.CASCADE, related_name='baptism_detail')
    father_name = models.CharField(max_length=150, blank=True, null=True)
    mother_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'baptism_details'


class CommunionDetail(models.Model):
    sacrament = models.OneToOneField(Sacrament, on_delete=models.CASCADE, related_name='communion_detail')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'communion_details'


class ConfirmationDetail(models.Model):
    sacrament = models.OneToOneField(Sacrament, on_delete=models.CASCADE, related_name='confirmation_detail')
    confirmation_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'confirmation_details'


class MarriageDetail(models.Model):
    sacrament = models.OneToOneField(Sacrament, on_delete=models.CASCADE, related_name='marriage_detail')
    spouse_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'marriage_details'


class LastRitesDetail(models.Model):
    sacrament = models.OneToOneField(Sacrament, on_delete=models.CASCADE, related_name='last_rites_detail')
    condition_notes = models.TextField(blank=True, null=True)
    family_contact = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'last_rites_details'


class Pledge(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='pledges')
    description = models.CharField(max_length=255)
    amount_pledged = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'pledges'
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.member} - {self.description}"

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def balance(self):
        return self.amount_pledged - self.total_paid

    @property
    def amount_promised(self):
        return self.amount_pledged

    def update_status(self):
        paid = self.total_paid
        if paid <= 0:
            self.status = 'unpaid'
        elif paid >= self.amount_pledged:
            self.status = 'paid'
        else:
            self.status = 'partial'
        self.save()


class PledgePayment(models.Model):
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.pledge}"

    @property
    def amount(self):
        return self.amount_paid

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pledge.update_status()
