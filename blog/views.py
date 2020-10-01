from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm, ContactUsForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib import messages

# Create your views here.
def home_page(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) # 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/index.html', {'page': page, 'posts': posts, 'tag': tag})

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) # 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             )

    read_length = post.read_length
    # List of active comments for this post
    comments = post.comments.filter(active=True, parent__isnull=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create reply comment object
                    reply_comment = comment_form.save(commit=False)
                    # assign parent_obj to reply comment
                    reply_comment.parent = parent_obj
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

    # Previous & Next Posts
    
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment, 
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # form was submitted by user
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields pass validation
            cd = form.cleaned_data
            # TO-DO: send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                                rank=SearchRank(search_vector, search_query)
                                                ).filter(rank__gte=0.3).order_by('-rank')
            if not results:
                results = Post.published.annotate(similarity=TrigramSimilarity('title', query),
                                                ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html',
                            {'form': form,
                            'query': query,
                            'results': results})
def about_page(request):
    return render(request, 'blog/post/about.html')

def contact(request):
    if request.method == 'POST':
        f = ContactUsForm(request.POST)
        if f.is_valid:
            f.save()
            messages.add_message(request, messages.INFO, 'Thank You! Your message has been submitted.')
            return redirect('/blog/contactus')
    else:
        f = ContactUsForm()
    return render(request, 'blog/post/contactus.html', {'form': f})
