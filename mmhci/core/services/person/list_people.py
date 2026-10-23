import operator
from functools import reduce
from django.db.models import Q
from mmhci.core.models.person import Person


class ListPeopleService:
    def __init__(self, request):
        self.request = request

    def search(self, q):
        # TODO: enforce permissions; send private or full name depending
        # see the Person model for custom properties for name/permissions
        q_list = q.strip().split(" ")
        q_filter = [
            Q(first_name__istartswith=search_string) |
            Q(last_name__istartswith=search_string)
            for search_string in q_list
        ]
        people = Person.objects.filter(
            reduce(operator.or_, q_filter)
        )
        return people

    def execute(self):
        # TODO: enforce permissions; send private or full name depending
        # see the Person model for custom properties for name/permissions
        people = Person.objects.all()
        return people
