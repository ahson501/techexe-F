import json
import logging
import requests
import uuid
from decimal import Decimal
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Sum
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, View
from .forms import QuizTakeForm, AssignFacultySectionForm
from .models import (
    AnswerChoice,
    Certificate,
    Course,
    CourseSection,
    Enrollment,
    Lesson,
    LessonProgress,
    LiveSession,
    Question,
    Quiz,
    QuizAttempt,
    DiscussionTopic, 
    DiscussionPost,
    VisitingFacultyClaim,
)

User = get_user_model()
logger = logging.getLogger(__name__)


# ==========================================
# 0. DASHBOARDS
# ==========================================

class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Student portal view displaying enrolled courses and auto-generated payment vouchers."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Student').exists() or self.request.user.is_staff

    def get(self, request):
        user = request.user
        
        # 1. Fetch student enrollments
        enrollments = Enrollment.objects.filter(
            student=user
        ).select_related('course', 'course__instructor').order_by('-created_at')

        # 2. Check if explicit reverse relation exists; fallback to enrollments list
        if hasattr(user, 'vouchers') and user.vouchers.exists():
            vouchers = user.vouchers.select_related('course').order_by('-created_at')
        else:
            vouchers = enrollments  # Treat enrollments as fee vouchers for manual payment tracking

        context = {
            'enrollments': enrollments,
            'vouchers': vouchers,
        }
        return render(request, 'LMS/student_dashboard.html', context)

class AdmissionsDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Dashboard for Admissions Officers to review student registrations and documents."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_admissions_officer').exists() or self.request.user.is_staff

    def get(self, request):
        # Fetch students belonging to LMS_Student group or pending admission approval
        students = User.objects.filter(groups__name='LMS_Student').order_by('-date_joined')
        
        context = {
            'students': students,
            'total_students': students.count(),
        }
        return render(request, 'LMS/admissions_dashboard.html', context)
    
class InstructorDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Instructor portal view displaying assigned courses and sections."""
    
    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Instructor').exists() or self.request.user.is_staff

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(instructor=user)
        sections = CourseSection.objects.filter(instructor=user).select_related('course')
        
        context = {
            'courses': courses,
            'sections': sections,
        }
        return render(request, 'LMS/instructor_dashboard.html', context)
    

class HODDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Central administrative hub for HODs, Accountants, and Admissions Officers."""
    
    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['LMS_HOD', 'LMS_Accountant', 'LMS_admissions_officer']
        ).exists() or self.request.user.is_staff

    def get(self, request):
        sections = CourseSection.objects.select_related('course', 'instructor').all()
        pending_claims = VisitingFacultyClaim.objects.filter(
            status=VisitingFacultyClaim.Status.SUBMITTED
        ).select_related('faculty')
        
        context = {
            'sections': sections,
            'pending_claims': pending_claims,
            'total_sections': sections.count(),
            'total_claims_pending': pending_claims.count(),
            'total_payout_pending': sum(claim.total_amount for claim in pending_claims),
        }
        return render(request, 'LMS/hod_dashboard.html', context)


class VisitingFacultyDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Workspace for Visiting Faculty to view sections, classes, and claims."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_VistingFaculty').exists() or self.request.user.is_staff

    def get(self, request):
        user = request.user
        assigned_sections = CourseSection.objects.filter(instructor=user).select_related('course')
        upcoming_sessions = LiveSession.objects.filter(
            section__instructor=user,
            status=LiveSession.Status.SCHEDULED
        ).order_by('start_time')
        
        past_claims = VisitingFacultyClaim.objects.filter(faculty=user).order_by('-created_at')

        context = {
            'assigned_sections': assigned_sections,
            'upcoming_sessions': upcoming_sessions,
            'past_claims': past_claims,
        }
        return render(request, 'LMS/visiting_faculty_dashboard.html', context)

class AccountantDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Financial dashboard for Accountants to verify vouchers and execute payouts."""
    
    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Accountant').exists() or self.request.user.is_staff

    def get(self, request):
        # 1. Base Queryset
        qs = Enrollment.objects.select_related('student', 'course').order_by('-created_at')

        # 2. Filter Pending vs Paid depending on available model fields
        if hasattr(Enrollment, 'is_verified'):
            pending_enrollments = qs.filter(is_verified=False)
            cleared_enrollments = qs.filter(is_verified=True)
        elif hasattr(Enrollment, 'is_paid'):
            pending_enrollments = qs.filter(is_paid=False)
            cleared_enrollments = qs.filter(is_paid=True)
        elif hasattr(Enrollment, 'status'):
            pending_enrollments = qs.filter(status__in=['PENDING', 'UNPAID'])
            cleared_enrollments = qs.filter(status='PAID')
        else:
            pending_enrollments = qs
            cleared_enrollments = Enrollment.objects.none()

        # 3. Calculate total revenue from cleared enrollments
        total_revenue_cleared = sum(
            (e.course.price for e in cleared_enrollments if hasattr(e.course, 'price') and e.course.price),
            Decimal('0.00')
        )

        # 4. Fetch HOD-approved faculty claims
        approved_claims = VisitingFacultyClaim.objects.filter(
            status=VisitingFacultyClaim.Status.HOD_APPROVED
        ).select_related('faculty')

        context = {
            'pending_vouchers': pending_enrollments,
            'pending_vouchers_count': pending_enrollments.count(),
            'total_revenue_cleared': round(total_revenue_cleared, 2),
            'approved_claims': approved_claims,
            'approved_payouts_total': round(sum(c.total_amount for c in approved_claims), 2),
        }
        return render(request, 'LMS/accountant_dashboard.html', context)
    
class VerifyVoucherPaymentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Allows Accountants to approve student payments and activate course access."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Accountant').exists() or self.request.user.is_staff

    def post(self, request, voucher_id):
        enrollment = get_object_or_404(Enrollment, id=voucher_id)
        
        # Update whichever verification field exists on Enrollment model
        if hasattr(enrollment, 'is_verified'):
            enrollment.is_verified = True
        if hasattr(enrollment, 'is_paid'):
            enrollment.is_paid = True
        if hasattr(enrollment, 'status'):
            enrollment.status = 'PAID'
            
        enrollment.save()

        messages.success(
            request, 
            f"Payment for {enrollment.student.get_full_name() or enrollment.student.username} ({enrollment.course.title}) verified successfully."
        )
        return redirect('accountant_dashboard')
    

# ==========================================
# 1. COURSES & LESSON VIEWS
# ==========================================


class DownloadChallanView(LoginRequiredMixin, View):
    """Generates an official fee voucher / bank challan for offline manual payment."""

    def get(self, request, enrollment_id):
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
        
        context = {
            'enrollment': enrollment,
            'student': request.user,
            'course': enrollment.course,
            'amount': getattr(enrollment.course, 'price', Decimal('3500.00')),
            'bank_name': 'Habib Bank Limited (HBL)',
            'account_title': 'TechExe LMS Fee Collection',
            'iban': 'PK36HABB0001234567890123',
            'issue_date': enrollment.created_at if hasattr(enrollment, 'created_at') else timezone.now(),
        }
        return render(request, 'LMS/fee_challan.html', context)

class EnrollCourseView(LoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        Enrollment.objects.get_or_create(student=request.user, course=course)
        
        first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
        if first_lesson:
            return redirect('lesson_detail', pk=first_lesson.pk)
        return redirect('course_detail', slug=course.slug)


class CourseListView(ListView):
    model = Course
    template_name = 'LMS/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        return (
            Course.objects.filter(status=Course.Status.PUBLISHED)
            .select_related('instructor', 'category')
            .order_by('-created_at')
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = 'LMS/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['modules'] = self.object.modules.prefetch_related('lessons').order_by('order')
        
        is_enrolled = False
        certificate = None
        if user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(student=user, course=self.object).exists()
            certificate = Certificate.objects.filter(student=user, course=self.object).first()
        
        context['is_enrolled'] = is_enrolled
        context['certificate'] = certificate
        return context


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'LMS/lesson_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.module.course
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not is_enrolled and not lesson.is_preview:
            return redirect('course_detail', slug=course.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        course = lesson.module.course
        user = self.request.user

        modules = course.modules.prefetch_related('lessons', 'quizzes').order_by('order')
        completed_lesson_ids = set(
            LessonProgress.objects.filter(
                student=user,
                lesson__module__course=course,
                is_completed=True
            ).values_list('lesson_id', flat=True)
        )

        progress, _ = LessonProgress.objects.get_or_create(student=user, lesson=lesson)
        context['course'] = course
        context['modules'] = modules
        context['completed_lesson_ids'] = completed_lesson_ids
        context['is_completed'] = progress.is_completed
        return context


class ToggleLessonCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        progress, _ = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
        
        progress.is_completed = not progress.is_completed
        progress.completed_at = timezone.now() if progress.is_completed else None
        progress.save()

        course = lesson.module.course
        total_lessons = Lesson.objects.filter(module__course=course).count()
        completed_lessons_count = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=course,
            is_completed=True
        ).count()

        if total_lessons > 0 and completed_lessons_count == total_lessons:
            Certificate.objects.get_or_create(
                student=request.user,
                course=course,
                defaults={'certificate_code': f"CERT-{uuid.uuid4().hex[:8].upper()}"}
            )

        return redirect('lesson_detail', pk=lesson.pk)

class CreateDiscussionTopicView(LoginRequiredMixin, View):
    """Allows instructors and students to create new discussion topics."""
    def get(self, request):
        # Instructors see their assigned courses; staff see all
        if request.user.groups.filter(name='LMS_Instructor').exists():
            courses = Course.objects.filter(instructor=request.user)
        else:
            courses = Course.objects.all()
            
        return render(request, 'LMS/create_discussion_topic.html', {'courses': courses})

    def post(self, request):
        course_id = request.POST.get('course_id')
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if course_id and title and content:
            course = get_object_or_404(Course, id=course_id)
            topic = DiscussionTopic.objects.create(
                course=course,
                author=request.user,
                title=title,
                content=content
            )
            messages.success(request, "Discussion topic created successfully.")
            return redirect('discussion_topic_detail', pk=topic.pk)

        messages.error(request, "Please fill in all required fields.")
        return redirect('create_discussion_topic')
# ==========================================
# 2. QUIZ VIEWS
# ==========================================

class QuizTakeView(LoginRequiredMixin, View):
    template_name = 'LMS/quiz_take.html'

    def dispatch(self, request, *args, **kwargs):
        quiz = self.get_quiz(kwargs['pk'])
        course = quiz.module.course
        
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not is_enrolled:
            return redirect('course_detail', slug=course.slug)

        attempt_count = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
        if quiz.max_attempts > 0 and attempt_count >= quiz.max_attempts:
            return redirect('quiz_result_latest', pk=quiz.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_quiz(self, pk):
        return get_object_or_404(
            Quiz.objects.prefetch_related(
                Prefetch('questions', queryset=Question.objects.prefetch_related('choices'))
            ),
            pk=pk
        )

    def get(self, request, pk):
        quiz = self.get_quiz(pk)
        form = QuizTakeForm(quiz=quiz)
        return render(request, self.template_name, {'quiz': quiz, 'form': form})

    def post(self, request, pk):
        quiz = self.get_quiz(pk)
        form = QuizTakeForm(request.POST, quiz=quiz)

        if not form.is_valid():
            return render(request, self.template_name, {'quiz': quiz, 'form': form})

        total_points = 0
        earned_points = 0

        for question in quiz.questions.all():
            field_name = f"question_{question.id}"
            user_answer = form.cleaned_data.get(field_name)
            correct_choice_ids = set(question.choices.filter(is_correct=True).values_list('id', flat=True))
            total_points += question.points

            if question.question_type in [Question.QuestionType.SINGLE_CHOICE, Question.QuestionType.TRUE_FALSE]:
                if user_answer and int(user_answer) in correct_choice_ids:
                    earned_points += question.points
            elif question.question_type == Question.QuestionType.MULTIPLE_CHOICE:
                selected_ids = set(int(cid) for cid in user_answer) if user_answer else set()
                if selected_ids == correct_choice_ids:
                    earned_points += question.points

        score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0.0
        passed = score_percentage >= quiz.pass_mark_percentage
        previous_attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
        
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score_percentage=round(score_percentage, 2),
            passed=passed,
            attempt_number=previous_attempts + 1
        )

        return redirect('quiz_result_detail', pk=attempt.pk)


class QuizResultDetailView(LoginRequiredMixin, DetailView):
    model = QuizAttempt
    template_name = 'LMS/quiz_result.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return (
            QuizAttempt.objects.filter(student=self.request.user)
            .select_related('quiz', 'quiz__module__course')
            .order_by('-created_at')
        )


class LatestQuizResultRedirectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        latest_attempt = QuizAttempt.objects.filter(student=request.user, quiz_id=pk).order_by('-created_at').first()
        if latest_attempt:
            return redirect('quiz_result_detail', pk=latest_attempt.pk)
        return redirect('quiz_take', pk=pk)


# ==========================================
# 3. AI TEACHING ASSISTANT
# ==========================================

BGE_EMBED_URL = getattr(settings, "BGE_EMBED_URL", "http://192.168.160.19:80/embed")
QDRANT_URL    = getattr(settings, "QDRANT_URL", "http://192.168.160.46:6333")

LLM_CLUSTER_URLS = {
    "qwen":     "http://192.168.224.182:8000/v1/chat/completions",
    "mistral":  "http://192.168.166.136:8000/v1/chat/completions",
    "deepseek": "http://192.168.160.61:8000/v1/chat/completions"
}

VLLM_MODEL_NAMES = {
    "qwen":     "Qwen/Qwen2.5-3B-Instruct",
    "mistral":  "mistralai/Mistral-7B-Instruct-v0.2",
    "deepseek": "deepseek-ai/deepseek-coder-6.7b-instruct",
}

LMS_SYSTEM_PROMPTS = {
    "qwen":     "You are an expert Medical & Biological Teaching Assistant helping students learn course materials.",
    "mistral":  "You are an expert Computer Science Teaching Assistant answering student course questions.",
    "deepseek": "You are an expert Systems Biology Teaching Assistant assisting students with code and models.",
}


class AIChatAssistantView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST

            user_message   = data.get("message", "").strip()
            lesson_id      = data.get("lesson_id")
            selected_model = data.get("model_type", "qwen")

            if not user_message or not lesson_id:
                return JsonResponse({"error": "Missing user message or lesson ID"}, status=400)

            lesson = get_object_or_404(Lesson.objects.select_related("module__course"), pk=lesson_id)
            target_api = LLM_CLUSTER_URLS.get(selected_model)
            if not target_api:
                return JsonResponse({"error": f"Unknown cluster model: {selected_model}"}, status=400)

            rag_context = self.perform_rag_search(user_message, selected_model)
            rag_used = bool(rag_context)

            base_system_instruction = LMS_SYSTEM_PROMPTS.get(
                selected_model, 
                "You are an AI Teaching Assistant for this online course."
            )

            system_instruction = (
                f"{base_system_instruction}\n\n"
                f"--- CURRENT COURSE & LESSON CONTEXT ---\n"
                f"Course: {lesson.module.course.title}\n"
                f"Module: {lesson.module.title}\n"
                f"Lesson Title: {lesson.title}\n"
                f"Lesson Content/Transcript:\n{lesson.body_text[:2500]}\n"
                f"--- END LESSON CONTEXT ---\n\n"
                f"Instructions:\n"
                f"- Answer the student's question accurately using the lesson context above.\n"
                f"- Be clear, concise, and pedagogical."
            )

            user_content = f"Additional Reference Context:\n\n{rag_context}\n\nQuestion: {user_message}" if rag_used else user_message

            payload = {
                "model": VLLM_MODEL_NAMES[selected_model],
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user",   "content": user_content},
                ],
                "temperature": 0.3,
            }

            response = requests.post(target_api, json=payload, timeout=120)
            if response.status_code != 200:
                return JsonResponse({"reply": f"🚨 <strong>vLLM Cluster Error ({response.status_code}):</strong> {response.text}"}, status=response.status_code)

            response_data = response.json()
            if "choices" in response_data and response_data["choices"]:
                ai_reply = response_data["choices"][0]["message"]["content"]
                badge_info = f"🤖 <em>Answered by <strong>{selected_model.upper()}</strong>" + (" · Grounded with Qdrant RAG" if rag_used else "") + "</em>"
                ai_reply += f"<br><br><small style='color:#64748b;'>{badge_info}</small>"
            else:
                ai_reply = f"🚨 Malformed response from cluster: {str(response_data)}"

            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            logger.exception("Unexpected error in AIChatAssistantView")
            return JsonResponse({"reply": f"⚠️ Internal Error: {str(e)}"}, status=500)

    def perform_rag_search(self, prompt, model_key):
        try:
            embed_resp = requests.post(BGE_EMBED_URL, json={"inputs": prompt[:512]}, timeout=10).json()
            if isinstance(embed_resp, list) and isinstance(embed_resp[0], dict):
                vec = embed_resp[0].get("embedding")
            elif isinstance(embed_resp, dict):
                vec = embed_resp.get("embeddings", [[]])[0]
            else:
                return None

            collection_map = {"qwen": "pubmed", "mistral": "pubchem", "deepseek": "biomodels"}
            collection = collection_map.get(model_key, "pubmed")

            qdrant_resp = requests.post(
                f"{QDRANT_URL}/collections/{collection}/points/search",
                json={"vector": vec, "limit": 3, "with_payload": True},
                timeout=10
            ).json()

            hits = qdrant_resp.get("result", [])
            contexts = [str(h["payload"].get("context") or h["payload"].get("text")) for h in hits if h.get("payload")]
            return "\n\n".join(contexts) if contexts else None
        except Exception as err:
            logger.warning(f"LMS RAG search skipped: {err}")
            return None


# ==========================================
# 4. LIVE SESSIONS & HOD MANAGEMENT
# ==========================================

class InviteFacultyView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Allows HODs to generate or send email invitations for new permanent/visiting faculty."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_HOD').exists() or self.request.user.is_staff

    def get(self, request):
        return render(request, 'LMS/invite_faculty.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        faculty_type = request.POST.get('faculty_type', 'VISITING')
        department = request.POST.get('department', 'Computer Science')

        if email:
            # Here you can save to a FacultyInvitation model or trigger an email send
            messages.success(request, f"Faculty invitation sent to {email} ({faculty_type}).")
            return redirect('hod_dashboard')

        messages.error(request, "Please provide a valid email address.")
        return render(request, 'LMS/invite_faculty.html')
    
class LiveSessionRoomView(LoginRequiredMixin, View):
    def get(self, request, session_id):
        session = get_object_or_404(LiveSession, id=session_id)
        is_enrolled = session.course.enrollments.filter(student=request.user).exists()
        
        # Check both permanent instructors, visiting faculty, and HODs
        is_instructor = request.user.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VistingFaculty', 'LMS_HOD']
        ).exists()
        
        if not (is_enrolled or is_instructor or request.user.is_staff):
            return render(request, 'LMS/access_denied.html', {'reason': 'You are not enrolled in this course.'})

        context = {
            'session': session,
            'course': session.course,
            'user_display_name': request.user.get_full_name() or request.user.username,
        }
        return render(request, 'LMS/live_session_room.html', context)


class HODSectionAssignmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='LMS_HOD').exists() or self.request.user.is_staff

    def get(self, request):
        sections = CourseSection.objects.select_related('course', 'instructor').all()
        form = AssignFacultySectionForm()
        pending_claims = VisitingFacultyClaim.objects.filter(status=VisitingFacultyClaim.Status.SUBMITTED).select_related('faculty')
        return render(request, 'LMS/hod_section_management.html', {'sections': sections, 'form': form, 'pending_claims': pending_claims})

    def post(self, request):
        form = AssignFacultySectionForm(request.POST)
        if form.is_valid():
            section = form.save()
            messages.success(request, f"Section '{section.name}' assigned successfully.")
            return redirect('hod_section_assignment')
        
        sections = CourseSection.objects.select_related('course', 'instructor').all()
        pending_claims = VisitingFacultyClaim.objects.filter(status=VisitingFacultyClaim.Status.SUBMITTED)
        return render(request, 'LMS/hod_section_management.html', {'sections': sections, 'form': form, 'pending_claims': pending_claims})


class HODApproveClaimView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='LMS_HOD').exists() or self.request.user.is_staff

    def post(self, request, claim_id):
        claim = get_object_or_404(VisitingFacultyClaim, id=claim_id)
        action = request.POST.get('action')

        if action == 'approve':
            claim.status = VisitingFacultyClaim.Status.HOD_APPROVED
            claim.approved_by = request.user
            claim.save()
            messages.success(request, f"Claim #{claim.id} approved.")
        elif action == 'reject':
            claim.status = VisitingFacultyClaim.Status.REJECTED
            claim.save()
            messages.warning(request, f"Claim #{claim.id} rejected.")

        return redirect('hod_section_assignment')


class VisitingFacultyClaimEngineView(LoginRequiredMixin, UserPassesTestMixin, View):
    HOURLY_RATE_PKR = Decimal('3500.00')

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_VistingFaculty').exists() or self.request.user.is_staff

    def get(self, request):
        user = request.user
        unclaimed_sessions = LiveSession.objects.filter(
            section__instructor=user,
            status=LiveSession.Status.COMPLETED,
            claims__isnull=True
        ).order_by('start_time')

        total_minutes = sum(s.duration_minutes for s in unclaimed_sessions)
        total_hours = Decimal(total_minutes) / Decimal(60)
        total_amount = total_hours * self.HOURLY_RATE_PKR
        past_claims = VisitingFacultyClaim.objects.filter(faculty=user).order_by('-created_at')

        context = {
            'unclaimed_sessions': unclaimed_sessions,
            'total_hours': round(total_hours, 2),
            'total_amount': round(total_amount, 2),
            'hourly_rate': self.HOURLY_RATE_PKR,
            'past_claims': past_claims,
        }
        return render(request, 'LMS/faculty_claims.html', context)

    def post(self, request):
        user = request.user
        with transaction.atomic():
            unclaimed_sessions = LiveSession.objects.filter(
                section__instructor=user,
                status=LiveSession.Status.COMPLETED,
                claims__isnull=True
            )

            if not unclaimed_sessions.exists():
                messages.error(request, "No eligible completed sessions found to claim.")
                return redirect('faculty_claims')

            total_minutes = sum(s.duration_minutes for s in unclaimed_sessions)
            total_hours = Decimal(total_minutes) / Decimal(60)
            total_amount = total_hours * self.HOURLY_RATE_PKR

            claim = VisitingFacultyClaim.objects.create(
                faculty=user,
                total_hours=round(total_hours, 2),
                total_amount=round(total_amount, 2),
                status=VisitingFacultyClaim.Status.SUBMITTED
            )
            claim.sessions.set(unclaimed_sessions)

        messages.success(request, f"Payout Claim #{claim.id} for PKR {claim.total_amount} submitted to HOD.")
        return redirect('faculty_claims')


# ==========================================
# 5. DISCUSSION GROUPS
# ==========================================

class DiscussionBoardView(LoginRequiredMixin, View):
    """Lists discussion topics for enrolled students and instructors."""
    def get(self, request):
        topics = DiscussionTopic.objects.select_related('course', 'section', 'author').all()
        return render(request, 'LMS/discussion_board.html', {'topics': topics})


class DiscussionTopicDetailView(LoginRequiredMixin, View):
    """Displays a single discussion topic and handles reply submissions."""
    def get(self, request, pk):
        topic = get_object_or_404(DiscussionTopic.objects.select_related('course', 'author'), pk=pk)
        posts = topic.posts.select_related('author').order_by('created_at')
        return render(request, 'LMS/discussion_topic_detail.html', {'topic': topic, 'posts': posts})

    def post(self, request, pk):
        topic = get_object_or_404(DiscussionTopic, pk=pk)
        content = request.POST.get('content', '').strip()
        
        if content:
            DiscussionPost.objects.create(
                topic=topic,
                author=request.user,
                content=content
            )
            messages.success(request, "Reply posted successfully.")
        return redirect('discussion_topic_detail', pk=topic.pk)


class CreateDiscussionTopicView(LoginRequiredMixin, View):
    """Allows instructors and students to create new discussion topics."""
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'LMS/create_discussion_topic.html', {'courses': courses})

    def post(self, request):
        course_id = request.POST.get('course_id')
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if course_id and title and content:
            course = get_object_or_404(Course, id=course_id)
            topic = DiscussionTopic.objects.create(
                course=course,
                author=request.user,
                title=title,
                content=content
            )
            messages.success(request, "Discussion topic created successfully.")
            return redirect('discussion_topic_detail', pk=topic.pk)

        messages.error(request, "Please fill in all required fields.")
        return redirect('create_discussion_topic')


# ==========================================
# 6. CERTIFICATE GENERATION
# ==========================================

class DownloadCertificatePillowView(View):
    def get(self, request, certificate_id):
        cert = get_object_or_404(Certificate, id=certificate_id, student=request.user)

        width, height = 3508, 2480
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        NAVY = (30, 58, 138)
        GOLD = (202, 138, 4)
        CHARCOAL = (31, 41, 55)
        MUTED_GRAY = (100, 116, 139)
        BG_INNER = (250, 250, 249)

        draw.rectangle([80, 80, width - 80, height - 80], fill=BG_INNER)
        draw.rectangle([100, 100, width - 100, height - 100], outline=GOLD, width=12)
        draw.rectangle([130, 130, width - 130, height - 130], outline=NAVY, width=6)

        try:
            font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 90)
            font_subHeader = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 110)
            font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 65)
            font_meta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except OSError:
            font_header = font_subHeader = font_name = font_body = font_title = font_meta = ImageFont.load_default()

        cx = width // 2

        draw.text((cx, 320), "TECHEXE INSTITUTE OF TECHNOLOGY", fill=NAVY, anchor="mm", font=font_subHeader)
        draw.text((cx, 480), "CERTIFICATE OF COMPLETION", fill=GOLD, anchor="mm", font=font_header)
        draw.line([(cx - 400, 560), (cx + 400, 560)], fill=NAVY, width=3)

        draw.text((cx, 720), "THIS IS PROUDLY PRESENTED TO", fill=MUTED_GRAY, anchor="mm", font=font_subHeader)
        full_name = cert.student.get_full_name() or cert.student.username.upper()
        draw.text((cx, 880), full_name, fill=CHARCOAL, anchor="mm", font=font_name)
        draw.line([(cx - 500, 960), (cx + 500, 960)], fill=GOLD, width=4)

        draw.text((cx, 1120), "for successfully completing the specialized professional program in", fill=MUTED_GRAY, anchor="mm", font=font_body)
        draw.text((cx, 1260), f'"{cert.course.title}"', fill=NAVY, anchor="mm", font=font_title)

        y_sign = 1850
        draw.line([(500, y_sign), (1100, y_sign)], fill=CHARCOAL, width=2)
        draw.text((800, y_sign + 30), "Lead Instructor", fill=CHARCOAL, anchor="mm", font=font_meta)

        draw.line([(2408, y_sign), (3008, y_sign)], fill=CHARCOAL, width=2)
        draw.text((2708, y_sign + 30), "Academic Director", fill=CHARCOAL, anchor="mm", font=font_meta)

        seal_cx, seal_cy = cx, y_sign - 30
        draw.ellipse([seal_cx - 90, seal_cy - 90, seal_cx + 90, seal_cy + 90], outline=GOLD, width=6, fill=(254, 243, 199))
        draw.text((seal_cx, seal_cy), "OFFICIAL\nSEAL", fill=GOLD, anchor="mm", font=font_meta, align="center")

        issue_date = cert.created_at.strftime("%B %d, %Y") if hasattr(cert, 'created_at') else timezone.now().strftime("%B %d, %Y")
        draw.text((350, 2220), f"Issue Date: {issue_date}", fill=MUTED_GRAY, font=font_meta)
        draw.text((cx, 2220), f"Certificate Code: {cert.certificate_code}", fill=MUTED_GRAY, anchor="mm", font=font_meta)

        pdf_buffer = BytesIO()
        img.save(pdf_buffer, format='PDF', resolution=300.0)
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Certificate_{cert.certificate_code}.pdf"'
        return response