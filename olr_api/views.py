import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .db_manager import QueryManager
from functools import singledispatch

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import render


def index(request):
    template = loader.get_template('index.html')
    olr_inst = OLRDialerViewset()
    olr_data = olr_inst.get_data()
    context = {'olr_data': olr_data}
    print(context)
    return HttpResponse(template.render(context, request))

class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class DataPageView(TemplateView):
    def get(self, request, **kwargs):
        # we will pass this context object into the
        # template so that we can access the data
        # list in the template
        context = {
            'data': [
                {
                    'name': 'Celeb 1',
                    'worth': '3567892'
                },
                {
                    'name': 'Celeb 2',
                    'worth': '23000000'
                },
                {
                    'name': 'Celeb 3',
                    'worth': '1000007'
                },
                {
                    'name': 'Celeb 4',
                    'worth': '456789'
                },
                {
                    'name': 'Celeb 5',
                    'worth': '7890000'
                },
                {
                    'name': 'Celeb 6',
                    'worth': '12000456'
                },
                {
                    'name': 'Celeb 7',
                    'worth': '896000'
                },
                {
                    'name': 'Celeb 8',
                    'worth': '670000'
                }
            ]
        }

        return render(request, 'data.html', context)


class OLRDialerViewset(APIView):
    """
    OLRDialer class contains GET and POST APIs
    to retrieve and insert data respectively.
    """

    def get(self, request):
        """
        Fetch data from database
        :param request:
        :return: data and status
        """

        try:
            data = self.get_data()
            resp = {"olr_data": data}
            return Response(resp, status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status.HTTP_400_BAD_REQUEST)

    def get_data(self):
        """
        This method actually holds logic for get request
        """

        try:
            data = QueryManager().fetch_data_from_cdr_plus_sip_tbl()
            return data
        except Exception as e:
            error_msg = json.dumps({"msg": e}, default=self.to_serializable)
            return error_msg


    def post(self, request):
        """
        Insert data into database
        :param request: 
        :return: msg and status
        """

        try:
            QueryManager().insert_data_into_cdr_plus_sip_tbl(request.data)
        except Exception as e:
            error_msg = json.dumps({"msg": e}, default=self.to_serializable)
            return Response(error_msg, status.HTTP_400_BAD_REQUEST)
        return Response("Data inserted successfully into Database", status.HTTP_200_OK)


    @singledispatch
    def to_serializable(self, val):
        """Used by default."""
        return str(val)