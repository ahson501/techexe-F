# Standard Library Imports
import os
import json
import logging
import uuid
import qrcode
from decimal import Decimal
from io import BytesIO

# Third-Party Imports
import requests
from PIL import Image, ImageDraw, ImageFont


# Django Core & Auth Imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.db import transaction
from django.db.models import Count, Prefetch, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, View
# services
from .services import AIAssistanceService

# Local Application Imports
from .forms import AssignFacultySectionForm, QuizTakeForm
from .models import (
    AnswerChoice,
    Certificate,
    Enrollment,
    Course,
    CourseSection,
    DiscussionComment,
    DiscussionPost,
    DiscussionTopic,
    Enrollment,
    FacultyInvitation,
    Lesson,
    LessonProgress,
    LiveSession,
    SessionAttendance,
    Question,
    Quiz,
    QuizAttempt,
    StudentProfile,
    VisitingFacultyClaim,
)
from django.contrib.auth.decorators import login_required

User = get_user_model()
logger = logging.getLogger(__name__)


# ==========================================
# 0. DASHBOARDS
# ==========================================

class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
   
    def test_func(self):
        user = self.request.user
        # Require user to be active AND belong to LMS_Student group (or staff)
        return user.is_active and (user.groups.filter(name='LMS_Student').exists() or user.is_staff)

    def handle_no_permission(self):
        if self.request.user.is_authenticated and not self.request.user.is_active:
            messages.error(
                self.request,
                "Your account is currently pending approval by Admissions. You cannot access the dashboard yet."
            )
        else:
            messages.error(
                self.request,
                "Access restricted. You must be an approved student to view this page."
            )
        return redirect('login')
    def get(self, request):
        user = request.user

        # 1. Fetch student enrollments
        enrollments = Enrollment.objects.filter(
            student=user
        ).select_related('course', 'course__instructor').order_by('-created_at')

        # 2. Extract course IDs that are strictly PAID / ACTIVE (Uses valid status field)
        paid_enrollments = enrollments.filter(status__in=['PAID', 'ACTIVE'])
        paid_course_ids = paid_enrollments.values_list('course_id', flat=True)

        # 3. Check fee vouchers
        if hasattr(user, 'vouchers') and user.vouchers.exists():
            vouchers = user.vouchers.select_related('course').order_by('-created_at')
        else:
            vouchers = enrollments

        # 4. Query Live Sessions ONLY for PAID/ACTIVE courses & sections
        section_ids = CourseSection.objects.filter(
            course_id__in=paid_course_ids
        ).values_list('id', flat=True)

        live_sessions = LiveSession.objects.filter(
            Q(section_id__in=section_ids) |
            Q(course_id__in=paid_course_ids) |
            Q(section__course_id__in=paid_course_ids)
        ).distinct().select_related('section', 'course').order_by('-start_time')

        # 5. Fetch list of session IDs the student actually joined (Read-Only)
        attended_session_ids = set(
            SessionAttendance.objects.filter(
                student=user, 
                attended=True
            ).values_list('session_id', flat=True)
        )

        context = {
            'enrollments': enrollments,
            'vouchers': vouchers,
            'live_sessions': live_sessions,
            'paid_course_ids': set(paid_course_ids),
            'attended_session_ids': attended_session_ids,
        }

        return render(request, 'LMS/student_dashboard.html', context)

class UploadStudentDocumentsView(LoginRequiredMixin, View):
    """Allows enrolled students to submit CNIC/B-Form details and document files."""

    def post(self, request):
        cnic_number = request.POST.get('cnic_number', '').strip()
        cnic_front = request.FILES.get('cnic_front')
        cnic_back = request.FILES.get('cnic_back')

        profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        if cnic_number:
            profile.cnic_number = cnic_number
        if cnic_front:
            profile.cnic_front = cnic_front
        if cnic_back:
            profile.cnic_back = cnic_back

        # Reset status to PENDING upon new submission
        profile.verification_status = StudentProfile.VerificationStatus.PENDING
        profile.save()

        messages.success(request, "Your CNIC/B-Form documents have been uploaded successfully for review.")
        return redirect('student_dashboard')
    
User = get_user_model()


class AdmissionsDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Dashboard for Admissions Officers to review student registrations and documents."""

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='LMS_admissions_officer').exists()

    def get(self, request):
        # FIX: Use groups__name__in instead of groups__name for list filtering
        students = User.objects.filter(
            groups__name__in=['LMS_Instructor', 'LMS_Student']
        ).select_related('student_profile').prefetch_related('groups').order_by('-date_joined').distinct()

        context = {
            'students': students,
            'total_students': students.count(),
        }
        return render(request, 'LMS/admissions_dashboard.html', context)

class VerifyStudentDocumentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Handles Account Activation and CNIC Document Verification for Students and Instructors."""

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='LMS_admissions_officer').exists()

    def post(self, request, student_id):
        student = get_object_or_404(User, id=student_id)
        profile, _ = StudentProfile.objects.get_or_create(user=student)
        action = request.POST.get('action')

        # Detect User Role
        is_instructor = student.groups.filter(name='LMS_Instructor').exists()
        role_label = "Instructor" if is_instructor else "Student"

        if action == 'approve':
            has_documents = bool(profile.cnic_front or profile.cnic_back)

            # 1. DOCUMENT APPROVAL (If files are uploaded)
            if has_documents:
                profile.verification_status = StudentProfile.VerificationStatus.VERIFIED
                profile.save()
                student.is_active = True
                student.save()

                if student.email:
                    subject = f"Document Verified - TechExe LMS {role_label} Account"
                    message = f"""Hello {student.username},

Great news! Your uploaded CNIC/B-Form identity documents have been reviewed and approved by Admissions.

Your {role_label.lower()} profile is now fully verified.

Log in here: http://techexe.net/iccbs/login/

Best regards,
TechExe Academic Management
"""
                    try:
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'nsninsaan@gmail.com'),
                            recipient_list=[student.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass

                messages.success(
                    request,
                    f"Documents for {role_label.lower()} '{student.username}' verified and approved successfully!"
                )

            # 2. INITIAL ACCOUNT APPROVAL (No documents uploaded yet)
            else:
                student.is_active = True
                student.save()

                if student.email:
                    subject = f"Account Approved - Welcome to TechExe LMS as an {role_label}!"
                    message = f"""Hello {student.username},

Your {role_label.lower()} account has been reviewed and approved by Admissions.

You can now log in to your dashboard: http://techexe.net/iccbs/login/

Best regards,
TechExe Academic Management
"""
                    try:
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'nsninsaan@gmail.com'),
                            recipient_list=[student.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass

                messages.success(
                    request,
                    f"{role_label} account '{student.username}' activated successfully!"
                )

        elif action == 'reject':
            profile.verification_status = StudentProfile.VerificationStatus.REJECTED
            profile.save()
            student.is_active = False
            student.save()

            if student.email:
                subject = f"Action Required: {role_label} Verification Rejected"
                message = f"""Hello {student.username},

Your registration documents for TechExe LMS have been rejected by Admissions.

Please contact support or re-submit clear document copies.

Best regards,
TechExe Academic Management
"""
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'nsninsaan@gmail.com'),
                        recipient_list=[student.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            messages.warning(
                request,
                f"Account and documents for {role_label.lower()} '{student.username}' marked as rejected."
            )

        return redirect('admissions_dashboard')
       
class DeleteStudentDocumentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Deletes uploaded document files safely and resets verification status to PENDING."""

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='LMS_admissions_officer').exists()

    def post(self, request, student_id):
        student = get_object_or_404(User, id=student_id)

        if hasattr(student, 'student_profile') and student.student_profile:
            profile = student.student_profile

            # 1. Safely delete physical files from storage
            if profile.cnic_front:
                profile.cnic_front.delete(save=False)

            if profile.cnic_back:
                profile.cnic_back.delete(save=False)

            # 2. RESET VERIFICATION STATUS BACK TO PENDING
            profile.verification_status = StudentProfile.VerificationStatus.PENDING
            profile.save()

            # 3. (Optional) Deactivate user if re-verification is strictly mandatory
            # student.is_active = False
            # student.save()

            messages.warning(request, f"Uploaded documents for '{student.username}' cleared and status reset to Pending.")
        else:
            messages.error(request, f"No profile found for '{student.username}'.")

        return redirect('admissions_dashboard')
class DeleteStudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Permanently deletes a student user account and cascades all associated data."""

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='LMS_admissions_officer').exists()

    def post(self, request, student_id):
        student = get_object_or_404(User, id=student_id)
        username = student.username

        # Delete user (cascades to profile, documents, and registrations)
        student.delete()

        messages.error(request, f"Student account '{username}' has been permanently deleted.")
        return redirect('admissions_dashboard')

class InstructorDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Dashboard for instructors to manage courses, sections, live sessions, and attendance."""
    
    def test_func(self):
        return self.request.user.is_active and self.request.user.groups.filter(name='LMS_Instructor').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Your instructor account is pending review by the Department Head.")
        return redirect('login')

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(instructor=user)
        sections = CourseSection.objects.filter(instructor=user).select_related('course')
        
        # Query live sessions with attendance records pre-fetched
        live_sessions = LiveSession.objects.filter(
            Q(section__instructor=user) | Q(course__instructor=user)
        ).distinct().prefetch_related('attendances__student').order_by('-start_time')

        context = {
            'courses': courses,
            'sections': sections,
            'live_sessions': live_sessions,
            'total_active_sections': sections.count(),  # Fixes "0 Total Active Sections" badge
        }
        return render(request, 'LMS/instructor_dashboard.html', context)
    
class CreateCourseView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Allows instructors or staff to create new courses directly from the front-end."""

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='LMS_Instructor').exists()

    def post(self, request):
        title = request.POST.get('title', '').strip()
        price = request.POST.get('price', '0.00').strip()
        status = request.POST.get('status', 'PUBLISHED')
        
        if not title:
            messages.error(request, "Course title is required.")
            return redirect('instructor_dashboard')

        # Auto-generate a unique slug
        slug = slugify(title)
        if Course.objects.filter(slug=slug).exists():
            slug = f"{slug}-{Course.objects.count() + 1}"

        Course.objects.create(
            title=title,
            slug=slug,
            price=price,
            status=status,
            instructor=request.user
        )

        messages.success(request, f"Course '{title}' created successfully!")
        return redirect('instructor_dashboard')

# ==========================================
# Predictive Analytics At-Risk Dashboard
# ==========================================

User = get_user_model()

class InstructorAtRiskDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Predictive Analytics Dashboard: Identifies students at risk of failing 
    based on live session attendance and assignment/quiz metrics.
    """
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
        ).exists()

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        enrollments = course.enrollments.filter(status__in=['PAID', 'ACTIVE']).select_related('student')
        
        # Total held live sessions for this course
        total_sessions = LiveSession.objects.filter(
            Q(course=course) | Q(section__course=course)
        ).count()

        at_risk_students = []

        for enrollment in enrollments:
            student = enrollment.student
            
            # 1. Attendance Metrics
            attended_count = SessionAttendance.objects.filter(
                session__course=course,
                student=student,
                attended=True
            ).count()
            
            attendance_rate = (attended_count / total_sessions * 100) if total_sessions > 0 else 100.0

            # 2. Derive At-Risk Score (Weighted: Attendance 70%, Activity 30%)
            risk_score = 100.0 - attendance_rate
            
            if risk_score >= 50:
                risk_level = "CRITICAL"
                badge_color = "red"
            elif risk_score >= 25:
                risk_level = "WARNING"
                badge_color = "amber"
            else:
                risk_level = "ON_TRACK"
                badge_color = "emerald"

            at_risk_students.append({
                'student': student,
                'attended_count': attended_count,
                'total_sessions': total_sessions,
                'attendance_rate': round(attendance_rate, 1),
                'risk_score': round(risk_score, 1),
                'risk_level': risk_level,
                'badge_color': badge_color,
            })

        # Sort highest risk first
        at_risk_students.sort(key=lambda x: x['risk_score'], reverse=True)

        context = {
            'course': course,
            'at_risk_students': at_risk_students,
            'critical_count': sum(1 for s in at_risk_students if s['risk_level'] == 'CRITICAL'),
            'warning_count': sum(1 for s in at_risk_students if s['risk_level'] == 'WARNING'),
        }
        return render(request, 'LMS/at_risk_dashboard.html', context)
    
# ==========================================
# Mobile Offline Synchronization APIs
# ==========================================

class MobileCourseSyncAPIView(LoginRequiredMixin, View):
    """
    Mobile Sync API: Package course details, modules, and lessons for offline caching.
    """
    def get(self, request):
        user = request.user
        
        # Enrolled courses with active payment status
        paid_course_ids = Enrollment.objects.filter(
            student=user, status__in=['PAID', 'ACTIVE']
        ).values_list('course_id', flat=True)

        courses = Course.objects.filter(id__in=paid_course_ids).prefetch_related('modules__lessons')

        payload = []
        for course in courses:
            course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "modules": []
            }
            for module in course.modules.all():
                mod_data = {
                    "id": module.id,
                    "title": module.title,
                    "lessons": [
                        {
                            "id": lesson.id,
                            "title": lesson.title,
                            "body_text": lesson.body_text[:1000],  # Concise body for local cache
                        }
                        for lesson in module.lessons.all()
                    ]
                }
                course_data["modules"].append(mod_data)
            payload.append(course_data)

        return JsonResponse({"status": "success", "courses": payload}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class MobileAttendanceSyncAPIView(LoginRequiredMixin, View):
    """
    Mobile Offline Queue Batch Sync API: Receive attendance queue gathered offline 
    and log valid records.
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            offline_records = data.get('attendance_queue', [])
            synced_count = 0

            for item in offline_records:
                session_id = item.get('session_id')
                session = LiveSession.objects.filter(id=session_id).first()
                
                if session and session.can_be_joined:
                    _, created = SessionAttendance.objects.get_or_create(
                        session=session,
                        student=request.user,
                        defaults={
                            'attended': True, 
                            'joined_via': SessionAttendance.ModeJoined.ONLINE
                        }
                    )
                    if created:
                        synced_count += 1

            return JsonResponse({
                "status": "success",
                "message": f"Successfully synchronized {synced_count} offline attendance records."
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
class CreateLiveSessionView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Allows instructors to schedule live classroom sessions (Zoom, Teams, or built-in Jitsi)."""

    def test_func(self):
        user = self.request.user
        if user.is_staff:
            return True
        allowed_groups = {
            'LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD'
        }
        return bool(allowed_groups & set(user.groups.values_list('name', flat=True)))

    def handle_no_permission(self):
        messages.error(self.request, "Unauthorized access: Instructor permissions required.")
        return redirect('instructor_dashboard')

    def post(self, request):
        section_id = request.POST.get('section_id')
        title = request.POST.get('title', '').strip()
        # Default to empty string "" to satisfy database NOT NULL constraint
        meeting_link = request.POST.get('meeting_link', '').strip()
        start_time = request.POST.get('start_time')

        if not section_id or not title or not start_time:
            messages.error(request, "Section, title, and start time are required.")
            return redirect('instructor_dashboard')

        if request.user.is_staff or request.user.groups.filter(name='LMS_HOD').exists():
            section = get_object_or_404(CourseSection, id=section_id)
        else:
            section = get_object_or_404(CourseSection, id=section_id, instructor=request.user)

        # Save session with course, section, and non-null join_url
        LiveSession.objects.create(
            course=section.course,
            section=section,
            title=title,
            join_url=meeting_link,  # Stores "" for Jitsi, or external link for Zoom/Teams
            start_time=start_time,
            status=LiveSession.Status.SCHEDULED,
            mode=LiveSession.Mode.ONLINE
        )

        messages.success(request, f"Live session '{title}' scheduled successfully!")
        return redirect('instructor_dashboard')

@login_required
def join_live_session(request, session_id):
    """
    Legacy functional endpoint wrapper. Routes through JoinLiveSessionView 
    to enforce enrollment, timing guards, and dynamic attendance logging.
    """
    return JoinLiveSessionView.as_view()(request, session_id=session_id)

class HodDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Central administrative hub for HODs to allocate sections and approve faculty payout claims."""

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(
            name__in=['LMS_HOD', 'LMS_Accountant', 'LMS_admissions_officer']
        ).exists()

    def handle_no_permission(self):
        messages.error(self.request, "Unauthorized access: HOD permissions required.")
        return redirect('student_dashboard')

    def get(self, request):
        # 1. Fetch all course sections
        course_sections = CourseSection.objects.select_related('course', 'instructor').all()

        # 2. Query ALL courses explicitly for the modal selection dropdown
        courses = Course.objects.all().order_by('-id')

        # 3. Query all active instructors (Faculty & Visiting Faculty)
        instructors = User.objects.filter(
            groups__name__in=['LMS_Instructor', 'LMS_VisitingFaculty']
        ).distinct()

        # 4. Pending faculty payout claims
        pending_claims = VisitingFacultyClaim.objects.filter(
            status='PENDING'
        ) if hasattr(VisitingFacultyClaim, 'status') else []

        # Calculate pending payout sum
        total_payout_pending = sum(
            getattr(claim, 'total_amount', 0) for claim in pending_claims if getattr(claim, 'total_amount', None)
        )

        context = {
            'course_sections': course_sections,
            'courses': courses,
            'instructors': instructors,
            'pending_claims': pending_claims,
            'total_sections': course_sections.count(),
            'total_claims_pending': len(pending_claims),
            'total_payout_pending': total_payout_pending,
        }
        return render(request, 'LMS/hod_dashboard.html', context)
class CreateSectionView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Allows HOD or staff to create course sections and assign instructors."""

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='LMS_HOD').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Unauthorized: HOD permissions required.")
        return redirect('hod_dashboard')

    def post(self, request):
        course_id = request.POST.get('course_id')
        name = request.POST.get('name', '').strip()
        instructor_id = request.POST.get('instructor_id')

        if not course_id or not name or not instructor_id:
            messages.error(request, "All fields are required to create a section.")
            return redirect('hod_dashboard')

        course = get_object_or_404(Course, id=course_id)
        instructor = get_object_or_404(User, id=instructor_id)

        CourseSection.objects.create(
            course=course,
            name=name,
            instructor=instructor,
            confirmed_by_faculty=True
        )

        messages.success(request, f"Section '{name}' for '{course.title}' created and assigned to {instructor.username}!")
        return redirect('hod_dashboard')
    
class VisitingFacultyDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Workspace for Visiting Faculty to view sections, classes, and claims."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_VisitingFaculty').exists() or self.request.user.is_staff

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
    """Financial dashboard for Accountants to verify vouchers and review course revenue."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Accountant').exists() or self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('student_dashboard')

    def get(self, request):
        # 1. Calculate Total Cleared Revenue directly from Active/Completed Enrollments
        total_revenue_aggr = Enrollment.objects.filter(
            status__in=[Enrollment.Status.ACTIVE, Enrollment.Status.COMPLETED]
        ).aggregate(total=Sum('course__price'))['total']
        
        total_revenue = total_revenue_aggr if total_revenue_aggr is not None else Decimal('0.00')

        # 2. Course-wise Financial Breakdown
        course_revenue_list = Course.objects.annotate(
            verified_students=Count(
                'enrollments',
                filter=Q(enrollments__status__in=[Enrollment.Status.ACTIVE, Enrollment.Status.COMPLETED])
            ),
            total_collected=Sum(
                'enrollments__course__price',
                filter=Q(enrollments__status__in=[Enrollment.Status.ACTIVE, Enrollment.Status.COMPLETED])
            )
        ).order_by('-total_collected')

        # 3. Pending payment vouchers
        pending_vouchers = Enrollment.objects.filter(status=Enrollment.Status.PENDING)

        context = {
            'total_cleared_revenue': total_revenue, # Primary key
            'total_revenue': total_revenue,         # Legacy lookup backup
            'course_revenue_list': course_revenue_list,
            'pending_vouchers': pending_vouchers,
            'pending_count': pending_vouchers.count(),
        }
        return render(request, 'LMS/accountant_dashboard.html', context)
    
class VerifyVoucherPaymentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """View for accountants to verify student bank vouchers and activate course enrollment."""

    def test_func(self):
        return self.request.user.groups.filter(name='LMS_Accountant').exists() or self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('student_dashboard')

    def post(self, request, voucher_id):
        # Fetch enrollment record using the voucher ID
        enrollment = get_object_or_404(Enrollment, id=voucher_id)
        
        # Update enrollment status to ACTIVE
        enrollment.status = Enrollment.Status.ACTIVE
        enrollment.save()

        messages.success(request, f"Payment verified for {enrollment.student.username}. Course access granted!")
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
            'issue_date': getattr(enrollment, 'created_at', timezone.now()),
        }
        return render(request, 'LMS/fee_challan.html', context)


class EnrollCourseView(LoginRequiredMixin, View):
    """Handles course enrollment requests via slug, PK, or UUID."""

    def post(self, request, slug=None, course_id=None, *args, **kwargs):
        identifier = slug or course_id or kwargs.get('pk') or kwargs.get('id')
        
        if hasattr(Course, 'slug') and Course.objects.filter(slug=identifier).exists():
            course = get_object_or_404(Course, slug=identifier)
        else:
            course = get_object_or_404(Course, pk=identifier)
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'status': Enrollment.Status.PENDING}
        )
        
        if created:
            messages.success(request, f"Successfully enrolled in {course.title}. Please submit your fee challan for verification.")
        else:
            messages.info(request, f"You are already registered for {course.title}.")

        if hasattr(course, 'slug') and course.slug:
            return redirect('course_detail', slug=course.slug)
        return redirect('course_detail', pk=course.pk)


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
        
        if hasattr(self.object, 'modules'):
            context['modules'] = self.object.modules.prefetch_related('lessons').order_by('order')
        
        enrollment = None
        certificate = None
        is_access_granted = False
        is_course_completed = False
        
        if user.is_authenticated:
            enrollment = Enrollment.objects.filter(student=user, course=self.object).first()
            
            if enrollment:
                is_access_granted = enrollment.status in [Enrollment.Status.ACTIVE, Enrollment.Status.COMPLETED]

                # Check actual progress matching total course lessons
                total_lessons = Lesson.objects.filter(module__course=self.object).count()
                completed_lessons = LessonProgress.objects.filter(
                    student=user,
                    lesson__module__course=self.object,
                    is_completed=True
                ).count()

                if total_lessons > 0 and completed_lessons == total_lessons:
                    is_course_completed = True
                    certificate = Certificate.objects.filter(student=user, course=self.object).first()

        # Staff or Course Instructor gets full access
        if user.is_staff or getattr(self.object, 'instructor', None) == user:
            is_access_granted = True

        context['enrollment'] = enrollment
        context['is_access_granted'] = is_access_granted
        context['is_enrolled'] = enrollment is not None
        context['certificate'] = certificate if is_course_completed else None
        context['timezone'] = timezone
        return context

