from . import render
from functions.users import get_level

@get_level
def missing(response, page, user):
    render('global/error.html', response, {"page": page, "error": 404})