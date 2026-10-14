from django import forms
from .models import Question, AnswerChoice
from .models import CourseSection, Course, User, LiveSession

class AssignFacultySectionForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ['course', 'name', 'instructor']
        widgets = {
            'course': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 p-2 text-sm'}),
            'name': forms.TextInput(attrs={'class': 'w-full rounded-lg border-gray-300 p-2 text-sm', 'placeholder': 'e.g., Section A (Batch 2026)'}),
            'instructor': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 p-2 text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter instructor dropdown to users with faculty profile or lms_instructor group
        self.fields['instructor'].queryset = User.objects.filter(
            groups__name='LMS_Instructor'
        ).distinct()
class QuizTakeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        super().__init__(*args, **kwargs)

        # Dynamically build inputs for every question in the quiz
        for question in quiz.questions.prefetch_related('choices').all():
            field_name = f"question_{question.id}"
            choices = [(choice.id, choice.text) for choice in question.choices.all()]

            if question.question_type == Question.QuestionType.SINGLE_CHOICE or question.question_type == Question.QuestionType.TRUE_FALSE:
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'space-y-2'}),
                    label=question.text,
                    required=True
                )
            elif question.question_type == Question.QuestionType.MULTIPLE_CHOICE:
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
                    label=question.text,
                    required=False
                )