class LessonDetailView(LoginRequiredMixin, DetailView):
    """Displays lesson details with strict payment verification and progress tracking."""
    model = Lesson
    template_name = 'LMS/lesson_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = getattr(lesson, 'course', None) or lesson.module.course
        user = request.user

        def get_course_redirect():
            if hasattr(course, 'slug') and course.slug:
                return redirect('course_detail', slug=course.slug)
            return redirect('course_detail', pk=course.pk)

        # Allow Staff or Course Instructor
        if user.is_staff or getattr(course, 'instructor', None) == user:
            return super().dispatch(request, *args, **kwargs)

        # Allow free preview lessons
        if getattr(lesson, 'is_preview', False):
            return super().dispatch(request, *args, **kwargs)

        # Check Enrollment & Status
        enrollment = Enrollment.objects.filter(student=user, course=course).first()

        if not enrollment:
            messages.error(request, "You must enroll in this course to access lessons.")
            return get_course_redirect()

        is_access_granted = enrollment.status in [Enrollment.Status.ACTIVE, Enrollment.Status.COMPLETED]

        if not is_access_granted:
            messages.error(
                request, 
                "Access Restricted: Your payment for this course is pending accountant verification."
            )
            return get_course_redirect()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        course = getattr(lesson, 'course', None) or lesson.module.course
        user = self.request.user

        modules = course.modules.prefetch_related('lessons', 'quizzes').order_by('order') if hasattr(course, 'modules') else []
        
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
    """Toggles lesson completion status and issues certificate upon 100% completion."""

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        course = getattr(lesson, 'course', None) or lesson.module.course
        
        progress, _ = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
        
        progress.is_completed = not progress.is_completed
        progress.completed_at = timezone.now() if progress.is_completed else None
        progress.save()

        # Check total course completion
        total_lessons = Lesson.objects.filter(module__course=course).count() if hasattr(lesson, 'module') else Lesson.objects.filter(course=course).count()
        
        completed_lessons_count = LessonProgress.objects.filter(
            student=request.user,
            is_completed=True
        ).filter(
            lesson__module__course=course if hasattr(lesson, 'module') else lesson__course
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


class DiscussionTopicDetailView(LoginRequiredMixin, View):
    """View details of a discussion topic and its replies."""

    def get(self, request, pk):
        topic = get_object_or_404(DiscussionTopic, pk=pk)
        return render(request, 'LMS/discussion_topic_detail.html', {'topic': topic})


class AddDiscussionCommentView(LoginRequiredMixin, View):
    """Allows enrolled students or instructors to post a comment to a topic."""

    def post(self, request, topic_id):
        topic = get_object_or_404(DiscussionTopic, id=topic_id)
        content = request.POST.get('content', '').strip()

        if content:
            DiscussionComment.objects.create(
                topic=topic,
                author=request.user,
                content=content
            )
            messages.success(request, "Your reply has been posted.")
        else:
            messages.error(request, "Reply cannot be empty.")

        return redirect('discussion_topic_detail', pk=topic.id)
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

BGE_EMBED_URL = getattr(settings, "BGE_EMBED_URL", "http://192.168.224.163:80/embed")
QDRANT_URL    = getattr(settings, "QDRANT_URL", "http://192.168.160.63:6333")

LLM_CLUSTER_URLS = {
    "qwen":     "http://192.168.224.164:8000/v1/chat/completions",
    "mistral":  "http://192.168.166.175:8000/v1/chat/completions",
    "deepseek": "http://192.168.160.13:8000/v1/chat/completions"
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

            # --- ADAPTIVE ENGINE INTEGRATION ---
            # Run adaptive check for current student and course
            engine = AdaptiveLearningEngine(student=request.user, course=lesson.module.course)
            adaptive_data = engine.generate_personalized_remedial_plan()
            adaptive_guidance = adaptive_data.get('ai_tutor_focus_prompt', '')

            system_instruction = (
                f"{base_system_instruction}\n\n"
                f"--- ADAPTIVE LEARNING GUIDANCE ---\n"
                f"{adaptive_guidance}\n\n"
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

class AIQuizGeneratorView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Faculty Tool: Automatically generates draft quiz questions for a lesson."""
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
        ).exists()

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        questions = AIAssistanceService.generate_quiz_from_lesson(
            lesson_title=lesson.title,
            lesson_text=lesson.body_text
        )
        return JsonResponse({"status": "success", "questions": questions})



User = get_user_model()

class AIAdmissionAssistantView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Admin Tool: Provides automated preliminary evaluation for admissions staff
    based on student user records and uploaded document profiles.
    """
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name__in=['LMS_Admissions', 'LMS_admissions_officer']).exists()

    def get(self, request, student_id):
        student = get_object_or_404(User, id=student_id)
        
        profile = getattr(student, 'student_profile', None)
        cnic_num = getattr(profile, 'cnic_number', 'Not Provided') if profile else 'Not Provided'
        verification_status = getattr(profile, 'verification_status', 'PENDING') if profile else 'PENDING'
        has_documents = bool(profile and profile.cnic_front)

        bio_notes = (
            f"CNIC/B-Form: {cnic_num} | "
            f"Verification Status: {verification_status} | "
            f"Document Files Uploaded: {'Yes' if has_documents else 'No'}"
        )

        try:
            evaluation_notes = AIAssistanceService.analyze_admission_documents(
                student_name=student.get_full_name() or student.username,
                applied_course="General University Admission & Document Verification",
                bio_notes=bio_notes
            )
            return JsonResponse({"status": "success", "evaluation": evaluation_notes})
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "evaluation": f"Evaluation error: {str(e)}"
            }, status=200)


