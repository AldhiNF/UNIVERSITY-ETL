import pandas as pd         # Untuk manipulasi dan analisis data
import json                 # Untuk membaca file JSON mentah
import os                   # Untuk operasi file dan folder

# Fungsi utama untuk membersihkan dan memperkaya data universitas
def clean_university_data(input_path, output_path):
    # Membaca file JSON dari path input
    with open(input_path, encoding='utf-8') as f:
        raw_data = json.load(f)

    # Mengubah list of dict JSON menjadi DataFrame
    df = pd.DataFrame(raw_data)

    # Memilih kolom penting saja dari data mentah
    df_clean = df[['name', 'country', 'alpha_two_code', 'domains', 'web_pages']].copy()

    # Tambahkan kolom baru: jumlah domain per universitas (jumlah elemen di list 'domains')
    df_clean['domain_count'] = df_clean['domains'].apply(lambda x: len(x))

    # Menghapus duplikat berdasarkan kombinasi nama universitas dan negaranya
    df_clean.drop_duplicates(subset=['name', 'country'], inplace=True)

    # Tambahkan kolom baru: top-level domain (misalnya: 'ac.id' → 'id')
    df_clean['top_level_domain'] = df_clean['domains'].apply(lambda x: x[0].split('.')[-1])

    # Dictionary mapping negara ke benua (continent)
    country_to_continent = {
    # North America
    'United States': 'North America',
    'Canada': 'North America',
    'Mexico': 'North America',
    'Cuba': 'North America',
    'Jamaica': 'North America',
    'Dominican Republic': 'North America',
    'Haiti': 'North America',
    'Panama': 'North America',
    'Costa Rica': 'North America',
    'Guatemala': 'North America',
    'Honduras': 'North America',
    'El Salvador': 'North America',
    'Nicaragua': 'North America',
    'Bahamas': 'North America',
    'Barbados': 'North America',
    'Trinidad and Tobago': 'North America',
    'Belize': 'North America',

    # South America
    'Brazil': 'South America',
    'Argentina': 'South America',
    'Chile': 'South America',
    'Colombia': 'South America',
    'Peru': 'South America',
    'Venezuela': 'South America',
    'Paraguay': 'South America',
    'Uruguay': 'South America',
    'Bolivia': 'South America',
    'Ecuador': 'South America',
    'Guyana': 'South America',
    'Suriname': 'South America',

    # Europe
    'United Kingdom': 'Europe',
    'Germany': 'Europe',
    'France': 'Europe',
    'Italy': 'Europe',
    'Spain': 'Europe',
    'Portugal': 'Europe',
    'Netherlands': 'Europe',
    'Belgium': 'Europe',
    'Switzerland': 'Europe',
    'Sweden': 'Europe',
    'Norway': 'Europe',
    'Finland': 'Europe',
    'Denmark': 'Europe',
    'Poland': 'Europe',
    'Czech Republic': 'Europe',
    'Slovakia': 'Europe',
    'Hungary': 'Europe',
    'Austria': 'Europe',
    'Ireland': 'Europe',
    'Greece': 'Europe',
    'Ukraine': 'Europe',
    'Russia': 'Europe',
    'Romania': 'Europe',
    'Bulgaria': 'Europe',
    'Serbia': 'Europe',
    'Croatia': 'Europe',
    'Slovenia': 'Europe',
    'Lithuania': 'Europe',
    'Latvia': 'Europe',
    'Estonia': 'Europe',
    'Iceland': 'Europe',
    'Moldova': 'Europe',
    'North Macedonia': 'Europe',
    'Albania': 'Europe',
    'Bosnia and Herzegovina': 'Europe',
    'Montenegro': 'Europe',
    'Malta': 'Europe',
    'Luxembourg': 'Europe',
    'Andorra': 'Europe',
    'Monaco': 'Europe',
    'Liechtenstein': 'Europe',
    'San Marino': 'Europe',
    'Vatican City': 'Europe',

    # Asia
    'China': 'Asia',
    'India': 'Asia',
    'Japan': 'Asia',
    'Indonesia': 'Asia',
    'Pakistan': 'Asia',
    'Bangladesh': 'Asia',
    'Vietnam': 'Asia',
    'Philippines': 'Asia',
    'Thailand': 'Asia',
    'South Korea': 'Asia',
    'North Korea': 'Asia',
    'Malaysia': 'Asia',
    'Singapore': 'Asia',
    'Nepal': 'Asia',
    'Sri Lanka': 'Asia',
    'Myanmar': 'Asia',
    'Laos': 'Asia',
    'Cambodia': 'Asia',
    'Afghanistan': 'Asia',
    'Iran': 'Asia',
    'Iraq': 'Asia',
    'Saudi Arabia': 'Asia',
    'Israel': 'Asia',
    'Turkey': 'Asia',
    'Jordan': 'Asia',
    'Lebanon': 'Asia',
    'Syria': 'Asia',
    'Qatar': 'Asia',
    'Kuwait': 'Asia',
    'Bahrain': 'Asia',
    'Oman': 'Asia',
    'United Arab Emirates': 'Asia',
    'Kazakhstan': 'Asia',
    'Uzbekistan': 'Asia',
    'Turkmenistan': 'Asia',
    'Kyrgyzstan': 'Asia',
    'Tajikistan': 'Asia',
    'Georgia': 'Asia',
    'Armenia': 'Asia',
    'Azerbaijan': 'Asia',
    'Yemen': 'Asia',

    # Africa
    'South Africa': 'Africa',
    'Nigeria': 'Africa',
    'Egypt': 'Africa',
    'Kenya': 'Africa',
    'Ethiopia': 'Africa',
    'Ghana': 'Africa',
    'Morocco': 'Africa',
    'Algeria': 'Africa',
    'Tanzania': 'Africa',
    'Uganda': 'Africa',
    'Angola': 'Africa',
    'Mozambique': 'Africa',
    'Zimbabwe': 'Africa',
    'Senegal': 'Africa',
    'Ivory Coast': 'Africa',
    'Cameroon': 'Africa',
    'Zambia': 'Africa',
    'Sudan': 'Africa',
    'South Sudan': 'Africa',
    'Namibia': 'Africa',
    'Botswana': 'Africa',
    'Rwanda': 'Africa',
    'Burundi': 'Africa',
    'Malawi': 'Africa',
    'Mali': 'Africa',
    'Niger': 'Africa',
    'Liberia': 'Africa',
    'Togo': 'Africa',
    'Benin': 'Africa',
    'Chad': 'Africa',
    'Gambia': 'Africa',
    'Sierra Leone': 'Africa',
    'Burkina Faso': 'Africa',
    'Congo (Kinshasa)': 'Africa',
    'Congo (Brazzaville)': 'Africa',
    'Somalia': 'Africa',
    'Madagascar': 'Africa',
    'Mauritius': 'Africa',

    # Oceania
    'Australia': 'Oceania',
    'New Zealand': 'Oceania',
    'Fiji': 'Oceania',
    'Papua New Guinea': 'Oceania',
    'Samoa': 'Oceania',
    'Tonga': 'Oceania',
    'Vanuatu': 'Oceania',
    'Solomon Islands': 'Oceania',
    'Micronesia': 'Oceania',
    'Palau': 'Oceania',
    'Marshall Islands': 'Oceania',
    'Nauru': 'Oceania',
    'Tuvalu': 'Oceania',

    # Others (Special cases or often appear in data)
    'Hong Kong': 'Asia',
    'Taiwan': 'Asia',
    'Palestine': 'Asia',
    'Kosovo': 'Europe',
    'Greenland': 'North America',
    'Puerto Rico': 'North America',
    'Antigua and Barbuda': 'North America',
    'Aruba': 'North America',
    'Bahamas': 'North America',
    'Bermuda': 'North America',
    'Dominica': 'North America',
    'Grenada': 'North America',
    'Saint Kitts and Nevis': 'North America',
    'Saint Lucia': 'North America',
    'Saint Vincent and the Grenadines': 'North America',
    'Sint Maarten': 'North America',
    'Turks and Caicos Islands': 'North America',
    'Anguilla': 'North America',
    'Montserrat': 'North America',
    'French Guiana': 'South America',
    'Falkland Islands': 'South America',
    'Mayotte': 'Africa',
    'Réunion': 'Africa',
    'Seychelles': 'Africa',
    'Comoros': 'Africa',
    'Cape Verde': 'Africa',
    'Eswatini': 'Africa',
    'Lesotho': 'Africa',
    'Djibouti': 'Africa',
    'Equatorial Guinea': 'Africa',
    'Gabon': 'Africa',
    'Guinea': 'Africa',
    'Guinea-Bissau': 'Africa',
    'Central African Republic': 'Africa',
    'Eritrea': 'Africa',
    'Western Sahara': 'Africa',
    'Timor-Leste': 'Asia',
    'Brunei': 'Asia',
    'Bhutan': 'Asia',
    'Maldives': 'Asia',
    'Mongolia': 'Asia',
    'Macau': 'Asia',
    'British Indian Ocean Territory': 'Asia',
    'Cook Islands': 'Oceania',
    'Niue': 'Oceania',
    'New Caledonia': 'Oceania',
    'French Polynesia': 'Oceania',
    'Guam': 'Oceania',
    'American Samoa': 'Oceania',
    'Northern Mariana Islands': 'Oceania',
    'Wallis and Futuna': 'Oceania',
    'Tokelau': 'Oceania',
    'Bouvet Island': 'Antarctica',
    'Heard Island and McDonald Islands': 'Antarctica',
    'South Georgia and the South Sandwich Islands': 'Antarctica',
    'Norfolk Island': 'Oceania',
    'Saint Pierre and Miquelon': 'North America',
    'Faroe Islands': 'Europe',
    'Isle of Man': 'Europe',
    'Gibraltar': 'Europe',
    'Guernsey': 'Europe',
    'Jersey': 'Europe',
    'Aland Islands': 'Europe',
}

    # Tambahkan kolom 'continent' berdasarkan mapping negara → benua
    df_clean['continent'] = df_clean['country'].map(country_to_continent)

    # Buat folder output jika belum ada
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Simpan data bersih dan diperkaya ke file CSV
    df_clean.to_csv(output_path, index=False)

    # Tampilkan pesan sukses di terminal
    print(f"✅ Data bersih disimpan ke {output_path}")

# Menjalankan fungsi jika script dijalankan langsung
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)  # Pastikan folder data ada
    clean_university_data("data/raw_universities.json", "data/cleaned_universities.csv")
