from datetime import datetime

from pony.orm import *

sqlite = Database()
postgres = Database()

# could probably be a file
COUNTRY_TOTALS = {'Algeria': 11506781, 'USA': 33884474, 'afghanistan': 558382, 'albania': 506594, 'austria': 1249388,
                  'azerbaijan': 99472, 'bahrain': 1424217, 'bolivia': 1969195, 'botswana': 240590, 'brazil': 4064912,
                  'bulgaria': 432473, 'burkina faso': 6413, 'costa rica': 999997, 'czech republic': 1000000,
                  'ecuador': 318819, 'el salvador': 13437, 'estonia': 262599, 'ethopia': 12753, 'fiji': 5364,
                  'finland': 1000000, 'georgia': 95193, 'ghana': 999987, 'haiti': 15407, 'honduras': 16142,
                  'hong kong': 1937830, 'indonesia': 130309, 'israel': 2000000, 'italy': 35677312, 'japan': 428615,
                  'kazakhstan': 2000000, 'luxemburj': 188201, 'mauritius': 848554, 'moldova': 46237, 'namibia': 409352,
                  'philpine': 899612, 'sweden': 1542057, 'uruguay': 999996}


# UNUSED TEMPORARILY
class Account(postgres.Entity):
    id = PrimaryKey(int, auto=True)
    phone_number = Required(int, size=64, unique=True, index=True)
    facebook_id = Required(int, size=64, index=True)
    first_name = Optional(str)
    last_name = Optional(str)
    gender = Optional(str)
    location = Optional(str)
    birth_location = Optional(str)
    relationship_status = Optional(str)
    work_place = Optional(str)
    dc_country = Required(str, index=True)
    creation_date = Optional(datetime)

    @staticmethod
    @db_session
    def find(**kwargs):
        query = Account.select(kwargs).limit(1)
        return query.get()

    @property
    def censored_first_name(self):
        asterisks = len(self.first_name) - 2

        return self.first_name[0] + ('*' * asterisks) + self.first_name[-1]

    @property
    def censored_last_name(self):
        asterisks = len(self.last_name) - 2

        return self.last_name[0] + ('*' * asterisks) + self.last_name[-1]

    def dictize(self):
        return {
            'first_name': self.censored_first_name,
            'last_name': self.censored_last_name,
            'gender': bool(self.gender),
            'relationship_status': bool(self.relationship_status),
            'location': bool(self.location),
            'work_place': bool(self.work_place),
            'country': {
                'name': self.dc_country,
                'count': COUNTRY_TOTALS[self.dc_country]
            }
        }


class Stats(postgres.Entity):
    name = PrimaryKey(str)
    value = Required(int, size=64)

    @staticmethod
    @db_session
    def increment(name):
        Stats.get(name=name).value += 1


# TEMPORARY
class SQLiteAccount(sqlite.Entity):
    id = PrimaryKey(int, auto=True, size=64)
    facebook_id = Required(int, size=64, index=True)
    first_name = Optional(str)
    last_name = Optional(str)
    gender = Optional(str)
    phone_number = Optional(int, size=64, index=True)
    location = Optional(str)
    birth_location = Optional(str)
    relationship_status = Optional(str)
    work_place = Optional(str)
    dc_country = Required(str, index=True)
    creation_date = Optional(datetime)

    @staticmethod
    def find(phone_number):
        query = SQLiteAccount.select(lambda a: a.phone_number == phone_number).limit(1)
        return query[0] if query else None

    @property
    def censored_first_name(self):
        asterisks = len(self.first_name) - 1

        return self.first_name[0] + ('*' * asterisks)

    @property
    def censored_last_name(self):
        asterisks = len(self.last_name) - 1

        return self.last_name[0] + ('*' * asterisks)

    def dictize(self):
        return {
            'first_name': self.censored_first_name,
            'last_name': self.censored_last_name,
            'gender': bool(self.gender),
            'relationship_status': bool(self.relationship_status),
            'location': bool(self.location),
            'work_place': bool(self.work_place),
            'country': {
                'name': self.dc_country,
                'count': COUNTRY_TOTALS[self.dc_country]
            }
        }


def setup():
    print('Setting up DB...', flush=True)

    postgres.bind(provider='postgres', host='postgres', user='postgres', password='', database='facebookleak')
    postgres.generate_mapping(create_tables=True)

    # temporarily needs to use sqlite for the accounts (still migrating to postgres)
    sqlite.bind(provider='sqlite', filename='/usr/src/app/database.sqlite')
    sqlite.generate_mapping(create_tables=True)
