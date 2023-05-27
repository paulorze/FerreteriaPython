#Importamos json para poder manejar los datos de los archivos.
import json

#Creamos la variable que indicara al programa principal si el usuario ha iniciado sesion o es invitado.
#Creamos la variable que indica si el usuario es administrador o no, para modificar las opciones a las cuales tendra acceso.
#Creamos la variable que guardara el nombre de usuario una vez que inicia sesion de manera exitosa y la variable que guardara la lista en caso de que coloque productos en el carrito.
sesion_iniciada = False
sesion_administrador = False
sesion_username = ""
sesion_mail = ""
sesion_carrito = []
#Creamos la funcion que utilizaremos para iniciar sesion
def iniciar_sesion ():
# En primera instancia, accedemos al archivo que contiene los nombres de usuario.
# Luego, transformamos el archivo (para poder iterar sus diccionarios).
    users = open('./users.txt','r',encoding='utf-8')
    users_list = json.load(users)
#Pedimos al usuario que ingrese su nombre de usuario y contraseña, lo almacenamos en dos variables.
    username = input('Por favor, ingrese su nombre de usuario: ')
    password = input('Por favor, ingrese su contraseña: ')
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
                print(f'Bienvenido {sesion_username}.')
        else:
            break
    if sesion_iniciada == False:
        iniciar_sesion_nuevamente()
    else:
        if sesion_administrador == False:
            opciones_registrado()
        else:
            opciones_administrador()

#Creamos una funcion que permitira al usuario decidir si desea intentar nuevamente iniciar sesion o simplemente acceder como invitado.
def iniciar_sesion_nuevamente ():
    print('''
            ### El nombre de usuario o contraseña ingresados son incorrectos. ¿Desea intentarlo nuevamente? ###
                    [1] Iniciar Sesion.
                    [2] Continuar como invitado.
                    [3] Salir del programa''')
    decision = input('''
                    Opcion elegida: ''')
    if decision == '1':
        iniciar_sesion()
    elif decision == '2':
        print('continuaras como invitado')
    elif decision == '3':
        print('saliste del programa')
    else:
        print('Por favor, ingrese una opcion valida')
        iniciar_sesion_nuevamente()

#Creamos una funcion que permita al usuario crear un nuevo usuario.
def crear_usuario():
    users = open('./users.txt','r',encoding='utf-8')
    users_list = json.load(users)
    username_existente = False
    mail_existente = False
    print('''
        ########### Bienvenido al menu de creacion de usuario. ##########
        ''')
    print('''
        En primer lugar, ingrese su nombre de usuario. El mismo no debera exstir en nuestra base de datos. No distingue entre mayusculas y minusculas.
        ''')
    username = input('>>> ').lower()
    if len(username) == 0:
        print('Por favor, ingrese un nombre de usuario.')
        username_existente = True
        crear_usuario()
    else:
        for user in users_list:
            if user["username"] == username:
                print('El nombre de usuario ingresado ya existe en nuestra base de datos.')
                username_existente = True
                crear_usuario()
                break
    if username_existente == False:
        print('''
        En segundo lugar, ingrese su mail. El mismo no debera existir en nuestra base de datos y debe tener un formato valido (incluir '@' y '.com'). No distingue entre mayusculas y minusculas.
        ''')
        mail = input('>>> ').lower()
        if len(mail) < 8 or not '@' in mail or not '.com' in mail:
            print('Por favor, ingrese un mail de formato valido.')
            mail_existente = True
            crear_usuario()
        else:
            for user in users_list:
                if user["mail"] == mail:
                    print('El mail ingresado ya existe en nuestra base de datos.')
                    mail_existente = True
                    crear_usuario()
                    break
    if username_existente == False and mail_existente == False:
        print('''
        En tercer lugar, ingrese su contrasena. La misma debe contar con al menos 8 caracteres, una mayuscula, una minuscula y un numero.
        ''')
        primera_contrasena = input('>>> ')
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
            print('Por favor, ingrese una contrasena valida.')
            crear_usuario()
        else:
            print('''
        Por favor, confirme su contrasena ingresandola nuevamente.
        ''')
            segunda_contrasena = input('>>> ')
            if segunda_contrasena != primera_contrasena:
                print('Las contrasenas no coinciden.')
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
                    users_nuevo.write(json.dumps(users_list))
                print('El usuario ha sido creado exitosamente. Por favor, inicie sesion para confirmar el usuario.')
                iniciar_sesion()

