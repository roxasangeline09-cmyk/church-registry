from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import (Member, Sacrament, SacramentParticipant,
                     BaptismDetail, ConfirmationDetail, CommunionDetail,
                     MarriageDetail, LastRitesDetail, Pledge, PledgePayment)
from .forms import (MemberForm, SacramentForm, BaptismDetailForm,
                    ConfirmationDetailForm, CommunionDetailForm,
                    MarriageDetailForm, LastRitesDetailForm,
                    PledgeForm, PledgePaymentForm)


# ─── AUTH ─────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'registry/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    return render(request, 'registry/dashboard.html', {
        'total_members':       Member.objects.filter(is_active=True).count(),
        'total_baptisms':      Sacrament.objects.filter(sacrament_type='baptism').count(),
        'total_confirmations': Sacrament.objects.filter(sacrament_type='confirmation').count(),
        'total_communions':    Sacrament.objects.filter(sacrament_type='communion').count(),
        'total_marriages':     Sacrament.objects.filter(sacrament_type='marriage').count(),
        'total_last_rites':    Sacrament.objects.filter(sacrament_type='last_rites').count(),
        'total_pledges':       Pledge.objects.count(),
        'outstanding_pledges': Pledge.objects.filter(status__in=['unpaid', 'partial']).count(),
        'recent_members':      Member.objects.filter(is_active=True).order_by('-created_at')[:5],
    })


# ─── MEMBERS ──────────────────────────────────────────────────────────────────

@login_required
def member_list(request):
    q = request.GET.get('q', '')
    members = Member.objects.filter(is_active=True)
    if q:
        members = members.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(middle_name__icontains=q) | Q(contact_number__icontains=q)
        )
    return render(request, 'registry/members/list.html', {'members': members, 'q': q})


@login_required
def member_create(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Member registered successfully.')
        return redirect('member_list')
    return render(request, 'registry/members/form.html', {'form': form, 'title': 'Register New Member'})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    sacraments = member.sacraments.all()
    return render(request, 'registry/members/detail.html', {
        'member':       member,
        'baptism':      sacraments.filter(sacrament_type='baptism').first(),
        'confirmation': sacraments.filter(sacrament_type='confirmation').first(),
        'communion':    sacraments.filter(sacrament_type='communion').first(),
        'marriages':    sacraments.filter(sacrament_type='marriage'),
        'last_rites':   sacraments.filter(sacrament_type='last_rites').first(),
    })


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, 'Member updated successfully.')
        return redirect('member_detail', pk=pk)
    return render(request, 'registry/members/form.html', {'form': form, 'title': 'Edit Member', 'member': member})


