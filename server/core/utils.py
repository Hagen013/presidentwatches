from django.urls import reverse
from django.http import HttpResponseRedirect


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = list(
        map(lambda x: "{key}={values}".format(
            key=x,
            values=",".join([str(i) for i in kwargs[x]])),
            kwargs.keys()
        )
    )
    if len(params) == 0:
        return HttpResponseRedirect(url)
    params = '&'.join(params)
    return HttpResponseRedirect(url + "?%s" % params)
