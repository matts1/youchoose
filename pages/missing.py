from . import render
from functions.users import require_none

@require_none
def missing(response, page, user):
    render('global/error.html', response, {"page": page, "error": 404})