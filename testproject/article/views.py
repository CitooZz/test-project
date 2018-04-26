from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, View

from article.models import Article
from article.permissions import ReviewArticlePermission, MyArticlePermission


class HomeView(LoginRequiredMixin, ListView):
    model = Article
    queryset = Article.objects.open_articles()
    context_object_name = 'articles'
    template_name = 'article/home.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_writer:
            messages.error(request, "User Editor can't assign.")
            return redirect(reverse('home'))

        article = get_object_or_404(Article, id=request.POST.get('article_id'))
        article.set_status(Article.ASSIGNED, request.user)
        messages.success(request, "The article has been assigned to you.")

        return redirect(reverse('home'))


class MyArticleView(LoginRequiredMixin, MyArticlePermission, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'article/my_article.html'

    def get_queryset(self):
        return Article.objects.my_articles(self.request.user)

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=request.POST.get('article_id'))
        if article.assignee != request.user:
            messages.error(request, "You don't have permission to send review this article.")
            return redirect(reverse('article:my_article'))

        article.set_status(Article.REVIEW)
        messages.success(request, "The article has been sent to review.")
        return redirect(reverse('article:my_article'))


class AddGoogleDocLinkView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        google_doc_link = request.POST.get('google_doc_link')
        article = get_object_or_404(Article, id=request.POST.get('article_id'))

        if not google_doc_link:
            messages.error(request, "Google doc link required.")
            return redirect(reverse('article:my_article'))

        article.google_doc_link = google_doc_link
        article.save()
        messages.success(request, "Google doc link has been added.")
        return redirect(reverse('article:my_article'))


class ReviewArticleView(LoginRequiredMixin, ReviewArticlePermission, ListView):
    model = Article
    queryset = Article.objects.review_articles()
    context_object_name = 'articles'
    template_name = 'article/review_article.html'

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=request.POST.get('article_id'))
        article.set_status(Article.APPROVED)

        return redirect(reverse('article:review_article'))
