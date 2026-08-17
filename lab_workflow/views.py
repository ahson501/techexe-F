
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import SopModule, StudentSopCertification, InventoryItem, ThesisPipeline
from .models import UPLCRequest, NMRRequest, AuditLog, Approval, Workflow
from .forms import UPLCRequestForm, NMRRequestForm

# =========================
# LANDING PAGE
# =========================

@login_required
def service_hub(request):
    user = request.user
    
    # 1. Identity & Permissions Verification Gateway
    is_supervisor = user.groups.filter(name__in=[
        'uplc_supervisor', 'nmr_supervisor', 'mediate_supervisor', 'supervisor', 'final_approvar'
    ]).exists() or user.is_superuser or user.is_staff

    # Force students to pass the SOP gate first before they can see the hub
    if not is_supervisor and not request.session.get('sop_accepted', False):
        return redirect('lab_workflow:sop_gate')

    # 2. Central Instrumentation Definitions Map
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
    ]

    # 3. Dynamic Failover Load-Balancing for NodePorts
    k8s_nodes = ["172.16.2.13", "172.16.2.38", "172.16.2.35", "172.16.2.39"]
    selected_node = random.choice(k8s_nodes)

    # 4. High-Performance Computing Context Configuration Object
    hpc_cluster = {
        "id": "jupyter_gpu",
        "name": "ICCBS GPU Jupyter Notebook Workspace",
        "hardware_spec": "NVIDIA RTX 5000 Shared Cluster Infrastructure",
        "icon": "🎛️",
        "cluster_url": f"http://{selected_node}:32372/hub/spawn"
    }

    # ==========================================
    # EXTRACT DATA FOR ACADEMIC & SERVICES TABS
    # ==========================================
    
    # Fetch student's custom certified SOP instruments
    certified_module_ids = list(StudentSopCertification.objects.filter(
        student=user
    ).values_list('module__instrument_id', flat=True))
    
    # Fetch all baseline SOP training modules available
    sop_modules = SopModule.objects.all()

    # Fetch snapshot of critical stock levels from Central Inventory Store
    critical_inventory = InventoryItem.objects.all()[:6] 

    # PERFORMANCE OPTIMIZATION: Check existing pipeline records in ONE single database query
    existing_stages = set(ThesisPipeline.objects.filter(student=user).values_list('stage', flat=True))
    stages_pool = ['1_synopsis', '2_coursework', '3_data', '4_pub_gate', '5_writing', '6_defense']
    
    # Bulk-create missing milestone stages ONLY if they do not exist yet (e.g., first-time user login)
    missing_stages = [stage for stage in stages_pool if stage not in existing_stages]
    if missing_stages:
        bulk_milestones = [ThesisPipeline(student=user, stage=stage) for stage in missing_stages]
        ThesisPipeline.objects.bulk_create(bulk_milestones)
    
    # Query final ordered pipeline dataset for context rendering
    student_milestones = ThesisPipeline.objects.filter(student=user).order_by('stage')

    # SINGLE COMPREHENSIVE OUTPUT LAYER
    return render(request, 'lab_workflow/service_hub.html', {
        'available_forms': available_forms,
        'hpc_cluster': hpc_cluster,
        'is_supervisor': is_supervisor,
        'sop_modules': sop_modules,
        'certified_module_ids': certified_module_ids,
        'critical_inventory': critical_inventory,
        'student_milestones': student_milestones,
    })

import logging
import re
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import AiResearchSession

logger = logging.getLogger(__name__)

# ── Cluster Endpoints ──────────────────────────────────────────────
BGE_EMBED_URL = "http://192.168.224.177:80/embed"        # embedding-bge pod IP
QDRANT_URL    = "http://192.168.224.180:6333"            # qdrant pod IP

LLM_CLUSTER_URLS = {
    "qwen":     "http://192.168.224.155:8000/v1/chat/completions",
    "mistral":  "http://192.168.166.187:8000/v1/chat/completions",
    "deepseek": "http://192.168.160.15:8000/v1/chat/completions",
}

