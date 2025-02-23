import json
import psycopg2
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Configura logging
logging.basicConfig(filename="webservice.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@csrf_exempt
def ImportaDatiAltervista(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Metodo non permesso. Usa POST."}, status=405)

    try:
        dati = json.loads(request.body)
        if "data" not in dati:
            return JsonResponse({"status": "error", "message": "Il JSON non contiene il nodo 'data'"}, status=400)
        dati = dati["data"]

        logging.info(f"Dati ricevuti: {json.dumps(dati, indent=2)}")  # Debug JSON ricevuto

        conn = psycopg2.connect(
            database="Telefonia",
            user="postgres",
            password="password", 
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # contratti telefonici
        if "ContrattoTelefonico" in dati:
            for contratto in dati["ContrattoTelefonico"]:
                try:
                    data_attivazione = datetime.strptime(contratto["dataAttivazione"], '%d/%m/%Y').date()
                    credito_residuo = float(contratto["creditoResiduo"].replace("€", "").replace(",", ".").strip()) if contratto.get("creditoResiduo") else 0.0

                    cur.execute("""
                        INSERT INTO "ContrattoTelefonico" (numero, "dataAttivazione", tipo, "minutiResidui", "creditoResiduo")
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (numero) DO UPDATE SET
                            "dataAttivazione" = EXCLUDED."dataAttivazione",
                            tipo = EXCLUDED.tipo,
                            "minutiResidui" = EXCLUDED."minutiResidui",
                            "creditoResiduo" = EXCLUDED."creditoResiduo";
                    """, (
                        contratto["numero"],
                        data_attivazione,
                        contratto["tipo"],
                        contratto.get("minutiResidui", 0),
                        credito_residuo
                    ))
                    logging.info(f"✅ Contratto aggiornato: {contratto['numero']}")
                except Exception as e:
                    logging.error(f"Errore inserimento contratto {contratto['numero']}: {str(e)}")

            conn.commit()  # Commit dopo ogni inserimento per evitare perdite

        # SIM attive
        if "SIMAttiva" in dati:
            for sim in dati["SIMAttiva"]:
                try:
                    data_attivazione = datetime.strptime(sim["dataAttivazione"], '%d/%m/%Y').date()
                    cur.execute("SELECT 1 FROM \"ContrattoTelefonico\" WHERE numero = %s", (sim["associataA"],))
                    if cur.fetchone() is None:
                        logging.warning(f"❌ ERRORE: Contratto {sim['associataA']} non trovato. Skipping SIM.")
                        continue
                    cur.execute("""
                        INSERT INTO "SIMAttiva" (codice, "tipoSIM", "associataA", "dataAttivazione")
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                            "tipoSIM" = EXCLUDED."tipoSIM",
                            "associataA" = EXCLUDED."associataA",
                            "dataAttivazione" = EXCLUDED."dataAttivazione";
                    """, (sim["codice"], sim["tipoSIM"], sim["associataA"], data_attivazione))
                    logging.info(f"✅ SIM attiva aggiornata: {sim['codice']}")
                except Exception as e:
                    logging.error(f"Errore inserimento SIM {sim['codice']}: {str(e)}")

            conn.commit()  # Commit per SIMAttiva

        # SIM disattivate
        if "SIMDisattiva" in dati:
            for sim in dati["SIMDisattiva"]:
                try:
                    data_attivazione = datetime.strptime(sim["dataAttivazione"], '%d/%m/%Y').date()
                    data_disattivazione = datetime.strptime(sim["dataDisattivazione"], '%d/%m/%Y').date()

                    cur.execute("""
                        INSERT INTO "SIMDisattiva" (codice, "tipoSIM", "eraAssociataA", "dataAttivazione", "dataDisattivazione")
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                            "tipoSIM" = EXCLUDED."tipoSIM",
                            "eraAssociataA" = EXCLUDED."eraAssociataA",
                            "dataAttivazione" = EXCLUDED."dataAttivazione",
                            "dataDisattivazione" = EXCLUDED."dataDisattivazione";
                    """, (sim["codice"], sim["tipoSIM"], sim["eraAssociataA"], data_attivazione, data_disattivazione))

                    logging.info(f"✅ SIM disattivata aggiornata: {sim['codice']}")

                except Exception as e:
                    logging.error(f"❌ ERRORE inserimento SIM disattivata {sim['codice']}: {str(e)}")

            conn.commit()  # Commit dopo aver elaborato tutte le SIM disattivate


        # SIM non attive
        if "SIMNonAttiva" in dati:
            for sim in dati["SIMNonAttiva"]:
                try:
                    cur.execute("""
                        INSERT INTO "SIMNonAttiva" (codice, "tipoSIM")
                        VALUES (%s, %s)
                        ON CONFLICT (codice) DO UPDATE SET
                            "tipoSIM" = EXCLUDED."tipoSIM";
                    """, (sim["codice"], sim["tipoSIM"]))
                    logging.info(f"✅ SIM non attiva aggiornata: {sim['codice']}")
                except Exception as e:
                    logging.error(f"Errore inserimento SIM non attiva {sim['codice']}: {str(e)}")

            conn.commit()  # Commit per SIMNonAttiva

        # telefonate
        if "Telefonata" in dati:
            for tel in dati["Telefonata"]:
                try:
                    data = datetime.strptime(tel["data"], '%d/%m/%Y').date()
                    ora = datetime.strptime(tel["ora"], '%H:%M').time()
                    durata = int(tel["durata"].split(":")[0]) * 60 + int(tel["durata"].split(":")[1])
                    costo = float(tel["costo"].replace("€", "").replace(",", "."))

                    cur.execute("""
                        INSERT INTO "Telefonata" (id, "effettuataDa", data, ora, durata, costo)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            "effettuataDa" = EXCLUDED."effettuataDa",
                            data = EXCLUDED.data,
                            ora = EXCLUDED.ora,
                            durata = EXCLUDED.durata,
                            costo = EXCLUDED.costo;
                    """, (tel['id'], tel['effettuataDa'], data, ora, durata, costo))
                    logging.info(f"✅ Telefonata aggiornata: {tel['id']}")
                except Exception as e:
                    logging.error(f"Errore inserimento telefonata {tel['id']}: {str(e)}")

            conn.commit()  # Commit per Telefonata

        return JsonResponse({"status": "success", "message": "Dati importati con successo"})

    except Exception as e:
        conn.rollback()
        logging.error(f"Errore generale: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)})

    finally:
        cur.close()
        conn.close()
