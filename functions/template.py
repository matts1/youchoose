from .users import get_user
from cgi import escape
from .form import form
from .table import table

def makecontext(context, response):
    if context == None:
        context = {}
    if response == None:
        user = None
    else:
        user = get_user(response)
    customcontext = {
        "form": form,
        "esc": escape,
        "user": user,
        "table": table,
    }
    for field in customcontext:
        if field in context:
            raise ValueError(field + " should not be provided to context")
        context[field] = customcontext[field]
    return context