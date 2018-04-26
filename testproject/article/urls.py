from django.conf.urls import url

from article.views import MyArticleView, AddGoogleDocLinkView, ReviewArticleView

urlpatterns = [
    url(r'^my_article/$', MyArticleView.as_view(), name='my_article'),
    url(r'^add_google_doc_link/$', AddGoogleDocLinkView.as_view(), name='add_google_doc_link'),
    url(r'^review_article/$', ReviewArticleView.as_view(), name='review_article')
]
