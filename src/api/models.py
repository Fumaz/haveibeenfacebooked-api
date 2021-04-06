import json

from pony.orm import *

sqlite = Database()
countries_data = {}


class Stats(sqlite.Entity):
    name = PrimaryKey(str)
    value = Required(int, size=64)

    @staticmethod
    @db_session
    def increment(name):
        s = Stats.get(name=name)

        if not s:
            Stats(name=name, value=1)
            return

        s.value += 1


class Account(sqlite.Entity):
    _table_ = 'account'
    ROWID = PrimaryKey(int, auto=True)
    phone_number = Required(str, index=True)
    facebook_id = Required(int, size=64)
    first_name = Optional(str)
    last_name = Optional(str)
    gender = Required(bool)
    location = Required(bool)
    birth_location = Required(bool)
    relationship_status = Required(bool)
    work_place = Required(bool)
    dc_country = Required(str, index=True)

    @staticmethod
    def find(phone_number):
        query = Account.select(lambda a: a.phone_number == phone_number).limit(1)
        return query[0] if query else None

    def dictize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'relationship_status': self.relationship_status,
            'location': self.location,
            'work_place': self.work_place,
            'country': {
                'name': self.dc_country,
                'count': countries_data.get(self.dc_country, 'unknown')
            }
        }


def setup():
    global countries_data
    print('Setting up DB...', flush=True)

    countries_data = json.load(open('/usr/src/app/assets/countries.json', 'r'))

    sqlite.bind(provider='sqlite', filename='/usr/src/app/database.sqlite')
    sqlite.generate_mapping()
