from os.path import isabs
from json import loads as json_loads
from os.path import join
from werkzeug.utils import secure_filename

from .abc.genericuser import GenericUser


class DiskUser(GenericUser):

    _usersdir = None

    def __init__(self, id_or_token, password=None, usersdir=None):
        if usersdir is None:
            usersdir = self.usersdir

        if usersdir is None:
            raise ValueError("Must specify usersdir in the class attrs or" +
                             "pass it as a kwarg")
        self.usersdir = usersdir
        super().__init__(id_or_token, password=password)

    def get_user_credentials(self, identifier):
        if identifier != secure_filename(identifier):
            raise ValueError("Invalid User Identifier")
        try:
            r = None
            with open(join(self.usersdir, identifier), 'r') as f:
                r = json_loads(f.read())
                return r
        except:
            raise ValueError("Invalid User Identifier / " +
                             "Corrupted User Credentials")

    @classmethod
    def get_usersdir(self):
        return self._usersdir

    @classmethod
    def set_usersdir(self, usersdir):
        if not isabs(usersdir):
            raise ValueError(".usersdir must be an absolute path")
        self._usersdir = usersdir

    usersdir = property(get_usersdir, set_usersdir)
