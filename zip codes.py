import sqlite3
import re

conn = sqlite3.connect('apartment_data.db')
cursor = conn.cursor()

places = ['8800 Boardwalk Trail Dr, Tampa, FL 33637', '2633 Azalea Garden Pl, Tampa, FL 33619',
          '1250 E Madison St, Tampa, FL 33602', '10881 Caladesi Ave, Tampa, FL 33610']


def get_zip(address):
    zip_code = re.findall('FL 3....', address)[0]
    zip_code = zip_code.replace('FL ', '')

    return zip_code


addresses = cursor.execute("""SELECT Address
                              FROM apartments;""").fetchall()

for (address,) in addresses:
    zip_code = get_zip(address)
    cursor.execute(
        "UPDATE apartments SET ZipCode = ? WHERE Address = ?;",
        (zip_code, address)
    )

conn.commit()
