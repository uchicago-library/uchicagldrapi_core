class UserLoader(object):
    def __init__(self, UserClass, token_signing_key=None):
        self.UserClass = UserClass
        if token_signing_key:
            self.UserClass.token_signing_key = token_signing_key

    def load_user(self, request, session=None):
        """
        Function for use with the login_manager.user_loader callback.

        See https://flask-login.readthedocs.io/en/latest/ for more information.

        This implementation looks in a variety of places for either a token
        or a username password combo

        It fails silently on *any* error and returns None
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
        # Then look in form data
        if user is None:
            user, password = request.form.get('user'), \
                request.form.get('password')
        # Then look in the session, if we have it
        if user is None:
            if session is not None:
                user = session.get('user_token', None)
        if user is not None:
            try:
                u = self.UserClass(user, password=password)
                return u
            except:
                return None
        return None
