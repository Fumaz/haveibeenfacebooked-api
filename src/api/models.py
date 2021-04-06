from pony.orm import *

sqlite = Database()

# could probably be a file
COUNTRY_TOTALS = {'Algeria': 11000000, 'Brazil': 8064909, 'Canada': 3494381, 'Colombia': 17957881, 'France': 19848556,
                  'Germany': 6054420, 'India': 6162122, 'Israel': 3956428, 'Italy': 34999986, 'Spain': 10894205,
                  'Tunisia': 6247880, 'UK': 11122317, 'USA': 28999989, 'Afghanistan': 558392, 'Albania': 506598,
                  'Argentina': 2339553, 'Austria': 1249388, 'Azerbaijan': 99472, 'Bahrain': 1424219, 'Belgium': 3183538,
                  'Bolivia': 2969197, 'Botswana': 240606, 'Brunei': 213795, 'Bulgaria': 432473, 'Burkina Faso': 6413,
                  'Burundi': 15709, 'Cameroon': 1997648, 'Chile': 6889071, 'China': 670334, 'Costa Rica': 1464000,
                  'Croatia': 659115, 'Cyprus': 119021, 'Czech Republic': 1375988, 'Denmark': 639841, 'Dibouti': 14327,
                  'Ecuador': 318820, 'El Salvador': 4479, 'Estonia': 87533, 'Ethopia': 12753, 'Fiji': 5364,
                  'Finland': 1381566, 'Georgia': 95193, 'Ghana': 1027960, 'Greece': 617714, 'Guatemala': 1645058,
                  'Haiti': 15407, 'Honduras': 16142, 'Hong Kong': 2937834, 'Hungary': 377045, 'Iceland': 31343,
                  'Indonesia': 130315, 'Jamaica': 385890, 'Japan': 428615, 'Kazakhstan': 3214290, 'Lithunia': 220160,
                  'Luxemburj': 188201, 'Macao': 414282, 'Malaysia': 11675713, 'Maldives': 86337, 'Malta': 115366,
                  'Mauritius': 848556, 'Mexico': 13330528, 'Moldova': 46237, 'Namibia': 409354, 'Netherlands': 5430387,
                  'Nigeria': 8999999, 'Norway': 475809, 'Panama': 1502308, 'Philpine': 899619, 'Poland': 2669381,
                  'Portugal': 2277361, 'Puerto Rico': 138183, 'Serbia': 162898, 'Slovenia': 229038,
                  'South Africa': 14323568, 'Sweden': 2542059, 'Switzerland': 1592039, 'Taiwan': 734803,
                  'Uruguay': 1509315, 'bangladesh': 3816349}


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
                'count': COUNTRY_TOTALS[self.dc_country]
            }
        }


def setup():
    print('Setting up DB...', flush=True)

    # temporarily needs to use sqlite for the accounts (still migrating to postgres)
    sqlite.bind(provider='sqlite', filename='/usr/src/app/database.sqlite')
    sqlite.generate_mapping()
