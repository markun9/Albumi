import csv
import os
import requests
import sys
import re


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w',encoding='utf-8') as datoteka:
        datoteka.write(r.text)
        print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


zanri=['Alternative','Avantgarde','Industrial','Black','Death','Doom','Post','Progressive','Stoner','Heavy','Math','Gothic','Sludge']
for zanr in zanri:
    shrani('http://www.metalstorm.net/bands/albums_top.php?album_style=' + zanr, zanr + '.html')

slovar = {'vrstni_red':[],'bendi':[],'zanri':[], 'albumi':[], 'ocene':[], 'st_glasov':[]}   
for zanr in zanri:
    with open(zanr + '.html','r',encoding='utf-8') as v:
         print("pridem do sm", v)
         #print(v.read())
         for line in v:
             bend = re.findall('''<b><a href=/bands/band.php\?band_id=\d+&\w+=[-#&;ÿöä:ô()ÖăåáA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*>([-#&;ÿöä:ô()Ö'ă%åáA-Za-z0-9 _.,!?"'/$\t\s\+\w-]*)</a></b>''', line, flags=re.DOTALL)
             po_vrsti = re.findall('''<span class=dark>(\d+\.)</span>''', line, flags=re.DOTALL)
             album = re.findall('''<a href=/bands/album.php\?album_id=\d+>([-\[\]#&;ÿöä:ô()ÖăåáA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*)</a> <span class=dark>(\(\d+\))</span></td>''', line, flags=re.DOTALL)
             ocena = re.findall('''<a href=/bands/rating.php\?album_id=\d+>(\d+\.?\d+)</a>''', line, flags=re.DOTALL)
             st_glasov = re.findall('''<span class=dark>\| (\d+)</span>''', line, flags=re.DOTALL)
             if po_vrsti!= []:
                 slovar['vrstni_red'].append(po_vrsti)
             if bend != []:
                 slovar['bendi'].append(bend)
                 slovar['zanri'].append([zanr])
             if album != []:
                 slovar['albumi'].append(album)
             if ocena != []:
                 slovar['ocene'].append(ocena)
             if st_glasov != []:
                 slovar['st_glasov'].append(st_glasov)
print("bendov imam" + str(len(slovar['bendi'])))
print("zanrov imam" + str(len(slovar['zanri'])))
print("cifr je" + str(len(slovar['vrstni_red'])))
print("albumov je" + str(len(slovar['albumi'])))
print("ocena je" + str(len(slovar['ocene'])))
print("glasov glasov je" + str(len(slovar['st_glasov'])))

print("torej, nek random album je", slovar['bendi'][544], slovar['zanri'][544],
      slovar['albumi'][544], slovar['ocene'][544], slovar['vrstni_red'][544])


