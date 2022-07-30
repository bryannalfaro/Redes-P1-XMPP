
from ClientSide import *
from Authentication import *

import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    parser = ArgumentParser(description=ClientChat.__doc__)
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()
    flag = True

    #logging.basicConfig(level=args.loglevel,format='%(levelname)-8s %(message)s')
    #logging.basicConfig(level=logging.DEBUG,format='%(levelname)-8s %(message)s')

    register_choice = 0
    while flag:
        if register_choice == 0:
            print("_______________________________________________")
            print("Bienvenido al chat :)")
            print("Selecciona una opcion: ")
            print("1. Iniciar sesion")
            print("2. Registrar cuenta")
            print("3. Salir\n")
            opcion = int(input(">> "))
            print("_______________________________________________")
        else:
            opcion = register_choice

        if opcion == 1:
            jid = input("Ingresa tu username: ")
            jid = jid+"@alumchat.fun"
            password = getpass("Ingresa tu contraseña: ")
            print("Intentando conectar...\n")
            client = ClientChat(jid, password)
            client.connect(disable_starttls=True)

            client.process(forever=False)
            if client.FLAG_AUTH==0:
                print("Error de autenticacion")
            if client.TERMINATE_USER == 1:
                flag = False
            if client.TERMINATE_USER == 2:
                print("Eliminar usuario")
                print(jid, password)
                client = DeleteUsersChat(jid, password)
                client.connect(disable_starttls=True)
                client.process(forever=False)
                client.disconnect()
                flag = False
            '''if flag:
                client_flag = True
                print("Conectado con exito :)")
                print("_______________________________________________")
            else:
                client_flag = False
                print("Error de autenticacion :(")
                print("_______________________________________________")
            while client_flag:
                option_client = second_menu()
                if option_client == 7:
                    print("Eliminar usuario")
                    print(jid, password)
                    client = DeleteUsersChat(jid, password)
                    client.connect(disable_starttls=True)
                    client.process(forever=False)
                    client.disconnect()
                    flag = False
                    client_flag = False
                elif option_client == 8:
                    client_flag = False'''

        elif opcion == 2:
            jid = input("Ingresa el username que deseas : ")
            jid = jid+"@alumchat.fun"
            password = getpass("Ingresa tu contraseña: ")
            print("Intentando registrar...\n")
            client = RegisterChat(jid, password)
            client['xep_0077'].force_registration = True
            client.connect()
            client.process(forever=False)
            print("Registrado con exito :)")
            flag = False
            '''option_client = third_menu()

            if option_client ==1:
                register_choice = option_client
            else:
                register_choice = option_client+1'''

        elif opcion == 3:
            print("Gracias por usar el chat :)")
            print("_______________________________________________")
            exit()
        else:
            print("Opcion invalida")
            print("_______________________________________________")
            exit()

