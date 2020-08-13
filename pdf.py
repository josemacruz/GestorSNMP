################################
#Fichero: pdf.py
#Descripción: Fichero que nos permite crear
#             el pdf con la información.
################################

# Librerias utilizadas
import itertools
from reportlab.lib.styles import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import funciones
from funciones import *
from fpdf import FPDF 

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

################################
#Función: crearinformacion
#Descripción: Crea pdf con la informaciónSNMP.             
#Parámetros: No tiene.                        
################################
def crearinformacion():

    # Valores del grupo system
    sysDescr = funciones.get('localhost',['1.3.6.1.2.1.1.1.0'],hlapi.CommunityData('public'))
    sysObjectID = funciones.get('localhost',['1.3.6.1.2.1.1.2.0'],hlapi.CommunityData('public'))
    sysUpTime = funciones.get('localhost',['1.3.6.1.2.1.1.3.0'],hlapi.CommunityData('public'))
    sysContact = funciones.get('localhost',['1.3.6.1.2.1.1.4.0'],hlapi.CommunityData('public'))
    sysName = funciones.get('localhost',['1.3.6.1.2.1.1.5.0'],hlapi.CommunityData('public'))
    sysLocation = funciones.get('localhost',['1.3.6.1.2.1.1.6.0'],hlapi.CommunityData('public'))
    sysServices = funciones.get('localhost',['1.3.6.1.2.1.1.7.0'],hlapi.CommunityData('public'))
    timeticks = sysUpTime['1.3.6.1.2.1.1.3.0']

    sysDescr = sysDescr['1.3.6.1.2.1.1.1.0']
    sysObjectID = sysObjectID['1.3.6.1.2.1.1.2.0']
    sysContact = sysContact['1.3.6.1.2.1.1.4.0']
    sysName = sysName['1.3.6.1.2.1.1.5.0']
    sysLocation = sysLocation['1.3.6.1.2.1.1.6.0']
    sysServices = sysServices['1.3.6.1.2.1.1.7.0']
    
    textLines = [
    f'•sysDescr.0 = {sysDescr:.63}',
    f'•sysObjectID.0 = {sysObjectID}',
    f'•sysUpTime.0 = timeticks({timeticks})',
    f'•sysContact.0 = {sysContact}',
    f'•sysName.0 = {sysName}',
    f'•sysLocation.0 = {sysLocation}'
    ]
    
    # Valores de la tabla de ruta
    Ip = []
    Mask = []
    Metric = []
    Gateway = []
    # Tabla de ruta
    valor_1,valor_2,valor_3,x = funciones.siguiente('1.3.6.1.2.1.4.21.1',13)
    for i in range(x):
        Ip.append(valor_2[i])
        Mask.append(valor_2[i+10*x])
        Metric.append(valor_2[i+2*x])
        Gateway.append(valor_2[i+6*x])

    data = [("IP", "MASK", "METRIC", "GATEWAY")]
    for i in range(x):
        ip = Ip[i]
        mask = Mask[i]
        metric = Metric[i]
        gateway = Gateway[i]
        data.append((ip, mask, metric, gateway))

    # Valores tabla de interfaces
    Descrip = []
    Type = []
    Speed = []
    PhyAdd = []
    valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.2.2',22)
    for i in range(x):
        if valor_2[i+2*x] == '6':
               valor_2[i+2*x] = "ethernetCsmacd"
        if valor_2[i+2*x] == '24':
               valor_2[i+2*x] = "softwareLoopback"
        Descrip.append(valor_3[i+1*x])
        Type.append(valor_2[i+2*x])
        Speed.append(valor_2[i+4*x])
        PhyAdd.append(valor_2[i+5*x])
    
    data_1 = [("DESCRIPTION", "TYPE", "SPEED", "PHYSICAL ADDR.")]
    for i in range(x):
        descrip_1 = Descrip[i]
        descrip = descrip_1[:31]
        typ = Type[i]
        speed = Speed[i]
        phyadd = PhyAdd[i]
        data_1.append((descrip, typ, speed, phyadd))
        
    # Valores de tabla tcp
    LocalAddr_1 = []
    LocalPort = []
    DestiAdd_1 = []
    DestiPort = []
    Status = []
    valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.6.13',5)
    for i in range(x):
        if valor_3[i] == '1':
               valor_3[i] = "closed"
        if valor_3[i] == '2':
               valor_3[i] = "listen"
        if valor_3[i] == '5':
               valor_3[i] = "established"
        if valor_3[i] == '11':
               valor_3[i] = "timeWait"
        LocalAddr_1.append(valor_2[i+1*x])
        LocalPort.append(valor_2[i+2*x])
        DestiAdd_1.append(valor_2[i+3*x])
        DestiPort.append(valor_2[i+4*x])
        Status.append(valor_3[i])

    data_2 = [("LOCAL ADDR.", "LOCAL PORT", "DESTINATION ADDR.", "DESTINATION PORT", "STATUS")]
    for i in range(x):
        localaddr_1 = LocalAddr_1[i]
        localport = LocalPort[i]
        destiaddr_1 = DestiAdd_1[i]
        destiport = DestiPort[i]
        status = Status[i]
        data_2.append((localaddr_1, localport, destiaddr_1, destiport, status))
        
    # Valores de tabla udp
    LocalAddr_2 = []
    DestiAdd_2 = []
    valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.7.5',2)
    for i in range(x):
        LocalAddr_2.append(valor_2[i])
        DestiAdd_2.append(valor_2[i+1*x])

    data_3 = [("LOCAL ADDR.", "LOCAL PORT")]
    for i in range(x):
        localaddr_2= LocalAddr_2[i]
        destiaddr_2 = DestiAdd_2[i]
        data_3.append((localaddr_2, destiaddr_2))

     # Valores de tabla de dispositivos
    Device = []
    Status = []
    valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.25.3.2',6)
    for i in range(x):
        if valor_3[i+4*x] == '1':
               valor_3[i+4*x] = "unknown"
        if valor_3[i+4*x] == '2':
               valor_3[i+4*x] = "running"
        if valor_3[i+4*x] == '3':
               valor_3[i+4*x] = "warning"
        if valor_3[i+4*x] == '4':
               valor_3[i+4*x] = "testing"
        if valor_3[i+4*x] == '5':
               valor_3[i+4*x] = "down"
        Device.append(valor_3[i+2*x])
        Status.append(valor_3[i+4*x])

    data_4 = [("DEVICE", "STATUS")]
    for i in range(x):
        device= Device[i]
        status = Status[i]
        data_4.append((device, status))
        
    ############################### Comienza la creacion del fichero
    fileName = 'infoSNMP.pdf'
    documentTitle = 'infoSNMP'
    title = 'Información monitorizada mediante SNMP'
    subTitle_1 = 'Grupo system:'
    subTitle_2 = 'Tabla de ruta:'
    subTitle_3 = 'Tabla de interfaces:'
    subTitle_4 = 'Tabla de conexiones TCP:'
    subTitle_5 = 'Tabla de escucha UDP:'
    subTitle_6 = 'Tabla de dispositivos:'
    
    c = canvas.Canvas(fileName, pagesize=A4)
    c.setTitle(documentTitle)
    w, h = A4

    max_rows_per_page = 45
  

     # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics


    c.setFont('Courier-Bold', 16)
    c.drawCentredString(300, 770, title)


    # ###################################
    # 2) Dibujar línea
    c.line(30, 750, 550, 750)

    # ###################################
    # 3) Sub Title_1 : Gestion de sistema
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(90,700, subTitle_1)
    
    text = c.beginText(50, 680)
    text.setFont("Courier", 11)
    for line in textLines:
       text.textLine(line)
    c.drawText(text)
    
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(100,580, subTitle_2)
    
    # Creamos tabla de ruta
    # Margin.
    x_offset = 50 # Posición x en el pdf
    y_offset = 280 # Posición y en el pdf
    # Space between rows.
    padding = 15

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 120, 240, 300, 420]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    #c.save()

    # Creamos tabla de interfaces
    # Margin.
    x_offset = 30 # Posición x en el pdf
    y_offset = 80 # Posición y en el pdf
    # Space between rows.
    padding = 15

    c.setFont("Courier-Bold", 12)
    c.drawCentredString(100,780, subTitle_3)

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 230, 350, 430, 540]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in grouper(data_1, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    

    # Creamos tabla de conexiones tcp
    
    # Margin.
    x_offset = 30 # Posición x en el pdf
    y_offset = 80 # Posición y en el pdf
    # Space between rows.
    padding = 15

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 120, 200, 340, 460, 550]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(100,780, subTitle_4)

    for rows in grouper(data_2, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    

    # Creamos tabla udp
    
    # Margin.
    x_offset = 50 # Posición x en el pdf
    y_offset = 80 # Posición y en el pdf
    # Space between rows.
    padding = 15

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 120,260]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(100,780, subTitle_5)
    
    for rows in grouper(data_3, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()

     # Creamos tabla device
    
    # Margin.
    x_offset = 30 # Posición x en el pdf
    y_offset = 80 # Posición y en el pdf
    # Space between rows.
    padding = 15

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 470, 540]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(100,780, subTitle_6)
    
    for rows in grouper(data_4, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    
    c.save()
    
################################
#Función: crearprocesos
#Descripción: Crea pdf con la información de los procesos.             
#Parámetros: No tiene.                        
################################
def crearprocesos():
    # Valores de la tabla de procesos
    PID = []
    ProcessName = []
    Type = []
    State = []
    # Tabla de procesos
    valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.25.4.2',7)
    for i in range(x):
        if valor_2[i+5*x] == '1':
               valor_2[i+5*x] = "unknown"
        if valor_2[i+5*x] == '2':
               valor_2[i+5*x] = "operatingSystem"
        if valor_2[i+5*x] == '3':
               valor_2[i+5*x] = "deviceDriver"
        if valor_2[i+5*x] == '4':
               valor_2[i+5*x] = "Application"
        if valor_2[i+6*x] == '1':
               valor_2[i+6*x] = "Running"
        if valor_2[i+6*x] == '2':
               valor_2[i+6*x] = "Runnable"
        if valor_2[i+6*x] == '3':
               valor_2[i+6*x] = "NotRunnable"
        if valor_2[i+6*x] == '4':
               valor_2[i+6*x] = "Invalid"
        PID.append(valor_2[i])
        ProcessName.append(valor_2[i+x])
        Type.append(valor_2[i+5*x])
        State.append(valor_2[i+6*x])

    data = [("PID", "PROCESS NAME", "TYPE", "STATE")]
    for i in range(x):
        pid = PID[i]
        processname_1 = ProcessName[i]
        processname = processname_1[:31]
        tipo = Type[i]
        state = State[i]
        data.append((pid, processname, tipo, state))

    
        
    ############################### Comienza la creacion del fichero
    fileName = 'infoProcesos.pdf'
    documentTitle = 'infoProcesos'
    title = 'Información sobre procesos activos'
    
    
    
    c = canvas.Canvas(fileName, pagesize=A4)
    c.setTitle(documentTitle)
    w, h = A4

    max_rows_per_page = 40
  

     # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics


    c.setFont('Courier-Bold', 16)
    c.drawCentredString(300, 770, title)


    # ###################################
    # 2) Dibuja línea
    c.line(30, 750, 550, 750)

    # ###################################
    # 3) Sub Title_1 : Tabla de procesos actuales
    # RGB - Red Green and Blue
    c.setFont("Helvetica", 12)
    
    
    # Creamos tabla de procesos
    # Margin.
    x_offset = 70 # Posición x en el pdf
    y_offset = 120 # Posición y en el pdf
    # Space between rows.
    padding = 15

    #xlist es la posicion de cada columna de la tabla
    xlist = [x + x_offset for x in [0, 70, 270, 360, 420]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
   
    c.save()

  ################################
#Función: convierte
#Descripción: Convierte logUsers.txt en un pdf para enviarlo por correo.             
#Parámetros: No tiene.                        
################################
def convierte(): 
    # save FPDF() class into  
    # a variable pdf 
    pdf = FPDF()    
       
    # Add a page 
    pdf.add_page() 
       
    # set style and size of font  
    # that you want in the pdf 
    pdf.set_font("Arial", size = 12) 
      
    # open the text file in read mode 
    f = open("log.txt", "r") 
      
    # insert the texts in pdf 
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 1, align = 'L') 
       
    # save the pdf with name .pdf 
    pdf.output("LogUsers.pdf")


