import json
import logging
import requests

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import DetailView, ListView, View

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .models import Certificate

from .forms import QuizTakeForm
from .models import (
    AnswerChoice,
    Certificate,
    Course,
    Enrollment,
    Lesson,
    LessonProgress,
    Question,
    Quiz,
    QuizAttempt,
)

logger = logging.getLogger(__name__)


# ==========================================
# 1. COURSES & LESSON VIEWS
# ==========================================

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
        
        # Prefetch modules and lessons to avoid N+1 queries
        context['modules'] = self.object.modules.prefetch_related('lessons').order_by('order')
        
        # Check enrollment and certificate status
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
        
        # Verify enrollment or allow preview lessons
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not is_enrolled and not lesson.is_preview:
            return redirect('course_detail', slug=course.slug)
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        course = lesson.module.course
        user = self.request.user

        # Fetch full navigation tree for sidebar
        modules = course.modules.prefetch_related('lessons').order_by('order')
        
        # Get completed lessons set for the current user
        completed_lesson_ids = set(
            LessonProgress.objects.filter(
                student=user,
                lesson__module__course=course,
                is_completed=True
            ).values_list('lesson_id', flat=True)
        )

        # Track view on current lesson
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

        return redirect('lesson_detail', pk=lesson.pk)


# ==========================================
# 2. QUIZ VIEWS
# ==========================================

class QuizTakeView(LoginRequiredMixin, View):
    template_name = 'LMS/quiz_take.html'

    def dispatch(self, request, *args, **kwargs):
        quiz = self.get_quiz(kwargs['pk'])
        course = quiz.module.course
        
        # Verify enrollment
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not is_enrolled:
            return redirect('course_detail', slug=course.slug)

        # Check maximum attempts limit
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

        # --- SCORING ENGINE ---
        total_points = 0
        earned_points = 0

        for question in quiz.questions.all():
            field_name = f"question_{question.id}"
            user_answer = form.cleaned_data.get(field_name)
            
            correct_choice_ids = set(
                question.choices.filter(is_correct=True).values_list('id', flat=True)
            )
            
            total_points += question.points

            if question.question_type in [Question.QuestionType.SINGLE_CHOICE, Question.QuestionType.TRUE_FALSE]:
                if user_answer and int(user_answer) in correct_choice_ids:
                    earned_points += question.points

            elif question.question_type == Question.QuestionType.MULTIPLE_CHOICE:
                selected_ids = set(int(cid) for cid in user_answer) if user_answer else set()
                if selected_ids == correct_choice_ids:
                    earned_points += question.points

        score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0.0
        score_percentage = round(score_percentage, 2)
        passed = score_percentage >= quiz.pass_mark_percentage

        previous_attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
        
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score_percentage=score_percentage,
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
        latest_attempt = (
            QuizAttempt.objects.filter(student=request.user, quiz_id=pk)
            .order_by('-created_at')
            .first()
        )

        if latest_attempt:
            return redirect('quiz_result_detail', pk=latest_attempt.pk)
        return redirect('quiz_take', pk=pk)


# ==========================================
# 3. K8S VLLM AI TEACHING ASSISTANT
# ==========================================

BGE_EMBED_URL = getattr(settings, "BGE_EMBED_URL", "http://192.168.160.19:80/embed")
QDRANT_URL    = getattr(settings, "QDRANT_URL", "http://192.168.160.46:6333")

