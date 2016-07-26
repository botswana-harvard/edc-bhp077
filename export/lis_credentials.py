import os
from django.conf import settings


class LisCredentials:
    """Reads cnf file of format:

        username = <username>
        password = <password>
        host = <host>
        port = 1433
        name = <db name>"""

    def __init__(self):
        lis_etc = os.path.join(settings.BASE_DIR.ancestor(1), 'etc', 'mssql.cnf')
        with open(lis_etc, 'r') as f:
            rows = f.read()
        data = rows.split('\n')
        data = [item.replace(' ', '').replace('\'', '') for item in data if item]
        credentials = {}
        for item in data:
            k, v = item.split('=')
            credentials.update({k: v})
        self.username = credentials.get('username')
        self.password = credentials.get('password')
        self.port = credentials.get('port')
        self.host = credentials.get('host')
        self.db = credentials.get('name')
