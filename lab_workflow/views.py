from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import UPLCRequest, AuditLog
from .forms import UPLCRequestForm
from django.contrib import messages

# =========================
# FORM SUBMISSION (PUBLIC)
# =========================
def uplc_form_view(request):
    if request.method == "POST":
        form = UPLCRequestForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            # Since there is no login, we assign the first superuser or a default admin
            # If no users exist in your DB yet, this might need a check
            default_user = User.objects.filter(is_superuser=True).first()
            obj.applicant = default_user 

            # Handle solubility (multiple choice → string)
            solubility_list = request.POST.getlist('solubility')
            obj.solubility = ",".join(solubility_list)
            
            # Set initial status for ERP workflow
            obj.status = 'in_review'
            obj.save()

            # Create an Audit Log entry
            AuditLog.objects.create(
                user=default_user, 
                request=obj, 
                action='submitted', 
                message="Form submitted via public access."
            )

            messages.success(request, "Request submitted successfully!")
            return redirect('dashboard')
    else:
        form = UPLCRequestForm()

    return render(request, "lab_workflow/uplc_form.html", {"form": form})


# =========================
# DASHBOARD (PUBLIC)
# =========================
def dashboard(request):
    # Without login, we show ALL requests so anyone can see the status
    requests = UPLCRequest.objects.all().order_by('-created_at')
    return render(request, "lab_workflow/dashboard.html", {"requests": requests})


# =========================
# APPROVE REQUEST (PUBLIC)
# =========================
def approve_request(request, pk):
    obj = get_object_or_404(UPLCRequest, pk=pk)

    # Broadened to check for 'pending' OR 'in_review'
    # We use .lower() to ensure it catches 'IN_REVIEW' from your screenshot
    if obj.status.lower() in ['pending', 'in_review']:
        obj.status = 'approved'
        obj.approved_at = now()
        obj.save()
        
        AuditLog.objects.create(
            request=obj, 
            action='approved', 
            message="Approved via public dashboard."
        )

    return redirect('dashboard')


# =========================
# REJECT REQUEST (PUBLIC)
# =========================
def reject_request(request, pk):
    obj = get_object_or_404(UPLCRequest, pk=pk)

    if obj.status.lower() in ['pending', 'in_review']:
        obj.status = 'rejected'
        obj.save()
        
        AuditLog.objects.create(
            request=obj, 
            action='rejected', 
            message="Rejected via public dashboard."
        )

    return redirect('dashboard')