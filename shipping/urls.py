from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('shipping.views',
    url(r'estimation/?$', 'estimation', name='shipping-estimation'),
)
