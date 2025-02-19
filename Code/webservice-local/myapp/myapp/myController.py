import json
import psycopg2
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Necessario per ricevere POST da servlet
def ImportaDatiAltervista(request):
    if request.method == 'POST':
        try:
            # Leggi i dati JSON dalla richiesta POST
            dati = json.loads(request.body)
            
            # Connessione al database
            conn = psycopg2.connect(
                database="telefonia",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            
            #Inserimento TELEFONATE
            for telefonata in dati['telefonate']:
                # Converti data e ora da stringa a oggetti date e time
                data = datetime.strptime(telefonata['data'], '%Y-%m-%d').date()
                ora = datetime.strptime(telefonata['ora'], '%H:%M:%S').time()
                
                cur.execute("""
                    INSERT INTO telefonata (id, effettuatada, data, ora, durata, costo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        effettuatada = EXCLUDED.effettuatada,
                        data = EXCLUDED.data,
                        ora = EXCLUDED.ora,
                        durata = EXCLUDED.durata,
                        costo = EXCLUDED.costo
                """, (
                    telefonata['id'],
                    telefonata['effettuataDa'],
                    data,
                    ora,
                    telefonata['durata'],
                    float(telefonata['costo'])
                ))

            # Inserimento CONTRATTI TELEFONICI
            for contratto in dati['contratti']:
                data_attivazione = datetime.strptime(contratto['dataAttivazione'], '%Y-%m-%d').date()
                
                cur.execute("""
                    INSERT INTO contrattotelefonico (numero, dataattivazione, tipo, minutiresidui, creditoresiduo)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (numero) DO UPDATE SET
                        dataattivazione = EXCLUDED.dataattivazione,
                        tipo = EXCLUDED.tipo,
                        minutiresidui = EXCLUDED.minutiresidui,
                        creditoresiduo = EXCLUDED.creditoresiduo
                """, (
                    contratto['numero'],
                    data_attivazione,
                    contratto['tipo'],
                    contratto.get('minutiResidui', None),  # usando .get() per gestire campi opzionali
                    contratto.get('creditoResiduo', None)
                ))

            # Inserimento SIM ATTIVE
            for sim in dati['simAttive']:
                data_attivazione = datetime.strptime(sim['dataAttivazione'], '%Y-%m-%d').date()
                
                cur.execute("""
                    INSERT INTO simattiva (codice, tiposim, associataa, dataattivazione)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (codice) DO UPDATE SET
                        tiposim = EXCLUDED.tiposim,
                        associataa = EXCLUDED.associataa,
                        dataattivazione = EXCLUDED.dataattivazione
                """, (
                    sim['codice'],
                    sim['tipoSIM'],
                    sim['associataA'],
                    data_attivazione
                ))

            # Inserimento SIM DISATTIVE
            for sim in dati['simDisattive']:
                data_att = datetime.strptime(sim['dataAttivazione'], '%Y-%m-%d').date()
                data_disatt = datetime.strptime(sim['dataDisattivazione'], '%Y-%m-%d').date()
                
                cur.execute("""
                    INSERT INTO simdisattiva (codice, tiposim, eraassociataa, dataattivazione, datadisattivazione)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (codice) DO UPDATE SET
                        tiposim = EXCLUDED.tiposim,
                        eraassociataa = EXCLUDED.eraassociataa,
                        dataattivazione = EXCLUDED.dataattivazione,
                        datadisattivazione = EXCLUDED.datadisattivazione
                """, (
                    sim['codice'],
                    sim['tipoSIM'],
                    sim['eraAssociataA'],
                    data_att,
                    data_disatt
                ))

            # Inserimento SIM NON ATTIVE
            for sim in dati['simNonAttive']:
                cur.execute("""
                    INSERT INTO simnonattiva (codice, tiposim)
                    VALUES (%s, %s)
                    ON CONFLICT (codice) DO UPDATE SET
                        tiposim = EXCLUDED.tiposim
                """, (
                    sim['codice'],
                    sim['tipoSIM']
                ))

            # Commit delle transazioni
            conn.commit()
            
            return JsonResponse({
                "status": "success",
                "message": "Dati importati con successo"
            })

        except Exception as e:
            # In caso di errore, rollback
            if 'conn' in locals():
                conn.rollback()
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

        finally:
            # Chiudi sempre la connessione
            if 'conn' in locals():
                cur.close()
                conn.close()

    else:
        return JsonResponse({
            "status": "error",
            "message": "Metodo non permesso. Usa POST."
        })


def TestConnessione(request):
    res = HttpResponse(content_type="text/html")
    
    try:
        conn = psycopg2.connect(
            database="telefonia",
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        res.write("Connessione locale riuscita!")
        conn.close()
        
    except Exception as e:
        res.write(f"Errore di connessione al db: {str(e)}")
    
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
	
	