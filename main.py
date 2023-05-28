#Importamos json para poder manejar los datos de los archivos.
import json
#Importamos os para poder limpiar la consola antes de mostrar una tabla o un menu de opciones.
import os

#Creamos la variable que indicara al programa principal si el usuario ha iniciado sesion o es invitado.
#Creamos la variable que indica si el usuario es administrador o no, para modificar las opciones a las cuales tendra acceso.
#Creamos la variable que guardara el nombre de usuario una vez que inicia sesion de manera exitosa y la variable que guardara la lista en caso de que coloque productos en el carrito.
sesion_iniciada = False
sesion_administrador = False
sesion_username = ""
sesion_mail = ""
sesion_carrito = []

#Creamos la funcion que mostrara el menu de entrada y nos derivara a la opcion correspondiente dependiendo de la eleccion del usuario.
def menu_principal():
    print(f'''
                                                                ######################################
                                                                ######################################
                                                                ####{'FERRETERIA':^30s}####
                                                                ####{'LO':^30s}####
                                                                ####{'PRESTI':^30s}####
                                                                ######################################
                                                                ######################################
    
                            Bienvenido a nuestro programa. Podras ver todos nuestros productos, filtrarlos por categoria o buscar por nombre y codigo.
                Puedes entrar como invitado, pero si inicias sesion, podras acceder tambien a la posibilidad de agregar productos a un carrito y solicitarnos un presupuesto.
                    
                                                                    [1] Continuar como invitado.
                                                                    [2] Iniciar Sesion.
                                                                    [3] Crear un nuevo usuario.
                                                                    [x] Cerrar el programa. 
        ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        opciones_invitado()
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        iniciar_sesion()
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        crear_usuario()
    elif decision == 'x':
        print('¡¡¡Gracias por haber utilizado nuestro programa!!!')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_principal()

#Creamos la funcion que utilizaremos para iniciar sesion
def iniciar_sesion ():
# En primera instancia, accedemos al archivo que contiene los nombres de usuario.
# Luego, transformamos el archivo (para poder iterar sus diccionarios).
    users = open('./users.txt','r',encoding='utf-8')
    users_list = json.load(users)
#Pedimos al usuario que ingrese su nombre de usuario y contraseña, lo almacenamos en dos variables.
    print(f'''
                    ######################################
                    ######################################
                    ####{'FERRETERIA':^30s}####
                    ####{'LO':^30s}####
                    ####{'PRESTI':^30s}####
                    ######################################
                    ######################################
        ''')
    print(f'''
                    ////////////////////////////////////
                    ////////// INICIAR SESION //////////
                    ////////////////////////////////////
        ''')
    username = input('>>>>> Por favor, ingrese su nombre de usuario >>>>> ')
    password = input('>>>>>    Por favor, ingrese su contraseña     >>>>> ')
#Llamamos a las variables iniciadas globalmente para que sean reconocidas dentro de la funcion.
    global sesion_iniciada
    global sesion_administrador
    global sesion_username
    global sesion_mail
#Iniciamos un bucle for en el cual revisamos cada user en users_list para ver si coinciden el usuario Y la contraseña, siempre que aun no se haya encontrado ninguna correspondencia.
#Si el usuario corresponde al de un administrador, tambien volvemos verdadera la variable sesion_administrador.
#Si no se encuentran correspondencias de usuario y contraseña, se le comunica al usuario y se vuelven a pedir los datos.
    for user in users_list:
        if sesion_iniciada == False:
            if user['username'] == username and user['password'] == password:
                sesion_iniciada = True
                sesion_username = user['username']
                sesion_mail = user['mail']
                if user['administrator'] == True:
                    sesion_administrador = True
        else:
            break
    if sesion_iniciada == False:
        print('''
    ❌❌❌ El nombre de usuario o contraseña ingresados son incorrectos. ¿Desea intentarlo nuevamente? ❌❌❌
                                
                                        [1] Iniciar Sesion nuevamente.
                                        [2] Continuar como invitado.
                                        [x] Salir del programa
                        ''')
        iniciar_sesion_nuevamente()
    else:
        if sesion_administrador == False:
            opciones_registrado()
        else:
            opciones_administrador()

#Creamos una funcion que permitira al usuario decidir si desea intentar nuevamente iniciar sesion o simplemente acceder como invitado.
def iniciar_sesion_nuevamente ():
    decision = input('''>>>>> La opcion elegida es >>>>> ''')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        iniciar_sesion()
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        opciones_invitado()
    elif decision == 'x':
        print('¡¡¡Gracias por haber utilizado nuestro programa!!!')
    else:
        print('❌❌❌ Por favor, ingrese una opcion valida ❌❌❌')
        iniciar_sesion_nuevamente()

#Creamos una funcion que permita al usuario crear un nuevo usuario.
def crear_usuario():
    users = open('./users.txt','r',encoding='utf-8')
    users_list = json.load(users)
    username_invalido = False
    mail_invalido = False
    print('''
                ////////////////////////////////////////////////////
                //// Bienvenido al menu de creacion de usuario. ////
                ////////////////////////////////////////////////////
        ''')
    print('''
        En primer lugar, ingrese su Nombre de Usuario. El mismo no debera exstir en nuestra base de datos. No distingue entre mayusculas y minusculas.
        ''')
    username = input('>>>>> Nombre de Usuario deseado >>>>> ').lower()
    if len(username) == 0:
        username_invalido = True
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese un nombre de usuario ❌❌❌')
        crear_usuario()
    else:
        for user in users_list:
            if user["username"] == username:
                username_invalido = True
                os.system('cls' if os.name == 'nt' else 'clear')
                print('❌❌❌ El Nombre de Usuario solicitado ya existe en nuestra base de datos. ❌❌❌')
                crear_usuario()
                break
    if username_invalido == False:
        print('''
        En segundo lugar, ingrese su mail. El mismo no debera existir en nuestra base de datos y debe tener un formato valido (incluir '@' y '.com'). No distingue entre mayusculas y minusculas.
        ''')
        mail = input('>>>>> Su direccion de mail es >>>>> ').lower()
        if len(mail) < 8 or not '@' in mail or not '.com' in mail:
            mail_invalido = True
            os.system('cls' if os.name == 'nt' else 'clear')
            print('❌❌❌ Por favor, ingrese un mail de formato valido. ❌❌❌')
            crear_usuario()
        else:
            for user in users_list:
                if user["mail"] == mail:
                    mail_invalido = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('❌❌❌ El mail ingresado ya existe en nuestra base de datos. ❌❌❌')
                    crear_usuario()
                    break
    if username_invalido == False and mail_invalido == False:
        print('''
        En tercer lugar, ingrese su contrasena. La misma debe contar con al menos 8 caracteres, una mayuscula, una minuscula y un numero.
        ''')
        primera_contrasena = input('>>>>> Nueva contrasena >>>>> ')
        contrasena_valida = True
        if len(primera_contrasena) < 8:
            contrasena_valida = False
        for caracter in primera_contrasena:
            if caracter.isupper():
                contrasena_valida = True
                break
            contrasena_valida = False
        for caracter in primera_contrasena:
            if caracter.islower():
                contrasena_valida = True
                break
            contrasena_valida = False
        for caracter in primera_contrasena:
            if caracter.isdigit():
                contrasena_valida = True
                break
            contrasena_valida = False
        if contrasena_valida == False:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('❌❌❌ Por favor, ingrese una contrasena valida.❌❌❌')
            crear_usuario()
        else:
            print('''
        Por favor, confirme su contrasena ingresandola nuevamente.
        ''')
            segunda_contrasena = input('>>>>> Ingrese nuevamente su contrasena >>>>> ')
            if segunda_contrasena != primera_contrasena:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('❌❌❌ Las contrasenas no coinciden. ❌❌❌')
                crear_usuario()
            else:
                nuevo_usuario = {
                    "username" : username,
                    "password" : primera_contrasena,
                    "mail" : mail,
                    "administrator" : False
                }
                users_list.append(nuevo_usuario)
                with open ('./users.txt','w',encoding='UTF-8') as users_nuevo:
                    users_nuevo.write(json.dumps(users_list,indent=2))
                os.system('cls' if os.name == 'nt' else 'clear')
                print('''
        El usuario ha sido creado exitosamente. Por favor, inicie sesion para confirmar el usuario.''')
                iniciar_sesion()

#A continuacion crearemos un menu especializado para cada tipo de usuario.
#Creamos la funcion que mostrara las opciones en caso de ser un usuario de tipo invitado. Solamente podra ver los productos, filtrarlos y ver su stock.
def opciones_invitado ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print(f'''
                        ######################################
                        ######################################
                        ####{'FERRETERIA':^30s}####
                        ####{'LO':^30s}####
                        ####{'PRESTI':^30s}####
                        ######################################
                        ######################################
        ''')
    print('''
                    ###############################################
                    ############## Usuario Invitado ###############
                    ###############################################
                    
                    Usted podra acceder a las siguientes opciones:
                    
                        [1] Mostrar todos los productos en stock.
                        [2] Mostrar todos los productos nacionales.
                        [3] Mostrar todos los productor importados.
                        [4] Filtrar productos por categoria.
                        [5] Buscar productos por codigo.
                        [6] Buscar productos por nombre.
                        [0] Volver al Menu Principal.
                        [x] Cerrar el programa.
                                    ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(productos_lista)
        retroceder_menu(opciones_invitado)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,True)
        retroceder_menu(opciones_invitado)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,False)
        retroceder_menu(opciones_invitado)
    elif decision == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_menu(productos_lista,opciones_invitado)
    elif decision == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'codigo')
        retroceder_menu(opciones_invitado)
    elif decision == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'nombre')
        retroceder_menu(opciones_invitado)
    elif decision == '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_principal()
    elif decision == 'x':
        print('¡¡¡Gracias por haber utilizado nuestro programa!!!')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese una opcion valida ❌❌❌')
        opciones_invitado()

