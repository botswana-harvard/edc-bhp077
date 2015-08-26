from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Q

from microbiome.models import SubjectConsent


class MaternalSearchView(TemplateView):
    template_name = 'microbiome_maternal_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title="Microbiome",
            header=[
                'Subject Identifier', 'Date Consent', 'First Name', 'Initials', 'Date of Birth']
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MaternalSearchView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Allows a GET."""
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        """Allows a GET."""
        context = self.get_context_data(**kwargs)
        context.update(
            search=True,
            consents_search_result=self.search_results(request),
            identifier=request.POST.get('identifier_search', None)
        )
        return render(request, self.template_name, context)

    def search_results(self, request):
        """Search for receive with specified identifier."""
        search_value = request.POST.get('identifier_search', None)
        return SubjectConsent.objects.filter(
            Q(subject_identifier__icontains=search_value)
        ).order_by('created')
