from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UPLCRequest, NMRRequest, AuditLog, Approval, Workflow
from .forms import UPLCRequestForm, NMRRequestForm
from django.http import HttpResponseForbidden

# =========================
# LOGIN REDIRECT ✅ REQUIRED FOR URLS.PY
# =========================
@login_required
def post_login_redirect(request):

    lab_groups = {
        'uplc_student',
        'nmr_student',
        'uplc_supervisor',
        'nmr_supervisor',
        'supervisor'
    }

    if request.user.groups.filter(name__in=lab_groups).exists():
        return redirect('lab_workflow:lab_dashboard')

    return redirect('/iccbs/profile/')


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    user = request.user
    
    # 1. Identify Roles
    is_nmr_sup = user.groups.filter(name='nmr_supervisor').exists()
    is_uplc_sup = user.groups.filter(name='uplc_supervisor').exists()
    is_final_approver = user.groups.filter(name='supervisor').exists()

    # 2. Student's Own History (Personal)
    uplc_requests = UPLCRequest.objects.filter(applicant=user)
    nmr_requests = NMRRequest.objects.filter(user=user)

    # 3. Supervisor's Master View (Departmental)
    # This fetches ALL forms for the department regardless of who submitted them
    master_nmr_list = None
    master_uplc_list = None

    if is_nmr_sup or is_final_approver:
        master_nmr_list = NMRRequest.objects.all().order_by('-id')
    
    if is_uplc_sup or is_final_approver:
        master_uplc_list = UPLCRequest.objects.all().order_by('-id')

    # 4. Pending Tasks Logic (Your existing working logic)
    approvals = Approval.objects.filter(
        approver=user, 
        status='pending'
    ).select_related('uplc_request', 'nmr_request', 'step')
    
    valid_approvals = []
    for approval in approvals:
        request_obj = approval.uplc_request or approval.nmr_request
        prev_step_orders = request_obj.approvals.filter(
            step__step_order__lt=approval.step.step_order
        ).values_list('step__step_order', flat=True).distinct()
        
        if not any(not request_obj.approvals.filter(step__step_order=order, status='approved').exists() for order in prev_step_orders):
            valid_approvals.append(approval)

    return render(request, "lab_workflow/dashboard.html", {
        "uplc_requests": uplc_requests,
        "nmr_requests": nmr_requests,
        "master_nmr_list": master_nmr_list,   # Use these in template
        "master_uplc_list": master_uplc_list, # Use these in template
        "pending_approvals": valid_approvals,
        "is_any_supervisor": (is_nmr_sup or is_uplc_sup or is_final_approver)
    })
# =========================
# UPLC FORM
# =========================
@login_required
def uplc_form_view(request):

    if request.method == "POST":
        form = UPLCRequestForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.applicant = request.user
            obj.status = 'in_review'

            workflow = Workflow.objects.filter(name="UPLC Workflow").first()
            if workflow:
                obj.workflow = workflow

            obj.save()

            # assign ALL users in role
            for step in obj.workflow.steps.all().order_by('step_order'):

                approvers = User.objects.filter(groups__name=step.role)

                for approver in approvers:
                    Approval.objects.create(
                        uplc_request=obj,
                        step=step,
                        approver=approver,
                        status='pending'
                    )

            AuditLog.objects.create(
                user=request.user,
                request=obj,
                action='submitted',
                message="UPLC submitted"
            )

            messages.success(request, "UPLC submitted")
            return redirect('lab_workflow:lab_dashboard')

    else:
        form = UPLCRequestForm()

    return render(request, "lab_workflow/uplc_form.html", {"form": form})


