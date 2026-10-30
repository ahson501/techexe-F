from django.urls import path
from . import views

urlpatterns = [
    # Default Index Routes
    path('', views.CourseListView.as_view(), name='lms_index'),
    path('lessons/', views.CourseListView.as_view(), name='lessons_index'),

    # Course Catalog & Enrollment
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<slug:slug>/enroll/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('course/<uuid:course_id>/builder/', views.CourseBuilderView.as_view(), name='course_builder'),
    path('course/create/', views.CreateCourseView.as_view(), name='create_course'),
    path('section/create/', views.CreateSectionView.as_view(), name='create_section'),
    path('course/<uuid:course_id>/personalized-path/', views.StudentPersonalizedPathView.as_view(), name='student_personalized_path'),
    
    # Role Dashboards
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/instructor/', views.InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('dashboard/visiting-faculty/', views.VisitingFacultyDashboardView.as_view(), name='visiting_faculty_dashboard'),
    path('dashboard/hod/', views.HodDashboardView.as_view(), name='hod_dashboard'),
    path('dashboard/accountant/', views.AccountantDashboardView.as_view(), name='accountant_dashboard'),
    path('dashboard/admissions/', views.AdmissionsDashboardView.as_view(), name='admissions_dashboard'),

    # Payments, Verification & Student Documents
    path('voucher/<int:voucher_id>/verify/', views.VerifyVoucherPaymentView.as_view(), name='verify_voucher_payment'),
    path('challan/<int:enrollment_id>/download/', views.DownloadChallanView.as_view(), name='download_challan'),
    path('student/upload-documents/', views.UploadStudentDocumentsView.as_view(), name='upload_student_documents'),
    path('admissions/verify-student/<int:student_id>/', views.VerifyStudentDocumentView.as_view(), name='verify_student_document'), 
    path('admissions/delete-document/<int:student_id>/', views.DeleteStudentDocumentView.as_view(), name='delete_student_document'), 
    path('admissions/delete-student/<int:student_id>/', views.DeleteStudentView.as_view(), name='delete_student'),

    # Live Sessions & Classroom Routing
    path('session/create/', views.CreateLiveSessionView.as_view(), name='create_live_session'),
    path('live/<int:session_id>/', views.LiveSessionRoomView.as_view(), name='live_session_room'),
    path('live-session/<int:session_id>/join/', views.JoinLiveSessionView.as_view(), name='join_live_session'),
    path('live-session/<int:session_id>/launch/', views.launch_live_session, name='launch_live_session'),

    # HOD & Faculty Management
    path('hod/invite-faculty/', views.InviteFacultyView.as_view(), name='invite_faculty'),
    path('faculty/accept-invite/<str:token>/', views.AcceptFacultyInvitationView.as_view(), name='accept_faculty_invitation'),
    path('faculty/claims/', views.VisitingFacultyClaimEngineView.as_view(), name='faculty_claims'),
    path('hod/sections/', views.HODSectionAssignmentView.as_view(), name='hod_section_assignment'),
    path('hod/claims/<int:claim_id>/approve/', views.HODApproveClaimView.as_view(), name='approve_claim'),

    # Discussion Boards
    path('discussions/', views.DiscussionBoardView.as_view(), name='discussion_board'),
    path('discussions/topic/<int:pk>/', views.DiscussionTopicDetailView.as_view(), name='discussion_topic_detail'),
    path('discussions/topic/<int:topic_id>/comment/', views.AddDiscussionCommentView.as_view(), name='add_discussion_comment'),
    path('discussions/create/', views.CreateDiscussionTopicView.as_view(), name='create_discussion_topic'),

    # Lessons & Quizzes
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/toggle-complete/', views.ToggleLessonCompleteView.as_view(), name='toggle_lesson_complete'),
    path('quizzes/<int:pk>/take/', views.QuizTakeView.as_view(), name='quiz_take'),
    path('quizzes/<int:pk>/latest-result/', views.LatestQuizResultRedirectView.as_view(), name='quiz_result_latest'),
    path('quiz-attempts/<int:pk>/', views.QuizResultDetailView.as_view(), name='quiz_result_detail'),

    # Phase 3 Analytics & Sync APIs
    path('course/<uuid:course_id>/at-risk-dashboard/', views.InstructorAtRiskDashboardView.as_view(), name='at_risk_dashboard'),
    path('api/v1/mobile/sync/courses/', views.MobileCourseSyncAPIView.as_view(), name='mobile_course_sync_api'),
    path('api/v1/mobile/sync/attendance/', views.MobileAttendanceSyncAPIView.as_view(), name='mobile_attendance_sync_api'),
    path('api/ai-assistant/', views.AIChatAssistantView.as_view(), name='ai_assistant_api'),
    path('api/v1/ai/generate-quiz/<int:lesson_id>/', views.AIQuizGeneratorView.as_view(), name='ai_generate_quiz'),
    path('api/v1/ai/evaluate-admission/<int:student_id>/', views.AIAdmissionAssistantView.as_view(), name='ai_evaluate_admission'),
    path('faculty/lesson/<int:lesson_id>/generate-quiz/', views.AIQuizGeneratorView.as_view(), name='ai_generate_quiz'),
    path('support/ai-helpdesk/', views.AIAdminHelpdeskView.as_view(), name='ai_admin_helpdesk'),
    
    # Certificates & Public QR Verification
    path('certificates/<uuid:certificate_id>/download/', views.DownloadCertificatePillowView.as_view(), name='download_certificate'),
    path('verify/certificate/<uuid:certificate_id>/', views.PublicCertificateVerifyView.as_view(), name='public_certificate_verify'),
]