class AIAdminHelpdeskView(LoginRequiredMixin, View):
    """
    Admin & Student Support: Auto-responds to admissions and fee queries.
    """
    def post(self, request):
        user_query = request.POST.get('query', '').strip()
        if not user_query:
            return JsonResponse({"error": "Empty query provided"}, status=400)

        response = AIAssistanceService.solve_admin_helpdesk_query(user_query)
        return JsonResponse({"status": "success", "reply": response})
    
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
        email = request.POST.get('email', '').strip().lower()
        faculty_type = request.POST.get('faculty_type', FacultyInvitation.FacultyType.VISITING)
        department = request.POST.get('department', 'Computer Science').strip()

        if not email:
            messages.error(request, "Please provide a valid email address.")
            return render(request, 'LMS/invite_faculty.html')

        # 1. Save or update the record in your FacultyInvitation model
        invitation, created = FacultyInvitation.objects.update_or_create(
            email=email,
            defaults={
                'department': department,
                'faculty_type': faculty_type,
                'status': FacultyInvitation.Status.INVITED
            }
        )

        # 2. Generate a secure, time-stamped token based on the recipient email
        signer = TimestampSigner()
        signed_token = signer.sign(invitation.email)

        # 3. Build the full absolute activation link
        accept_url = request.build_absolute_uri(
            reverse('accept_faculty_invitation', kwargs={'token': signed_token})
        )

        # 4. Dispatch email via Docker Compose SMTP settings
        subject = f"Faculty Invitation: Join TechExe LMS ({invitation.get_faculty_type_display()})"
        message = f"""Hello,

You have been invited by the Department Head to join TechExe LMS as a {invitation.get_faculty_type_display()} in the {department} department.

Please click the link below to accept your invitation and complete your account setup:
{accept_url}

Best regards,
TechExe Academic Management
"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'nsninsaan@gmail.com'),
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f"Faculty invitation email sent to {email} ({invitation.get_faculty_type_display()}).")
        except Exception as e:
            messages.error(request, f"Failed to send email to {email}: {str(e)}")

        return redirect('hod_dashboard')



User = get_user_model()


class AcceptFacultyInvitationView(View):
    """Handles faculty activation and account setup via signed email links."""

    def get_invitation_from_token(self, token):
        signer = TimestampSigner()
        try:
            # Token valid for 7 days (604,800 seconds)
            email = signer.unsign(token, max_age=604800)
            return FacultyInvitation.objects.get(email=email, status=FacultyInvitation.Status.INVITED)
        except (BadSignature, SignatureExpired, FacultyInvitation.DoesNotExist):
            return None

    def get(self, request, token):
        invitation = self.get_invitation_from_token(token)
        if not invitation:
            messages.error(request, "This invitation link is invalid or has expired.")
            return redirect('login')

        return render(request, 'LMS/accept_invitation.html', {'invitation': invitation, 'token': token})

    def post(self, request, token):
        invitation = self.get_invitation_from_token(token)
        if not invitation:
            messages.error(request, "This invitation link is invalid or has expired.")
            return redirect('login')

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        cnic = request.POST.get('cnic_or_passport', '').strip()
        qualification = request.POST.get('qualification', '').strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'LMS/accept_invitation.html', {'invitation': invitation, 'token': token})

        # Create user account
        user = User.objects.create_user(
            username=username,
            email=invitation.email,
            password=password
        )

        # Map faculty_type to User Group
        group_name = (
            'LMS_VisitingFaculty'
            if invitation.faculty_type == FacultyInvitation.FacultyType.VISITING
            else 'LMS_Instructor'
        )
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # Update invitation and link to user
        invitation.user = user
        invitation.cnic_or_passport = cnic
        invitation.qualification = qualification
        invitation.status = FacultyInvitation.Status.ACTIVE
        invitation.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')




# ==========================================
# LAUNCH / JOIN LIVE SESSION VIEWS
# ==========================================

def launch_live_session(request, session_id):
    """
    Instructor endpoint to start a session. Sets status to HELD and routes 
    to external URL or Jitsi stream room.
    """
    session = get_object_or_404(LiveSession, id=session_id)
    user = request.user

    is_section_instructor = session.section and session.section.instructor == user
    is_course_instructor = session.course and session.course.instructor == user
    is_authorized_faculty = is_section_instructor or is_course_instructor or user.groups.filter(
        name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
    ).exists() or user.is_staff

    # Mark session status as active HELD when launched by faculty
    if is_authorized_faculty:
        session.status = LiveSession.Status.HELD
        session.save(update_fields=['status'])

    # External stream URL (Zoom/Teams) vs Embedded Jitsi Room
    if session.join_url:
        return redirect(session.join_url)
    return redirect('live_session_room', session_id=session.id)


class JoinLiveSessionView(LoginRequiredMixin, View):
    """
    Primary routing view for student entry. Checks enrollment, payment lock, timing guards, 
    and logs attendance.
    """
    def get(self, request, session_id):
        session = get_object_or_404(LiveSession, id=session_id)
        user = request.user

        is_instructor = user.is_staff or user.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
        ).exists()

        # 1. Instructors bypass enrollment, payment, and timing guards
        if is_instructor:
            if session.join_url:
                return redirect(session.join_url)
            return redirect('live_session_room', session_id=session.id)

        # 2. Check student enrollment
        enrollment = session.course.enrollments.filter(student=user).first()
        if not enrollment:
            return render(request, 'LMS/access_denied.html', {'reason': 'You are not enrolled in this course.'})

        # 3. ENFORCE PAYMENT LOCK: Block students with pending fees
        is_paid_or_active = getattr(enrollment, 'status', None) in ['PAID', 'ACTIVE']
        if not is_paid_or_active:
            messages.error(
                request, 
                "Access Denied: You have pending fees for this course. Please submit your payment to unlock live sessions."
            )
            return redirect('student_dashboard')

        # 4. Check existing attendance record
        has_attended = SessionAttendance.objects.filter(
            session=session, student=user, attended=True
        ).exists()

        # 5. Block student if session is EXPIRED and they didn't attend live
        if session.is_expired and not has_attended:
            messages.error(request, "This live session has expired and is no longer accessible.")
            return redirect('student_dashboard')

        # 6. BLOCK premature student entry if class is not live yet
        if not session.can_be_joined and not has_attended:
            formatted_time = session.start_time.strftime('%b %d, %Y @ %I:%M %p')
            messages.warning(
                request, 
                f"Class is not live yet! You can join starting 15 minutes prior to {formatted_time}."
            )
            return redirect('student_dashboard')

        # 7. Auto-log student attendance ONLY when joining within valid live timeframe
        SessionAttendance.objects.get_or_create(
            session=session,
            student=user,
            defaults={'attended': True, 'joined_via': SessionAttendance.ModeJoined.ONLINE}
        )

        # 8. Redirect to external meeting URL or built-in Jitsi room
        if session.join_url:
            return redirect(session.join_url)
        return redirect('live_session_room', session_id=session.id)


class LiveSessionRoomView(LoginRequiredMixin, View):
    """
    Internal embedded room (Jitsi). Provides display access & security verification.
    Attendance creation is handled upstream by JoinLiveSessionView to avoid duplication.
    """
    def get(self, request, session_id):
        session = get_object_or_404(LiveSession, id=session_id)
        user = request.user

        is_instructor = user.is_staff or user.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
        ).exists()

        # 1. Check enrollment
        enrollment = session.course.enrollments.filter(student=user).first()
        if not (enrollment or is_instructor):
            return render(request, 'LMS/access_denied.html', {'reason': 'You are not enrolled in this course.'})

        # 2. ENFORCE PAYMENT LOCK (Direct URL Access Prevention)
        if not is_instructor:
            is_paid_or_active = getattr(enrollment, 'status', None) in ['PAID', 'ACTIVE']
            if not is_paid_or_active:
                messages.error(
                    request, 
                    "Access Denied: You have pending fees for this course. Please submit your payment to unlock live sessions."
                )
                return redirect('student_dashboard')

        # 3. Check attendance history
        has_attended = SessionAttendance.objects.filter(
            session=session, student=user, attended=True
        ).exists()

        # 4. Block direct URL entry if expired AND didn't attend
        if not is_instructor and session.is_expired and not has_attended:
            messages.error(request, "This live session has expired and is no longer accessible.")
            return redirect('student_dashboard')

        # 5. Block direct URL entry if premature
        if not is_instructor and not session.can_be_joined and not has_attended:
            messages.warning(request, "This session is not live yet.")
            return redirect('student_dashboard')

        # 6. Derive course safely
        course = getattr(session, 'course', None) or getattr(session.section, 'course', None)

        context = {
            'session': session,
            'course': course,
            'user_display_name': user.get_full_name() or user.username,
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
        return self.request.user.groups.filter(name='LMS_VisitingFaculty').exists() or self.request.user.is_staff

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


# LMS/views.py
from .services import AdaptiveLearningEngine

class StudentPersonalizedPathView(LoginRequiredMixin, View):
    """
    Student View: Displays individualized adaptive recommendations 
    and customized study focus areas.
    """
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        
        # Verify student enrollment
        enrollment = course.enrollments.filter(student=request.user, status__in=['PAID', 'ACTIVE']).first()
        if not enrollment:
            messages.error(request, "You are not actively enrolled in this course.")
            return redirect('student_dashboard')

        # Run Adaptive Learning Engine
        engine = AdaptiveLearningEngine(student=request.user, course=course)
        remedial_plan = engine.generate_personalized_remedial_plan()

        context = {
            'course': course,
            'remedial_plan': remedial_plan,
        }
        return render(request, 'LMS/personalized_learning_path.html', context)

# ==========================================
# 6. CERTIFICATE GENERATION
# ==========================================


class DownloadCertificatePillowView(View):
    """Generates a high-resolution PDF certificate with an embedded verification QR code."""
    
    def get(self, request, certificate_id):
        # 1. Fetch certificate ensuring student ownership (or allow staff)
        cert = get_object_or_404(Certificate, id=certificate_id)
        if not (request.user == cert.student or request.user.is_staff):
            messages.error(request, "You do not have permission to download this certificate.")
            return redirect('student_dashboard')

        # 2. Block download if certificate is revoked
        if getattr(cert, 'is_revoked', False):
            messages.error(request, "This certificate has been revoked and cannot be downloaded.")
            return redirect('student_dashboard')

        # 3. Canvas Dimensions (300 DPI A4 Landscape)
        width, height = 3508, 2480
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Color Palette
        NAVY = (30, 58, 138)
        GOLD = (202, 138, 4)
        CHARCOAL = (31, 41, 55)
        MUTED_GRAY = (100, 116, 139)
        BG_INNER = (250, 250, 249)

        # Borders & Background
        draw.rectangle([80, 80, width - 80, height - 80], fill=BG_INNER)
        draw.rectangle([100, 100, width - 100, height - 100], outline=GOLD, width=12)
        draw.rectangle([130, 130, width - 130, height - 130], outline=NAVY, width=6)

        # Fonts
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

        # Header Section
        draw.text((cx, 320), "TECHEXE INSTITUTE OF TECHNOLOGY", fill=NAVY, anchor="mm", font=font_subHeader)
        draw.text((cx, 480), "CERTIFICATE OF COMPLETION", fill=GOLD, anchor="mm", font=font_header)
        draw.line([(cx - 400, 560), (cx + 400, 560)], fill=NAVY, width=3)

        # Recipient Section
        draw.text((cx, 720), "THIS IS PROUDLY PRESENTED TO", fill=MUTED_GRAY, anchor="mm", font=font_subHeader)
        full_name = cert.student.get_full_name() or cert.student.username.upper()
        draw.text((cx, 880), full_name, fill=CHARCOAL, anchor="mm", font=font_name)
        draw.line([(cx - 500, 960), (cx + 500, 960)], fill=GOLD, width=4)

        # Course Section
        draw.text((cx, 1120), "for successfully completing the specialized professional program in", fill=MUTED_GRAY, anchor="mm", font=font_body)
        draw.text((cx, 1260), f'"{cert.course.title}"', fill=NAVY, anchor="mm", font=font_title)

        # Signatures & Seal
        y_sign = 1850
        draw.line([(500, y_sign), (1100, y_sign)], fill=CHARCOAL, width=2)
        draw.text((800, y_sign + 30), "Lead Instructor", fill=CHARCOAL, anchor="mm", font=font_meta)

        draw.line([(2408, y_sign), (3008, y_sign)], fill=CHARCOAL, width=2)
        draw.text((2708, y_sign + 30), "Academic Director", fill=CHARCOAL, anchor="mm", font=font_meta)

        seal_cx, seal_cy = cx, y_sign - 30
        draw.ellipse([seal_cx - 90, seal_cy - 90, seal_cx + 90, seal_cy + 90], outline=GOLD, width=6, fill=(254, 243, 199))
        draw.text((seal_cx, seal_cy), "OFFICIAL\nSEAL", fill=GOLD, anchor="mm", font=font_meta, align="center")

        # Code & Dates
        cert_code = getattr(cert, 'certificate_code', str(cert.id))
        issue_date_obj = getattr(cert, 'issued_at', getattr(cert, 'created_at', timezone.now()))
        issue_date = issue_date_obj.strftime("%B %d, %Y")

        draw.text((350, 2220), f"Issue Date: {issue_date}", fill=MUTED_GRAY, font=font_meta)
        draw.text((cx, 2220), f"Certificate Code: {cert_code}", fill=MUTED_GRAY, anchor="mm", font=font_meta)

        # 4. Generate & Embed Dynamic Verification QR Code
        verify_url = request.build_absolute_uri(f"/LMS/verify/certificate/{cert.id}/")
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(verify_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Resize QR code and paste into bottom right margin
        qr_img = qr_img.resize((240, 240))
        img.paste(qr_img, (width - 600, 2080))
        draw.text((width - 480, 2330), "Scan to Verify", fill=MUTED_GRAY, anchor="mm", font=font_meta)

        # 5. Export to PDF Buffer
        pdf_buffer = BytesIO()
        img.save(pdf_buffer, format='PDF', resolution=300.0)
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Certificate_{cert_code}.pdf"'
        return response


class PublicCertificateVerifyView(View):
    """Publicly accessible verification endpoint (No login required)."""
    
    def get(self, request, certificate_id):
        try:
            cert = Certificate.objects.select_related('student', 'course', 'course__instructor').get(id=certificate_id)
            context = {
                'is_valid': not getattr(cert, 'is_revoked', False),
                'certificate': cert,
                'student_name': cert.student.get_full_name() or cert.student.username,
                'course_title': cert.course.title,
                'issued_at': getattr(cert, 'issued_at', getattr(cert, 'created_at', None)),
                'is_revoked': getattr(cert, 'is_revoked', False),
                'revocation_reason': getattr(cert, 'revocation_reason', None),
            }
        except (Certificate.DoesNotExist, ValueError):
            context = {
                'is_valid': False,
                'error_message': 'Invalid or non-existent Certificate ID.'
            }

        return render(request, 'LMS/public_certificate_verify.html', context)