VLLM_MODEL_NAMES = {
    "qwen":     "Qwen/Qwen2.5-3B-Instruct",
    "mistral":  "mistralai/Mistral-7B-Instruct-v0.2",
    "deepseek": "deepseek-ai/deepseek-coder-6.7b-instruct",
}

SYSTEM_PROMPTS = {
    "qwen":     "You are an expert Medical & Biological Research Assistant at ICCBS, backed by PubMed literature.",
    "mistral":  "You are an expert Computational Chemist at ICCBS, backed by PubChem molecular data.",
    "deepseek": "You are an expert Systems Biology Scientist at ICCBS, backed by BioModels repositories.",
}

SCIENTIFIC_KEYWORDS = [
    "molecule", "compound", "pubmed", "pubchem", "protein", "dna", "rna",
    "drug", "inhibitor", "kinase", "cancer", "mutation", "gene", "egfr",
    "synthesis", "reaction", "toxicity", "formula", "pathway", "signaling",
    "biomodel", "clinical", "genomic", "snp", "enzyme", "receptor", "antibody",
    "cell", "tumor", "therapy", "chemotherapy", "pharmacokinetics", "molecular",
    "isl1", "kmh-1", "sclc", "smiles", "cid", "pmid", "sbml",
]

COLLECTION_MAP = {
    "qwen":     "pubmed",
    "mistral":  "pubchem",
    "deepseek": "biomodels",
}

# Matches explicit paths (/data/, /uploads/) or specific research file extensions
FILE_PATH_REGEX = re.compile(
    r'(/data/|/uploads/|[\w\-]+\.(fasta|fastq|vcf|gff|bed|pdb|mol2?|sdf|smiles|'
    r'docx|txt|csv|xlsx|md|pdf|json|bam|sam|ab1|gbk|genbank|cif|mmcif)\b)',
    re.IGNORECASE
)


def detect_rag_collection(prompt, selected_model):
    """Choose Qdrant collection based on prompt keywords."""
    p = prompt.lower()
    
    # Check BioModels keywords
    if any(k in p for k in ["biomodel", "model2", "biomd", "pathway", "simulate", "sbml", "signaling", "equation", "pharmacokinetics"]):
        return "biomodels"
        
    # Check PubChem keywords
    if any(k in p for k in ["molecule", "compound", "drug", "inhibitor", "smiles", "docking", "pubchem", "cid"]):
        return "pubchem"
        
    # Check PubMed keywords
    if any(k in p for k in ["pubmed", "dna", "rna", "protein", "gene", "cancer", "clinical", "disease", "pmid", "sclc", "isl1", "kmh-1"]):
        return "pubmed"
        
    return COLLECTION_MAP.get(selected_model, "pubmed")


def rag_search(prompt, collection):
    """Embed query and search Qdrant. Returns context string or None."""
    try:
        # Step 1: Embed via BGE (Safe parsing for lists or dict response formats)
        embed_resp = requests.post(
            BGE_EMBED_URL,
            json={"inputs": prompt[:512]},
            timeout=15
        ).json()

        if isinstance(embed_resp, list):
            vec = embed_resp[0]
            if isinstance(vec, dict) and "embedding" in vec:
                vec = vec["embedding"]
        elif isinstance(embed_resp, dict) and "embeddings" in embed_resp:
            vec = embed_resp["embeddings"][0]
        else:
            logger.warning("Unknown BGE embedding response structure")
            return None

        # Step 2: Search Qdrant (Increased limit to 5 for complete context extraction)
        qdrant_resp = requests.post(
            f"{QDRANT_URL}/collections/{collection}/points/search",
            json={"vector": vec, "limit": 5, "with_payload": True},
            timeout=10
        ).json()

        hits = qdrant_resp.get("result", [])
        if not hits:
            return None

        # Step 3: Join contexts safely
        contexts = []
        for h in hits:
            payload = h.get("payload", {})
            # Checks common context field names
            ctx_text = payload.get("context") or payload.get("text") or payload.get("document")
            if ctx_text:
                contexts.append(str(ctx_text))

        return "\n\n".join(contexts) if contexts else None

    except Exception as e:
        logger.warning(f"RAG search failed: {e}")
        return None


