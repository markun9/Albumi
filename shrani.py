import csv
import os
import requests
import sys
import re
import os.path

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



zanri=['Alternative','Avantgarde','Industrial','Black','Death','Doom','Post-metal','Power','Symphonic','Progressive','Stoner','Heavy','Math','Gothic','Sludge','Folk']
for zanr in zanri:
    shrani('http://www.metalstorm.net/bands/albums_top.php?album_style=' + zanr, zanr + '.html')

slovar = {'vrstni_red':[],'album':[],'leto':[],'avtor':[],'podzvrst':[], 'ocena':[], 'st_glasov':[]}
slovar2 = {'avtor':[], 'podzvrst':[], 'drzava':[]}

# tole je treba izvest samo enkrat, dokler podatki2 ni dobro narejena
for i in range(1,100):
    shrani('http://www.metalstorm.net/bands/band.php?band_id=' + str(i) + '&bandname=', str(i) + '.html')
    with open (str(i) + '.html','r',encoding='utf8') as v:
        zanrilist = []
        for line in v:
            bend = re.findall('''([-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*) - Metal Storm</title>''', line, flags=re.DOTALL)
            zanr = re.findall('''<a href=index.php\?b_where=s.style&b_what=[^>]*> ?([-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*)</a>''', line, flags=re.DOTALL)
            drzava = re.findall('''<a href=index.php\?b_where=p.country&b_what=[-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*>([-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*)</a></td>''', line, flags=re.DOTALL)
            if bend != []:
                slovar2['avtor'].append(bend)
            if zanr != []:
                zanrilist.append(zanr)
            if drzava != []:
                slovar2['drzava'].append(drzava)
        slovar2['podzvrst'].append(zanrilist)
    v.close()
    os.remove(str(i) + '.html')


for zanr in zanri:
    with open(zanr + '.html','r',encoding='utf-8') as v:

         for line in v:
             bend = re.findall('''<b><a href=/bands/band.php\?band_id=\d+&\w+=[-#&;ÿöä:ô()ÖăåáA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*>([-#&;ÿēöä:ô()Ö'ă%åáA-Za-z0-9 _.,!?"'/$\t\s\+\w-]*)</a></b>''', line, flags=re.DOTALL)
             po_vrsti = re.findall('''<span class=dark>(\d+\.)</span>''', line, flags=re.DOTALL)
             album = re.findall('''<a href=/bands/album.php\?album_id=\d+>([-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*)</a> <span class=dark>\(\d+\)</span></td>''', line, flags=re.DOTALL)
             leto = re.findall('''<a href=/bands/album.php\?album_id=\d+>[-\[\]#&; Âiöšēäš:ô()Â;ÖšēăáÂA-Za-z0-9' _%.,!?"'/$\t\s\+\w]*</a> <span class=dark>\((\d+)\)</span></td>''', line, flags=re.DOTALL)
             ocena = re.findall('''<a href=/bands/rating.php\?album_id=\d+>(\d+\.?\d+)</a>''', line, flags=re.DOTALL)
             st_glasov = re.findall('''<span class=dark>\| (\d+)</span>''', line, flags=re.DOTALL)
             if po_vrsti!= []:
                 slovar['vrstni_red'].append(po_vrsti)
               #  print(po_vrsti)
             if bend != []:
                 slovar['avtor'].append(bend)
                 slovar['podzvrst'].append(zanr)
             if album != []:
                 slovar['album'].append(album)
                # print(album)
             if ocena != []:
                 slovar['ocena'].append(ocena)
             if st_glasov != []:
                 slovar['st_glasov'].append(st_glasov)
             if leto != []:
                 slovar['leto'].append(leto)
print("bendov imam" + str(len(slovar['avtor'])))
print("zanrov imam" + str(len(slovar['podzvrst'])))
print("cifr je" + str(len(slovar['vrstni_red'])))
print("albumov je" + str(len(slovar['album'])))
print("let je" + str(len(slovar['leto'])))
print("ocena je" + str(len(slovar['ocena'])))
print("glasov glasov je" + str(len(slovar['st_glasov'])))
print("DRZAV" + str(len(slovar2['drzava'])))

print("torej, nek random album je", slovar['avtor'][544], slovar['podzvrst'][544],
      slovar['album'][544], slovar['ocena'][544], slovar['vrstni_red'][544], slovar['leto'][544])
print(slovar2)

with open('Podatki.csv','w+') as csvfile:
    oznake = ['vrstni_red', 'album','leto','avtor', 'podzvrst', 'ocena', 'st_glasov']
    # print(csv)
    napisi = csv.DictWriter(csvfile, fieldnames=oznake)
    napisi.writeheader()
    for i in range(len(slovar['album'])):
        napisi.writerow({'vrstni_red': str((slovar['vrstni_red'][i])[0]),
                         'album': str((slovar['album'][i])[0]),
                         'avtor' : str((slovar['avtor'][i])[0]),
                         'leto' : str((slovar['leto'][i])[0]),
                         'podzvrst' : str(slovar['podzvrst'][i]),
                         'ocena' : str((slovar['ocena'][i])[0]),
                         'st_glasov' : str((slovar['st_glasov'][i])[0])})
with open('Podatki2.csv','w+') as csvfile:
    oznake = ['avtor', 'podzvrst', 'drzava']
    print(csv)
    napisi = csv.DictWriter(csvfile, fieldnames=oznake)
    napisi.writeheader()
    for i in range(len(slovar2['avtor'])):
        for a in range(len(slovar2['podzvrst'][i])):
            napisi.writerow({'avtor': str(slovar2['avtor'][i][0]),
                             'podzvrst': str(slovar2['podzvrst'][i][a][0]),
                             'drzava':str(slovar2['drzava'][i][0])})

    
with open('povp_na_leto.csv','w+') as csvfile:
    oznake = ['leto','ocena']
    napisi = csv.DictWriter(csvfile, fieldnames=oznake)
    napisi.writeheader()
    for i in range(len(slovar['leto'])):
        napisi.writerow({'leto' : str((slovar['leto'][i])[0]),
                         'ocena' : str((slovar['ocena'][i])[0])})
        
    
    
