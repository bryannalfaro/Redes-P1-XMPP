from ClientSide import *
from Authentication import *

import asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=ClientChat.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()
    flag = True
    logging.basicConfig(level=args.loglevel,format='%(levelname)-8s %(message)s')
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)-8s %(message)s')
    while flag:
        print("_______________________________________________")
        print("Bienvenido al chat :)")
        print("Selecciona una opcion: ")
        print("1. Iniciar sesion")
        print("2. Registrar cuenta")
        print("3. Salir\n")
        opcion = int(input(">> "))
        print("_______________________________________________")

        if opcion == 1:
            jid = input("Ingresa tu username: ")
            password = getpass("Ingresa tu contraseña: ")
            print("Intentando conectar...\n")
            client = ClientChat(jid, password)
            client.connect(disable_starttls=True)
            client.process(forever=False)
            print("Conectado con exito :)")
            print("_______________________________________________")
            option_client = second_menu()
            while option_client != 3:
                if option_client == 1:
                    print("Eliminar usuario")
                    print(jid, password)
                    client = DeleteUsersChat(jid, password)
                    client.connect(disable_starttls=True)
                    client.process(forever=False)
                    client.disconnect()

                    flag = False
                    break

        elif opcion == 2:
            jid = input("Ingresa el username que deseas : ")
            password = getpass("Ingresa tu contraseña: ")
            print("Intentando registrar...\n")
            client = RegisterChat(jid, password)
            client['xep_0077'].force_registration = True


            client.connect()
            client.process(forever=False)
            print("Registrado con exito :)")
            option_client = third_menu()

            if option_client ==1:
                opcion = option_client
            else:
                exit(1)
            print("_______________________________________________")

        elif opcion == 3:
            print("Gracias por usar el chat :)")
            print("_______________________________________________")
            exit()
        else:
            print("Opcion invalida")
            print("_______________________________________________")
            exit()

