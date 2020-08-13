import itertools
from random import randint
from statistics import mean
from reportlab.lib.styles import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import funciones
from funciones import *

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def crear():

   
    
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
        processname = ProcessName[i]
        tipe = Type[i]
        state = State[i]
        data.append((pid, processname, tipe, state))

    
        
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
    # 2) Draw a line
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
    xlist = [x + x_offset for x in [0, 70, 260, 360, 420]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
   
    c.save()
