################################
#Fichero: bot_telegram.py
#Descripción: Tiene todas las funciones para que el bot
#             se ejecute de manera correcta
################################

# Librerias utilizadas
from telegram import *
from telegram.ext import *
import time
import funciones
from funciones import *
import pdf
import correo
import threading

TOKEN = 'TOKEN'

# Usuarios autorizados para tener acceso al bot
usuarios_permitidos = [CODIGOUSUARIO1, CODIGOUSUARIO2]

# Manejadores de comandos

################################
#Función: start
#Descripción: Inicia el bot y autoriza al usuario (Registrandolo en el fichero logUsers)             
#Parámetros: update, context                           
################################
def start(update, context): 
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('Bienvenido al bot de Gestión de Redes de Telecomunicación {} donde monitorizamos la MIB-2 y HOST-RESOURCES-MIB. Usando /ayuda para ver los comandos disponibles.'.format(user['username']))
        log = open('log.txt','a')
        mensaje = user['username']+' se ha conectado al bot: '+time.strftime('%c')+'\n'
        log.write(mensaje)
        log.read()
        log.close()
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha conectado al bot: '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: ayuda
#Descripción: Muestra la lista de comandos disponibles             
#Parámetros: update, context                           
################################
def ayuda(update, context):
    update.message.reply_text('Lista de comandos implementados: \n\n'
                              +'/start - Comando de inicio\n'
                              +'/ayuda - Consulta la lista de comandos implementados y la descripcion de estos\n'
                              +'/system - Muesta los valores del grupo system\n'
                              +'/routetable - Muestra la tabla de ruta (Ipdest, máscara, métrica y puerta de enlace)\n'
                              +'/modsystem - Para modificar valores del grupo system\n'
                              +'/interfacetable - Muestra la tabla de interfaces (Dirección, tipo, velocidad, dirección física)\n'
                              +'/tcptable - Muestra la tabla de conexiones TCP (Dirección origen, puerto origen, direccion destino, puerto destino)\n'
                              +'/udptable - Muestra la tabla de escucha UDP (Dirección local, puerto local)\n'
                              +'/devicetable - Muestra la tabla de dispoitivos que contiene el host (Device, status)\n'
                              +'/swrun - Informacion sobre los procesos de software que se ejecutan en el sistema (Proceso, tipo, estado)\n'
                              +'/generapdf - Genera un pdf con los datos y se envia por email, junto con el log de los usuarios\n')

