import json
import psycopg2
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt  # Necessario per ricevere POST da servlet
def ImportaDatiAltervista(request):
    if request.method == 'POST':
        try:
            # 1️⃣ Leggi i dati JSON dalla richiesta POST
            dati = json.loads(request.body)
            if "data" not in dati:
                return JsonResponse({"status": "error", "message": "Il JSON non contiene il nodo 'data'"}, status=400)
            dati = dati["data"]

            # 2️⃣ Connessione al database
            conn = psycopg2.connect(
                database="Telefonia",
                user="postgres",
                password="password",  # Sostituisci con la tua password
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            # 3️⃣ Inserisci le telefonate
            if "Telefonata" in dati:
                for tel in dati["Telefonata"]:
                    data = datetime.strptime(tel["data"], '%d/%m/%Y').date()
                    ora = datetime.strptime(tel["ora"], '%H:%M').time()
                    durata = int(tel["durata"].split(":")[0]) * 60 + int(tel["durata"].split(":")[1])
                    costo = float(tel["costo"].replace("€", "").replace(",", "."))

                    cur.execute("""
                        INSERT INTO "Telefonata" (id, effettuatada, data, ora, durata, costo)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                        effettuatada = EXCLUDED.effettuatada,
                        data = EXCLUDED.data,
                        ora = EXCLUDED.ora,
                        durata = EXCLUDED.durata,
                        costo = EXCLUDED.costo
                    """, (tel["id"], tel["effettuataDa"], data, ora, durata, costo))

            # 4️⃣ Inserisci i contratti
            if "ContrattoTelefonico" in dati:
                for contratto in dati["ContrattoTelefonico"]:
                    data_attivazione = datetime.strptime(contratto["dataAttivazione"], '%d/%m/%Y').date()

                    cur.execute("""
                        INSERT INTO "ContrattoTelefonico" (numero, dataAttivazione, tipo, minutiResidui, creditoResiduo)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (numero) DO UPDATE SET
                        dataAttivazione = EXCLUDED.dataAttivazione,
                        tipo = EXCLUDED.tipo,
                        minutiResidui = EXCLUDED.minutiResidui,
                        creditoResiduo = EXCLUDED.creditoResiduo
                    """, (contratto["numero"], data_attivazione, contratto["tipo"], 
                          contratto.get("minutiResidui"), contratto.get("creditoResiduo")))

            # 5️⃣ Inserisci le SIM attive
            if "SIMAttiva" in dati:
                for sim in dati["SIMAttiva"]:
                    data_attivazione = datetime.strptime(sim["dataAttivazione"], '%d/%m/%Y').date()

                    cur.execute("""
                        INSERT INTO "SIMAttiva" (codice, tipoSIM, associataA, dataAttivazione)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                        tipoSIM = EXCLUDED.tipoSIM,
                        associataA = EXCLUDED.associataA,
                        dataAttivazione = EXCLUDED.dataAttivazione
                    """, (sim["codice"], sim["tipoSIM"], sim["associataA"], data_attivazione))

            # 6️⃣ Inserisci le SIM disattivate
            if "SIMDisattiva" in dati:
                for sim in dati["SIMDisattiva"]:
                    data_attivazione = datetime.strptime(sim["dataAttivazione"], '%d/%m/%Y').date()
                    data_disattivazione = datetime.strptime(sim["dataDisattivazione"], '%d/%m/%Y').date()

                    cur.execute("""
                        INSERT INTO "SIMDisattiva" (codice, tipoSIM, eraAssociataA, dataAttivazione, dataDisattivazione)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                        tipoSIM = EXCLUDED.tipoSIM,
                        eraAssociataA = EXCLUDED.eraAssociataA,
                        dataAttivazione = EXCLUDED.dataAttivazione,
                        dataDisattivazione = EXCLUDED.dataDisattivazione
                    """, (sim["codice"], sim["tipoSIM"], sim["eraAssociataA"], data_attivazione, data_disattivazione))

            # 7️⃣ Inserisci le SIM non attive
            if "SIMNonAttiva" in dati:
                for sim in dati["SIMNonAttiva"]:
                    cur.execute("""
                        INSERT INTO "SIMNonAttiva" (codice, tipoSIM)
                        VALUES (%s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                        tipoSIM = EXCLUDED.tipoSIM
                    """, (sim["codice"], sim["tipoSIM"]))

            # ✅ Commit finale
            conn.commit()
            return JsonResponse({"status": "success", "message": "Dati importati con successo"})
            

        except Exception as e:
            # In caso di errore, rollback
            if 'conn' in locals():
                conn.rollback()
            return JsonResponse({"status": "error", "message": str(e)})

        finally:
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
	
	