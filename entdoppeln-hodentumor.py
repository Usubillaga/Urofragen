#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trennt uro-hod-00001 und uro-hod-00008, die in Fragestellung und richtiger
Antwort wortgleich waren (Aehnlichkeit 1.0) und damit dieselbe Aussage zweimal
prueften. Beide behalten ihre richtige Antwort; sie pruefen jetzt aber
unterschiedliche Punkte:

  00001 Seminom      -> die Nachsorge stuetzt sich auf Bildgebung,
                        weil die Marker meist nicht informativ sind
  00008 Nichtseminom -> die Nachsorge stuetzt sich auf Marker

Aufruf:  python3 tools/entdoppeln-hodentumor.py
"""
import json
from difflib import SequenceMatcher
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "data" / "fragen" / "hodentumor.json"

NEU = {
    "uro-hod-00001": {
        "de": {
            "lead_in": "Welches Vorgehen ist beim reinen Seminom im Stadium I Standard?",
            "C": ("Aktive Surveillance mit bildgebungsgestützter Nachsorge",
                  "Ohne Risikomerkmale liegt das Rezidivrisiko bei etwa 15 Prozent, und Rezidive sind fast immer heilbar. Getragen wird die Überwachung von der Schnittbildgebung, weil die Marker beim Seminom meist im Normbereich bleiben."),
            "D": ("Nachsorge allein mit Tumormarkern ohne Bildgebung",
                  "Beim Seminom sind AFP definitionsgemäß normal und beta-hCG nur bei einem Teil erhöht. Eine markergestützte Nachsorge ohne Bildgebung übersieht das retroperitoneale Rezidiv."),
        },
        "en": {
            "lead_in": "What is the standard approach in pure stage I seminoma?",
            "C": ("Active surveillance based on cross-sectional imaging",
                  "Without risk features the relapse risk is around 15 per cent and relapses are almost always curable. Surveillance rests on imaging, because markers usually stay normal in seminoma."),
            "D": ("Follow-up with tumour markers alone, without imaging",
                  "In seminoma AFP is normal by definition and beta-hCG raised in only a proportion. Marker-based follow-up without imaging misses the retroperitoneal relapse."),
        },
        "es": {
            "lead_in": "¿Cuál es el enfoque estándar en el seminoma puro en estadio I?",
            "C": ("Vigilancia activa apoyada en pruebas de imagen seriadas",
                  "Sin factores de riesgo el riesgo de recidiva ronda el 15 por ciento y las recidivas son casi siempre curables. La vigilancia se apoya en la imagen, porque en el seminoma los marcadores suelen ser normales."),
            "D": ("Seguimiento solo con marcadores tumorales, sin imagen",
                  "En el seminoma la AFP es normal por definición y la beta-hCG se eleva solo en una parte. Un seguimiento basado en marcadores sin imagen pasa por alto la recidiva retroperitoneal."),
        },
    },
    "uro-hod-00008": {
        "de": {
            "lead_in": "Welches Vorgehen ist beim Nichtseminom ohne lymphovaskuläre Invasion Standard?",
            "D": ("Aktive Surveillance mit engmaschigen Markerkontrollen",
                  "Ohne lymphovaskuläre Invasion liegt das Rezidivrisiko bei etwa 15 Prozent. Anders als beim Seminom tragen hier AFP und beta-hCG die Überwachung, weil sie ein Rezidiv oft vor der Bildgebung anzeigen."),
            "B": ("Primäre retroperitoneale Lymphadenektomie einseitig",
                  "Sie bleibt Sonderfällen vorbehalten: Ablehnung oder Kontraindikation der Chemotherapie, hoher Teratomanteil oder eine nicht sicherzustellende Nachsorge."),
        },
        "en": {
            "lead_in": "What is the standard approach in non-seminoma without lymphovascular invasion?",
            "D": ("Active surveillance with close tumour marker checks",
                  "Without lymphovascular invasion the relapse risk is around 15 per cent. Unlike seminoma, AFP and beta-hCG carry surveillance here, because they often signal relapse before imaging does."),
            "B": ("Primary unilateral retroperitoneal lymph node dissection",
                  "It is reserved for special situations: refusal of or contraindication to chemotherapy, high teratoma content, or follow-up that cannot be assured."),
        },
        "es": {
            "lead_in": "¿Cuál es el enfoque estándar en el no seminoma sin invasión linfovascular?",
            "D": ("Vigilancia activa con controles estrechos de marcadores",
                  "Sin invasión linfovascular el riesgo de recidiva ronda el 15 por ciento. A diferencia del seminoma, aquí la AFP y la beta-hCG sostienen la vigilancia, porque a menudo señalan la recidiva antes que la imagen."),
            "B": ("Linfadenectomía retroperitoneal primaria unilateral",
                  "Se reserva para situaciones especiales: rechazo o contraindicación de la quimioterapia, alto componente de teratoma, o un seguimiento que no pueda asegurarse."),
        },
    },
}


def main():
    doc = json.loads(P.read_text(encoding="utf-8"))
    for q in doc["fragen"]:
        spec = NEU.get(q["id"])
        if not spec:
            continue
        for lang, s in spec.items():
            b = q["content"][lang]
            b["lead_in"] = s["lead_in"]
            for k, wert in s.items():
                if k == "lead_in":
                    continue
                text, rat = wert
                b["options"][k]["text"] = text
                b["options"][k]["rationale"] = rat
        q["version"] = int(q.get("version", 1)) + 1
    P.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def sig(q, lc="de"):
        ck = [o["key"] for o in q["options"] if o["correct"]][0]
        b = q["content"][lc]
        return b["lead_in"] + " " + b["options"][ck]["text"]

    a = [q for q in doc["fragen"] if q["id"] == "uro-hod-00001"][0]
    b = [q for q in doc["fragen"] if q["id"] == "uro-hod-00008"][0]
    for lc in ("de", "en", "es"):
        r = SequenceMatcher(None, sig(a, lc), sig(b, lc)).ratio()
        print(f"{lc}: Aehnlichkeit jetzt {r:.2f} (vorher 1.00)")


if __name__ == "__main__":
    main()