#A continuacion iremos creando todas las funciones que seran utilizadas por cualquiera de los usuarios.
#Creamos la funcion que mostrara todos los objetos de una lista. Tendra un parametro, que es la lista sobre la cual se va a iterar.
def mostrar_productos (lista):
    print('''
        ###### A continuacion, se mostraran todos los productos en stock ######
        ''')
    print('::N°:: ::Codigo:: ::Nombre del producto::  ::Categoria:: ::Stock Disponible:: ::Es Nacional::')
    indice = 1
    for producto in lista:
        if producto['esNacional']:
            print(f'::{indice}:: ::{producto["codigo"]}:: ::{producto["nombre"]}:: ::{producto["categoria"]}:: ::{producto["cantidad"]}:: ::Producto Nacional::')
            indice = indice + 1
        else:
            print(f'::{indice}:: ::{producto["codigo"]}:: ::{producto["nombre"]}:: ::{producto["categoria"]}:: ::{producto["cantidad"]}:: ::Producto Importado::')
            indice = indice + 1

#Creamos la funcion que mostrara todos los objetos de una lista, si 'esNacional' cumple con el parametro dado. Tendra dos parametros.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo es para indicar si el valor de 'esNacional' debe ser True o False.
def filtrar_productos_esNacional (lista,valor):
    print('::Codigo:: ::Nombre del producto::  ::Categoria:: ::Stock Disponible::')
    for producto in lista:
        if producto['esNacional'] == valor:
            print(f'::{producto["codigo"]}:: ::{producto["nombre"]}:: ::{producto["categoria"]}:: ::{producto["cantidad"]}::')

#Creamos la funcion que mostrara todos los objetos de una lista, si 'categoria' cumple con el parametro dado. Tendra dos parametros dados.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo es para indicar el valor con el cual se filtraran los resultados.
def filtrar_productos_categoria (lista,valor):
    print('::Codigo:: ::Nombre del producto::  ::Categoria:: ::Stock Disponible::')
    for producto in lista:
        if producto['categoria'] == valor:
            print(f'::{producto["codigo"]}:: ::{producto["nombre"]}:: ::{producto["categoria"]}:: ::{producto["cantidad"]}::')

