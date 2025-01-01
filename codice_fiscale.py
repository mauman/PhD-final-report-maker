###################################################
##                                               ##
## codice_fiscale.py - Leosxe (Pasquale Scalise) ##
##                                               ##
###################################################

from string import digits

def get_CF(nome, cognome, sesso, giorno, mese, anno, comune):
    nome = nome.upper()
    cognome = cognome.upper()
    sesso = sesso.upper()
    comune = comune.title()

    voc=["A","E","I","O","U"]
    cog=[]
    nom=[]
    ann=[]
    par=[]
    dis=[]
    var1=0
    var2=0
    ctrl=0



    ################################
            ##COGNOME##

    for i in cognome:           #servono solo le prime tre consonanti
        if var1==3:
            break
        if i not in voc:        #passano solo le consonanti
            cog.append(i)
            var1+=1             #per far fluire il ciclo for

    if len(cog)<3:              #cognomi con troppe poche consonanti
        for i in cognome:
            if i in voc:
                cog.append(i)

    while len(cog)>3:           #nomi con troppe consonanti o troppe vocali
        del cog[-1]

    if len(cog)==1:             #una vocale
        cog.append("X")
        cog.append("X")
    elif len(cog)==2:           #due vocali
        cog.append("X")


    cog="".join(cog)

    ################################


    ################################
            ##NOME##

    for i in nome:
        if i not in voc:        #passano solo le consonanti
            nom.append(i)

    if len(nom)>3:              #nomi con 4 consonanti finiscono qui (ex.Pasquale)
        del nom[1]

    if len(nom)<3:              #nomi con troppe poche consonanti (ex.Luca)
        for i in nome:
            if i in voc:
                nom.append(i)

    while len(nom)>3:           #nomi con troppe consonanti o troppe vocali
        del nom[-1]

    if len(nom)==1:             #una sola lettera
        nom.append("X")
        nom.append("X")

    if len(nom)==2:             #due lettere
        nom.append("X")

    nom="".join(nom)

    ################################


    ################################
            ##GIORNO E SESSO##

    if len(giorno)==1:          #Ex. trasforma i "4" in "04"
        giorno="0"+giorno

    if sesso=="F":
        grn=int(giorno)
        giorno=str(grn+40)

    ################################


    ################################
            ##MESE##

    mdic={"01":"A","02":"B","03":"C","04":"D","05":"E","06":"H","07":"L","08":"M","09":"P","10":"R","11":"S","12":"T"}

    if len(mese)==1:            #Ex. trasforma i "4" in "04"
        mese="0"+mese

    mse=mdic[mese]

    ################################


    ################################
            ##ANNO##

    for i in anno:              #mette tutte le cifre in una lista, numero per numero
        ann.append(i)

    if len(ann)==4:             #Ex. trasforma i "1978" in "78"
        del ann[1]
        del ann[0]

    ann0="".join(ann)

    ################################


    ################################
            ##COMUNE##

    db=open("listacomuni.txt", encoding = "ISO-8859-1")

    lines=(db.read()).split('\n')   #divide il database in linee

    for l in lines[1:]:             #esclude la prima riga
        valori=l.split(';')         #divide i valori con ;
        if comune==valori[1]:
            c0mune=valori[6]        #assegna il Codice Catastale
            break

    db.close()

    ################################

    cfo=cog+nom+ann0+mse+giorno+c0mune  #codice fin ora

    ################################
            ##CONTROLLO PT.1##

    dpar={"A":"0","B":"1","C":"2","D":"3","E":"4","F":"5","G":"6","H":"7","I":"8","J":"9","K":"10","L":"11","M":"12","N":"13","O":"14","P":"15","Q":"16","R":"17","S":"18","T":"19","U":"20","V":"21","W":"22","X":"23","Y":"24","Z":"25"}

    ddis={"0":"1","1":"0","2":"5","3":"7","4":"9","5":"13","6":"15","7":"17","8":"19","9":"21","A":"1","B":"0","C":"5","D":"7","E":"9","F":"13","G":"15","H":"17","I":"19","J":"21","K":"2","L":"4","M":"18","N":"20","O":"11","P":"3","Q":"6","R":"8","S":"12","T":"14","U":"16","V":"10","W":"22","X":"25","Y":"24","Z":"23"}

    for i in cfo:               #si inizia con i dispari perché nel codice originario iniziano a contare da 1
        if var2%2==0:
            dis.append(i)
        else:
            par.append(i)
        var2+=1                    #per far fluire il ciclo for

    for i in par:               #numeri pari
        if i not in digits:
            ctrpar=dpar[i]
            ctrl+=int(ctrpar)
        elif i in digits:
            ctrl+=int(i)

    for i in dis:               #numeri dispari
        ctrdis=ddis[i]
        ctrl+=int(ctrdis)

    ################################


    ################################
            ##CONTROLLO PT.2##

    dicf={"0":"A","1":"B","2":"C","3":"D","4":"E","5":"F","6":"G","7":"H","8":"I","9":"J","10":"K","11":"L","12":"M","13":"N","14":"O","15":"P","16":"Q","17":"R","18":"S","19":"T","20":"U","21":"V","22":"W","23":"X","24":"Y","25":"Z"}

    fin=ctrl%26
    deff=dicf[str(fin)]

    ################################


    cf=cfo+deff
    return cf
