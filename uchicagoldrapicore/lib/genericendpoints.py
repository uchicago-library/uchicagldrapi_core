from flask import jsonify, make_response, session
from flask_restufl import Resource, reqparse
from flask_login import login_required

from ..responses.apiresponse import APIResponse
from .apiexceptionhandler import APIExceptionHandler

_EXCEPTION_HANDLER = APIExceptionHandler()


class Login(Resource):
    def get(self):
        # A handy dandy HTML interface for use in the browser
        return make_response("""<center>
                                <form action="#" method="post">
                                Username:<br>
                                <input type="text" name="user">
                                <br>
                                Password:<br>
                                <input type="password" name="password">
                                <br><br>
                                <input type="submit" value="Submit">
                                </form>
                             </center>""")

    def post(self):
        # Generate a token (valid for default token lifespan) and set it in the
        # session so that the user can stop passing credentials manually if they
        # want
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user', type=str, required=True,
                                location=['values', 'json', 'form'])
            parser.add_argument('password', type=str,
                                location=['values', 'json', 'form'])
            args = parser.parse_args()
            session['user_token'] = User(
                args['user'],
                password=args['password']
            ).generate_token()
            return jsonify(APIResponse("success").dictify())
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())


class Logout(Resource):

    method_decorators = [login_required]

    def get(self):
        # Pop the token out of the session if login generated one
        try:
            del session['user_token']
            return jsonify(
                APIResponse("success").dictify()
            )
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())
