from django.http import HttpResponseForbidden


class FieldsSetterMixin:
    def dispatch(self, request, *args, **kargs):
        if request.user.is_superuser:
            self.fields = ["title", "sub_title", "author", "publisher", "reference", "slug", "description", "thumbnail",
                           "status", "category", ]
        elif request.user.is_author:
            self.fields = ["title", "sub_title", "publisher", "reference", "slug", "description", "thumbnail",
              "category",]
        else:
            raise HttpResponseForbidden('You are not a super user or an author')
        return super().dispatch(request, *args, **kargs)


class FormValidationMixin:
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
        return super().form_valid(form)