#Creamos la funcion que permitira al usuario elegir la categoria por la cual filtrar los resultados. Tendra dos parametros.
#El primero es para elegir la lista sobre la cual se va a iterar. El segundo, es para indicar a que menu debera volver.
def filtrar_productos_menu (lista,menuAnterior):
    print('''
        ######### Filtrar por Categoria ##########
        [1] Mostrar productos de la Categoria Herramientas.
        [2] Mostrar productos de la Categoria Casa.
        [3] Mostrar productos de la Categoria Bazaar.
        [0] Volver al Menu Anterior.
        ''')
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de la Categoria Herramientas ######
        ''')
        filtrar_productos_categoria(lista,"Herramienta")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '2':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de la Categoria Casa ######
        ''')
        filtrar_productos_categoria(lista,"Casa")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '3':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de la Categoria Bazaar ######
        ''')
        filtrar_productos_categoria(lista,"Bazaar")
        filtrar_productos_menu(lista,menuAnterior)
    elif decision == '0':
        menuAnterior()
    else:
        print('>>>> Por favor, ingrese una opcion valida')
        filtrar_productos_menu(lista,menuAnterior)

#Creamos la funcion que permitira al usuario buscar un producto segun el parametro deseado. Se creara una lista, se la imprimira y se la retornara, para ser utilizada en otras funciones (agregar_carrito).
def buscar_productos (lista,llave):
    print(f'''
        ###### Por favor, ingrese el {llave} del producto deseado. ######
        ''')
    decision = input('>>> ').lower()
    productos_encontrados = []
    for producto in lista:
        if  decision in producto[llave].lower():
            productos_encontrados.append({"codigo": producto["codigo"],"nombre" : producto["nombre"],"categoria": producto["categoria"],"cantidad": producto["cantidad"]})
    if len(productos_encontrados) == 0:
        print('No hemos encontrado ningun resultado para su busqueda. Por favor, intentelo nuevamente.')
        buscar_productos(lista,llave)
    else:
        indice = 1
        print('''
            ########## Su busqueda ha arrojado los siguientes resultados ##########
            ''')
        print('::N°:: ::Codigo:: ::Nombre del producto::  ::Categoria:: ::Stock Disponible::')
        for producto_encontrado in productos_encontrados:
            print(f'::{indice}:: ::{producto_encontrado["codigo"]}:: ::{producto_encontrado["nombre"]}:: ::{producto_encontrado["categoria"]}:: ::{producto_encontrado["cantidad"]}::')
            indice = indice + 1
        return productos_encontrados

# Creamos la funcion que permitira al usuario agregar productos al carrito. En caso de no ingresar un numero,
# se atrapara el error con un except y se volvera a pedir el numero de producto. En caso de no colocar una opcion valida, se volvera a pedir el numero de producto. Se solicitara la cantidad de unidades deseadas
# y se haran las comprobaciones necesarias.
def agregar_carrito (lista,menuAnterior):
    global sesion_carrito
    print('''
        Ingrese el numero del producto que desea agregar al carrito. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>> ')
    if producto_elegido != 'x':
        try:
            producto_indice = int(producto_elegido)
            if producto_indice <= len(lista):
                print(f'Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}". Contamos con {lista[producto_indice - 1]["cantidad"]} unidades.')
                print('''
                Ingrese las unidades del producto que desea agregar al carrito. Si desea elegir otro producto, ingrese 'x':
                ''')
                producto_cantidad_elegida = input('>>> ')
                if producto_cantidad_elegida != 'x':
                    try:
                        producto_cantidad = int(producto_cantidad_elegida)
                        if producto_cantidad <= lista[producto_indice - 1]['cantidad'] :
                            print(f'Se han agregado al carrito {producto_cantidad} unidades de {lista[producto_indice - 1]["nombre"]}.')
                            sesion_carrito.append({"codigo": lista[producto_indice - 1]["codigo"],"nombre": lista[producto_indice - 1]["nombre"],"categoria": lista[producto_indice - 1]["categoria"],"cantidad_solicitada": producto_cantidad})
                            presupuestar_productos_menu(lista,opciones_registrado)
                        else:
                            print('No hay suficientes unidades en stock, por favor ingrese la cantidad nuevamente.')
                            agregar_carrito(lista,menuAnterior)
                    except ValueError:
                        print('Por favor, ingrese un numero valido.')
                        agregar_carrito(lista,menuAnterior)
                else:
                    agregar_carrito(lista,menuAnterior)
            else:
                print('Por favor, ingrese un producto valido')
                agregar_carrito(lista,menuAnterior)
        except ValueError:
            print('Por favor, ingrese una opcion valida.')
            agregar_carrito(lista,menuAnterior)
    else:
        menuAnterior()

#Creamos la funcion que permitira al usuario ver los productos que ha ingresado al carrito.
def mostrar_carrito ():
    if len(sesion_carrito) == 0:
        print('###### Aun no ha agregado productos a su carrito ######')
        opciones_registrado()
    else:
        indice = 1
        print('''
        ###### A continuacion, se mostraran todos los productos en su Carrito ######
        ''')
        print('::N°:: ::Codigo:: ::Nombre del producto:: ::Categoria:: ::Cantidad solicitada::')
        for producto in sesion_carrito:
            print(f'::{indice}:: ::{producto["codigo"]}:: ::{producto["nombre"]}:: ::{producto["categoria"]}:: ::{producto["cantidad_solicitada"]}::')
            indice = indice + 1