@login_required
@csrf_protect
def route_ai_query(request):
    """Routes student prompts — RAG-enhanced for scientific queries."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    selected_model = request.POST.get("model_type")
    user_prompt    = request.POST.get("prompt")

    if not user_prompt:
        return JsonResponse({"error": "Prompt cannot be blank"}, status=400)

    # ── Guard: Short-Circuit Local File References ───────────────────
    if FILE_PATH_REGEX.search(user_prompt):
        return JsonResponse({
            "reply": (
                "📁 <strong>File Access Required</strong><br><br>"
                "This query references a local file path or specific attachment. "
                "Direct file analysis requires the <strong>AI Agent service</strong>.<br><br>"
                "Please switch to the <strong>Agent tab</strong> to upload and parse files, "
                "or copy and paste the file content directly into this prompt."
            )
        })

    target_api = LLM_CLUSTER_URLS.get(selected_model)
    if not target_api:
        return JsonResponse({"error": f"Unknown model: {selected_model}"}, status=400)

    # ── RAG Context Evaluation ──────────────────────────────────────
    is_scientific = any(k in user_prompt.lower() for k in SCIENTIFIC_KEYWORDS)
    rag_context   = None
    rag_used      = False
    collection    = detect_rag_collection(user_prompt, selected_model)

    if is_scientific:
        rag_context = rag_search(user_prompt, collection)
        if rag_context:
            rag_used = True
            logger.info(f"RAG context retrieved from '{collection}' for model '{selected_model}'")
        else:
            logger.info(f"RAG search returned no context for collection '{collection}'")

    # ── Build Prompt Payload ────────────────────────────────────────
    system_instruction = SYSTEM_PROMPTS.get(
        selected_model,
        "You are an expert institutional research assistant at ICCBS."
    )

    if rag_used:
        user_content = (
            f"Use the following context retrieved from the ICCBS institutional "
            f"database to answer the question accurately.\n\n"
            f"--- CONTEXT ---\n{rag_context}\n--- END CONTEXT ---\n\n"
            f"Question: {user_prompt}"
        )
    else:
        user_content = user_prompt

    payload = {
        "model": VLLM_MODEL_NAMES[selected_model],
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user",   "content": user_content},
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(target_api, json=payload, timeout=120)

        if response.status_code != 200:
            return JsonResponse({
                "reply": f"🚨 <strong>Compute Node Exception:</strong> vLLM returned {response.status_code}. {response.text}"
            }, status=response.status_code)

        response_data = response.json()

        if "choices" in response_data and response_data["choices"]:
            ai_reply = response_data["choices"][0]["message"]["content"]
            if rag_used:
                ai_reply += (
                    "<br><br><small style='color:#64748b;'>"
                    f"📚 <em>Response grounded in ICCBS institutional database ({collection} collection)</em>"
                    "</small>"
                )
        else:
            ai_reply = f"🚨 <strong>Malformed Response:</strong> {str(response_data)}"

        return JsonResponse({"reply": ai_reply})

    except requests.exceptions.Timeout:
        return JsonResponse({
            "reply": "⏳ <strong>Connection Interrupted:</strong> Compute pod timeout. Cluster under heavy load."
        })  # Defaults to status=200

    except Exception as e:
        logger.error(f"Error in route_ai_query: {str(e)}")
        return JsonResponse({
            "reply": f"⚠️ <strong>Internal Error:</strong> {str(e)}"
        })  # Defaults to status=200

# ICCBS ai-agent

import json
import logging
import requests

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required

# Ensure models are imported correctly (Adjust module path if necessary)
# from .models import AiResearchSession

logger = logging.getLogger(__name__)

# Direct Pod IP reachability (Matches working setup for Qwen/Mistral/DeepSeek)
AGENTS_SVC_URL = "http://192.168.107.16:8080"


@login_required
@csrf_protect
def route_agents_query(request):
    """
    Dedicated endpoint for the Agents microservice (agents-svc).
    Routes requests directly to http://192.168.107.16:8080/query
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)

    # 1. Parse prompt from JSON body or FormData
    if request.content_type == "application/json":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user_prompt = body.get("prompt")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    else:
        user_prompt = request.POST.get("prompt")

    if not user_prompt:
        return JsonResponse({"error": "Prompt cannot be blank"}, status=400)

    # 2. Prepare payload for the Agents microservice
    payload = {
        "prompt": user_prompt,
        "user_id": request.user.username,
    }

    # 3. Forward to agents-svc
    try:
        response = requests.post(
            f"{AGENTS_SVC_URL}/query",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return JsonResponse({
                "reply": f"⚠️ <strong>Agents Service Error:</strong> Code {response.status_code}. Response: {response.text}"
            }, status=response.status_code)

        data = response.json()
        ai_reply = data.get("reply") or data.get("answer") or str(data)

        # 4. Save session log
        try:
            AiResearchSession.objects.create(
                student=request.user,
                model_used="agents-service",
                prompt_text=user_prompt,
                response_text=ai_reply,
            )
        except Exception as db_err:
            logger.error(f"Failed to log AiResearchSession: {db_err}")

        return JsonResponse({"reply": ai_reply})

    except requests.exceptions.Timeout:
        return JsonResponse({
            "reply": "⚠️ <strong>Timeout:</strong> The agents service took longer than 120s to respond."
        }, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            "reply": f"⚠️ <strong>Connection Error:</strong> Cannot reach agents service at <code>{AGENTS_SVC_URL}</code>. Check pod status."
        }, status=502)
    except Exception as e:
        return JsonResponse({"reply": f"⚠️ <strong>Error:</strong> {str(e)}"}, status=500)


