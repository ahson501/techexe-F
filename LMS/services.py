# LMS/services.py
from django.db.models import Q
from .models import LiveSession, Lesson, Course, SessionAttendance
import requests
import json
import logging
from django.conf import settings


class AdaptiveLearningEngine:
    """
    Analyzes student performance metrics and generates dynamic,
    personalized learning paths and remedial study plans.
    """
    def __init__(self, student, course):
        self.student = student
        self.course = course

    def generate_personalized_remedial_plan(self):
        # 1. Identify missed live sessions
        all_sessions = LiveSession.objects.filter(
            Q(course=self.course) | Q(section__course=self.course)
        )
        attended_session_ids = SessionAttendance.objects.filter(
            student=self.student,
            session__in=all_sessions,
            attended=True
        ).values_list('session_id', flat=True)

        missed_sessions = all_sessions.exclude(id__in=attended_session_ids)

        # 2. Map missed sessions back to recommended course modules/lessons
        recommended_lessons = []
        for session in missed_sessions:
            # Find lessons in the same module or matching topics
            if session.section:
                lessons = Lesson.objects.filter(module__course=self.course)
                for lesson in lessons:
                    recommended_lessons.append({
                        'lesson_id': lesson.id,
                        'lesson_title': lesson.title,
                        'reason': f"Recommended to cover topics missed in live session '{session.title}'",
                    })

        # Deduplicate recommendations
        unique_recommendations = {l['lesson_id']: l for l in recommended_lessons}.values()

        # 3. Formulate custom AI Tutor system prompt override
        ai_focus_topics = [r['lesson_title'] for r in unique_recommendations]
        custom_ai_prompt = (
            f"This student is currently on a remedial path. Focus explanations on simplifying: "
            f"{', '.join(ai_focus_topics[:3]) if ai_focus_topics else 'core foundational concepts'}."
        )

        return {
            'student_id': self.student.id,
            'course_id': self.course.id,
            'missed_session_count': missed_sessions.count(),
            'recommended_lessons': list(unique_recommendations),
            'ai_tutor_focus_prompt': custom_ai_prompt,
        }
    

logger = logging.getLogger(__name__)

class AIAssistanceService:
    """
    AI Co-Pilot service for Faculty (quiz generation) 
    and Administrators (admissions analysis & support helpdesk).
    """
    @classmethod
    def get_llm_url(cls, model_key="qwen"):
        cluster_urls = getattr(settings, "LLM_CLUSTER_URLS", {})
        return cluster_urls.get(model_key, "http://192.168.224.164:8000/v1/chat/completions")

    @classmethod
    def get_model_name(cls, model_key="qwen"):
        model_names = getattr(settings, "VLLM_MODEL_NAMES", {})
        return model_names.get(model_key, "Qwen/Qwen2.5-3B-Instruct")

    @classmethod
    def generate_quiz_from_lesson(cls, lesson_title, lesson_text, question_count=3):
        """Generates structured multiple-choice questions from lesson text."""
        prompt = (
            f"You are an expert academic assessment generator.\n"
            f"Based on the following lesson text, generate {question_count} multiple-choice questions.\n"
            f"Respond ONLY with valid JSON in this exact structure:\n"
            f"[\n"
            f"  {{\n"
            f'    "question": "Question text here?",\n'
            f'    "options": ["Option A", "Option B", "Option C", "Option D"],\n'
            f'    "correct_answer": "Option A",\n'
            f'    "explanation": "Brief explanation why."\n'
            f"  }}\n"
            f"]\n\n"
            f"Lesson Title: {lesson_title}\n"
            f"Lesson Text:\n{lesson_text[:2000]}"
        )

        payload = {
            "model": cls.get_model_name("qwen"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        try:
            response = requests.post(cls.get_llm_url("qwen"), json=payload, timeout=60)
            if response.status_code == 200:
                raw_reply = response.json()["choices"][0]["message"]["content"]
                clean_json = raw_reply.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json.split("```")[1].strip()
                return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            return []

    @classmethod
    def analyze_admission_documents(cls, student_name, applied_course, bio_notes=""):
        """Generates an initial admission summary note for Admissions officers."""
        prompt = (
            f"You are an AI Admissions Evaluation Assistant.\n"
            f"Provide a brief, 3-bullet-point executive summary recommending verification steps for this applicant.\n\n"
            f"Applicant Name: {student_name}\n"
            f"Course / Registration Scope: {applied_course}\n"
            f"Student Profile Details: {bio_notes}\n"
        )

        payload = {
            "model": cls.get_model_name("qwen"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }

        try:
            response = requests.post(cls.get_llm_url("qwen"), json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"vLLM cluster returned status code {response.status_code}."
        except Exception as e:
            logger.error(f"Admissions analysis failed: {e}")
            return f"Unable to reach AI evaluation cluster ({str(e)})."

    @classmethod
    def solve_admin_helpdesk_query(cls, user_query):
        """Automates support desk responses for admissions and portal queries."""
        system_prompt = (
            "You are an AI Admissions & Student Support Desk Assistant for the university LMS.\n"
            "Help students and officers with questions about document verification, fee vouchers, and enrollment rules."
        )

        payload = {
            "model": cls.get_model_name("qwen"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            "temperature": 0.3,
        }

        try:
            response = requests.post(cls.get_llm_url("qwen"), json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return "Support system returned an unexpected status."
        except Exception as e:
            logger.error(f"Admin Helpdesk query failed: {e}")
            return "Support system currently offline."