LLM_CLUSTER_URLS = {
    "qwen":     "http://192.168.224.182:8000/v1/chat/completions",
    "mistral":  "http://192.168.166.148:8000/v1/chat/completions",
    "deepseek": "http://192.168.160.44:8000/v1/chat/completions",
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
    """
    LMS AI Teaching Assistant: 
    Routes student queries to self-hosted K8s vLLM cluster (Qwen/Mistral/DeepSeek)
    with lesson-specific context and optional Qdrant RAG grounding.
    """

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

            lesson = get_object_or_404(
                Lesson.objects.select_related("module__course"), 
                pk=lesson_id
            )

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
                f"- Be clear, concise, and pedagogical.\n"
                f"- If the question is off-topic, gently redirect the student to the lesson material."
            )

            user_content = (
                f"Additional Reference Context:\n\n{rag_context}\n\nQuestion: {user_message}"
                if rag_used else user_message
            )

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
                return JsonResponse({
                    "reply": f"🚨 <strong>vLLM Cluster Error ({response.status_code}):</strong> {response.text}"
                }, status=response.status_code)

            response_data = response.json()

            if "choices" in response_data and response_data["choices"]:
                ai_reply = response_data["choices"][0]["message"]["content"]
                badge_info = f"🤖 <em>Answered by <strong>{selected_model.upper()}</strong>"
                if rag_used:
                    badge_info += " · Grounded with Qdrant RAG"
                badge_info += "</em>"
                ai_reply += f"<br><br><small style='color:#64748b;'>{badge_info}</small>"
            else:
                ai_reply = f"🚨 Malformed response from cluster: {str(response_data)}"

            return JsonResponse({"reply": ai_reply})

        except requests.exceptions.Timeout:
            return JsonResponse({
                "reply": "⏳ <strong>Cluster Timeout:</strong> The AI model pod took longer than 120s to respond."
            }, status=504)
        except requests.exceptions.ConnectionError as err:
            logger.error(f"Failed to connect to vLLM Pod: {err}")
            return JsonResponse({
                "reply": "⚠️ <strong>Cluster Error:</strong> Unable to connect to Kubernetes vLLM pod."
            }, status=502)
        except Exception as e:
            logger.exception("Unexpected error in AIChatAssistantView")
            return JsonResponse({"reply": f"⚠️ Internal Error: {str(e)}"}, status=500)

    def perform_rag_search(self, prompt, model_key):
        try:
            embed_resp = requests.post(
                BGE_EMBED_URL,
                json={"inputs": prompt[:512]},
                timeout=10
            ).json()

            if isinstance(embed_resp, list):
                vec = embed_resp[0]
                if isinstance(vec, dict) and "embedding" in vec:
                    vec = vec["embedding"]
            elif isinstance(embed_resp, dict) and "embeddings" in embed_resp:
                vec = embed_resp["embeddings"][0]
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
            if not hits:
                return None

            contexts = []
            for h in hits:
                payload = h.get("payload", {})
                ctx_text = payload.get("context") or payload.get("text") or payload.get("document")
                if ctx_text:
                    contexts.append(str(ctx_text))

            return "\n\n".join(contexts) if contexts else None

        except Exception as err:
            logger.warning(f"LMS RAG search skipped: {err}")
            return None


# ==========================================
# 4. CERTIFICATES
# ==========================================

class DownloadCertificatePillowView(View):
    def get(self, request, certificate_id):
        cert = get_object_or_404(Certificate, id=certificate_id, student=request.user)

        # 1. Create a blank landscape canvas (A4 @ 300 DPI: 3508 x 2480 px)
        img = Image.new('RGB', (3508, 2480), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 2. Draw border
        draw.rectangle([100, 100, 3408, 2380], outline=(37, 99, 235), width=20)

        # 3. Add text (using standard fonts or loaded TTF)
        font_large = ImageFont.load_default() # Or ImageFont.truetype("arial.ttf", 100)
        
        draw.text((1754, 500), "CERTIFICATE OF COMPLETION", fill=(30, 58, 138), anchor="mm", font=font_large)
        draw.text((1754, 900), f"This is presented to: {cert.student.username}", fill=(15, 23, 42), anchor="mm")
        draw.text((1754, 1200), f"Course: {cert.course.title}", fill=(37, 99, 235), anchor="mm")
        draw.text((1754, 1500), f"Code: {cert.certificate_code}", fill=(100, 116, 139), anchor="mm")

        # 4. Save directly as PDF into memory buffer
        pdf_buffer = BytesIO()
        img.save(pdf_buffer, format='PDF', resolution=300.0)
        pdf_buffer.seek(0)

        # 5. Return HTTP Response
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Certificate_{cert.certificate_code}.pdf"'
        return response