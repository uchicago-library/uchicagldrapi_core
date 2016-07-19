from abc import ABCMeta, abstractmethod
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, \
    SignatureExpired
from hashlib import sha256


class GenericUser(ABCMeta):

    """
    An ABC for providing basic user login functionality to UChicagoLDR APIs

    All subclasses should implement .retrieve_user_information() to the minimum
    specifications laid out in that functions docstring

    All subclasses inits should also accept one required argument (the id
    or token) and one optional argument (the password). The ABC init implements
    this footprint, so there is no need to override the init unless you want
    more functionality in it.
    """

    _TOKEN_SIGNING_KEY = None
    _id = None
    _is_active = False
    _is_authenticated = False
    _is_anonymous = True

    def __init__(self, id_or_token, password=None):
        # See if whats in id_or_token is a valid token
        validated = None
        try:
            validated = self.validate_token(id_or_token)
        except (BadSignature, SignatureExpired):
            pass

        # Attempt token login if it looks like a valid token
        if validated is not None:
            id = validated['id']
            self.id = id
            try:
                user_dict = self.retrieve_user_information(self.id)
            except:
                raise ValueError("Token implied bad user id")
            self.password = user_dict['password']
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False
        # Attempt user/pass login if it looks like an id and not a token
        else:
            self.id = id_or_token
            try:
                user_dict = self.retrieve_user_information(self.id)
            except:
                raise ValueError("Bad Token / Bad ID")
            if self.hash_password(self.id, password, user_dict['salt']) !=  \
                    user_dict['password']:
                raise ValueError("Bad password")
            self.password = user_dict['password']
            self.salt = user_dict['salt']
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False

    def __repr__(self):
        # This repr has per user "private" information in it (their hashed
        # password and their salt). So override this in your subclass if you
        # don't want str-ing the object to emit that information
        return str(self.dictify())

    def get_is_authenticated(self):
        return self._is_authenticated

    def set_is_authenticated(self, x):
        if not isinstance(x, bool):
            raise ValueError(".is_authenticated must be a bool")
        self._is_authenticated = x

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, x):
        if not isinstance(x, bool):
            raise ValueError(".is_active must be a bool")
        self._is_active = x

    def get_is_anonymous(self):
        return self._is_anonymous

    def set_is_anonymous(self, x):
        if not isinstance(x, bool):
            raise ValueError(".is_anonymous must be a bool")
        self._is_anonymous = x

    def get_id(self):
        return self._id

    def set_id(self, x):
        self._id = x

    def dictify(self):
        r = {}
        r['id'] = self.id
        r['password'] = self.password
        r['salt'] = self.salt
        return r

    def generate_token(self, expiration=60*60*24):
        s = TimedJSONWebSignatureSerializer(self.token_signing_key,
                                            expires_in=expiration)
        x = s.dumps({'id': self.id}).decode("utf-8")
        return x

    @classmethod
    def validate_token(cls, token):
        s = TimedJSONWebSignatureSerializer(cls.token_signing_key)
        x = s.loads(token)
        return x

    @staticmethod
    def hash_password(id, password, salt):
        return sha256(
            "{}{}{}".format(id, password, salt).encode("utf-8")
        ).hexdigest()

    def verify_password(self, password):
        if self.hash_password(self.id, password, self.salt) == self.password:
            return True
        return False

    @staticmethod
    @abstractmethod
    def retrieve_user_information(id):
        """
        This function should return a dictionary containing *at least*
        "id", "password", and "salt" keys with appropriate string values when
        provided with a user id.

        Password in this case is a salted hashed password, *!!NOT!!* the
        plaintext. This classes .hash_password() function will create
        such a string for you on new user creation given a plaintext string.
        """
        pass

    @classmethod
    def get_token_signing_key(cls):
        return cls._TOKEN_SIGNING_KEY

    @classmethod
    def set_token_signing_key(cls, key):
        cls._TOKEN_SIGNING_KEY = key

    @classmethod
    def del_token_signing_key(cls):
        cls._TOKEN_SIGNING_KEY = None

    token_signing_key = property(get_token_signing_key,
                                 set_token_signing_key,
                                 del_token_signing_key)

    is_active = property(get_is_active,
                         set_is_active)

    is_authenticated = property(get_is_authenticated,
                                set_is_authenticated)

    is_anonymous = property(get_is_anonymous,
                            set_is_anonymous)

    id = property(get_id,
                  set_id)
