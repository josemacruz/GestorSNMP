################################
#Fichero: funciones.py
#Descripción: Fichero que describe las funciones SNMP:
#             GET,SET,NEXT
################################

# Librerias utilizadas
from pysnmp import hlapi
from pysnmp.hlapi import *

################################
#Función: construct_object_types
#Descripción: Método para construir el ObjectTypes             
#Parámetros: list_of_oids                        
################################
def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))

    return object_types

################################
#Función: cast
#Descripción: Método para convertir los valores en enteros, flotante o string             
#Parámetros: value                      
################################
def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

################################
#Función: fetch
#Descripción: Método que obtiene el valor del oid            
#Parámetros: handler, count                        
################################
def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

################################
#Función: construct_value_pairs
#Descripción: Método para contruir el ObjectType con el valor.           
#Parámetros: list_of_pairs                         
################################
def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
    return pairs

################################
#Función: get
#Descripción: Método GET de SNMP            
#Parámetros: target, oids, credentials, port, engine, context                         
################################
def get(target, oids,credentials,port=161,engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        hlapi.CommunityData('public'),
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids))
    return fetch(handler, 1)[0]

################################
#Función: set
#Descripción: Método SET de SNMP            
#Parámetros: target, oids, credentials, port, engine, context                         
################################
def set(target, value_pairs, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.setCmd(
        engine,
        hlapi.CommunityData('public'),
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs ( value_pairs ))
    return fetch(handler, 1)[0]

################################
#Función: get_bulk_auto
#Descripción: Método GETNEXT de SNMP para devolver tablas             
#Parámetros: target, oids, credentials, port, engine, context                         
################################
def get_bulk_auto(target, oids, credentials, count_oid, start_from=0, port=161,engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    count = get(target, [count_oid], credentials, port, engine, context)[count_oid]
    return get_bulk(target, oids, credentials, count, start_from, port, engine, context)

################################
#Función: get_bulk
#Descripción: Método bulk de SNMP                 
#Parámetros: target, oids, credentials, port, engine, context                       
################################
def get_bulk(target, oids, credentials, count, start_from=0, port=161,engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(engine,credentials,hlapi.UdpTransportTarget((target, port)),context,start_from, count,*construct_object_types(oids))
    return fetch(handler, count)

# GetNext para recorrer las tablas
################################
#Función: siguiente
#Descripción: Método GETNEXT de SNMP           
#Parámetros: oid, col                      
################################
def siguiente(oid,col):
    g = nextCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=1),
        UdpTransportTarget(('localhost', 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    )

    valor_1 = []
    valor_2 = []
    valor_3 = []
    while True:
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(g);
            if errorIndication:
                print(errorIndication)
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and     varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for var_bind in varBinds:
                    valor_1.append(var_bind[0])
                    valor_2.append(var_bind[1].prettyPrint()) # Para direcciones IP y MAC
                    valor_3.append(str(var_bind[1])) # Para String
        except StopIteration:
            break

    # Variable para calcular longitud de la tabla (como tiene x columnas las dividimos por el nº total)
    # y obtenemos el numero de filas
    x = int(len(valor_1)/col)
    # Devuelve identificador, valor y numero de filas de la tabla
    return valor_1,valor_2,valor_3,x