################################
#Función: system
#Descripción: Muestra las variables monitorizadas del grupo system (MIB-2)           
#Parámetros: update, context                           
################################
def system(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        sysDescr = funciones.get('localhost',['1.3.6.1.2.1.1.1.0'],hlapi.CommunityData('public'))
        sysObjectID = funciones.get('localhost',['1.3.6.1.2.1.1.2.0'],hlapi.CommunityData('public'))
        sysUpTime = funciones.get('localhost',['1.3.6.1.2.1.1.3.0'],hlapi.CommunityData('public'))
        sysContact = funciones.get('localhost',['1.3.6.1.2.1.1.4.0'],hlapi.CommunityData('public'))
        sysName = funciones.get('localhost',['1.3.6.1.2.1.1.5.0'],hlapi.CommunityData('public'))
        sysLocation = funciones.get('localhost',['1.3.6.1.2.1.1.6.0'],hlapi.CommunityData('public'))
        sysServices = funciones.get('localhost',['1.3.6.1.2.1.1.7.0'],hlapi.CommunityData('public'))
        timeticks = sysUpTime['1.3.6.1.2.1.1.3.0']
    
        update.message.reply_text('*Grupo System*',"Markdown")
        update.message.reply_text('•*sysDescr.0 *= '+sysDescr['1.3.6.1.2.1.1.1.0'],parse_mode = "Markdown")
        update.message.reply_text('•*sysObjectID.0 *= '+sysObjectID['1.3.6.1.2.1.1.2.0'],parse_mode = "Markdown")
        update.message.reply_text('•*sysUpTime.0 *= Timeticks: ('+str(timeticks)+')',parse_mode = "Markdown")
        update.message.reply_text('•*sysContact.0 *= '+sysContact['1.3.6.1.2.1.1.4.0'],parse_mode = "Markdown")
        update.message.reply_text('•*sysName.0 *= '+sysName['1.3.6.1.2.1.1.5.0'],parse_mode = "Markdown")
        update.message.reply_text('•*sysLocation.0 *= '+sysLocation['1.3.6.1.2.1.1.6.0'],parse_mode = "Markdown")
        update.message.reply_text('•*sysServicios.0 *= '+sysServices['1.3.6.1.2.1.1.7.0'],parse_mode = "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /system sin permisos : '+time.strftime('%c')+'\n') 
        log.close()

################################
#Función: modsystem
#Descripción: Muestras las variables modificables del grupo system (MIB-2)           
#Parámetros: update, context                           
################################
def modsystem(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('Lista de comandos para modificar el grupo system: \n\n'
                                  +'/syscontact - Modificar contacto del sistema\n'
                                  +'/sysname - Modificar nombre del sistema\n'
                                  +'/syslocation - Modifica localización del sistema')
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /modsystem sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: syscontact
#Descripción: Modifica la variable syscontact del grupo system (MIB-2)          
#Parámetros: update, context                           
################################
def syscontact(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        valor_mod = str(context.args[0])
        valor = set('localhost',{'1.3.6.1.2.1.1.4.0':valor_mod})
        update.message.reply_text('Nuevo valor de *sysContact*: '+valor['1.3.6.1.2.1.1.4.0'],"Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /syscontact sin permisos : '+time.strftime('%c')+'\n')
        log.close()
        
################################
#Función: sysname
#Descripción: Modifica la variable sysname del grupo system (MIB-2)          
#Parámetros: update, context                           
################################        
def sysname(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        valor_mod = str(context.args[0])
        valor = set('localhost',{'1.3.6.1.2.1.1.5.0':valor_mod})
        update.message.reply_text('Nuevo valor de *sysName*: '+valor['1.3.6.1.2.1.1.5.0'],"Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /sysname sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: syslocation
#Descripción: Modifica la variable syslocation del grupo system (MIB-2)          
#Parámetros: update, context                           
################################
def syslocation(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        valor_mod = str(context.args[0])
        valor = set('localhost',{'1.3.6.1.2.1.1.6.0':valor_mod})
        update.message.reply_text('Nuevo valor de *sysLocation*: '+valor['1.3.6.1.2.1.1.6.0'],"Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /syslocation sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: routetable
#Descripción: Muestra la tabla de ruta (MIB-2)          
#Parámetros: update, context                           
################################
def routetable(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la tabla de ruta:*', "Markdown")
        valor_1,valor_2,valor_3,x = funciones.siguiente('1.3.6.1.2.1.4.21.1',13)
        for i in range(x):
            update.message.reply_text('*Ip* = {0}\n*Mask* = {1}\n*Metric* = {2}\n*Gateway* = {3}'.format(valor_2[i],valor_2[i+10*x],valor_2[i+2*x],valor_2[i+6*x]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /routetable sin permisos : '+time.strftime('%c')+'\n')
        log.close()
        
################################
#Función: devicetable
#Descripción: Muestra la tabla de dispositivos (MIB-2)        
#Parámetros: update, context                           
################################
def devicetable(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la tabla de dispositivos:*', "Markdown")
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
            update.message.reply_text('*Device* = {0}\n*Status* = {1}'.format(valor_3[i+2*x],valor_3[i+4*x]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /devicetable sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: interfacetable
#Descripción: Muestra la tabla de interfaces (MIB-2)        
#Parámetros: update, context                           
################################
def interfacetable(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la tabla de interfaces:*', "Markdown")
        valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.2.2',22)
      
        for i in range(x):
            if valor_2[i+2*x] == '6':
               valor_2[i+2*x] = "ethernetCsmacd"
            if valor_2[i+2*x] == '24':
               valor_2[i+2*x] = "softwareLoopback"
            update.message.reply_text('*Description* = {0}\n*Type* = {1}\n*Speed* = {2}\n*Physical Addr.* = {3}'.format(valor_3[i+1*x],valor_2[i+2*x],valor_2[i+4*x],valor_2[i+5*x]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /interfacetable sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: tcptable
#Descripción: Muestra la tabla de conexiones TCP (MIB-2)        
#Parámetros: update, context                           
################################            
def tcptable(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la tabla de conexiones TCP:*', "Markdown")
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
            update.message.reply_text('*Local Addr.* = {0}\n*Local Port* = {1}\n*Destination Addr.* = {2}\n*Destination Port* = {3}\n*State* = {4}'.format(valor_2[i+1*x],valor_2[i+2*x],valor_2[i+3*x],valor_2[i+4*x],valor_3[i]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /tcptable sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: tcptable
#Descripción: Muestra la tabla de escucha UDP (MIB-2)        
#Parámetros: update, context                           
################################  
def udptable(update, context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la tabla de escucha UDP:*', "Markdown")
        valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.7.5',2)
        for i in range(x):
            update.message.reply_text('*Local Addr.* = {0}\n*Local Port* = {1}'.format(valor_2[i],valor_2[i+1*x]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /udptable sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: swrun
#Descripción: Muestra la tabla de los procesos software que se ejecutan en el sistema (HOST-RESOURCES-MIB)        
#Parámetros: update, context                           
################################ 
def swrun(update,context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        update.message.reply_text('*Se muestra la lista de procesos en ejecución:*', "Markdown")
        valor_1,valor_2,valor_3,x = funciones.siguiente('.1.3.6.1.2.1.25.4.2',7)
        for i in range(x):
            
            if valor_2[i+5*x] == '1':
               valor_2[i+5*x] = "unknown"
            elif valor_2[i+5*x] == '2':
               valor_2[i+5*x] = "operatingSystem"
            elif valor_2[i+5*x] == '3':
               valor_2[i+5*x] = "deviceDriver"
            elif valor_2[i+5*x] == '4':
               valor_2[i+5*x] = "Application"
               
            if valor_2[i+6*x] == '1':
               valor_2[i+6*x] = "Running"
            elif valor_2[i+6*x] == '2':
               valor_2[i+6*x] = "Runnable"
            elif valor_2[i+6*x] == '3':
               valor_2[i+6*x] = "NotRunnable"
            elif valor_2[i+6*x] == '4':
               valor_2[i+6*x] = "Invalid"

            update.message.reply_text('*PID* = {0}\n*Process Name* = {1}\n*Type* = {2}\n*State* = {3}'.format(valor_2[i],valor_2[i+x],valor_2[i+5*x],valor_2[i+6*x]), "Markdown")
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' ha intentado utilizar /swrun sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: generapdf
#Descripción: Genera un pdf con toda la información monitorizada.       
#Parámetros: update, context                           
################################ 
def generapdf(update,context):
    user = update.message.from_user
    # Autorizamos a los usuarios cuyo chat_id este registrado en usuarios_permitidos
    if user['id'] in usuarios_permitidos:
        user = update.message.from_user
        pdf.crearinformacion()
        pdf.convierte()
        update.message.reply_text('*Se han generado los PDF con la información SNMP y con el log de usuarios.*',"Markdown")
        update.message.reply_text('Los pdf se enviarán por correo electrónico a {}'.format(user['username']))
        correo.email(user) #Envia correo con pdf
    else:
        update.message.reply_text('{} no tiene acceso al bot.'.format(user['username']))
        log = open('log.txt','a')
        log.write(user['username']+' se ha intentado utilizar /generapdf sin permisos : '+time.strftime('%c')+'\n')
        log.close()

################################
#Función: trap
#Descripción: Monitoriza la variable hrSystemProcesses y genera un trap.       
#Parámetros: No tiene parámetros                           
################################        
def trap():
    control = 0
    while(1):
        # Número de procesos activos
        hrSystemProcesses = funciones.get('localhost',['1.3.6.1.2.1.25.1.6.0'],hlapi.CommunityData('public'))
        # Si el numero de procesos es mayor a 100, y nunca ha notificado
        if hrSystemProcesses['1.3.6.1.2.1.25.1.6.0']>100 and control==0:
            control = 1
            print('TRAP GENERADO. Hay {} procesos, superando el umbral de 100.'.format(hrSystemProcesses['1.3.6.1.2.1.25.1.6.0']))
            pdf.crearprocesos()
            print('Envio de informacion al correo')
            correo.emailprocesos()
        elif hrSystemProcesses['1.3.6.1.2.1.25.1.6.0']<100 and control==1:
            #Ponemos la variable control a 0
            #por si vuelve a subir los 100 procesos
            print('Hemos bajado de los 100 procesos')
            control = 0;
        elif hrSystemProcesses['1.3.6.1.2.1.25.1.6.0']>100 and control==1:
            print('El trap ya ha sido enviado')
        else:
            print('No hay TRAP')
        time.sleep(20)

################################
#Función: desconocido
#Descripción: Si escribimos un comando desconocido, nos indica que no lo entiende.  
#Parámetros: update, context                          
################################ 
def desconocido(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Lo siento, no entendí ese comando.")
        
################################
#Función: main
#Descripción: Función ppal. del programa.
#Parámetros: No tiene                         
################################ 
def main():
    bot_updater = Updater(TOKEN, use_context=True)
    desconocido_handler = MessageHandler(Filters.command, desconocido)
    dp = bot_updater.dispatcher
    
    
    # Comandos que responde Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ayuda", ayuda))
    dp.add_handler(CommandHandler("system", system))
    dp.add_handler(CommandHandler("syscontact", syscontact))
    dp.add_handler(CommandHandler("sysname", sysname))
    dp.add_handler(CommandHandler("syslocation", syslocation))
    dp.add_handler(CommandHandler("modsystem", modsystem))
    dp.add_handler(CommandHandler("generapdf", generapdf))
    dp.add_handler(CommandHandler("routetable", routetable))
    dp.add_handler(CommandHandler("interfacetable", interfacetable))
    dp.add_handler(CommandHandler("tcptable", tcptable))
    dp.add_handler(CommandHandler("udptable", udptable))
    dp.add_handler(CommandHandler("devicetable", devicetable))
    dp.add_handler(CommandHandler("swrun", swrun))
    dp.add_handler(desconocido_handler)
    
    # Iniciar el bot
    bot_updater.start_polling()
    
    # Creamos un hilo, para monitorizar el trap simultaneamente con el bot.
    t = threading.Thread(target = trap)
    t.start()
    
    # Parar el bot con ctrol^C
    bot_updater.idle()

#Llamamos a la función main para que inicie el programa         
main()
