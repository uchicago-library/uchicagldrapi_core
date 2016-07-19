from flask import session, g


class UserLoader(object):
    def __init__(self, UserClass):
        self.UserClass = UserClass

    def load_user(self, request):
        """
        Function for use with the login_manager.user_loader callback.

        See https://flask-login.readthedocs.io/en/latest/ for more information.

        This implementation looks in a variety of places for either a token
        or a username password combo, and will do two things on a successful
        login via either.

        1) Set g.user to the User object
        2) Return the user for use by flask_login
        """
        # Try really hard to get the user out of where ever it could be
        # First look in the URL args, even though stuff probably shouldn't
        # be in there because the passwords would be in plaintext
        user, password = request.args.get('user'), request.args.get('password')
        # Then look in the JSON args of a post
        if user is None:
            if request.get_json():
                user, password = request.get_json().get('user'),  \
                    request.get_json().get('password')
        # Then look in the session
        if user is None:
            if session.get('user_token'):
                user = session.get('user_token')
        if user is not None:
            try:
                g.user = self.UserClass(user, password)
                return g.user
            except:
                return None
        return None