#Creamos la funcion que mostrara las opciones en caso de ser un usuario registrado. Podra ver los productos, filtrarlos y ver su stock. Ademas, podra agregar productos a un carrito.
def opciones_registrado ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print(f'''
                        ######################################
                        ######################################
                        ####{'FERRETERIA':^30s}####
                        ####{'LO':^30s}####
                        ####{'PRESTI':^30s}####
                        ######################################
                        ######################################
        ''')
    print('''
                    ###############################################
                    ############## Usuario Registrado##############
                    ###############################################
                    
                    Usted podra acceder a las siguientes opciones:
                    
                        [1] Mostrar todos los productos en stock.
                        [2] Mostrar todos los productos nacionales.
                        [3] Mostrar todos los productos importados.
                        [4] Filtrar productos por categoria.
                        [5] Buscar productos por codigo.
                        [6] Buscar productos por nombre.
                        [7] Solicitar Presupuesto.
                        [0] Cerrar el programa.
        ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(productos_lista)
        retroceder_menu(opciones_registrado)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,True)
        retroceder_menu(opciones_registrado)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,False)
        retroceder_menu(opciones_registrado)
    elif decision == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_menu(productos_lista,opciones_registrado)
    elif decision == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'codigo')
        retroceder_menu(opciones_registrado)
    elif decision == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'nombre')
        retroceder_menu(opciones_registrado)
    elif decision == '7':
        os.system('cls' if os.name == 'nt' else 'clear')
        carrito_menu(productos_lista,opciones_registrado)
    elif decision == '0':
        print('¡¡¡Gracias por haber utilizado nuestro programa!!!')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese una opcion valida ❌❌❌')
        opciones_registrado()

#Creamos la funcion que mostrara las opciones en caso de ser un usuario administrador. Podra ver los productos, filtrarlos y ver su stock. Ademas, podra agregar productos a un carrito.
def opciones_administrador ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print(f'''
                        ######################################
                        ######################################
                        ####{'FERRETERIA':^30s}####
                        ####{'LO':^30s}####
                        ####{'PRESTI':^30s}####
                        ######################################
                        ######################################
        ''')
    print('''
                    ###############################################
                    ############ Usuario Administrador ############
                    ###############################################
                    
                    Usted podra acceder a las siguientes opciones:
                    
                        [1] Mostrar todos los productos en stock.
                        [2] Mostrar todos los productos nacionales.
                        [3] Mostrar todos los productos importados.
                        [4] Mostrar productos por categoria.
                        [5] Buscar productos por codigo.
                        [6] Buscar productos por nombre.
                        [7] Menu de productos.
                        [8] Menu de presupuestos.
                        [0] Cerrar el programa.
        ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(productos_lista)
        retroceder_menu(opciones_administrador)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,True)
        retroceder_menu(opciones_administrador)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_esNacional(productos_lista,False)
        retroceder_menu(opciones_administrador)
    elif decision == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_menu(productos_lista,opciones_administrador)
        opciones_administrador()
    elif decision == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'codigo')
        opciones_administrador()
    elif decision == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        buscar_productos(productos_lista,'nombre')
        opciones_administrador()
    elif decision == '7':
        os.system('cls' if os.name == 'nt' else 'clear')
        crud_producto_menu(productos_lista, opciones_administrador)
    elif decision == '8':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_presupuestos()
    elif decision == '0':
        print('¡¡¡Gracias por haber utilizado nuestro programa!!!')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese una opcion valida ❌❌❌')
        opciones_administrador()

