from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import UPLCRequest, NMRRequest, AuditLog, Approval, Workflow
from .forms import UPLCRequestForm, NMRRequestForm
import random
# =========================
# LANDING PAGE
# =========================

@login_required
def service_hub(request):
    user = request.user
    user_groups = list(request.user.groups.values_list('name', flat=True))
    
    # Identify Roles
    is_supervisor = user.groups.filter(name__in=[
        'uplc_supervisor', 'nmr_supervisor', 'mediate_supervisor', 'supervisor', 'final_approvar'
    ]).exists() or user.is_superuser or user.is_staff

    # Force students to pass the SOP gate first before they can see the hub
    if not is_supervisor and not request.session.get('sop_accepted', False):
        return redirect('lab_workflow:sop_gate')

    available_forms = [
        # LIVE INSTRUMENTS (Active)
        {"id": "nmr", "name": "Nuclear Magnetic Resonance (NMR)", "icon": "⚛️", "active": True},
        {"id": "uplc", "name": "Ultra Performance Liquid Chromatography (UPLC)", "icon": "🧪", "active": True},
       
        # INACTIVE INSTRUMENTS (Placeholders)
        {"id": "one_d_nmr", "name": "One-Dimensional NMR Spectroscopy", "icon": "🧲", "active": False},
        {"id": "hplc", "name": "High-Performance Liquid Chromatography (HPLC)", "icon": "💧", "active": False},
        {"id": "prep_hplc", "name": "Preparative HPLC", "icon": "💎", "active": False},
        
        {"id": "pxrd", "name": "Powder X-ray Diffraction (PXRD)", "icon": "📐", "active": False},
        {"id": "sxrd", "name": "Single-Crystal X-ray Diffraction (SXRD)", "icon": "🎯", "active": False},
        
        {"id": "ir", "name": "Infrared Spectroscopy (IR)", "icon": "〰️", "active": False},
        {"id": "uv", "name": "UV-Visible Spectrophotometry (UV)", "icon": "🌈", "active": False},
        
        {"id": "sams", "name": "Nanotechnology Self-Assembled Monolayers (SAMs)", "icon": "🛡️", "active": False},
        {"id": "afm", "name": "Atomic Force Microscopy (AFM)", "icon": "📍", "active": False},
        
        {"id": "gcms", "name": "Gas Chromatography-Mass Spectrometry (GC-MS)", "icon": "📊", "active": False},
        {"id": "hej_ms", "name": "HEJ Mass Spectroscopy Sample", "icon": "🧬", "active": False},
        {"id": "esi_ms", "name": "Mass Spectroscopy for ESI-MS", "icon": "⚡", "active": False},
        {"id": "icp_ms", "name": "Mass Spectroscopy for ICP-MS", "icon": "🔥", "active": False},
    
        # Add the remaining 18 placeholder forms here...
    ]

    # 2. Dynamic Failover Load-Balancing for NodePorts
    k8s_nodes = ["172.16.2.13", "172.16.2.38", "172.16.2.35", "172.16.2.39"]
    selected_node = random.choice(k8s_nodes)

    # 3. Explicit High-Performance Computing Context Object
    hpc_cluster = {
        "id": "jupyter_gpu",
        "name": "ICCBS GPU Jupyter Notebook Workspace",
        "hardware_spec": "NVIDIA RTX 5000 Shared Cluster Infrastructure",
        "icon": "🎛️",
        "cluster_url": f"http://{selected_node}:32372/hub/spawn"
    }

    return render(request, 'lab_workflow/service_hub.html', {
        'available_forms': available_forms,
        'hpc_cluster': hpc_cluster,
        'is_supervisor': is_supervisor
    })

# =========================
# SOP GATE
# =========================
@login_required
def sop_gate(request):
    user_groups = list(request.user.groups.values_list('name', flat=True))

    # Only students can access SOP page
    if not ('nmr_student' in user_groups or 'uplc_student' in user_groups):
        return redirect('lab_workflow:service_hub')

    # Accept SOP
    if request.method == "POST":
        request.session['sop_accepted'] = True
        return redirect('lab_workflow:service_hub')

    return render(request, 'lab_workflow/sop_gate.html')

