from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin, LoginRequiredMixin
from django.contrib import messages
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from groups.models import Group
# Create your views here.
class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ("user","group")

    # queryset=models.Post.objects.all()

    # def get_context_data(self,**kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
    #     context['all_groups'] = Group.objects.all()
    #     context['other_groups'] = Group.objects.exclude(members__in=[self.request.user])
    #
    #     return context




# The get_queryset method on a ModelAdmin returns a QuerySet of all model instances that can be edited by the admin site. One use case for overriding this method is to show objects owned by the logged-in user:
# context izgleda ti e za templejtite  Getting information into your template’s context. What most people do is to overwrite get_context_data()
# context ti vrakja context dictionery za post_user


# https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/
# Often you simply need to present some extra information beyond that provided by the generic view. For example, think of showing a list of all the books on each publisher detail page.
# The DetailView generic view provides the publisher to the context, but how do we get additional information in that template?
#
# The answer is to subclass DetailView and provide your own implementation of the get_context_data method.
# The default implementation simply adds the object being displayed to the template, but you can override it to send more:
#
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Book.objects.all()
    #     return context



class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):

        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

class CreatePost(LoginRequiredMixin,generic.CreateView,SelectRelatedMixin):

    form_class = forms.PostForm
    # fields = ('message','group')
    model = models.Post
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):

    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