#A continuacion iremos creando todas las funciones que seran utilizadas por cualquiera de los usuarios.

#Creamos una funcion para volver al menu anterior.
def retroceder_menu (menuAnterior):
    print('''
        Cuando desee volver al menu anterior, presione 's'.
        ''')
    decision = input('>>>>> ¿Volver al menu anterior? >>>>> ')
    if decision != 's':
        retroceder_menu (menuAnterior)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        menuAnterior()

#Creamos la funcion que mostrara todos los objetos de una lista. Tendra un parametro, que es la lista sobre la cual se va a iterar.
def mostrar_productos (lista):
    print('''
                                    #######################################################################
                                    ###### A continuacion, se mostraran todos los productos en stock ######
                                    #######################################################################''')
    print("             ","="*121)
    print(f'              {"N°":^4s}     {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Stock Disponible":<16s}     {"Es Nacional":<17s}  ')
    print("             ","-"*121)
    indice = 1
    for producto in lista:
        if producto['esNacional']:
            print(f'              {indice:^4d}     {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad"]:^16d}     {"Producto Nacional":<17s}  ')
            indice = indice + 1
        else:
            print(f'              {indice:^4d}     {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad"]:^16d}     {"Producto Importado":<17s}  ')
            indice = indice + 1
    print("             ","-"*121)

