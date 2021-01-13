from tkinter import *
from tkinter import ttk
import numpy as np
import pyaudio 
import wave
import matplotlib.pyplot as plt
import winsound
import time
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from scipy.io import wavfile
from scipy import signal
  
def Iniciar():
    plt.close('all')
    p1 = np.loadtxt('patp1.csv')
    p2 = np.loadtxt('patp2.csv')
    p3 = np.loadtxt('patp3.csv')
    p4 = np.loadtxt('patp4.csv')
    p5 = np.loadtxt('patp5.csv')
    p6 = np.loadtxt('patp6.csv')
    p7 = np.loadtxt('patp7.csv')
    p8 = np.loadtxt('patp8.csv')
    p9 = np.loadtxt('patp9.csv')
    p10 = np.loadtxt('patp10.csv')
    
    r1 = np.loadtxt('patr1.csv')
    r2 = np.loadtxt('patr2.csv')
    r3 = np.loadtxt('patr3.csv')
    r4 = np.loadtxt('patr4.csv')
    r5 = np.loadtxt('patr5.csv')
    r6 = np.loadtxt('patr6.csv')
    r7 = np.loadtxt('patr7.csv')
    r8 = np.loadtxt('patr8.csv')
    r9 = np.loadtxt('patr9.csv')
    r10 = np.loadtxt('patr10.csv')
    
    Dicccionario_ABC_Morse={"A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.",
                            "G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..",
                            "M":"--","N":"-.","O":"---","P":".--.","Q":"--.-","R":".-.",
                            "S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-",
                            "Y":"-.--","Z":"--..","0":"-----","1":".----","2":"..---",
                            "3":"...--","4":"....-","5":".....","6":"-....","7":"--...",
                            "8":"---..","9":"----.",",":"..-..",".":".-.-.-","?":"..--..",
                            ";":"-.-.-",":":"---...","/":"-..-.","+":".-.-.","-":"-....-",
                            "=":"-...-"," ":" ","   ":"   "}
    
    Dicccionario_Morse_ABC={".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E","..-.":"F",
                            "--.":"G","....":"H","..":"I",".---":"J","-.-":"K",".-..":"L",
                            "--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R",
                            "...":"S","-":"T","..-":"U","...-":"V",".--":"W","-..-":"X",
                            "-.--":"Y","--..":"Z","-----":"0",".----":"1","..---":"2",
                            "...--":"3","....-":"4",".....":"5","-....":"6","--...":"7",
                            "---..":"8","----.":"9","..-..":",",".-.-.-":".","..--..":"?",
                            "-.-.-":";","---...":":","-..-.":"/",".-.-.":"+","-....-":"-",
                            "-...-":"="," ":" ","   ":"   "}
    
    def Morse(senal):
        patron = np.copy(senal) 
        #En dec se almacena el resultado de la prueba de correlacion de la entrada actual
        #con cada patron previamente establecido
        decdp = np.zeros(10)
        decdp[0] = fastdtw(patron, p1, dist=euclidean)[0]
        decdp[1] = fastdtw(patron, p2, dist=euclidean)[0]
        decdp[2] = fastdtw(patron, p3, dist=euclidean)[0]
        decdp[3] = fastdtw(patron, p4, dist=euclidean)[0]
        decdp[4] = fastdtw(patron, p5, dist=euclidean)[0]
        decdp[5] = fastdtw(patron, p6, dist=euclidean)[0]
        decdp[6] = fastdtw(patron, p7, dist=euclidean)[0]
        decdp[7] = fastdtw(patron, p8, dist=euclidean)[0]
        decdp[8] = fastdtw(patron, p9, dist=euclidean)[0]
        decdp[9] = fastdtw(patron, p10, dist=euclidean)[0]
        
        decdr = np.zeros(10)
        decdr[0] = fastdtw(patron, r1, dist=euclidean)[0]
        decdr[1] = fastdtw(patron, r2, dist=euclidean)[0]
        decdr[2] = fastdtw(patron, r3, dist=euclidean)[0]
        decdr[3] = fastdtw(patron, r4, dist=euclidean)[0]
        decdr[4] = fastdtw(patron, r5, dist=euclidean)[0]
        decdr[5] = fastdtw(patron, r6, dist=euclidean)[0]
        decdr[6] = fastdtw(patron, r7, dist=euclidean)[0]
        decdr[7] = fastdtw(patron, r8, dist=euclidean)[0]
        decdr[8] = fastdtw(patron, r9, dist=euclidean)[0]
        decdr[9] = fastdtw(patron, r10, dist=euclidean)[0]
    
        k = 7 #Numero de vecinos
        
        pos=[]
        dc=[]
        posKnn=[]
        Uno=[]
        Dos=[]
        
        dc = np.concatenate((decdp,decdr), axis=None) #Vector con todas las distancias
        pos=np.argpartition(dc,k+1) #Acomodamos los argumentos de menor a mayor
        posKnn=np.array([[pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6]]]) #Debido a que k = 7, obtenemos los 7 mas cercanos
        #Declaramos vectores booleanos de acuerdo con la posicion de los 7 argumentos mas cercanos
        Uno=posKnn<=9 # Clase punto
        Dos=(posKnn>9)&(posKnn<=19) # Clase raya
        #Establecemos el mayor numero de repeticiones de una clase para clasificar
        nv = 0
        for i in range(k):
            if Uno[0,i] == True:
                nv += 1
        
        if nv >= 4:
            letra = '.'
        else:
            letra = '-'
            
        return letra
    
    def MorseATexto(frase):
        mensaje=""
        letra=""
        n=0
        for sonido in frase:
            if sonido==" ":
                if n==1:
                    letra=" "
                mensaje+=Dicccionario_Morse_ABC[letra]
                letra=""
                n=1
            else:
                n=0
                letra+=sonido
        mensaje+=Dicccionario_Morse_ABC[letra]
        
        return mensaje
    
    #<====================== Reproducción Grabación =============================>
    fs = 8000 #Frecuencia de muestreo
    archivo=cuadrotiempo.get() #Nombre del archivo
    m1, sonido = wavfile.read(archivo)
    
    # Reproducir audio
    winsound.PlaySound(archivo, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    #<====================== Procesamiento de la señal ==========================>
    asf = np.hstack(sonido) #Junta los stacks de sonido en una sola variable
    #Filtro Pasa banda
    freq1 = 2 * 800 / fs
    freq2 = 2 * 1200 / fs
    b, c = signal.butter(4, [freq1, freq2], 'bandpass')
    a = signal.lfilter(b, c, asf)
    plt.figure()
    plt.plot(asf)
    plt.title('Señal de audio original')
    # plt.figure()
    # plt.plot(a)
    aa = a[2000:]
    # plt.figure(1)
    # plt.title('Señal de audio grabada')
    # plt.plot(aa)
    
    aa_norm = aa / np.max(np.abs(aa)) #Señal normalizada
    plt.figure(2)
    plt.plot(aa_norm)
    plt.title('Señal de audio filtrada y normalizada')
    
    # aa_norm = np.loadtxt('seppal.csv')
    # plt.figure(2)
    # plt.plot(aa_norm)
    # plt.title('Señal de audio normalizada')
    
    #Quitar las partes muertas
    bin1 = np.where(np.abs(aa_norm) >= 0.1, aa_norm, 0)
    plt.figure(3)
    plt.plot(bin1)  
    plt.title('Señal de audio sin partes muertas')
    plt.show()
    
    
    inicio = 0
    contesp = 0
    senal = []
    letra = ''
    palabra = ''
    
    for el in bin1:
        
        if el != 0:
            
            if contesp != 0 and contesp > 3000 and contesp < 10000:
                """SIMBOLO"""
                letra += Morse(senal)
                
                print('simbolo')
                contesp = 0
                senal = []
                senal.append(el)
                
            
            elif contesp != 0 and contesp > 10000 and contesp < 18000:
                """LETRA"""
                letra += Morse(senal)
                """traduccion de la letra"""
                palabra += MorseATexto(letra)
                
                print('letra')
                letra = ''
                contesp = 0
                senal = []
                senal.append(el)
            
            elif contesp != 0 and contesp > 18000:
                """PALABRA"""
                letra += Morse(senal)
                """traduccion de la letra"""
                palabra += MorseATexto(letra)
                palabra += ' '
                
                print('palabra')
                letra = ''
                contesp = 0
                senal = []
                senal.append(el)
            
            inicio = 1
            senal.append(el)
        
        elif el == 0 and inicio == 1:
            contesp += 1
    
    letra += Morse(senal)
    if contesp > 32000:
        print('simbolo')
    palabra += MorseATexto(letra)
    
    print()
    print(palabra)
    txtrespuesta.config(text=palabra)

#.....INTERFAZ CON TKINTER.....   
raiz=Tk()
raiz.title("Codigo Morse")
raiz.resizable(0,0)
raiz.iconbitmap("sos.ico")  
raiz.config(bg="blue")

#FRAME DEL TITULO 
frameT=Frame(raiz,width="400",height="80")
frameT.pack()
frameT.config(bg="blue")

#FRAME DE LA IMAGEN 
frameM=Frame(raiz,width="700",height="500")
frameM.pack(side="left")
frameM.config(bg="blue")

#FRAME DE LA BUSQUEDA 
frameS=Frame(raiz,width="500",height="600")
frameS.pack(side="right", anchor="n")
frameS.config(bg="blue")

###########################################################
#IMAGEN DEL CODIGO MORSE
imagenM=PhotoImage(file="Tabla_Morse.png")
labelM=Label(frameM,image=imagenM)
labelM.place(x=20,y=1)

# TEXTO DEL TITULO 
labelT=Label(frameT,text="CODIGO MORSE",font=("Arial Narrow",25))
labelT.place(x=80,y=25)
labelT.config(bg="blue")

# TEXTO DE RESPUESTA 
labelA=Label(frameS,text="Danos tu mensaje",font=("Arial Narrow",15))
labelA.place(x=150,y=20)
labelA.config(bg="blue")

#------------Cuadro de tiempo---------
cuadrotiempo=ttk.Combobox(frameS)#,state="readonly")
cuadrotiempo["values"]=['StarWarsRifa.wav','HolaKevin.wav','Python37.wav','Patrones.wav','Hola.wav','Adios.wav']
cuadrotiempo.place(x=130,y=166)

labeltiempo=Label(frameS,text="Seleccione el archivo:",font=("Arial Narrow",12))
labeltiempo.place(x=45,y=140)
labeltiempo.config(bg="blue")


#----------------- TEXTO DE RESPUESTA--------------------------
labelA=Label(frameS,text="El mensaje dice:",font=("Arial Narrow",10))
labelA.place(x=50,y=200)
labelA.config(bg="blue")

texto=StringVar()
txtrespuesta=Label(frameS,text="                                     ")#,state=DISABLED)
txtrespuesta.place(x=50,y=245)
txtrespuesta.config(bg="white")
# respuesta=Label(frameS, text="")
# respuesta.place(x=60,y=245)
# respuesta.pack()

#------------------ BOTON-------------------------------------
Bbuscar=Button(frameS,text="INICIAR", command=Iniciar)
Bbuscar.pack()
# Bbuscar=Button(frameS,text="GRABAR",command=boton_leer)
Bbuscar.place(x=200,y=95)
Bbuscar.config(bg="white")


raiz.mainloop()