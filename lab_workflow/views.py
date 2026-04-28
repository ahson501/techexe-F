from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib import messages
from .models import WorkflowStep, Workflow 
from django.contrib.auth.decorators import login_required

from .models import UPLCRequest, NMRRequest, AuditLog, Approval, WorkflowStep
from .forms import UPLCRequestForm, NMRRequestForm


# =========================
# LOGIN REDIRECT
# =========================
@login_required
def post_login_redirect(request):
    user = request.user
    
    # Using a list of groups that should see the lab dashboard
    lab_groups = {'uplc_student', 'nmr_student', 'uplc_supervisor', 'nmr_supervisor'}
    
    # Check if user has ANY of the lab groups
    if user.groups.filter(name__in=lab_groups).exists():
        return redirect('lab_workflow:lab_dashboard')

    # Fallback for staff/admin not in specific lab groups
    return redirect('/iccbs/profile/')
# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    # 1. Requests submitted by the user (Personal History)
    uplc_requests = UPLCRequest.objects.filter(applicant=request.user)
    nmr_requests = NMRRequest.objects.filter(user=request.user)

    # 2. Check if the user is a supervisor
    is_nmr_sup = request.user.groups.filter(name='nmr_supervisor').exists()
    is_uplc_sup = request.user.groups.filter(name='uplc_supervisor').exists()

    # 3. Fetch Tasks
    if is_nmr_sup or is_uplc_sup:
        # Fetch ALL pending approvals regardless of who the 'approver' field points to
        # OR fetch tasks where the 'approver' is the current user
        pending_approvals = Approval.objects.filter(status='pending').select_related(
            'uplc_request', 'nmr_request', 'uplc_request__applicant', 'nmr_request__user'
        )
    else:
        pending_approvals = None

    return render(request, "lab_workflow/dashboard.html", {
        "uplc_requests": uplc_requests,
        "nmr_requests": nmr_requests,
        "pending_approvals": pending_approvals,
    })
# =========================
# UPLC FORM SUBMISSION
# =========================
@login_required
def uplc_form_view(request):

    if request.method == "POST":
        form = UPLCRequestForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            # Assign logged-in user
            obj.applicant = request.user

            # Handle solubility (multi-select)
            solubility_list = request.POST.getlist('solubility')
            obj.solubility = ",".join(solubility_list)

            obj.status = 'in_review'
            obj.save()

            # ✅ Create Approval Workflow
            if obj.workflow:
                steps = obj.workflow.steps.all()

                for step in steps:
                    approver = User.objects.filter(groups__name=step.role).first()

                    if approver:
                        Approval.objects.create(
                            uplc_request=obj,
                            step=step,
                            approver=approver
                        )

            # Audit log
            AuditLog.objects.create(
                user=request.user,
                uplc_request=obj,
                action='submitted',
                message="UPLC form submitted"
            )

            messages.success(request, "Request submitted successfully!")
            return redirect('lab_workflow:lab_dashboard')

    else:
        form = UPLCRequestForm()

    return render(request, "lab_workflow/uplc_form.html", {"form": form})


# =========================
# NMR FORM SUBMISSION
# =========================
@login_required
def nmr_form_view(request):
    if request.method == "POST":
        # 1. Create the NMR Object (Your existing code is fine here)
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
            status_h_nmr=request.POST.get('status_h_nmr'),
            status_c_nmr=request.POST.get('status_c_nmr'),
            cosy='cosy' in request.POST,
            noesy='noesy' in request.POST,
            data_format=request.POST.get('data_format'),
        )

        # 2. Find Supervisor
        nmr_supervisor = User.objects.filter(groups__name='nmr_supervisor').first()

        if nmr_supervisor:
            # 3. Get the Step (More robust check)
            step = None
            
            # Try to get the specific NMR Workflow
            workflow = Workflow.objects.filter(name="NMR Workflow").first()
            if workflow:
                step = workflow.steps.first()
            
            # If still None, try to get ANY available step
            if not step:
                step = WorkflowStep.objects.first()

            # CRITICAL: Only create approval if we actually found a step
            if step:
                Approval.objects.create(
                    nmr_request=obj,
                    approver=nmr_supervisor,
                    step=step
                )
                
                AuditLog.objects.create(
                    user=request.user,
                    nmr_request=obj,
                    action='submitted',
                    message=f"NMR form submitted: {obj.sample_code}"
                )
                messages.success(request, "NMR Request submitted successfully!")
            else:
                # This happens if your WorkflowStep table is empty
                messages.error(request, "System Error: No Workflow Steps defined in Admin. Please contact Admin.")
                
            return redirect('lab_workflow:lab_dashboard')
        
        else:
            messages.warning(request, "Request saved, but no NMR Supervisor was found.")
            return redirect('lab_workflow:lab_dashboard')

    form = NMRRequestForm()
    return render(request, 'lab_workflow/nmr_form.html', {'form': form})
# =========================
# REQUEST DETAIL
# =========================
@login_required
def request_detail(request, pk):
    uplc_request = get_object_or_404(UPLCRequest, pk=pk)
    return render(request, 'lab_workflow/request_detail.html', {'r': uplc_request})


@login_required
def nmr_detail(request, pk):
    nmr_request = get_object_or_404(NMRRequest, pk=pk)
    return render(request, 'lab_workflow/nmr_detail.html', {'r': nmr_request})


# =========================
# APPROVE STEP (CORE LOGIC)
# =========================
@login_required
def approve_request(request, pk):
    approval = get_object_or_404(Approval, pk=pk)

    # Security: Only the assigned supervisor can approve
    if request.user != approval.approver:
        messages.error(request, "Not authorized")
        return redirect('lab_workflow:lab_dashboard')

    # Identify if we are approving UPLC or NMR
    target_obj = approval.uplc_request if approval.uplc_request else approval.nmr_request

    # Update Approval Step
    approval.status = 'approved'
    approval.action_at = now()
    approval.save()

    # Update the actual Sample Request status
    target_obj.status = 'approved'
    target_obj.approved_at = now()
    target_obj.save()

    # Create correct Audit Log entry
    AuditLog.objects.create(
        user=request.user,
        uplc_request=approval.uplc_request, # Will be None if it's NMR
        nmr_request=approval.nmr_request,   # Will be None if it's UPLC
        action='approved',
        message=f"Request {target_obj.sample_code} approved by {request.user.username}"
    )

    messages.success(request, "Approved successfully")
    return redirect('lab_workflow:lab_dashboard')


# =========================
# REJECT STEP
# =========================
@login_required
def reject_request(request, pk):
    approval = get_object_or_404(Approval, pk=pk)

    if request.user != approval.approver:
        messages.error(request, "Not authorized")
        return redirect('lab_workflow:lab_dashboard')

    approval.status = 'rejected'
    approval.action_at = now()
    approval.save()

    # Identify the target (UPLC or NMR)
    target_obj = approval.uplc_request if approval.uplc_request else approval.nmr_request
    target_obj.status = 'rejected'
    target_obj.save()

    AuditLog.objects.create(
        user=request.user,
        uplc_request=approval.uplc_request,
        nmr_request=approval.nmr_request,
        action='rejected',
        message="Request rejected by supervisor"
    )

    messages.error(request, "Request rejected")
    return redirect('lab_workflow:lab_dashboard')