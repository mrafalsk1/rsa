from server import Server
from client import Client
import time
import threading


def main():
    print("[Iniciando] Executando Cliente e Servidor...")
    server = Server()
    threading.Thread(target=server.start).start()

    time.sleep(1)

    client = Client()
    print(client)
    if client.connect_to_server():
        client.register()
        client.close()


if __name__ == "__main__":
    main()
