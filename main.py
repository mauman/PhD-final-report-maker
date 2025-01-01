import os
import csv
import random
import subprocess
from PyPDF2 import PdfMerger
from codice_fiscale import get_CF

class Candidato:
    def __init__(self, nome, cognome, sesso, giorno, mese, anno, luogo_nascita, ciclo):
        self.CF = get_CF(nome, cognome, sesso, giorno, mese, anno, luogo_nascita)
        self.nome = nome
        self.cognome = cognome
        self.sesso = sesso
        self.data_nascita = giorno + "/" + mese + "/" + anno
        self.comune_nascita = luogo_nascita
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
        result += "\\\n\\\n\\\nDott. " + c.nome + " " + c.cognome + " identificato con il seguente documento "
        result += "............................ rilasciato da " + "..................................$\\newline$"
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


#
# if type == "sapienza":
#     fileRef = open("2024-09-03 domande.csv", "r", encoding="utf-8")
# else:
#     fileRef = open("2024-04-08 domande unitelma.csv", "r", encoding="utf-8")
#
# # 2024-01-25
# # if type == "sapienza":
# #     combos = [(1, 3, 7), (2, 5, 8), (4, 6, 7), (1, 3, 8), (2, 5, 7), (4, 6, 8)]
# # else:
# #     combos = [(1, 2, 3)]
#
# # 2024-02-23
# # if type == "sapienza":
# #     combos = [(1, 7, 9), (3, 5, 10), (2, 8, 9), (4, 6, 10)]
# # else:
# #     combos = [(1, 2, 3)]
#
# combos = [(1, 2, 3, 4)]
#
# reader = csv.reader(fileRef, quotechar="\"", delimiter="\n")
#
# questions = []
#
# for row in reader:
#     questions.append(row[0])
#
# fileRef.close()

os.makedirs("output", exist_ok=True)


cycles = "35, 36, 37"

time_start = "9:00"

time_end = "14:00"

day = "15/1/2025"

decreto = "3512/2024 del 13/12/2024"

presidente = "Simone Calderara"
componente = "Antonio Piccinno"
segretario = "Giovanna Varni"

candidati = []

c = Candidato("Maurizio", "Mancini", "m", "6", "5", "1974", "Roma", 35)
c.assignTitle("una tesi veramente figa")
candidati.append(c)
c = Candidato("Flavia", "Onofri", "f", "17", "11", "1954", "Roma", 36)
c.assignTitle("una tesi ancora meglio")
candidati.append(c)

result = effify(template)

for candidateN, c in enumerate(candidati):

    name = c.nome
    surname = c.cognome
    title = c.title
    candidate = effify(attachmentN)
    result += candidate

    birthdate = c.data_nascita
    birthplace = c.comune_nascita
    cycle = c.ciclo
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
res = subprocess.call(f"pandoc {header} -V geometry:margin=0.75in -V papersize:a4 --variable=fontfamily:arev -i output/output.md -o output/output.pdf", shell=True)
