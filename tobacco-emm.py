from tqdm import tqdm
from bs4 import BeautifulSoup
import requests, re, csv

searches = [
    {
        'all':[
                # Bosnian
                "Duhan oduzimanje",
                "Duhan oduzete",
                "Duvan oduz*",
                "šverc cigaretama",
                "Duhan krijumčarenje",
                "Najjeftiniji duhan",
                "Fino rezanog duhana",
                "Rolling duhan",
                "Ručno rezani duvan",
                "Pušenje duhana",
                # Serbian
                "duvan oduzimanje",
                "duvan zaplenjeno",
                "Krijumčarenje duvana",
                "Šverc duvana",
                "Falsifikovani duvan",
                "Fine rezani duvan",
                "rolling duvan",
                "Hand-rolling tobacco",
                "duvan za pušenje",
                # Croatian
                "Duhan oduzimanje",
                "Duhan oduzeti",
                "Duhan oduz*",
                "Krijumčarenja duhana",
                "Contraband duhana",
                "Krivotvoreni duhan",
                "Fino sjeckana duhanska",
                "Rolling duhan",
                "Hand-valjanje duhan",
                "Pušenje duhana",
                ], 
        'country': 'BA'
    },
    {
        'all':[
                # Bulgarian
                "Тютюн изземване",
                "Тютюн иззети",
                "Тютюн иззе*",
                "Контрабандата на тютюн",
                "Контрабандата на тютюневи изделия",
                "Фалшифициране на тютюн",
                "Фино нарязания тютюн",
                "Rolling тютюн",
                "Тютюн за ръчно навиване",
                "Тютюнът за пушене",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
                ],
        'country': 'BG'
    },
    {
        'all':[ # Croatian
                "Duhan oduzimanje",
                "Duhan oduzeti",
                "Duhan oduz*",
                "Krijumčarenja duhana",
                "Contraband duhana",
                "Krivotvoreni duhan",
                "Fino sjeckana duhanska",
                "Rolling duhan",
                "Hand-valjanje duhan",
                "Pušenje duhana",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
                ],
        'country': 'HR'
    },
    {
        'all':[
                # Czech
                "tabák záchvat",
                "tabák zmocnili",
                "Pašování tabáku",
                "Pašování tabáku",
                "Padělaný tabák",
                "Jemně řezaného tabáku",
                "Rolling tabák",
                "K ruční výrobě cigaret",
                "tabák ke kouření",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'CZ'
    },
    {   'all': [
                # Greek
                "κατάσχεση καπνού",
                "καπνού κατασχέθηκαν",
                "Καπνού κατασχ*",
                "λαθρεμπόριο καπνού",
                "Λαθραία καπνού",
                "παραποιημένων καπνού",
                "Λεπτοκομμένο καπνό",
                "τροχαίο καπνού",
                "Χειροποίητα τσιγάρα",
                "καπνός για κάπνισμα",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'GR'
    },
    {   'all': [
                # Hungarian
                "dohány roham",
                "dohány lefoglalt",
                "Dohánycsempészet",
                "Dohánycsempészet",
                "Hamis dohány",
                "Finomra vágott dohány",
                "sodródohánypiac",
                "Sodródohánymárkáinak",
                "dohány",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'HU'
    },
    {   'all': [
                # Macedonian
                "тутун одземање",
                "тутун запленети",
                "шверцот на тутунот",
                "тутун шверцувани",
                "фалсификувани цигари",
                "Глоба тутун намалување",
                "Ролинг тутун",
                "Рака-тркалање тутун",
                "пушењето",
                # Serbian
                "duvan oduzimanje",
                "duvan zaplenjeno",
                "Krijumčarenje duvana",
                "Šverc duvana",
                "Falsifikovani duvan",
                "Fine rezani duvan",
                "rolling duvan",
                "Hand-rolling tobacco",
                "duvan za pušenje",
        ],
        'country': 'MK'
    },
    {   'all': [
                # Serbian
                "duvan oduzimanje",
                "duvan zaplenjeno",
                "Krijumčarenje duvana",
                "Šverc duvana",
                "Falsifikovani duvan",
                "Fine rezani duvan",
                "rolling duvan",
                "Hand-rolling tobacco",
                "duvan za pušenje",
        ],
        'country': 'ME'
    },
    {   'all': [
                # Polish
                "zajęcie tytoniowe",
                "Tytoń zajęte",
                "zajęt* tyto*",
                "Przemyt tytoniu",
                "Kontrabanda tytoniu",
                "Podrabiany tyto",
                "Drobno krojonego tytoniu",
                "Rolling tytoniu",
                "Tytoniu do ręcznego zwijania",
                "tytoń do palenia",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'PL'
    },
    {   'all': [
                # Romanian
                "sechestrare de tutun",
                "tutun confiscate",
                "Contrabanda cu tutun",
                "Contrabanda cu tutun",
                "Tutun contrafăcute",
                "tutun tăiat fin",
                "tutun de rulare",
                "Rulat manual tutun",
                "tutun de fumat",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'RO'
    },
    {   'all': [
                # Serbian
                "duvan oduzimanje",
                "duvan zaplenjeno",
                "Krijumčarenje duvana",
                "Šverc duvana",
                "Falsifikovani duvan",
                "Fine rezani duvan",
                "rolling duvan",
                "Hand-rolling tobacco",
                "duvan za pušenje",
                # English
                "Tobacco seizure",
                "Tobacco seized",
                "Tobacco seiz*",
                "Tobaccco smuggling",
                "Tobacco contraband",
                "Counterfeit tobacco",
                "Fine cut tobacco",
                "Rolling tobacco",
                "Hand-rolling tobacco",
                "Smoking tobacco",
        ],
        'country': 'RS'
    },
    {   'all': [
                # Slovakian
                "tabak záchvat",
                "tabak zmocnili",
                "Pašovania tabaku",
                "Pašovania tabaku",
                "Falšované tabak",
                "Jemne rezaného tabaku",
                "rolling tabak",
                "K ručnej výrobe cigariet",
                "tabak na fajčenie",
        ],
        'country': 'SK'
    },
    {   'all': [
                # Slovenian
                "tobak zaseg",
                "tobak zasegli",
                "Tobak zaseg*",
                "Tihotapljenje tobačnih",
                "Tihotapljenje tobačnih",
                "Ponarejeni tobak",
                "Drobno rezani tobak",
                "Rolling tobak",
                "Ročno tobak za zvijanje cigaret",
                "tobak za kajenje",
        ],
        'country': 'SI'
    },
]




template = "http://emm.newsbrief.eu/NewsBrief/dynamic?page={pagenum}&edition=searcharticles&option=advanced&all={all_kw}&lang=all&language=it&dateFrom=2015-04-01&dateTo=2016-01-01&_=1462442787213"
country_re = re.compile(r'([a-zA-Z]{2}).gif')
fieldnames = ['id', 'page', 'country', 'date', 'title', 'desc', 'link', 'meta', 'translation', 'kws', 'search_url']
for search in searches:

    csvfile = open("tobacco-emm-{}-latest.csv".format(search['country']), 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for kw in tqdm(search['all']):
        for pagenum in tqdm(range(1, 2000), desc=kw):
            url = template.format(pagenum=pagenum, all_kw=kw) + "&sourceCountry=" + search['country']

            html =  BeautifulSoup(requests.get(url).text, "html.parser")
            found = False
            for articolo in html.findAll(class_='articlebox_big'):
                found = True
                _top = articolo.find(class_='center_headline_top')
                titolo = _top.get_text()
                link = _top.a['href']
                _source = articolo.find(class_='center_headline_source')

                country = None
                _match  = country_re.finditer(_source.img['src'])
                for m in _match:
                    country = m.group(1)

                data = list(_source.strings)[3]
                meta = _source.get_text()

                desc = articolo.find(class_='center_leadin').get_text()
                translation = articolo.find(class_='item_translation')
                if translation:
                    translation = translation.get_text()

                writer.writerow({
                    'id': hash(link), 
                    'page': pagenum,
                    'title': titolo,
                    'link': link,
                    'country': country,
                    'date': data,
                    'meta': meta,
                    'desc': desc,
                    'translation': translation,
                    'kws': "{}".format(kw),
                    'search_url': url
                    })

                csvfile.flush()

            if not found:
                break
    csvfile.close()