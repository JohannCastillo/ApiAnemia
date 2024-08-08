from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def __init__(self, page_query_param = 'page', page_size_query_param = 'page_size'):
        self.page_query_param = page_query_param
        self.page_size_query_param = page_size_query_param

    def add_search_param(self, url, page_number):
        params = self.request.GET.copy()
        params[self.page_query_param] = page_number
        return f'{url}?{params.urlencode(params)}'

    def get_paginated_response(self, data):
        return {
            # **response_dict,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.get_page_size(self.request),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'data': data,
        }
    
def paginate_results(paginator_class, request, data):
    paginator = paginator_class
    page = paginator.paginate_queryset(request=request, queryset=data)
    if page is not None:
        return paginator.get_paginated_response(page)
    return data