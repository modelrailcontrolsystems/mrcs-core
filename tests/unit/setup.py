import sys

from mrcs_core.db.dbclient import DBClient, DBMode


class Setup(object):
    @classmethod
    def dbSetup(cls):
        if DBClient.client_db_mode() == DBMode.TEST:
            return

        DBClient.drop_all()
        DBClient.set_client_db_mode(DBMode.TEST)
        print('dbSetup: set DB for test', file=sys.stderr)