#Creamos una funcion que permita modificar el carrito una vez creado.
def modificar_carrito(lista,menuAnterior):
    print('''
        ###### Por favor, ingrese el numero del producto que quiere modificar. Si desea volver al menu anterior, ingrese 'x' ######
        ''')
    producto_elegido = input('>>> ')
    if producto_elegido != 'x':
        try:
            producto_indice = int(producto_elegido)
            if producto_indice <= len(sesion_carrito):
                print(f'''
                    En su carrito, usted tiene {sesion_carrito[producto_indice - 1]["cantidad_solicitada"]} unidades del producto "{sesion_carrito[producto_indice - 1]["nombre"]}". Elija una de las siguientes opciones
                    [1] Modificar la cantidad de unidades.
                    [9] Quitar este producto del carrito.
                    [cualquier tecla] Elegir otro producto.
                    ''')
                opcion_elegida = input('>>> ')
                if opcion_elegida == '1':
                    print('Por favor, ingrese la cantidad de unidades que desea.')
                    nuevas_unidades = input('>>> ')
                    try:
                        unidades = int(nuevas_unidades)
                        sesion_carrito[producto_indice - 1]["cantidad_solicitada"] = unidades
                        print(f'Ahora, en su carrito, usted tiene {sesion_carrito[producto_indice - 1]["cantidad_solicitada"]} unidades del producto "{sesion_carrito[producto_indice - 1]["nombre"]}".')
                        presupuestar_productos_menu(lista,menuAnterior)
                    except ValueError:
                        print('Por favor, ingrese un numero valido.')
                        modificar_carrito(lista,menuAnterior)
                elif opcion_elegida == '9':
                    del sesion_carrito[producto_indice - 1]
                    print(f'Se ha eliminado el producto de su carrito.')
                    presupuestar_productos_menu(lista,menuAnterior)
                else:
                    modificar_carrito(lista,menuAnterior)
            else:
                print('Por favor, ingrese un producto valido.')
                modificar_carrito(lista,menuAnterior)
        except ValueError:
            print('Por favor, ingrese una opcion valida.')
            modificar_carrito(lista,menuAnterior)
    else:
        presupuestar_productos_menu(lista,menuAnterior)

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
    carritos_nuevo.write(json.dumps(carritos_list))
    print('''
        ########## Su carrito ha sido guardado exitosamente. Le enviaremos un mail con el presupuesto por el mismo. ##########
        ##########                         Gracias por haber utilizado nuestro programa                             ##########
        ''')

