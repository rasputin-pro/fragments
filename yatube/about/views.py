from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "about/author.html"


class AboutTechView(TemplateView):
    template_name = "about/tech.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вот что я умею"
        context["text"] = 'Текст страницы "Технологии"'
        return context
