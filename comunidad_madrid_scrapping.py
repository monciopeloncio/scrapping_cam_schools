import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_school_codes():

    URL = 'http://gestiona.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    cod_centros = soup.find("input", {"name": "codCentrosExp"}).get('value')
    return cod_centros.split(';')


def get_school_info(school_code):

    URL = 'http://gestiona.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm'

    payload = f'navegador=&cdCentro={school_code}&dsCentro=&codCentrosNav=28060646%3B28063027%3B28047460%3B28047551%3B28044100%3B28043405%3B28043417%3B28067665%3B28047861%3B28070913%3B28072004%3B28044161%3B28068098%3B28079621%3B28062643%3B28043454%3B28049055%3B28065292%3B28068037%3B28043740%3B28049067%3B28043922%3B28072429%3B28070202%3B28068219%3B28068301%3B28049195%3B28044252%3B28068086%3B28058147%3B28043491%3B28044136%3B28044288%3B28064305%3B28046947%3B28064123%3B28044203%3B28043508%3B28070664%3B28068050%3B28043909%3B28047587%3B28058202%3B28044215%3B28067860%3B28072338%3B28072028%3B28061687%3B28047472%3B28068232%3B28070263%3B28072065%3B28071851%3B28043466%3B28070937%3B28063076%3B28064299%3B28043481%3B28048142%3B28071887%3B28068062%3B28070111%3B28072387%3B28067872%3B28047538%3B28046972%3B28057696%3B28043533%3B28047447%3B28048622%3B28064317%3B28079023%3B28073392%3B28047009%3B28043776%3B28068335%3B28047599%3B28043569%3B28078951%3B28067677%3B28068347%3B28048580%3B28047022%3B28068323%3B28064275%3B28065334%3B28073264%3B28044240%3B28043910%3B28043600%3B28048014%3B28043821%3B28068773%3B28060634%3B28068074%3B28043806%3B28048609%3B28044264%3B28073288%3B28068049&formularioConsulta=busquedaAvanzada&codCentrosComp=&dscCentrosComp=&siPrivadoComp=&cdTramoEdu=0010&cdNivelEdu=6027&cdEnsenanza=-2&cdEspecialidad=-2&cdEspecialidadII=-2&dsMuni=&cdMuni=&comboMunicipios=0&dsDistrito=&cdDistrito=&cdGenerico=0&filtro.dsCentro=&filtro.cdCentro=&cdLegislacionSE=LOGSE'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://gestiona.madrid.org',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://gestiona.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm',
        'Accept-Language': 'en,es;q=0.9,gl;q=0.8',
        'Cookie': 'selectedTab=solapas%3D1%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B%3B; JSESSIONID=V40JpdlBJpvyKwRgnbmpGw2Nh17nltWnxK1Rvbqn9Tr6Sc7v94PLu0021-1300843651u0021396966809; dtCookie=21$9E7675E49DD1C935FCE04903255C7AB3; _pk_ses..bbd2=*; _pk_ses.65.bbd2=*; NSC_mc_QSP_HFTUJPOB_7777=ffffffffc3a01e0745525d5f4f58455e445a4a422851; _pk_id..bbd2=577e9b30fba68432.1591530989.2.1591553707.1591532220.; _pk_id.65.bbd2=577e9b30fba68432.1591530989.2.1591553707.1591532220.; JSESSIONID=GJPqpvGTvh0GbRhM8pcT1KMyJ9WW6Xv2J0pzpT4vQ8KK0tJvpQDL!-802879182!-830108877; NSC_mc_QSP_HFTUJPOB_7777=ffffffffc3a01e0745525d5f4f58455e445a4a422851'
    }

    page = requests.request("POST", URL, headers=headers, data=payload)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find('div', {'id': 'capaDatIdentContent'}).find('td', {'class': 'pSizeMB'}).find('strong').text.strip()
    email = soup.find('span', {'class': "pB"}).find('strong').text.strip()

    print(name, email)

    return {'name': name, 'email': email}


names = []
emails = []


school_codes = get_school_codes()

print(f'Number of schools {len(school_codes)}')

for code in school_codes:
    print(f'School {code}')
    info = get_school_info(code)
    names.append(info['name'])
    emails.append(info['email'])

df = pd.DataFrame(
    {
        'Code': school_codes,
        'Name': names,
        'Email': emails,
    }
)

df.to_csv('results/madrid_schools.csv', index=False, encoding='utf-8')
