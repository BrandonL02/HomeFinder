import pandas as pd
import ast




def clean_amenity_data(df):
    # Clean dataset by removing empty values
    df = df.dropna(subset=['Apartment', 'Amenities'])

    # parse amenities if stored as string
    def parse(amenity_str):
        try:
            return ast.literal_eval(amenity_str)
        except (ValueError, SyntaxError):
            print(f'Unable to filter row for {amenity_str}')
            return []

    df['Amenities'] = df['Amenities'].apply(parse)

    desired_amenities = {
        'pets': ['Pets Allowed', 'Dogs Allowed', 'Cats Allowed'],
        'pool': ['Pool'],
        'gym': ['Fitness Center'],
        'laundry_in_unit': ['Washer & Dryer', 'Washer/Dryer'],
        'AC': ['Air Conditioning'],
        'Internet': ['High Speed Internet Access', 'Wi-Fi'],
        'clubhouse': ['Clubhouse'],
        'dishwasher': ['Dishwasher'],
        'refrigerator': ['Refrigerator'],
    }

    # Initialize final DataFrame
    amenity_df = pd.DataFrame()
    amenity_df['Apartment'] = df['Apartment']

    # Indicate if amenities are included
    for amenity, keyword_list in desired_amenities.items():
        amenity_df[amenity] = df['Amenities'].apply(
            lambda amenities: 'Y' if any(item in amenities for item in keyword_list) else 'N'
        )

    return amenity_df

