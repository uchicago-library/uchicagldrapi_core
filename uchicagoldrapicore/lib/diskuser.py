from os.path import isabs
from json import loads as json_loads
from os.path import join
from werkzeug.utils import secure_filename

from .abc.genericuser import GenericUser


class DiskUser(GenericUser):

    _usersdir = None

    def __init__(self, id_or_token, password=None):
        if self.get_usersdir() is None:
            raise ValueError("Must specify usersdir in the class attrs")
        GenericUser.__init__(self, id_or_token, password=password)

    def retrieve_user_information(self, identifier):
        if identifier != secure_filename(identifier):
            raise ValueError("Invalid User Identifier")
        try:
            r = None
            with open(join(self.get_usersdir(), identifier), 'r') as f:
                r = json_loads(f.read())
                return r
        except Exception as e:
            raise ValueError("Invalid User Identifier / " +
                             "Corrupted User Credentials")

    @classmethod
    def get_usersdir(cls):
        return cls._usersdir

    @classmethod
    def set_usersdir(cls, usersdir):
        if not isabs(usersdir):
            raise ValueError(".usersdir must be an absolute path")
        cls._usersdir = usersdir
