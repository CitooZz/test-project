from django.core.exceptions import PermissionDenied

from account.models import User


class ReviewArticlePermission(object):
    '''
    Permission for Review Article
    '''

    def has_permissions(self):
        return self.request.user.role == User.EDITOR

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied

        return super(ReviewArticlePermission, self).dispatch(request, *args, **kwargs)


class MyArticlePermission(object):
    '''
    Permission for My Article
    '''

    def has_permissions(self):
        return self.request.user.role == User.WRITER

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied

        return super(MyArticlePermission, self).dispatch(request, *args, **kwargs)
