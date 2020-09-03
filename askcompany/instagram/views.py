from django.shortcuts import render
from .models import Post
# Create your views here.

def post_list(request):
    qs = Post.objects.all() # 전체를 가져올 준비
    q = request.GET.get('q', '') # q라는 이름의 인자가 있으면 가져오고(request에서 q라는 이름으로 데이터를 날리기 때문), 없으면 None
    if q:
        qs = qs.filter(message__icontains=q)
        # instagram/templates/instagram/post_list.html
    return render(request, 'instagram/post_list.html', {
        'post_list' : qs,
        'q' : q,
    })
    