#Creamos la funcion que permitira al usuario buscar productos, agregar productos al carrito, modificar el carrito y guardar y enviar el carrito.
def presupuestar_productos_menu (lista,menuAnterior):
    print('''
        ######### Presupuestar ##########
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
        mostrar_productos(lista)
        agregar_carrito(lista,menuAnterior)
    elif decision == '2':
        productos_encontrados = buscar_productos (lista,'codigo')
        agregar_carrito(productos_encontrados,presupuestar_productos_menu)
        presupuestar_productos_menu(lista,menuAnterior)
    elif decision == '3':
        productos_encontrados = buscar_productos (lista,'nombre')
        agregar_carrito(productos_encontrados,presupuestar_productos_menu)
        presupuestar_productos_menu(lista,menuAnterior)
    elif decision == '4':
        mostrar_carrito()
        presupuestar_productos_menu(lista,menuAnterior)
    elif decision == '5':
        mostrar_carrito()
        if len(sesion_carrito) > 0:
            modificar_carrito(lista,menuAnterior)
        else:
            presupuestar_productos_menu(lista,menuAnterior)
    elif decision == '6':
        if len(sesion_carrito) > 0:
            guardar_carrito()
        else:
            print('Su carrito aun esta vacio.')
            presupuestar_productos_menu(lista,menuAnterior)
    elif decision == '0':
        menuAnterior()
    else:
        print('>>>> Por favor, ingrese una opcion valida')
        presupuestar_productos_menu(lista,menuAnterior)

#Creamos la funcion que permita al usuario modificar las cantidades de los productos.
def modificar_producto (lista,menuAnterior):
    print('''
        Ingrese el numero del producto del que desea modificar la cantidad. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>> ')
    if producto_elegido == 'x':
        crud_producto_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(lista) or producto_indice <= 0:
                print('Por favor, ingrese un producto valido')
                modificar_producto(lista,menuAnterior)
            else:
                print(f'Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}". Cuenta con {lista[producto_indice - 1]["cantidad"]} unidades.')
                print('''
                Ingrese las unidades actuales del producto. Si desea elegir otro producto, ingrese 'x':
                ''')
                producto_cantidad_elegida = input('>>> ')
                if producto_cantidad_elegida == 'x':
                    modificar_producto(lista,menuAnterior)
                else:
                    if producto_cantidad_elegida.isdigit():
                        lista[producto_indice - 1]['cantidad'] = producto_cantidad_elegida
                        with open('./stock.txt','w',encoding='utf-8') as lista_nueva:
                            lista_nueva.write(json.dumps(lista))
                        print(f'Se ha actualizado el stock de {lista[producto_indice - 1]["nombre"]}. Ahora cuenta con {producto_cantidad_elegida} unidades')
                        menuAnterior()
                    else:
                        print('Por favor, ingrese un numero valido.')
                        modificar_producto(lista,menuAnterior)
        except ValueError:
            print('Por favor, ingrese una opcion valida.')
            modificar_producto(lista,menuAnterior)

#Creamos la funcion que permita al usuario eliminar un producto.
def eliminar_producto (lista,menuAnterior):
    print('''
        Ingrese el numero del producto del que desea eliminar. Si desea volver al menu anterior, ingrese 'x':
        ''')
    producto_elegido = input('>>> ')
    if producto_elegido == 'x':
        crud_producto_menu(lista,menuAnterior)
    else:
        try:
            producto_indice = int(producto_elegido)
            if producto_indice > len(lista) or producto_indice <= 0:
                print('Por favor, ingrese un producto valido')
                eliminar_producto(lista,menuAnterior)
            else:
                print(f'Usted ha elegido el producto "{lista[producto_indice - 1]["nombre"]}"')
                print('''
                Para confirmar su eliminacion, presione 's'. Esta operacion no tiene vuelta atras. Si desea elegir otro producto, ingrese cualquier otra tecla:
                ''')
                decision = input('>>> ').lower()
                if decision != 's':
                    eliminar_producto(lista,menuAnterior)
                else:
                    del lista[producto_indice - 1]
                    with open('./stock.txt','w',encoding='utf-8') as lista_nueva:
                            lista_nueva.write(json.dumps(lista))
                    print(f'Se ha eliminado el producto satisfactoriamente.')
                    menuAnterior()
        except ValueError:
            print('Por favor, ingrese una opcion valida.')
            eliminar_producto(lista,menuAnterior)

#creamos la funcion que permita al usuario agregar un producto.
def agregar_producto (lista,menuAnterior):
    print('''
        Ingrese el codigo del nuevo producto. El mismo debe tener un formato de 'A99999'. Presione 'x' para volver al menu anterior.
        ''')
    codigo_ingresado = input('>>> ')
    if codigo_ingresado.lower() == 'x':
        menuAnterior()
    elif len(codigo_ingresado) != 6 or not codigo_ingresado[0].isupper() or not codigo_ingresado[1].isdigit() or not codigo_ingresado[2].isdigit() or not codigo_ingresado[3].isdigit() or not codigo_ingresado[4].isdigit() or not codigo_ingresado[5].isdigit():
        print('El formato del codigo no es el correcto. Por favor, ingrese el codigo con el formato "A99999".')
        agregar_producto(lista,menuAnterior)
    else:
        print('''
            Por favor, ingrese el nombre del producto.
            ''')
        nombre_ingresado = input('>>> ')
        print('''
            Por favor, ingrese la categoria del producto.
            ''')
        categoria_ingresada = input('>>> ')
        print('''
            Por favor, ingrese la cantidad de unidades en stock del producto.
            ''')
        cantidad_ingresada = input('>>> ')
        try:
            cantidad = int(cantidad_ingresada)
            if cantidad <= 0:
                print('Por favor, ingrese una cantidad de unidades valida.')
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
                            lista_nueva.write(json.dumps(lista))
                        print(f'Se ha anadido el producto satisfactoriamente.')
                        menuAnterior() 
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
                        lista_nueva.write(json.dumps(lista))
                        print(f'Se ha anadido el producto satisfactoriamente.')
                        menuAnterior() 
                else:
                    print('Por favor, ingrese una opcion valida.')
                    agregar_producto(lista,menuAnterior)
        except ValueError:
            print('Por favor, ingrese una cantidad de unidades valida.')
            agregar_producto(lista,menuAnterior)

#Creamos el menu en el que el usuario podra acceder a las opciones relacionadas a la actualizacion, eliminacion o agregado de productos.
def crud_producto_menu (lista, menuAnterior):
    print('''
        ######### Menu de Productos ##########
        [1] Modificar la cantidad de unidades en stock de un producto.
        [2] Eliminar un producto.
        [3] Agregar nuevo producto.
        [0] Volver al Menu Anterior.
        ''')
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        mostrar_productos(lista)
        modificar_producto(lista,menuAnterior)
    elif decision == '2':
        mostrar_productos(lista)
        eliminar_producto (lista,menuAnterior)
        crud_producto_menu(lista, menuAnterior)
    elif decision == '3':
        agregar_producto (lista,menuAnterior)
        crud_producto_menu(lista, menuAnterior)
    elif decision == '0':
        menuAnterior()
    else:
        print('>>>> Por favor, ingrese una opcion valida')
        crud_producto_menu(lista, menuAnterior)

#Creamos la funcion que mostrara los presupuestos a enviar y permitira al usuario eliminar aquellos que ya ha respondido.
def mostrar_presupuestos ():
    presupuestos = open('./carritos.txt','r',encoding='utf-8')
    presupuestos_lista = json.load(presupuestos)
    indice = 1
    for presupuesto in presupuestos_lista:
        print(f'''
            ###################### PRESUPUESTO {indice} ###########################
                        Nombre de Usuario: {presupuesto['username']}
                        Correo Electronico: {presupuesto['mail']}
            ::Codigo:: ::Nombre de Producto:: ::Categoria:: ::Cantidad::
            ''')
        for producto in presupuesto['productos']:
            print(f'''
            ::{producto['codigo']}:: ::{producto['nombre']}:: ::{producto['categoria']}:: ::{producto['cantidad_solicitada']}::
            ''')
        indice = indice + 1
    print('''
        ########## Desea eliminar algun presupuesto? ##########
        Si, asi lo desea, presione 's'. Sino, presione cualquier otra tecla.
        ''')
    decision = input('>>> ')
    if decision != 's':
        opciones_administrador()
    else:
        print('''
        ########## Por favor, ingrese el numero de presupuesto que desea eliminar ##########
        ''')
        numero_presupuesto_elegido = input('>>> ')
        try:
            numero_presupuesto = int(numero_presupuesto_elegido)
            if numero_presupuesto <= 0 or numero_presupuesto > indice - 1:
                print("Por favor, ingrese una opcion valida.")
                mostrar_presupuestos()
            else:
                print(f'''
            ########## Se eliminara el presupuesto {numero_presupuesto} ##########
            Si desea continuar, presione 's'. Sino, presione cualquier otra tecla.
                ''')
                confirmar_decision = input('>>> ')
                if confirmar_decision.lower() != 's':
                    mostrar_presupuestos()
                else:
                    del presupuestos_lista[numero_presupuesto - 1]
                    with open('./carritos.txt','w',encoding='utf-8') as nuevos_presupuestos:
                        nuevos_presupuestos.write(json.dumps(presupuestos_lista))
                    print('''
            ########## El presupuesto se ha eliminado satisfactoriamente. ##########
                    ''')
                    opciones_administrador()
        except ValueError:
            print("Por favor, ingrese una opcion valida.")
            mostrar_presupuestos()

#A continuacion crearemos un menu especializado para cada tipo de usuario.
#Creamos la funcion que mostrara las opciones en caso de ser un usuario de tipo invitado. Solamente podra ver los productos, filtrarlos y ver su stock.
def opciones_invitado ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print('''
        ############## Usuario Invitado##############
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
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        mostrar_productos(productos_lista)
        opciones_invitado()
    elif decision == '2':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Nacional ######
        ''')
        filtrar_productos_esNacional(productos_lista,True)
        opciones_invitado()
    elif decision == '3':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Importado ######
        ''')
        filtrar_productos_esNacional(productos_lista,False)
        opciones_invitado()
    elif decision == '4':
        filtrar_productos_menu(productos_lista,opciones_invitado)
    elif decision == '5':
        buscar_productos(productos_lista,'codigo')
        opciones_invitado()
    elif decision == '6':
        buscar_productos(productos_lista,'nombre')
        opciones_invitado()
    elif decision == '0':
        menu_principal()
    elif decision == 'x':
        print('Gracias por haber utilizado nuestro programa.')
    else:
        print('Por favor, ingrese una opcion valida.')
        opciones_invitado()

#Creamos la funcion que mostrara las opciones en caso de ser un usuario registrado. Podra ver los productos, filtrarlos y ver su stock. Ademas, podra agregar productos a un carrito.
def opciones_registrado ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print('''
        ############## Usuario Registrado##############
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
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        mostrar_productos(productos_lista)
        opciones_registrado()
    elif decision == '2':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Nacional ######
        ''')
        filtrar_productos_esNacional(productos_lista,True)
        opciones_registrado()
    elif decision == '3':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Importado ######
        ''')
        filtrar_productos_esNacional(productos_lista,False)
        opciones_registrado()
    elif decision == '4':
        filtrar_productos_menu(productos_lista,opciones_registrado)
    elif decision == '5':
        buscar_productos(productos_lista,'codigo')
        opciones_registrado()
    elif decision == '6':
        buscar_productos(productos_lista,'nombre')
        opciones_registrado()
    elif decision == '7':
        presupuestar_productos_menu(productos_lista,opciones_registrado)
    elif decision == '0':
        print('Gracias por haber utilizado nuestro programa.')
    else:
        print('Por favor, ingrese una opcion valida.')
        opciones_registrado()

