from django import template

register = template.Library()

@register.simple_tag
def change_url_params(request, **kwargs):
    """
    Function gets current url GET params and a set of new ones. If the parameter didn't
    exist in the original url, it adds them - replaces with a new value otherwise.
    """
    query_dict = request.GET.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return query_dict.urlencode()