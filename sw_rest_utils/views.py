from django.views.generic import TemplateView


class RestException(TemplateView):
    template_name = 'core/rest_exception.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'refresh_url': self.request.GET.get('refresh_url'),
            'message': self.request.GET.get('message'),
        })

        return super().get_context_data(**kwargs)
rest_exception = RestException.as_view()
