from pony.orm import *

sqlite = Database()

# could probably be a file
COUNTRY_TOTALS = {'Algeria': 11000000, 'Brazil': 8064909, 'Canada': 3494381, 'Colombia': 17957881, 'France': 19848556,
                  'Germany': 6054420, 'India': 6162122, 'Israel': 3956428, 'Italy': 34999986, 'Spain': 10894205,
                  'Tunisia': 6247880, 'UK': 11122317, 'USA': 28999989}


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


class SQLiteAccount(sqlite.Entity):
    phone_number = Required(str, size=64, unique=True)
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
        query = SQLiteAccount.select(lambda a: a.phone_number == phone_number).limit(1)
        return query[0] if query else None

    def dictize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.first_name,
            'gender': self.gender,
            'relationship_status': self.relationship_status,
            'location': self.location,
            'work_place': self.work_place,
            'country': {
                'name': self.dc_country,
                'count': COUNTRY_TOTALS[self.dc_country]
            }
        }


def setup():
    print('Setting up DB...', flush=True)

    # temporarily needs to use sqlite for the accounts (still migrating to postgres)
    sqlite.bind(provider='sqlite', filename='/usr/src/app/database.sqlite')
    sqlite.generate_mapping(create_tables=True)
