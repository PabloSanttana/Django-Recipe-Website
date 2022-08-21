import os
from recipes.models import Recipe
from django.views.generic import ListView
from utils.pagnation import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 9))
QTY_LINK_PAGE = int(os.environ.get('QTY_LINK_PAGE', 4))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    paginate_by = None
    template_name = 'recipes/pages/home.html'

    # MANIPULAR OS FILTROS
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs
    # MANIPULAR OS VARIVAIS QUE VAO PARA TEMPLATE

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE,
            QTY_LINK_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}

        )
        return ctx
