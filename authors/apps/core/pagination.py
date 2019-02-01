"""Custom pagination class """
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'pages': {
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