#Creamos la funcion que mostrara las opciones en caso de ser un usuario administrador. Podra ver los productos, filtrarlos y ver su stock. Ademas, podra agregar productos a un carrito.
def opciones_administrador ():
    productos = open('./stock.txt','r',encoding='utf-8')
    productos_lista = json.load(productos)
    print('''
        ############## Usuario Administrador ##############
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
    decision = input('>>> La opcion elegida es: ')
    if decision == '1':
        mostrar_productos(productos_lista)
        opciones_administrador()
    elif decision == '2':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Nacional ######
        ''')
        filtrar_productos_esNacional(productos_lista,True)
        opciones_administrador()
    elif decision == '3':
        print('''
        ###### A continuacion, se mostraran todos los productos en stock de origen Importado ######
        ''')
        filtrar_productos_esNacional(productos_lista,False)
        opciones_administrador()
    elif decision == '4':
        filtrar_productos_menu(productos_lista,opciones_administrador)
        opciones_administrador()
    elif decision == '5':
        buscar_productos(productos_lista,'codigo')
        opciones_administrador()
    elif decision == '6':
        buscar_productos(productos_lista,'nombre')
        opciones_administrador()
    elif decision == '7':
        crud_producto_menu(productos_lista, opciones_administrador)
    elif decision == '8':
        mostrar_presupuestos()
    elif decision == '0':
        print('Gracias por haber utilizado nuestro programa.')
    else:
        print('Por favor, ingrese una opcion valida.')
        opciones_administrador()

#Creamos la funcion que mostrara el menu de entrada y nos derivara a la opcion correspondiente dependiendo de la eleccion del usuario.
def menu_principal():
    print('''
                        #####################################
                        #####################################
                        #           FERRETERIA              #
                        #               LO                  #
                        #             PRESTI                #
                        #####################################
                        #####################################
    
    ////////// Bienvenido a nuestro programa. Podras ver todos nuestros productos, filtrarlos por categoria o buscar por nombre y codigo. \\\\\\\\\\
    ////////// Puedes entrar como invitado, pero si inicias sesion, podras acceder tambien a la posibilidad de solicitarnos un presupuesto. \\\\\\\\\\
    [1] Continuar como invitado.
    [2] Iniciar Sesion.
    [3] Crear un nuevo usuario.
    [0] Cerrar el programa.
        ''')
    decision = input('>>> ')
    if decision == '1':
        opciones_invitado()
    elif decision == '2':
        iniciar_sesion()
    elif decision == '3':
        crear_usuario()
    elif decision == '0':
        print('Gracias por haber utilizado nuestro programa.')

#Ejecutamos la funcion para que funcione el programa.
menu_principal()