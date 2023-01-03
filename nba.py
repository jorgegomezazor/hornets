import requests
import pandas as pd
from fpdf import FPDF
from PIL import Image
import bs4
def guardar_imagen(im, nombre):
    if im != 0:
        response = requests.get(im, stream=True).content # Descargo la imagen
        with open(nombre +'.png', 'wb') as f: # Guardo la imagen
            f.write(response) # Guardo la imagen
        del response # Borro la imagen de la memoria
    else:
        print('No hay imagen para guardar')
def leer_clave():
    with open('config.txt', 'r') as f: # Leo la clave
        for line in f:
            clave = line.strip()
    return clave # Devuelvo la clave
def extract():
    clave = leer_clave() # Leo la clave
    nba = requests.get('https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam/2022/CHA'+ clave) # Hago el request
    nba_json = nba.json() # Convierto el request en json
    hornets = pd.DataFrame(nba_json) # Creo el dataframe
    hornets = hornets[['Name', 'Team', 'Position', 'Games', 'Minutes', 'FieldGoalsMade', 'FieldGoalsAttempted', 'FieldGoalsPercentage', 'FreeThrowsMade', 'FreeThrowsAttempted', 'FreeThrowsPercentage', 'Rebounds', 'Assists', 'Steals', 'BlockedShots', 'Turnovers', 'Points','PlayerEfficiencyRating']] # Selecciono las columnas que me interesan
    return hornets # Devuelvo el dataframe
def transform(hornets):
    paginas = []
    for i in range(0, len(hornets)):
        paginas.append(hornets['Name'][i]) # Creo una lista con los nombres de los jugadores
    imagenes = []
    jug = 0
    imagenes = ['https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/6472.png&w=350&h=254', # Creo una lista con las imagenes de los jugadores
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/2488653.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4249.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3133603.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3074752.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/2991055.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4066383.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4230551.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4278078.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3138161.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4066731.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4432816.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4278076.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4431712.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4431699.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4702233.png&w=350&h=254',
    'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4432812.png&w=350&h=254']
    equipo = 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/cha.png&h=200&w=200' # Creo un string con la imagen del equipo
    guardar_imagen(equipo, 'Hornets') # Guardo la imagen del equipo
    for im in imagenes:
        guardar_imagen(im, paginas[jug]) # Guardo las imagenes de los jugadores
        jug += 1
    jugadores = []
    for i in range(len(hornets)):
        jugadores.append(hornets.iloc[[i]]) # Creo una lista con los dataframes de los jugadores
    img = Image.new('RGB', (210,297), "#cfe5ff" ) # Creo una imagen de fondo
    img.save('blue_colored.png') # Guardo la imagen de fondo
    return jugadores, hornets