@login_required
def member_deactivate(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.is_active = False
        member.save()
        messages.success(request, f'{member.full_name} has been deactivated.')
        return redirect('member_list')
    return render(request, 'registry/confirm_delete.html', {'object': member, 'type': 'Member'})


# ─── SACRAMENT HELPERS ────────────────────────────────────────────────────────

def _get_detail(sacrament):
    detail_map = {
        'baptism':      'baptism_detail',
        'confirmation': 'confirmation_detail',
        'communion':    'communion_detail',
        'marriage':     'marriage_detail',
        'last_rites':   'last_rites_detail',
    }
    attr = detail_map.get(sacrament.sacrament_type)
    return getattr(sacrament, attr, None) if attr else None


def _save_participants(request, sacrament):
    names = request.POST.getlist('participant_name[]')
    roles = request.POST.getlist('participant_role[]')
    sacrament.participants.all().delete()
    for name, role in zip(names, roles):
        name = name.strip()
        if name:
            SacramentParticipant.objects.create(sacrament=sacrament, name=name, role=role)


def _sacrament_create(request, member_pk, sacrament_type, detail_form_class, template, title, allow_multiple=False):
    member = get_object_or_404(Member, pk=member_pk)
    if not allow_multiple and member.sacraments.filter(sacrament_type=sacrament_type).exists():
        messages.warning(request, f'This member already has a {sacrament_type} record.')
        return redirect('member_detail', pk=member_pk)

    sac_form = SacramentForm(request.POST or None)
    det_form = detail_form_class(request.POST or None) if detail_form_class else None

    if request.method == 'POST' and sac_form.is_valid() and (det_form is None or det_form.is_valid()):
        sacrament = sac_form.save(commit=False)
        sacrament.member = member
        sacrament.sacrament_type = sacrament_type
        sacrament.save()
        if det_form:
            detail = det_form.save(commit=False)
            detail.sacrament = sacrament
            detail.save()
        _save_participants(request, sacrament)
        messages.success(request, f'{title} record saved.')
        return redirect('member_detail', pk=member_pk)

    return render(request, template, {'sac_form': sac_form, 'det_form': det_form, 'member': member, 'title': title})


def _sacrament_edit(request, pk, detail_form_class, template, title):
    sacrament = get_object_or_404(Sacrament, pk=pk)
    detail_instance = _get_detail(sacrament)
    sac_form = SacramentForm(request.POST or None, instance=sacrament)
    det_form = detail_form_class(request.POST or None, instance=detail_instance) if detail_form_class else None

    if request.method == 'POST' and sac_form.is_valid() and (det_form is None or det_form.is_valid()):
        sac_form.save()
        if det_form:
            detail = det_form.save(commit=False)
            detail.sacrament = sacrament
            detail.save()
        _save_participants(request, sacrament)
        messages.success(request, f'{title} record updated.')
        return redirect('member_detail', pk=sacrament.member.pk)

    return render(request, template, {'sac_form': sac_form, 'det_form': det_form, 'member': sacrament.member, 'title': title, 'sacrament': sacrament})


# ─── SACRAMENTS ───────────────────────────────────────────────────────────────

@login_required
def sacrament_list(request):
    q = request.GET.get('q', '')
    qs = Sacrament.objects.select_related('member')
    if q:
        qs = qs.filter(Q(member__first_name__icontains=q) | Q(member__last_name__icontains=q))
    return render(request, 'registry/sacraments/list.html', {
        'baptisms':      qs.filter(sacrament_type='baptism'),
        'confirmations': qs.filter(sacrament_type='confirmation'),
        'communions':    qs.filter(sacrament_type='communion'),
        'marriages':     qs.filter(sacrament_type='marriage'),
        'last_rites':    qs.filter(sacrament_type='last_rites'),
        'q': q,
        'all_members': Member.objects.filter(is_active=True).order_by('last_name', 'first_name'),
    })


@login_required
def baptism_create(request, member_pk):
    return _sacrament_create(request, member_pk, 'baptism', BaptismDetailForm, 'registry/sacraments/form_baptism.html', 'Baptism')

@login_required
def baptism_edit(request, pk):
    return _sacrament_edit(request, pk, BaptismDetailForm, 'registry/sacraments/form_baptism.html', 'Baptism')

@login_required
def baptism_print(request, pk):
    return render(request, 'registry/sacraments/print_baptism.html', {'baptism': get_object_or_404(Sacrament, pk=pk, sacrament_type='baptism')})


@login_required
def confirmation_create(request, member_pk):
    return _sacrament_create(request, member_pk, 'confirmation', ConfirmationDetailForm, 'registry/sacraments/form.html', 'Confirmation')

@login_required
def confirmation_edit(request, pk):
    return _sacrament_edit(request, pk, ConfirmationDetailForm, 'registry/sacraments/form.html', 'Confirmation')

@login_required
def confirmation_print(request, pk):
    return render(request, 'registry/sacraments/print_confirmation.html', {'conf': get_object_or_404(Sacrament, pk=pk, sacrament_type='confirmation')})


@login_required
def communion_create(request, member_pk):
    return _sacrament_create(request, member_pk, 'communion', CommunionDetailForm, 'registry/sacraments/form.html', 'First Holy Communion')

@login_required
def communion_edit(request, pk):
    return _sacrament_edit(request, pk, CommunionDetailForm, 'registry/sacraments/form.html', 'First Holy Communion')

@login_required
def communion_print(request, pk):
    return render(request, 'registry/sacraments/print_communion.html', {'communion': get_object_or_404(Sacrament, pk=pk, sacrament_type='communion')})


@login_required
def marriage_create(request, member_pk):
    return _sacrament_create(request, member_pk, 'marriage', MarriageDetailForm, 'registry/sacraments/form_marriage.html', 'Marriage', allow_multiple=True)

@login_required
def marriage_edit(request, pk):
    return _sacrament_edit(request, pk, MarriageDetailForm, 'registry/sacraments/form_marriage.html', 'Marriage')

@login_required
def marriage_print(request, pk):
    return render(request, 'registry/sacraments/print_marriage.html', {'marriage': get_object_or_404(Sacrament, pk=pk, sacrament_type='marriage')})


@login_required
def last_rites_create(request, member_pk):
    return _sacrament_create(request, member_pk, 'last_rites', LastRitesDetailForm, 'registry/sacraments/form.html', 'Last Rites')

@login_required
def last_rites_edit(request, pk):
    return _sacrament_edit(request, pk, LastRitesDetailForm, 'registry/sacraments/form.html', 'Last Rites')

@login_required
def last_rites_print(request, pk):
    return render(request, 'registry/sacraments/print_last_rites.html', {'lr': get_object_or_404(Sacrament, pk=pk, sacrament_type='last_rites')})


# ─── PLEDGES ──────────────────────────────────────────────────────────────────

@login_required
def pledge_list(request):
    q = request.GET.get('q', '')
    pledges = Pledge.objects.select_related('member')
    if q:
        pledges = pledges.filter(Q(member__first_name__icontains=q) | Q(member__last_name__icontains=q))
    return render(request, 'registry/pledges/list.html', {'pledges': pledges, 'q': q})


@login_required
def pledge_create(request):
    form = PledgeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Pledge recorded successfully.')
        return redirect('pledge_list')
    return render(request, 'registry/pledges/form.html', {'form': form, 'title': 'Add Pledge'})


@login_required
def pledge_detail(request, pk):
    pledge = get_object_or_404(Pledge, pk=pk)
    return render(request, 'registry/pledges/detail.html', {'pledge': pledge, 'payment_form': PledgePaymentForm()})


@login_required
def pledge_edit(request, pk):
    pledge = get_object_or_404(Pledge, pk=pk)
    form = PledgeForm(request.POST or None, instance=pledge)
    if form.is_valid():
        form.save()
        messages.success(request, 'Pledge updated.')
        return redirect('pledge_detail', pk=pk)
    return render(request, 'registry/pledges/form.html', {'form': form, 'title': 'Edit Pledge'})


@login_required
def pledge_delete(request, pk):
    pledge = get_object_or_404(Pledge, pk=pk)
    if request.method == 'POST':
        pledge.delete()
        messages.success(request, 'Pledge deleted.')
        return redirect('pledge_list')
    return render(request, 'registry/confirm_delete.html', {'object': pledge, 'type': 'Pledge'})


@login_required
def payment_add(request, pledge_pk):
    pledge = get_object_or_404(Pledge, pk=pledge_pk)
    form = PledgePaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.pledge = pledge
        payment.save()
        messages.success(request, 'Payment recorded.')
        return redirect('pledge_detail', pk=pledge_pk)
    return render(request, 'registry/pledges/payment_form.html', {'form': form, 'pledge': pledge})


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(PledgePayment, pk=pk)
    pledge_pk = payment.pledge.pk
    if request.method == 'POST':
        payment.delete()
        payment.pledge.update_status()
        messages.success(request, 'Payment removed.')
        return redirect('pledge_detail', pk=pledge_pk)
    return render(request, 'registry/confirm_delete.html', {'object': payment, 'type': 'Payment'})


# ─── PRINT ────────────────────────────────────────────────────────────────────

@login_required
def member_print(request, pk):
    return render(request, 'registry/members/print_member.html', {'member': get_object_or_404(Member, pk=pk)})

@login_required
def member_list_print(request):
    return render(request, 'registry/members/print_member_list.html', {'members': Member.objects.filter(is_active=True).order_by('last_name', 'first_name')})

@login_required
def pledge_print(request, pk):
    return render(request, 'registry/pledges/print_pledge.html', {'pledge': get_object_or_404(Pledge, pk=pk)})

@login_required
def pledge_list_print(request):
    return render(request, 'registry/pledges/print_pledge_list.html', {'pledges': Pledge.objects.select_related('member').order_by('member__last_name')})
