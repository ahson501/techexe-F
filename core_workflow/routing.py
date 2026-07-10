# core_workflow/routing.py
from .models import AssignmentType

def resolve_approver(instance, step):
    """
    Evaluates runtime rules to find target personnel.
    Returns: (User object or None, Group object or None)
    """
    applicant = instance.submitted_by

    if step.assignment_type == AssignmentType.USER:
        return step.assigned_user, None

    if step.assignment_type == AssignmentType.GROUP:
        return None, step.assigned_group

    if step.assignment_type == AssignmentType.SUPERVISOR:
        # Assumes a custom profile setup mapping: user.profile.supervisor
        if hasattr(applicant, 'profile') and applicant.profile.supervisor:
            return applicant.profile.supervisor, None
        raise ValueError(f"No Supervisor found configured for user: {applicant}")

    if step.assignment_type == AssignmentType.HOD:
        # Find the HOD for the applicant's department
        if hasattr(applicant, 'profile') and applicant.profile.department:
            hod = applicant.profile.department.head_of_department
            return hod, None
        raise ValueError(f"Could not map Department Head for user: {applicant}")

    if step.assignment_type == AssignmentType.DIRECTOR:
        # Returns the core system administrator or institutional director
        from django.contrib.auth.models import User
        director = User.objects.filter(groups__name="DIRECTOR").first()
        return director, None

    return None, None