# =========================
# NMR FORM
# =========================
@login_required
def nmr_form_view(request):

    if request.method == "POST":

        obj = NMRRequest.objects.create(
            user=request.user,
            student_name=request.POST.get('student_name'),
            supervisor=request.POST.get('supervisor'),
            thesis_title=request.POST.get('thesis_title'),
            lab_no=request.POST.get('lab_no'),
            extension_no=request.POST.get('extension_no'),
            sample_code=request.POST.get('sample_code'),
            solvent=request.POST.get('solvent'),
            solubility=request.POST.get('solubility'),
            molecular_weight=request.POST.get('molecular_weight'),
            amount=request.POST.get('amount'),
            concentration=request.POST.get('concentration'),
            cosy='cosy' in request.POST,
            noesy='noesy' in request.POST,
            data_format=request.POST.get('data_format'),
            status='pending'
        )

        workflow = Workflow.objects.filter(name="NMR Workflow").first()

        if workflow:
            obj.workflow = workflow
            obj.save()

            for step in workflow.steps.all().order_by('step_order'):

                approvers = User.objects.filter(groups__name=step.role)

                for approver in approvers:
                    Approval.objects.create(
                        nmr_request=obj,
                        step=step,
                        approver=approver,
                        status='pending'
                    )

            messages.success(request, "NMR submitted")
        else:
            messages.error(request, "Workflow missing")

        return redirect('lab_workflow:lab_dashboard')

    form = NMRRequestForm()
    return render(request, 'lab_workflow/nmr_form.html', {'form': form})


# =========================
# APPROVE
# =========================
@login_required
def approve_request(request, pk):
    approval = get_object_or_404(Approval, pk=pk)

    if request.user != approval.approver:
        messages.error(request, "Not allowed")
        return redirect('lab_workflow:lab_dashboard')

    approval.status = 'approved'
    approval.action_at = now()
    approval.save()

    request_obj = approval.uplc_request or approval.nmr_request
    
    # Check if there are any HIGHER step orders left
    remaining_steps = request_obj.approvals.filter(
        step__step_order__gt=approval.step.step_order,
        status='pending'
    )

    if not remaining_steps.exists():
        request_obj.status = 'approved'
        request_obj.approved_at = now()
    else:
        request_obj.status = 'in_review'

    request_obj.save()
    messages.success(request, "Approved")
    return redirect('lab_workflow:lab_dashboard')


# =========================
# REJECT
# =========================
@login_required
def reject_request(request, pk):

    approval = get_object_or_404(Approval, pk=pk)

    if request.user != approval.approver:
        messages.error(request, "Not allowed")
        return redirect('lab_workflow:lab_dashboard')

    approval.status = 'rejected'
    approval.action_at = now()
    approval.save()

    request_obj = approval.uplc_request or approval.nmr_request
    request_obj.status = 'rejected'
    request_obj.save()

    messages.error(request, "Rejected")
    return redirect('lab_workflow:lab_dashboard')


# =========================
# PRINT
# =========================
@login_required
def print_form(request, request_type, pk):
    # Force lowercase to avoid matching errors
    rtype = request_type.lower() 
    
    if rtype == 'nmr':
        obj = get_object_or_404(NMRRequest, pk=pk)
        template = 'lab_workflow/print_nmr.html'
    elif rtype == 'uplc':
        obj = get_object_or_404(UPLCRequest, pk=pk)
        template = 'lab_workflow/print_uplc.html'
    else:
        return HttpResponseForbidden("Invalid Request Type")

    if obj.status != 'approved':
        return HttpResponseForbidden("Only approved forms can be printed.")
    # Add this line to create a universal 'owner' variable
    obj.owner = obj.user if hasattr(obj, 'user') else obj.applicant
    return render(request, template, {'r': obj})

# =========================
# DETAILS
# =========================
@login_required
def request_detail(request, pk):
    uplc_request = get_object_or_404(UPLCRequest, pk=pk)
    return render(request, 'lab_workflow/request_detail.html', {'r': uplc_request})


@login_required
def nmr_detail(request, pk):
    nmr_request = get_object_or_404(NMRRequest, pk=pk)
    return render(request, 'lab_workflow/nmr_detail.html', {'r': nmr_request})