#Creamos la funcion que mostrara todos los objetos de una lista, si 'esNacional' cumple con el parametro dado. Tendra dos parametros.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo es para indicar si el valor de 'esNacional' debe ser True o False.
def filtrar_productos_esNacional (lista,valor):
    if valor == True:
        print('''
                            #######################################################################
                            #### A continuacion, se mostraran los productos de origen nacional ####
                            #######################################################################''')
    else:
        print('''
                            #######################################################################
                            ######## A continuacion, se mostraran los productos importados ########
                            #######################################################################''')
    print("             ","="*96)
    print(f'                  {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Stock Disponible":<16s}  ')
    print("             ","-"*96)
    for producto in lista: 
        if producto['esNacional'] == valor:
            print(f'                  {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad"]:^16d}  ')
    print("             ","-"*96)

#Creamos la funcion que mostrara todos los objetos de una lista, si 'categoria' cumple con el parametro dado. Tendra dos parametros dados.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo es para indicar el valor con el cual se filtraran los resultados.
def filtrar_productos_categoria (lista,valor):
    print(f'''
                #############################################################################################
                ######## {'A continuacion, se mostraran los productos de la categoria ' + valor:^75s} ########
                #############################################################################################''')
    print("             ","="*97)
    print(f'              {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Stock Disponible":<16s}  ')
    print("             ","-"*97)
    for producto in lista:
        if producto['categoria'] == valor:
            print(f'              {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad"]:^16d}  ')
    print("             ","-"*97)

