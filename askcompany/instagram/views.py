from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostForm
from django.contrib.messages import error
from django.contrib import messages
# Create your views here.

def post_list(request):
    qs = Post.objects.all() # 전체를 가져올 준비
    q = request.GET.get('q', '') # q라는 이름의 인자가 있으면 가져오고(request에서 q라는 이름으로 데이터를 날리기 때문), 없으면 None
    if q:
        qs = qs.filter(message__icontains=q)
        # instagram/templates/instagram/post_list.html

    # messages.info(request, 'message 테스트')

    return render(request, 'instagram/post_list.html', {
        'post_list' : qs,
        'q' : q,
    })

post_list = ListView.as_view(model=Post, paginate_by=10)
# CBV(클래스 기반 호출)로 구현

@login_required # request.user을 외래키 할당하려면 필히 로그인 상황임을 보장 받아야 함.
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.info(request, '포스팅을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {
        'form' : form,
        'post' : None,
    })
    
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 작성자 Check Tip!
    if post.author != request.user:
        messages.error(request, '작성자만 수정할 수 있습니다.')
        return redirect(post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.info(request, '포스팅을 수정했습니다.')
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'instagram/post_form.html', {
        'form' : form,
        'post' : post,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '포스팅을 삭제했습니다.')
        return redirect('instagram:post_list')
    return render(request, 'instagram/post_confirm_delete.html', {
        'post':post,
    })

# @method_decorator(login_required, name='dispatch')
# class PostListView(ListView):
#     model = Post
#     paginate_by = 10

# post_list = PostListView.as_view()

class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs

post_detail = PostDetailView.as_view()




# def post_detail(request : HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     # try:
#     #     post = Post.objects.get(pk=pk) # 없으면 DoesNotExist 예외 발생
#     #     # 앞 pk는 필드의 종류, 뒤 pk는 인자로 넘어온 값
#     # except Post.DoesNotExist:
#     #     raise Http404
#     return render(request, 'instagram/post_detail.html',{
#         'post' : post,
#     })

# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archives")

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)