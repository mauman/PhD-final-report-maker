import os
import subprocess
import csv

class Candidato:
    def __init__(self, nome, cognome, sesso, giorno, mese, anno, comune_nascita, provincia_nascita, cf, ciclo):
        self.CF = cf
        self.nome = nome
        self.cognome = cognome
        self.sesso = sesso
        self.data_nascita = giorno + "/" + mese + "/" + anno
        self.comune_nascita = comune_nascita
        self.provincia_nascita = provincia_nascita
        self.ciclo = ciclo
        self.title = ""

    def assignTitle(self, T):
        self.title = T

def candidati_nomi(candidati):
    result = ""
    for c in candidati:
        result += "* " + c.nome + " " + c.cognome + "\n"
    return result

def candidati_documenti(candidati):
    result = ""
    for c in candidati:
        if c.sesso == "m":
            result += "\\\n\\\n\\\nDott. "
        else:
            result += "\\\n\\\n\\\nDott.ssa "
        result += c.nome + " " + c.cognome + " identificat" + ("o" if c.sesso == "m" else "a") + " con il seguente documento "
        result += "............................$\\newline$\\\nrilasciato da " + "..................................$\\newline$\\\n"
        result += "Firma ......................................."
    return result

def effify(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')

fileRef = open("template.md", "r", encoding="utf-8")
template = fileRef.read()
fileRef.close()

fileRef = open("attachmentN.md", "r", encoding="utf-8")
attachmentN = fileRef.read()
fileRef.close()

fileRef = open("attachmentA.md", "r", encoding="utf-8")
attachmentA = fileRef.read()
fileRef.close()

fileRef = open("attachmentB.md", "r", encoding="utf-8")
attachmentB = fileRef.read()
fileRef.close()

fileRef = open("attestation.md", "r", encoding="utf-8")
attestation = fileRef.read()
fileRef.close()

fileRef = open("privacy.md", "r", encoding="utf-8")
privacy = fileRef.read()
fileRef.close()

os.makedirs("output", exist_ok=True)

time_start = "9:00"

time_end = "17:00"

day = "26/1/2026"

decreto = "3625/2025 del 16/12/2025"

presidente = "Barbara Re"
componente = "Han Van Der Aa"
segretario = "Chiara Di Francescomarino"

candidati = []
cycles = set()

with open('candidates.csv', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        C = Candidato(row["nome"], row["cognome"], row["sesso"].lower(), row["data_nascita"].split("/")[0], row["data_nascita"].split("/")[1], row["data_nascita"].split("/")[2], row["luogo_nascita"].strip(), row["prov_nascita"].strip(), row["codice_fiscale"].strip(), int(row["ciclo_numero"]))
        C.title = row["titolo"].strip()
        candidati.append(C)
        cycles.add(row["ciclo_numero"])

cycles = list(cycles)
cycles.sort()
cycles = ", ".join(cycles)

result = effify(template)

for candidateN, c in enumerate(candidati):

    name = c.nome
    surname = c.cognome
    title = c.title
    gender = c.sesso
    cycle = c.ciclo
    candidate = effify(attachmentN)
    result += candidate

    birthdate = c.data_nascita
    birthplace = c.comune_nascita
    province = c.provincia_nascita

    candidate = effify(attachmentB)
    result += candidate

    candidate = effify(attestation)
    result += candidate

    candidate = effify(privacy)
    result += candidate

result += effify(attachmentA)

    # result = f"\\fancyfoot[RO,RE]{{{i}}}\n" + result
fileRef = open(f"output/output.md", "w", encoding="utf-8")
fileRef.writelines(result)
fileRef.close()


    # if type == "sapienza":
header = "header-includes.yaml"
    # else:
    #     header = "header-includes-unitelma.yaml"
# res = subprocess.call(f"pandoc {header} -V pagestyle=empty -V geometry:margin=0.75in -V papersize:a4 --variable=fontfamily:arev -i output/output.md -o output/output.pdf", shell=True)
# res = subprocess.call(f"pandoc {header} -V pagestyle=empty -V geometry:margin=0.75in -V papersize:a4 -i output/output.md -o output/output.pdf", shell=True)
# Usa --metadata-file per evitare che Pandoc si confonda tra contenuto e configurazione
res = subprocess.call(f"pandoc --metadata-file=header-includes.yaml output/output.md -o output/output.pdf --pdf-engine=pdflatex", shell=True)

res = subprocess.call(f"pandoc --metadata-file=header-includes.yaml output/output.md -o output/output.docx", shell=True)
