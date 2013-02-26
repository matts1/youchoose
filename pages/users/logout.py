from functions.users import require_login
from models.tables import sessions

@require_login
def logout(response, user):
    key = response.get_secure_cookie("session_id").decode('utf-8')
    print key
    sessions.delete(key)

    response.redirect('/login')
