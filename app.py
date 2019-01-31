from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
import matplotlib.image as mpimg
import numpy as np


fum = 'Hello World!'
boo = True
image = mpimg.imread("téléchargement.png")
image = (image * 255).astype(np.uint8)


def hello_world(request):
    print('Incoming request')
    if boo is True:
        fum = 'Hello World!'
    if boo is False:
        fum = 'Hello Forks!'
    return Response(fum)


def booswitch(request):
    print('Incoming request for boo')
    global boo
    boo = False
    return Response(image)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('boo', '/boo')
        config.add_view(booswitch, route_name='boo')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)
