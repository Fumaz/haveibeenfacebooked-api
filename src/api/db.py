import aiosqlite

total_amount = 35677337
db_path = 'database.sqlite'


class Account:
    def __init__(self, phone_number: str, email_address: str, facebook_id: int, first_name: str,
                 last_name: str, gender: bool, location: bool, birth_location: bool, relationship_status: bool,
                 work_place: bool, dc_country: str):
        self.phone_number = phone_number
        self.email_address = email_address
        self.facebook_id = facebook_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.location = location
        self.birth_location = birth_location
        self.relationship_status = relationship_status
        self.work_place = work_place
        self.dc_country = dc_country

    @staticmethod
    async def fetch(phone_number=None, email_address=None):
        if not (phone_number or email_address):
            return None

        if phone_number:
            query = ("SELECT * FROM account WHERE phone_number=?;", (phone_number,))
        else:
            query = ("SELECT * FROM account WHERE email_address=?;", (email_address,))

        async with aiosqlite.connect(db_path) as db:
            async with db.execute(*query) as cursor:
                data = await cursor.fetchone()

                if not data:
                    return None

                return Account(phone_number=data[0], email_address=data[1], facebook_id=data[2], first_name=data[3],
                               last_name=data[4], gender=bool(data[5]), location=bool(data[6]),
                               birth_location=bool(data[7]), relationship_status=bool(data[8]),
                               work_place=bool(data[9]), dc_country=data[10])

    def dictize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': bool(self.email_address),
            'gender': self.gender,
            'relationship_status': self.relationship_status,
            'location': self.location,
            'birth_location': self.birth_location,
            'work_place': self.work_place,
            'country': {
                'name': self.dc_country,
                'count': total_amount
            }
        }
