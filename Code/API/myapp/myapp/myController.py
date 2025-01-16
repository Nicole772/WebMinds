import json
import psycopg2
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def ImportaDatiAltervista(request):
    res = HttpResponse(content_type="text/html")
    
    try:
        # Connessione al database
        conn = psycopg2.connect(
            database="telefonia", 
            user='postgres',  
            password='la_tua_password', 
            host='localhost', 
            port='5432'
        )

        conn.autocommit = True
        cursor = conn.cursor()

        if request.method == "POST":
            dati = json.loads(request.body)
            
            # Importazione Telefonate
            if 'telefonate' in dati:
                for telefonata in dati['telefonate']:
                    query = '''
                        INSERT INTO "Telefonata" 
                        ("id", "effettuataDa", "data", "ora", "durata", "costo")
                        VALUES (%s, %s, %s, %s, %s, %s);
                    '''
                    cursor.execute(query, (
                        telefonata['id'],
                        telefonata['effettuataDa'],
                        telefonata['data'],
                        telefonata['ora'],
                        telefonata['durata'],
                        telefonata['costo']
                    ))

            # Importazione Contratti Telefonici
            if 'contratti' in dati:
                for contratto in dati['contratti']:
                    query = '''
                        INSERT INTO "ContrattoTelefonico"
                        ("numero", "dataAttivazione", "tipo", "minutiResidui", "creditoResiduo")
                        VALUES (%s, %s, %s, %s, %s);
                    '''
                    cursor.execute(query, (
                        contratto['numero'],
                        contratto['dataAttivazione'],
                        contratto['tipo'],
                        contratto.get('minutiResidui'),  # .get() gestisce campi opzionali
                        contratto.get('creditoResiduo')
                    ))

            # Importazione SIM Attive
            if 'simAttive' in dati:
                for sim in dati['simAttive']:
                    query = '''
                        INSERT INTO "SIMAttiva"
                        ("codice", "tipoSIM", "associataA", "dataAttivazione")
                        VALUES (%s, %s, %s, %s);
                    '''
                    cursor.execute(query, (
                        sim['codice'],
                        sim['tipoSIM'],
                        sim['associataA'],
                        sim['dataAttivazione']
                    ))

            # Importazione SIM Disattive
            if 'simDisattive' in dati:
                for sim in dati['simDisattive']:
                    query = '''
                        INSERT INTO "SIMDisattiva"
                        ("codice", "tipoSIM", "eraAssociataA", "dataAttivazione", "dataDisattivazione")
                        VALUES (%s, %s, %s, %s, %s);
                    '''
                    cursor.execute(query, (
                        sim['codice'],
                        sim['tipoSIM'],
                        sim['eraAssociataA'],
                        sim['dataAttivazione'],
                        sim['dataDisattivazione']
                    ))

            # Importazione SIM Non Attive
            if 'simNonAttive' in dati:
                for sim in dati['simNonAttive']:
                    query = '''
                        INSERT INTO "SIMNonAttiva"
                        ("codice", "tipoSIM")
                        VALUES (%s, %s);
                    '''
                    cursor.execute(query, (
                        sim['codice'],
                        sim['tipoSIM']
                    ))
            
            res.write("Dati importati con successo")
        else:
            res.write("Metodo non consentito")

        cursor.close()
        conn.close()

    except Exception as e:
        res.write(f"Errore durante l'importazione: {str(e)}")
        
    return res



def TestConnessione(request):
    res = HttpResponse(content_type="text/html")
    
    try:
        conn = psycopg2.connect(
            database="telefonia",
            user='postgres',
            password='tua_password',
            host='localhost',
            port='5432'
        )
        res.write("Connessione riuscita!")
        conn.close()
        
    except Exception as e:
        res.write(f"Errore di connessione: {str(e)}")
    
    return res

def index(request):
	o1 = "<html> <body>"
	o2 = "<p>Welcome to DJANGO</p>"
	o3 = "</body> </html>"
	return HttpResponse(o1 + o2 + o3)
	
def index2(request):
	response = HttpResponse(content_type="text/html")
	response.write("<html> <body>")
	response.write("<p>Welcome to DJANGO again</p>")
	response.write("</body> </html>")
	return response
	
def paramsToJson(request):
	if request.method == "GET":
		params = request.GET
	else:
		params = request.POST
	
	o = {}
	for n in params.dict().keys():
		o[n] = params.get(n)
	
	res = HttpResponse(content_type="application/json")
	res.write(json.dumps(o))
	return res

def PostMongoDB(request):
	if request.method == "GET":
		prit("Hu")
	else:
		l = request.readlines()
		docjson = ""
		for r in l:
			docjson = docjson + r
		doc = json.reads(docjson)

def Hello(request):
	context = { "name": "John"}
	template = loader.get_template("Hello.html")
	page = template.render(context, request)
	
	res = HttpResponse(content_type="text/html")
	res.write(page)

	return res

def Nominativi(request):
	conn = psycopg2.connect(database="MyDB", user='MyUser',  
	password='MyPwd', host='localhost', port='5432')

	conn.autocommit = True

	cursor = conn.cursor() 
	query = 'SELECT "Name", "Age" FROM "Names";'

	cursor.execute(query) 
	results = cursor.fetchall()
	l = []
	for r in results:
		o = {}
		o["name"] = r[0]
		o["age"] = r[1]
		l.append(o)
	data = { "elementi": len(l)}
	data["list"]=l
	
	context = {"res": data}
	
	template = loader.get_template("Nominativi.html")
	page = template.render(context, request)
	
	res = HttpResponse(content_type="text/html")
	res.write(page)

	return res
	
def SessionCount(request):
	res = HttpResponse(content_type="text/html")

	counter = request.session.get("counter")
	if counter == None:
		res.write("No session activated")
	else:
		counter+=1;
		res.write("Counter is {}".format(counter))
		request.session["counter"]=counter;
	return res

def StartSession(request):
	res = HttpResponse(content_type="text/html")

	counter = request.session.get("counter")
	if counter == None:
		request.session["counter"] = 1
		res.write("Session Started")
	else:
		res.write("Session already started")
	return res

def CloseSession(request):
	res = HttpResponse(content_type="text/html")

	counter = request.session.get("counter")
	if counter != None:
		del request.session["counter"]
		res.write("Session stopped")
	else:
		res.write("Session not started")
	return res
	
	