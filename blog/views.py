from django.views import generic
from .models import Course, Chapter, Videos

class CourseList(generic.ListView):
    queryset = Course.objects.order_by('-date_created')
    template_name = 'course_list.html'
    paginate_by = 10

class CourseDetail(generic.DetailView):
    model = Course
    template_name = 'course_detail.html'

class ChapterDetail(generic.DetailView):
    model = Chapter
    template_name = 'chapter_detail.html'

class VideosDetail(generic.DetailView):
    model = Videos
    template_name = 'videos_detail.html'

