from flask import session, g, jsonify, make_response
from flask_login import login_required
from flask_restful import Resource

from ..responses.apiresponse import APIResponse
from apiexceptionhandler import APIExceptionHandler

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

    @login_required
    def post(self):
        try:
            u = g.user
            token = u.generate_token()
            session['user_token'] = token
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


class GetToken(Resource):

    method_decorators = [login_required]

    def get(self):
        # Generate a token for the user to use instead of their credentials
        try:
            t = g.user.generate_token()
            return jsonify(
                APIResponse("success", data={'token': t}).dictify()
            )
        except Exception as e:
            raise e
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())