def load(jugadores, hornets, salida):
    hornets_dicc = {} # Creo un diccionario
    hornets_dicc['Name'] = hornets['Name'] # Creo las claves del diccionario
    hornets_dicc['Team'] = hornets['Team']
    hornets_dicc['POS'] = hornets['Position']
    hornets_dicc['GP'] = hornets['Games']
    hornets_dicc['MIN'] = hornets['Minutes']
    hornets_dicc['FGM'] = hornets['FieldGoalsMade']
    hornets_dicc['FGA'] = hornets['FieldGoalsAttempted']
    hornets_dicc['FG%'] = hornets['FieldGoalsPercentage']
    hornets_dicc['FTM'] = hornets['FreeThrowsMade']
    hornets_dicc['FTA'] = hornets['FreeThrowsAttempted']
    hornets_dicc['FT%'] = hornets['FreeThrowsPercentage']
    hornets_dicc['REB'] = hornets['Rebounds']
    hornets_dicc['AST'] = hornets['Assists']
    hornets_dicc['STL'] = hornets['Steals']
    hornets_dicc['BLK'] = hornets['BlockedShots']
    hornets_dicc['TOV'] = hornets['Turnovers']
    hornets_dicc['PTS'] = hornets['Points']
    hornets_dicc['PER'] = hornets['PlayerEfficiencyRating']
    hornets = pd.DataFrame(hornets_dicc) # Creo un dataframe con el diccionario
    pdf = FPDF() # Creo el pdf
    pdf.add_page()  # Agrego una pagina
    pdf.image('blue_colored.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '') # Agrego la imagen de fondo
    pdf.set_font('Helvetica', size = 30)
    pdf.cell(200,10,'', ln=1, align='C')
    pdf.cell(200,10,'Charlotte Hornets', ln=1, align='C') # Agrego el nombre del equipo
    pdf.cell(100,10,'', ln=2, align='C')
    pdf.cell(100,10,'', ln=3, align='C')
    pdf.cell(100,10,'', ln=4, align='C')
    pdf.set_font('Helvetica', size = 7)
    row_height = pdf.font_size
    col_width = {column: max([len(str(x)) for x in hornets[column]])+5.6 for column in hornets.columns} # Creo un diccionario con el ancho de las columnas
    col_width['Name'] += 1.7
    for key, length in col_width.items():
        pdf.cell(length, row_height*2, str(key), border=1, align='C') # Agrego las columnas
    pdf.ln(row_height*2) # Salto de linea
    for i, row in hornets.iterrows(): # Agrego los datos de los jugadores
        for key, length in col_width.items(): 
            if key == 'Name':
                pdf.cell(length, row_height*2, str(row[key]), border=1) # Agrego el nombre del jugador
            else:
                pdf.cell(length, row_height*2, str(row[key]), border=1, align='C') # Agrego los datos del jugador
        pdf.ln(row_height*2) 
    pdf.set_font('Helvetica', size = 10)
    pdf.cell(100,10,'Pronóstico del siguiente partido:', ln=19, align='L') # Agrego el pronostico del siguiente partido
    pdf.set_font('Helvetica', size = 8)
    salida = salida.split(',')
    for s in salida:
        pdf.cell(100,10,s, ln=20, align='L') # Agrego el resultado del pronostico
    pdf.image('Hornets.png', 85, 250, 33) # Agrego la imagen del equipo
    pdf.ln(40)
    for i in range(len(jugadores)): # Agrego los datos de los jugadores en una pagina aparte
        pdf.add_page()
        pdf.image('blue_colored.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
        pdf.set_font('Arial', 'B', size = 10)
        pdf.cell(40, 10, 'Name: ' + jugadores[i]['Name'].to_string(index=False), ln=1)
        pdf.cell(40, 10, 'Position: ' + jugadores[i]['Position'].to_string(index=False), ln=2)
        pdf.cell(40, 10, 'Games: ' + jugadores[i]['Games'].to_string(index=False), ln=3)
        pdf.cell(40, 10, 'Minutes: ' + jugadores[i]['Minutes'].to_string(index=False), ln=4)
        pdf.cell(40, 10, 'FGM: ' + jugadores[i]['FieldGoalsMade'].to_string(index=False), ln=5)
        pdf.cell(40, 10, 'FGA: ' + jugadores[i]['FieldGoalsAttempted'].to_string(index=False), ln=6)
        pdf.cell(40, 10, 'FG%: ' + jugadores[i]['FieldGoalsPercentage'].to_string(index=False), ln=7)
        pdf.cell(40, 10, 'FTM: ' + jugadores[i]['FreeThrowsMade'].to_string(index=False), ln=8)
        pdf.cell(40, 10, 'FTA: ' + jugadores[i]['FreeThrowsAttempted'].to_string(index=False), ln=9)
        pdf.cell(40, 10, 'FT%: ' + jugadores[i]['FreeThrowsPercentage'].to_string(index=False), ln=10)
        pdf.cell(40, 10, 'Rebound: ' + jugadores[i]['Rebounds'].to_string(index=False), ln=11)
        pdf.cell(40, 10, 'Assists: ' + jugadores[i]['Assists'].to_string(index=False), ln=12)
        pdf.cell(40, 10, 'Steals: ' + jugadores[i]['Steals'].to_string(index=False), ln=13)
        pdf.cell(40, 10, 'Blocks: ' + jugadores[i]['BlockedShots'].to_string(index=False), ln=14)
        pdf.cell(40, 10, 'Turnovers: ' + jugadores[i]['Turnovers'].to_string(index=False),ln=15)
        pdf.cell(40, 10, 'Points: ' + jugadores[i]['Points'].to_string(index=False), ln=16)
        pdf.cell(40, 10, 'PER: ' + jugadores[i]['PlayerEfficiencyRating'].to_string(index=False), ln=17)
        pdf.image(jugadores[i]['Name'].to_string(index=False)+'.png', x = 70, y = 10, w = 70)
        pdf.image('Hornets.png', x=170/2, y=250, w=40)
    pdf.output('Hornets.pdf', 'F') # Guardo el pdf
def extract_2():
    url = 'https://www.solobasket.com/apuestas-deportivas/pronosticos-nba/' #url del que saco los datos del pronostico
    response = requests.get(url) #hago la peticion
    soup = bs4.BeautifulSoup(response.text, 'html.parser') #parseo el html
    return soup
def transform_2(soup):
    table = soup.find('tbody', {'class': 'nsn-tbody'}) #busco la tabla
    rows = table.find_all('tr') #busco las filas
    salida = ''
    hor = False
    for row in rows:
        if 'Hornets' in row.text: #busco el partido de los hornets
            salida = row.text #guardo el pronostico
            hor = True
            break
    if salida == '':
        salida = ' No hay partidos de Hornets,Se aporta el pronóstico del resto de partidos:,' #si no hay partidos de hornets, aporto el pronostico del resto de partidos
        for row in rows:
            if 'vs' in row.text: #busco los partidos
                salida += row.text #guardo el pronostico
                salida = salida.split()
                salida = salida[:-2]
                salida = ' '.join(salida)
                salida += ','
    return salida, hor
def load_2(salida, hornets):
    if hornets: #si hay partidos de hornets
        salida = salida.split()
        salida = salida[:-2]
        salida = ' '.join(salida)
        salida += ','
        print(salida) #imprimo el pronostico
    else: 
        salidas = salida.split(',') #si no hay partidos de hornets
        for s in salidas:
            print(s) #imprimo el pronostico
    return salida
if __name__ == '__main__':
    salida, hor = transform_2(extract_2())
    salida = load_2(salida, hor)
    hornets = extract()
    jugadores, hornets = transform(hornets)
    load(jugadores, hornets, salida)