# =========================
# LOGIN REDIRECT
# =========================
@login_required
def post_login_redirect(request):
    user_groups = list(request.user.groups.values_list('name', flat=True))

    # 1. Students → SOP first
    if 'nmr_student' in user_groups or 'uplc_student' in user_groups:
        return redirect('lab_workflow:sop_gate')

    # 2. Supervisors/admins → dashboard
    supervisor_roles = {
        'uplc_supervisor',
        'nmr_supervisor',
        'mediate_supervisor',
        'supervisor',
        'final_approvar'
    }

    if (
        any(role in user_groups for role in supervisor_roles)
        or request.user.is_superuser
        or request.user.is_staff
    ):
        return redirect('lab_workflow:service_hub')

    # 3. Fallback → ICCBS profile
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
    is_final_approver = user.groups.filter(name='final_approvar').exists() or user.groups.filter(name='supervisor').exists()
    is_mediate_sup = user.groups.filter(name='mediate_supervisor').exists()

    # 2. Student's Own History (Personal)
    uplc_requests = UPLCRequest.objects.filter(applicant=user)
    nmr_requests = NMRRequest.objects.filter(user=user)

    # 3. Supervisor's Master View (Departmental)
    master_nmr_list = None
    master_uplc_list = None

    if is_nmr_sup or is_final_approver or is_mediate_sup:
        master_nmr_list = NMRRequest.objects.all().order_by('-id')
    
    if is_uplc_sup or is_final_approver or is_mediate_sup:
        master_uplc_list = UPLCRequest.objects.all().order_by('-id')

    # 4. Pending Tasks Logic (Fixed Sequence Dependency Engine)
    approvals = Approval.objects.filter(
        approver=user, 
        status='pending'
    ).select_related('uplc_request', 'nmr_request', 'step')
    
    valid_approvals = []
    for approval in approvals:
        request_obj = approval.uplc_request or approval.nmr_request
        
        # Get all distinct lower tier step orders that exist for this specific record form
        prev_step_orders = request_obj.approvals.filter(
            step__step_order__lt=approval.step.step_order
        ).values_list('step__step_order', flat=True).distinct()
        
        # Verify that EVERY preceding tier step contains at least one approved action entry row
        can_show = True
        for order in prev_step_orders:
            tier_approved = request_obj.approvals.filter(step__step_order=order, status='approved').exists()
            if not tier_approved:
                can_show = False
                break
                
        if can_show:
            valid_approvals.append(approval)

    return render(request, "lab_workflow/dashboard.html", {
        "uplc_requests": uplc_requests,
        "nmr_requests": nmr_requests,
        "master_nmr_list": master_nmr_list,   
        "master_uplc_list": master_uplc_list, 
        "pending_approvals": valid_approvals,
        "is_mediate_sup": is_mediate_sup,
        "is_any_supervisor": (is_nmr_sup or is_uplc_sup or is_final_approver or is_mediate_sup)
    })


# =========================
# UPLC FORM
# =========================
@login_required
def uplc_form_view(request):
    if request.method == "POST":
        form = UPLCRequestForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.applicant = request.user
            obj.status = 'pending'  
            
            workflow = Workflow.objects.filter(name="UPLC Workflow").first()
            if workflow:
                obj.workflow = workflow
            
            obj.save()

            if workflow:
                for step in workflow.steps.all().order_by('step_order'):
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
                    uplc_request=obj,
                    action='submitted',
                    message="UPLC requisition request submitted successfully."
                )
                messages.success(request, "UPLC submitted successfully.")
            else:
                messages.error(request, "Workflow template configuration missing.")

            return redirect('lab_workflow:lab_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UPLCRequestForm()

    return render(request, "lab_workflow/uplc_form.html", {"form": form})


# =========================
# NMR FORM
# =========================
@login_required
def nmr_form_view(request):
    if request.method == "POST":
        form = NMRRequestForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.status = 'pending'
            
            workflow = Workflow.objects.filter(name="NMR Workflow").first()
            if workflow:
                obj.workflow = workflow
            
            obj.save()

            if workflow:
                for step in workflow.steps.all().order_by('step_order'):
                    approvers = User.objects.filter(groups__name=step.role)
                    for approver in approvers:
                        Approval.objects.create(
                            nmr_request=obj,
                            step=step,
                            approver=approver,
                            status='pending'
                        )
                messages.success(request, "NMR submitted successfully.")
            else:
                messages.error(request, "Workflow template configuration missing.")

            return redirect('lab_workflow:lab_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
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
    
    # Check if there are any HIGHER step orders left that haven't been completed yet
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
    messages.success(request, "Approved successfully.")
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

    # Cancel any remaining pending approvals for this workflow path
    request_obj.approvals.filter(status='pending').update(status='rejected', action_at=now())

    messages.error(request, "Request has been rejected.")
    return redirect('lab_workflow:lab_dashboard')


# =========================
# PRINT
# =========================
@login_required
def print_form(request, request_type, pk):
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

    obj.owner = obj.user if hasattr(obj, 'user') else obj.applicant
    return render(request, template, {'r': obj})


# =========================
# DETAILS
# =========================
@login_required
def uplc_detail(request, pk):
    uplc_request = get_object_or_404(UPLCRequest, pk=pk)
    return render(request, 'lab_workflow/uplc_detail.html', {'r': uplc_request})


@login_required
def nmr_detail(request, pk):
    nmr_request = get_object_or_404(NMRRequest, pk=pk)
    return render(request, 'lab_workflow/nmr_detail.html', {'r': nmr_request})


# ===============================================
# MEDIATE SUPERVISOR INVALID TLC REJECTION
# ===============================================
@login_required
def reject_invalid_tlc(request, request_type, pk):
    if not request.user.groups.filter(name='mediate_supervisor').exists():
       return HttpResponseForbidden("Access Denied: Only Mediate Supervisors can execute this action.")

    rtype = request_type.lower()
    if rtype == 'nmr':
       obj = get_object_or_404(NMRRequest, pk=pk)
    elif rtype == 'uplc':
       obj = get_object_or_404(UPLCRequest, pk=pk)
    else:
       return HttpResponseForbidden("Invalid Request Type")

    obj.status = 'rejected'
    obj.rejection_reason = "INVALID TLC"
    obj.save()

    obj.approvals.filter(status='pending').update(status='rejected', action_at=now())

    messages.error(request, f"Form {obj.sample_code} rejected due to INVALID TLC.")
    return redirect('lab_workflow:lab_dashboard')