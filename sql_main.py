import sqlite3

db_path = 'apartment_data.db'

def create_db_keys(database):

    # Connect and disable foreign keys temporarily
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cursor = conn.cursor()

    # Rename original tables to create new ones with primary/foreign key
    cursor.execute("ALTER TABLE apartments RENAME TO old_apartments;")
    cursor.execute("ALTER TABLE amenities RENAME TO old_amenities;")

    # Create new apartments table
    cursor.execute("""
        CREATE TABLE apartments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Apartment TEXT,
            Address TEXT,
            MinPrice REAL,
            MaxPrice REAL,
            Beds TEXT,
            Amenities TEXT
        );
    """)

    # Create new amenities table (linked by id with apartments)
    cursor.execute("""
        CREATE TABLE amenities (
            id INTEGER PRIMARY KEY,
            pets TEXT,
            pool TEXT,
            gym TEXT,
            laundry_in_unit TEXT,
            AC TEXT,
            Internet TEXT,
            clubhouse TEXT,
            dishwasher TEXT,
            refrigerator TEXT
        );
    """)

    # Step 3: Copy data from old apartment table to new one
    cursor.execute("""
        INSERT INTO apartments (Apartment, Address, MinPrice, MaxPrice, Beds, Amenities)
        SELECT Apartment, Address, MinPrice, MaxPrice, Beds, Amenities FROM old_apartments;
    """)

    # Step 4: Insert data into amenities table using matching row-ids

    cursor.execute("SELECT id, Apartment FROM apartments")
    apartment_ids = cursor.fetchall()

    for apt_id, apt_name in apartment_ids:
        cursor.execute("""
            SELECT pets, pool, gym, laundry_in_unit, AC, Internet, clubhouse, dishwasher, refrigerator
            FROM old_amenities WHERE Apartment = ?
        """, (apt_name,))
        amenity_row = cursor.fetchone()
        if amenity_row:
            cursor.execute("""
                INSERT INTO amenities (id, pets, pool, gym, laundry_in_unit, AC, Internet, clubhouse, dishwasher, refrigerator)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (apt_id, *amenity_row))

    # Remove original tables without keys
    cursor.execute("DROP TABLE old_apartments;")
    cursor.execute("DROP TABLE old_amenities;")

    # Re-enable foreign keys and close
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()

def delete_column(database, table_name, col_name):

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f""" ALTER TABLE {table_name}
                        DROP COLUMN {col_name}""")

    conn.commit()
    conn.close()

