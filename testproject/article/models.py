from django.db import models

from account.models import User


class ArticleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def my_articles(self, user):
        return self.filter(assignee=user)

    def open_articles(self):
        return self.filter(state=Article.OPEN)

    def review_articles(self):
        return self.filter(state__in=[Article.REVIEW, Article.APPROVED])


class Article(models.Model):
    OPEN = 0
    ASSIGNED = 1
    REVIEW = 2
    APPROVED = 3

    STATE_CHOICES = (
        (OPEN, "Open"),
        (ASSIGNED, "Assigned"),
        (REVIEW, "Review"),
        (APPROVED, "Approved")
    )

    title = models.CharField(max_length=100, verbose_name='Title')
    content = models.TextField(verbose_name='Content')

    assignee = models.ForeignKey(User, null=True, blank=True)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=OPEN)

    google_doc_link = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.state == self.ASSIGNED and self.google_doc_link

    @property
    def is_in_review(self):
        return self.state == self.REVIEW

    @property
    def is_approved(self):
        return self.state == self.APPROVED

    def set_status(self, status, user=None):
        self.state = status
        if status == self.ASSIGNED:
            self.assignee = user

        self.save()