#Creamos la funcion que permitira al usuario elegir la categoria por la cual filtrar los resultados. Tendra dos parametros.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo, es para indicar a que menu debera volver.
def filtrar_productos_menu (lista,menuAnterior):
    print('''
                    ///////////////////////////////////////////////
                    //////////   Filtrar por Categoria   //////////
                    ///////////////////////////////////////////////
        
        Al elegir una opcion, se mostraran los productos de la categoria elegida
        
                [1] Mostrar productos de la Categoria Herramientas.
                [2] Mostrar productos de la Categoria Casa.
                [3] Mostrar productos de la Categoria Bazaar.
                [0] Volver al Menu Anterior.
        ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_categoria(lista,"Herramienta")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_categoria(lista,"Casa")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        filtrar_productos_categoria(lista,"Bazaar")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        menuAnterior()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
        filtrar_productos_menu(lista,menuAnterior)

#Creamos la funcion que permitira al usuario buscar un producto segun el parametro deseado. Se creara una lista, se la imprimira y se la retornara, para ser utilizada en otras funciones (agregar_carrito).
def buscar_productos (lista,llave):
    print(f'''
                    ////////////////////////////////////
                    //////{"Buscar por " + llave:^24s}//////
                    ////////////////////////////////////

                A continuacion, podra buscar su producto por {llave}.
        ''')
    decision = input(f'>>>>> Por favor, ingrese el {llave} del producto deseado >>>>> ').lower()
    productos_encontrados = []
    for producto in lista:
        if  decision in producto[llave].lower():
            productos_encontrados.append({"codigo": producto["codigo"],"nombre" : producto["nombre"],"categoria": producto["categoria"],"cantidad": producto["cantidad"]})
    if len(productos_encontrados) == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'❌❌❌ No hemos encontrado ningun resultado para "{decision}". Por favor, intentelo nuevamente. ❌❌❌')
        buscar_productos(lista,llave)
    else:
        indice = 1
        print(f'''
                            ###################################################################
                            ######## Su busqueda ha arrojado los siguientes resultados ########
                            ###################################################################''')
        print("             ","="*97)
        print(f'              {"N°":^4s}     {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Stock Disponible":<16s}  ')
        print("             ","-"*97)
        for producto_encontrado in productos_encontrados:
            print(f'              {indice:^4d}     {producto_encontrado["codigo"]:^7s}     {producto_encontrado["nombre"]:<35s}     {producto_encontrado["categoria"]:<15s}     {producto_encontrado["cantidad"]:^16d}  ')
            indice = indice + 1
        return productos_encontrados

# Creamos la funcion que permitira al usuario agregar productos al carrito. En caso de no ingresar un numero,
# se atrapara el error con un except y se volvera a pedir el numero de producto. En caso de no colocar una opcion valida, se volvera a pedir el numero de producto. Se solicitara la cantidad de unidades deseadas
# y se haran las comprobaciones necesarias.
def agregar_carrito (lista,menuAnterior):
    global sesion_carrito
    print('''
        A continuacion, podra ingresar el numero (columna izquierda de la tabla) del producto que desea agregar al carrito. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>>>> Ingrese el numero del producto >>>>> ')
    if producto_elegido == 'x':
        os.system('cls' if os.name == 'nt' else 'clear')
        carrito_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(lista) or producto_indice <= 0:
                print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                agregar_carrito(lista,menuAnterior)
            else:
                print(f'''
        Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}". Contamos con {lista[producto_indice - 1]["cantidad"]} unidades.''')
                print('''
        Ingrese las unidades del producto que desea agregar al carrito. Si desea elegir otro producto, ingrese 'x':
                ''')
                producto_cantidad_elegida = input('>>>>> Cantidad de unidades que desea agregar >>>>> ')
                if producto_cantidad_elegida == 'x':
                    agregar_carrito(lista,menuAnterior)
                else:
                    try:
                        producto_cantidad = int(producto_cantidad_elegida)
                        if producto_cantidad > lista[producto_indice - 1]['cantidad'] or producto_cantidad <= 0:
                            print('❌❌❌ Por favor, ingrese una cantidad de unidades valida. ❌❌❌')
                            agregar_carrito(lista,menuAnterior)
                        else:
                            sesion_carrito.append({"codigo": lista[producto_indice - 1]["codigo"],"nombre": lista[producto_indice - 1]["nombre"],"categoria": lista[producto_indice - 1]["categoria"],"cantidad_solicitada": producto_cantidad})
                            print(f'''
        Se han agregado al carrito {producto_cantidad} unidades de {lista[producto_indice - 1]["nombre"]}.''')
                            carrito_menu(lista,menuAnterior)
                    except ValueError:
                        print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                        agregar_carrito(lista,menuAnterior)
        except ValueError:
            print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
            agregar_carrito(lista,menuAnterior)

#Creamos la funcion que permitira al usuario ver los productos que ha ingresado al carrito.
def mostrar_carrito ():
    if len(sesion_carrito) == 0:
        print(f'''
                #####################################################
                ##### Aun no ha agregado productos a su Carrito #####
                #####################################################
                ''')
    else:
        indice = 1
        print(f'''
                                ##########################################################################
                                ##### A continuacion, se mostraran todos los productos en su Carrito #####
                                ##########################################################################''')
        print("             ","="*101)
        print(f'              {"N°":^4s}     {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Cantidad Solicitada":<20s}  ')
        print("             ","-"*101)
        for producto in sesion_carrito:
            print(f'              {indice:^4d}     {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad_solicitada"]:^16d}  ')
            indice = indice + 1

#Creamos una funcion que permita modificar el carrito una vez creado.
def modificar_carrito(lista,menuAnterior):
    print('''
        A continuacion, podra ingresar el numero (columna izquierda de la tabla) del producto de su carrito que desea modificar. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>>>> Ingrese el numero del producto >>>>> ')
    if producto_elegido == 'x':
        os.system('cls' if os.name == 'nt' else 'clear')
        carrito_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(sesion_carrito) or producto_indice <= 0:
                print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                modificar_carrito(lista,menuAnterior)
            else:
                print(f'''
        En su carrito, usted tiene {sesion_carrito[producto_indice - 1]["cantidad_solicitada"]} unidades del producto "{sesion_carrito[producto_indice - 1]["nombre"]}". Elija una de las siguientes opciones

                    [1] Modificar la cantidad de unidades.
                    [9] Quitar este producto del carrito.
                    [cualquier tecla] Elegir otro producto.
                    ''')
                opcion_elegida = input('>>>>> La opcion elegida es >>>>> ')
                if opcion_elegida == '1':
                    print('''
        Por favor, ingrese la cantidad de unidades que desea actualmente.
        ''')
                    nuevas_unidades = input('>>>>> Unidades solicitadas actualmente >>>>> ')
                    try:
                        unidades = int(nuevas_unidades)
                        sesion_carrito[producto_indice - 1]["cantidad_solicitada"] = unidades
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'''
        Ahora, en su carrito usted tiene {sesion_carrito[producto_indice - 1]["cantidad_solicitada"]} unidades del producto "{sesion_carrito[producto_indice - 1]["nombre"]}".
        ''')
                        carrito_menu(lista,menuAnterior)
                    except ValueError:
                        print('❌❌❌ Por favor, ingrese un numero valido. ❌❌❌')
                        modificar_carrito(lista,menuAnterior)
                elif opcion_elegida == '9':
                    del sesion_carrito[producto_indice - 1]
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f'''
        Se ha eliminado el producto de su carrito.
        ''')
                    carrito_menu(lista,menuAnterior)
                else:
                    modificar_carrito(lista,menuAnterior)
        except ValueError:
            print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
            modificar_carrito(lista,menuAnterior)

#Creamos la funcion que permitira al usuario guardar el carrito. A los carritos guardados podran acceder los administradores para pasar los presupuestos correspondientes.
def guardar_carrito ():
    carritos = open('./carritos.txt','r',encoding='utf-8')
    carritos_list = json.load(carritos)
    nuevo_carrito = {
        "username": sesion_username,
        "mail" : sesion_mail,
        "productos": sesion_carrito}
    carritos_list.append(nuevo_carrito)
    carritos_nuevo = open('./carritos.txt','w')
    carritos_nuevo.write(json.dumps(carritos_list,indent=2))
    print('''
        ######################################################################################################################
        ########## Su carrito ha sido guardado exitosamente. Le enviaremos un mail con el presupuesto por el mismo. ##########
        ##########                      ¡¡¡Gracias por haber utilizado nuestro programa!!!                          ##########
        ######################################################################################################################
        ''')

#Creamos la funcion que permitira al usuario buscar productos, agregar productos al carrito, modificar el carrito y guardar y enviar el carrito.
def carrito_menu (lista,menuAnterior):
    print('''
                    ///////////////////////////////////
                    ////// Solicitar Presupuesto //////
                    ///////////////////////////////////
        
            A continuacion, podra agregar productos a su carrito, 
            verlo y guardarlo para que los administradores le envien
                        un mail con su presupuesto.
        
        [1] Agregar productos desde la lista de todos los productos en stock.
        [2] Agregar productos buscando por codigo.
        [3] Agregar productos buscando por nombre.
        [4] Ver Carrito.
        [5] Modificar Carrito.
        [6] Guardar el carrito, solicitar presupuesto y cerrar el programa.
        [0] Volver al Menu Anterior.
        ''')
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(lista)
        agregar_carrito(lista,menuAnterior)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        productos_encontrados = buscar_productos (lista,'codigo')
        agregar_carrito(productos_encontrados,carrito_menu)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        productos_encontrados = buscar_productos (lista,'nombre')
        agregar_carrito(productos_encontrados,carrito_menu)
    elif decision == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_carrito()
        carrito_menu(lista,menuAnterior)
    elif decision == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_carrito()
        if len(sesion_carrito) > 0:
            modificar_carrito()
        else:
            carrito_menu(lista,menuAnterior)
    elif decision == '6':
        mostrar_carrito()
        if len(sesion_carrito) > 0:
            guardar_carrito()
        else:
            carrito_menu(lista,menuAnterior)
    elif decision == '0':
        menuAnterior()
    else:
        print('>>>> Por favor, ingrese una opcion valida')
        carrito_menu(lista,menuAnterior)

#Creamos la funcion que permita al usuario modificar las cantidades de los productos.
def modificar_producto (lista,menuAnterior):
    print('''
        Ingrese el numero del producto (columna izquierda de la tabla) del que desea modificar la cantidad. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>>>> Numero del producto que desea modificar >>>>> ')
    if producto_elegido == 'x':
        os.system('cls' if os.name == 'nt' else 'clear')
        crud_producto_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(lista) or producto_indice <= 0:
                print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                modificar_producto(lista,menuAnterior)
            else:
                print(f'''
        Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}". Cuenta con {lista[producto_indice - 1]["cantidad"]} unidades.
        ''')
                print('''
        Ingrese las unidades actuales del producto. Si desea elegir otro producto, ingrese 'x':
                ''')
                producto_cantidad_elegida = input('>>>>> Unidades actuales del producto >>>>> ')
                if producto_cantidad_elegida == 'x':
                    modificar_producto(lista,menuAnterior)
                else:
                    try:
                        producto_cantidad = int(producto_cantidad_elegida)
                        lista[producto_indice - 1]['cantidad'] = producto_cantidad
                        with open('./stock.txt','w',encoding='utf-8') as lista_nueva:
                            lista_nueva.write(json.dumps(lista,indent=2))
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'''
        Se ha actualizado el stock de {lista[producto_indice - 1]["nombre"]}. Ahora cuenta con {producto_cantidad_elegida} unidades
        ''')
                        menuAnterior()
                    except ValueError:
                        print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                        modificar_producto(lista,menuAnterior)
        except ValueError:
            print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
            modificar_producto(lista,menuAnterior)

#Creamos la funcion que permita al usuario eliminar un producto.
def eliminar_producto (lista,menuAnterior):
    print('''
        Ingrese el numero del producto (columna izquierda de la tabla) del que desea eliminar. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>>>> Numero del producto que desea eliminar >>>>> ')
    if producto_elegido == 'x':
        crud_producto_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(lista) or producto_indice <= 0:
                print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                eliminar_producto(lista,menuAnterior)
            else:
                print(f'''
        Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}"
        ''')
                print('''
        Para confirmar su eliminacion, presione 's'. Esta operacion no tiene vuelta atras. Si desea elegir otro producto, ingrese cualquier otra tecla:
                ''')
                decision = input('>>>>> ¿Realmente desea eliminar este producto de la base de datos? >>>>> ').lower()
                if decision != 's':
                    eliminar_producto(lista,menuAnterior)
                else:
                    del lista[producto_indice - 1]
                    with open('./stock.txt','w',encoding='utf-8') as lista_nueva:
                            lista_nueva.write(json.dumps(lista,indent=2))
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f'''
        Se ha eliminado el producto satisfactoriamente.''')
                    crud_producto_menu(lista,menuAnterior)
        except ValueError:
            print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
            eliminar_producto(lista,menuAnterior)

#creamos la funcion que permita al usuario agregar un producto.
def agregar_producto (lista,menuAnterior):
    print('''
        Ingrese el codigo del nuevo producto. El mismo debe tener un formato de 'A99999'. Presione 'x' para volver al menu anterior.
        ''')
    codigo_ingresado = input('>>>>> El codigo del nuevo producto es >>>>> ')
    if codigo_ingresado.lower() == 'x':
        os.system('cls' if os.name == 'nt' else 'clear')
        crud_producto_menu(lista,menuAnterior)
    elif len(codigo_ingresado) != 6 or not codigo_ingresado[0].isupper() or not codigo_ingresado[1].isdigit() or not codigo_ingresado[2].isdigit() or not codigo_ingresado[3].isdigit() or not codigo_ingresado[4].isdigit() or not codigo_ingresado[5].isdigit():
        print('❌❌❌ El formato del codigo no es el correcto. Por favor, ingrese el codigo con el formato "A99999". ❌❌❌')
        agregar_producto(lista,menuAnterior)
    else:
        print('''
        Por favor, ingrese el nombre del producto.
            ''')
        nombre_ingresado = input('>>>>> Nombre del Producto >>>>> ')
        print('''
        Por favor, ingrese la categoria del producto.
            ''')
        categoria_ingresada = input('>>>>> Categoria del Producto >>>>> ')
        print('''
        Por favor, ingrese la cantidad de unidades en stock del producto.
            ''')
        cantidad_ingresada = input('>>>>> Unidades en stock del Producto >>>>> ')
        try:
            cantidad = int(cantidad_ingresada)
            if cantidad <= 0:
                print('❌❌❌ Por favor, ingrese una cantidad de unidades valida. ❌❌❌')
                agregar_producto(lista,menuAnterior)
            else:
                print('El producto es de Industria Nacional? Ingrese "s"/"n".')
                esNacional_input = input('>>> ')
                if esNacional_input == 's':
                    print(f'''
        Se ingresara el producto "{nombre_ingresado}" de codigo "{codigo_ingresado}", correspondiente a la categoria "{categoria_ingresada}", de produccion nacional.
        El mismo figurara con {cantidad} de unidades en stock. Si desea continuar, presione 's', sino presione cualquier otra tecla.
                        ''')
                    decision = input ('>>> ')
                    if decision.lower() != 's':
                        agregar_producto(lista,menuAnterior)
                    else:
                        lista.append({"codigo": codigo_ingresado,
                                    "nombre": nombre_ingresado,
                                    "categoria": categoria_ingresada,
                                    "cantidad": cantidad,
                                    "esNacional": True})
                        with open('./stock.txt','w',encoding='utf-8') as lista_nueva:
                            lista_nueva.write(json.dumps(lista,indent=2))
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'''
        Se ha anadido el producto satisfactoriamente.
        ''')
                        crud_producto_menu(lista,menuAnterior)
                elif esNacional_input == 'n':
                    print(f'''
        Se ingresara el producto "{nombre_ingresado}" de codigo "{codigo_ingresado}", correspondiente a la categoria "{categoria_ingresada}", importado.
        El mismo figurara con {cantidad} de unidades en stock. Si desea continuar, presione 's', sino presione cualquier otra tecla.
                        ''')
                    decision = input ('>>> ')
                    if decision.lower() != 's':
                        agregar_producto(lista,menuAnterior)
                    else:
                        lista.append({"codigo": codigo_ingresado,
                                    "nombre": nombre_ingresado,
                                    "categoria": categoria_ingresada,
                                    "cantidad": cantidad,
                                    "esNacional": False})
                        lista_nueva = open('./stock.txt','w')
                        lista_nueva.write(json.dumps(lista,indent=2))
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'''
        Se ha anadido el producto satisfactoriamente.
        ''')
                        crud_producto_menu(lista,menuAnterior)
                else:
                    print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                    agregar_producto(lista,menuAnterior)
        except ValueError:
            print('❌❌❌ Por favor, ingrese una cantidad de unidades valida. ❌❌❌')
            agregar_producto(lista,menuAnterior)

#Creamos el menu en el que el usuario podra acceder a las opciones relacionadas a la actualizacion, eliminacion o agregado de productos.
def crud_producto_menu (lista, menuAnterior):
    print('''
                    /////////////////////////////////////////
                    //////////  Menu de Productos  //////////
                    /////////////////////////////////////////
        
            A continuacion, podra modificar las unidades en stock de 
            un producto, crear uno nuevo o eliminar uno ya existente.
        
        [1] Modificar la cantidad de unidades en stock de un producto.
        [2] Agregar nuevo producto.
        [3] Eliminar un producto.
        [0] Volver al Menu Anterior.
        ''')
    decision = input('>>>>> La opcion elegida es >>>>> ')
    if decision == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(lista)
        modificar_producto(lista,menuAnterior)
    elif decision == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        agregar_producto (lista,menuAnterior)
    elif decision == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_productos(lista)
        eliminar_producto (lista,menuAnterior)
    elif decision == '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        menuAnterior()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
        crud_producto_menu(lista, menuAnterior)

#Creamos la funcion que mostrara los presupuestos a enviar y permitira al usuario eliminar aquellos que ya ha respondido.
def mostrar_presupuestos ():
    presupuestos = open('./carritos.txt','r',encoding='utf-8')
    presupuestos_lista = json.load(presupuestos)
    indice = 1
    for presupuesto in presupuestos_lista:
        print(f'''
                        ''')
        print(f'''
                        ################################
                        #####{"PRESUPUESTO NRO " + indice:^22s}######
                        ################################
                        
                        Nombre de Usuario: {presupuesto['username']}
                        Correo Electronico: {presupuesto['mail']}''')
        print("             ","="*92)
        print(f'              {"Codigo":<7s}     {"Nombre del producto":<35s}     {"Categoria":<15s}     {"Cantidad Solicitada":<20s}  ')
        print("             ","-"*92)
        for producto in presupuesto['productos']:
            print(f'''
            print(f'              {producto["codigo"]:^7s}     {producto["nombre"]:<35s}     {producto["categoria"]:<15s}     {producto["cantidad"]:^16d}  ')
            ''')
        indice = indice + 1
    print('''
        Si desea eliminar un presupuesto, presione 's'. Sino, presione cualquier otra tecla.
        ''')
    decision = input('>>>>> ¿Desea eliminar un presupuesto? >>>>> ')
    if decision != 's':
        os.system('cls' if os.name == 'nt' else 'clear')
        opciones_administrador()
    else:
        print('''
        A continuacion, ingrese el numero de presupuesto que desea eliminar.
        ''')
        numero_presupuesto_elegido = input('>>>>> El numero de presupuesto a eliminar es >>>>> ')
        try:
            numero_presupuesto = int(numero_presupuesto_elegido)
            if numero_presupuesto <= 0 or numero_presupuesto > indice - 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
                mostrar_presupuestos()
            else:
                print(f'''
        Se eliminara el presupuesto {numero_presupuesto}. Si desea continuar, presione 's'. Sino, presione cualquier otra tecla.
                ''')
                confirmar_decision = input(f'>>>>> ¿Desea eliminar el presupuesto {numero_presupuesto}? >>>>> ')
                if confirmar_decision.lower() != 's':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    mostrar_presupuestos()
                else:
                    del presupuestos_lista[numero_presupuesto - 1]
                    with open('./carritos.txt','w',encoding='utf-8') as nuevos_presupuestos:
                        nuevos_presupuestos.write(json.dumps(presupuestos_lista,indent=2))
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('''
        El presupuesto se ha eliminado satisfactoriamente.
                    ''')
                    opciones_administrador()
        except ValueError:
            print('❌❌❌ Por favor, ingrese una opcion valida. ❌❌❌')
            mostrar_presupuestos()

#Ejecutamos la funcion para que funcione el programa.
menu_principal()