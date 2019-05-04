
from pycallgraph import Config
from pycallgraph import PyCallGraph
from pycallgraph.globbing_filter import GlobbingFilter
from pycallgraph.output import GraphvizOutput
import time
import time
from django.conf import settings
from django.urls import resolve

from pycallgraph import Config
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import GlobbingFilter

import time
import pycallgraph
from django.conf import settings


class CallgraphMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    # __call__ method is called when the instance is called (treating an instance as a function)
    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
            config = Config()

            config.trace_filter = GlobbingFilter(include=['rest_framework.*', 'api.*', 'music.*'])

            graphviz = GraphvizOutput(output_file='callgraph-' + str(time.time()) + '.svg',
                                      output_type='svg')  # or 'png'
            pycallgraph = PyCallGraph(output=graphviz, config=config)
            pycallgraph.start()
            # noinspection PyAttributeOutsideInit
            self.pycallgraph = pycallgraph

            response = self.get_response(request)
            # Code to be executed for each request/response after
            # the view is called.

            self.pycallgraph.done()


            return response

    @staticmethod
    def to_debug(request):
        method = request.method
        if method is 'GET' and 'graph' in request.GET:
            return True
        url_path = request.path
        url_name = getattr(resolve(url_path), 'url_name', None)
        urls = getattr(settings, 'CALL_GRAPH_URLS', None)
        for url in urls:
            if url.get('name', None) is url_name and method in url.get('methods', None):
                return True
        return False

# class CallgraphMiddleware(object):
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         if settings.DEBUG and 'graph' in request.GET:
#             filter_func = pycallgraph.GlobbingFilter(include=['flato.*'],
#                     exclude=['flato.debug.*'])
#             pycallgraph.start_trace(filter_func=filter_func)
#
#     def process_response(self, request, response):
#         if settings.DEBUG and 'graph' in request.GET:
#             pycallgraph.make_dot_graph('callgraph-' + str(time.time()) + '.png')
#         return response

# class PyCallGraphMiddleware(object):
#
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         if 'graph' in request.GET:
#             config = Config()
#             config.trace_filter = GlobbingFilter(include=['rest_framework.*', 'api.*', 'music.*'])
#             graphviz = GraphvizOutput(output_file='pycallgraph-{}.png'.format(time.time()))
#             pycallgraph = PyCallGraph(output=graphviz, config=config)
#             pycallgraph.start()
#
#             self.pycallgraph = pycallgraph
#
#     def process_response(self, request, response):
#         if 'graph' in request.GET:
#             self.pycallgraph.done()
#
#         return response