from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.views.generic.detail import BaseDetailView
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator

from movies.models import Filmwork

from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal


class MyDjangoJSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


class MoviesListApi(BaseListView):
    http_method_names = ['get']
    model = Filmwork

    def get(self, request, *args, **kwargs):
        result = self.render_to_response(self.get_context_data(request))
        return result

    def get_queryset(self, request):
        return self.model.objects.order_by('id').values('id', 'title', 'description', 'creation_date', 'rating',
                                                        'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True)).annotate(
            directors=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Director'),
                               distinct=True)).annotate(
            writers=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Writer'),
                             distinct=True)).annotate(
            actors=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Actor'),
                            distinct=True)).values('id', 'title', 'description', 'creation_date', 'rating', 'type',
                                                   'genres', 'actors', 'directors', 'writers')

    def get_context_data(self, request, *, object_list=None, **kwargs):
        paginator = Paginator(self.get_queryset(request), 50)
        page_number = request.GET.get('page') if request.GET.get('page') is not None else '1'
        page_obj = paginator.get_page(page_number)

        context = {
            'count': page_obj.paginator.count,
            'total_pages': page_obj.paginator.num_pages - 1,
            'prev': page_obj.previous_page_number() if page_number.isdigit() and int(page_number) > 1 else (
                page_obj.paginator.num_pages - 2 if page_number == 'last' else None),
            'next': None if page_number == 'last' or page_number == page_obj.paginator.num_pages - 1 else page_obj.next_page_number(),
            'results': list(page_obj),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, encoder=MyDjangoJSONEncoder)


class MoviesDetailApi(BaseDetailView):
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get(self, request, *args, **kwargs):
        result = self.render_to_response(self.get_context_data())
        return result

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return self.model.objects.filter(id=pk).values('id', 'title', 'description', 'creation_date', 'rating',
                                                       'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True)).annotate(
            directors=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Director'),
                               distinct=True)).annotate(
            writers=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Writer'),
                             distinct=True)).annotate(
            actors=ArrayAgg('film_relation__person__name', filter=Q(film_relation__role='Actor'),
                            distinct=True)).values('id', 'title', 'description', 'creation_date', 'rating', 'type',
                                                   'genres', 'actors', 'directors', 'writers')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_queryset()[0]
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, encoder=MyDjangoJSONEncoder, safe=False)