@login_required
@csrf_exempt
def proxy_uploads(request):
    """
    Handles POST (file upload), GET (list files), and DELETE operations 
    by forwarding them directly to the Kubernetes agents service.
    """
    target_url = f"{AGENTS_SVC_URL}/uploads"

    try:
        # --- GET: Retrieve list of uploaded files ---
        if request.method == "GET":
            resp = requests.get(target_url, timeout=10)
            return HttpResponse(
                resp.content, 
                status=resp.status_code, 
                content_type="application/json"
            )

        # --- POST: Process File Upload from JavaScript / Form ---
        elif request.method == "POST":
            if not request.FILES:
                return JsonResponse({"error": "No files provided"}, status=400)

            # Build file dict for multipart forwarding
            files_to_forward = []
            for field_name, file_obj in request.FILES.items():
                file_obj.seek(0)  # Reset buffer position before reading
                files_to_forward.append(
                    ('file', (file_obj.name, file_obj.read(), file_obj.content_type))
                )

            resp = requests.post(target_url, files=files_to_forward, timeout=300)
            return HttpResponse(
                resp.content, 
                status=resp.status_code, 
                content_type="application/json"
            )

        # --- DELETE: Remove file from storage ---
        elif request.method == "DELETE":
            filename = request.GET.get('filename')
            if not filename:
                return JsonResponse({"error": "Filename parameter required"}, status=400)

            resp = requests.delete(f"{target_url}?filename={filename}", timeout=10)
            return HttpResponse(
                resp.content, 
                status=resp.status_code, 
                content_type="application/json"
            )

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except requests.exceptions.Timeout:
        return JsonResponse({"error": "Gateway timeout connecting to agents service"}, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({"error": f"Cannot reach agents service at {AGENTS_SVC_URL}"}, status=502)
    except Exception as e:
        logger.error(f"Error in proxy_uploads: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

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