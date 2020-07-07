import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_results(page: int):

    PARAM_URL = f'http://www.educa.jccm.es/educacion/cm/educa_jccm/BBDD_ACCESS.1.1.tkContent.27265/tkListResults?formName=SQLQueriesSearcher&nshow.sqlResults=3&position.sqlResults={page}&idQuery=961'
    page = requests.get(PARAM_URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    schools = soup.find_all('div', class_='elementList')

    for school in schools:
        nature = school.find('div', class_='campListNATURALEZA')
        name = school.find('div', class_='campListNOMBRE')
        school_id = school.find('div', class_='campListCENTID')
        school_type = school.find('div', class_='campListDDENGENCENT')
        address = school.find('div', class_='campListDOMICILIO')
        locality = school.find('div', class_='campListLOCALIDAD')
        province = school.find('div', class_='campListPROVINCIA')
        postal_code = school.find('div', class_='campListCP')
        fax = school.find('div', class_='campListFAX')
        phone_number = school.find('div', class_='campListTELEFONO')
        email = school.find('div', class_='campListEMAIL')
        web = school.find('div', class_='campListWEB')

        natures.append(nature.text.strip())
        names.append(name.text.strip())
        school_ids.append(school_id.text.strip())
        school_types.append(school_type.text.strip())
        if address:
            addresses.append(address.text.strip())
        else:
            addresses.append("")

        localities.append(locality.text.strip())
        provinces.append(province.text.strip())
        postal_codes.append(postal_code.text.strip())
        if fax:
            faxes.append(fax.text.strip())
        else:
            faxes.append("")
        if phone_number:
            phone_numbers.append(phone_number.text.strip())
        else:
            phone_numbers.append("")
        if email:
            emails.append(email.text.strip())
        else:
            emails.append("")
        if web:
            webs.append(web.text.strip())
        else:
            webs.append("")

    # print(natures)
    # print(names)
    # print(school_ids)
    # print(school_types)
    # print(addresses)
    # print(localities)
    # print(provinces)
    # print(postal_codes)
    # print(faxes)
    # print(phone_numbers)
    # print(emails)
    # print(webs)


URL = 'http://www.educa.jccm.es/educacion/cm/educa_jccm/BBDD_ACCESS.1.1.tkContent.27265/tkListResults?formName=SQLQueriesSearcher&nshow.sqlResults=3&position.sqlResults=0&idQuery=961'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
total_results = soup.find('div', class_='totalPageList').find('strong').text

natures = []
names = []
school_ids = []
school_types = []
addresses = []
localities = []
provinces = []
postal_codes = []
faxes = []
phone_numbers = []
emails = []
webs = []

print(f'Total results:{total_results}', end="\n")

for i in range(3, int(total_results.replace('.', '')) + 3, 3):
    print(f'Scraping page {i}', end="\n")
    try:
        get_page_results(i)
    except Exception as identifier:
        print(identifier, end='\n')


df = pd.DataFrame(
    {
        'Nombre': names,
        'Naturaleza': natures,
        'Id': school_ids,
        'Tipo': school_types,
        'Dirección': addresses,
        'Localidad': localities,
        'Provincia': provinces,
        'Código_Postal': postal_codes,
        'FAX': faxes,
        'Teléfono': phone_numbers,
        'Email': emails,
        'Web': webs
    }
)
df.to_csv('results/cam_schools.csv', index=False, encoding='utf-8')
