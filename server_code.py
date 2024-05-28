#!/usr/bin/env python3
"""Traccia 1: Sistema di Chat Client-Server.
Implementare un sistema di chat client-server in Python utilizzando
socket programming. Il server deve essere in grado di gestire più
client contemporaneamente e deve consentire agli utenti di inviare
e ricevere messaggi in una chatroom condivisa. Il client deve consentire
agli utenti di connettersi al server, inviare messaggi alla chatroom e
ricevere messaggi dagli altri utenti.
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging

# Configurazione del logger
def configura_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def accetta_connessioni_in_entrata(code="utf8"):
    """la funzione accetta le connessioni del client in entrata"""
    while True:
        try:
            client, client_add = SERVER.accept()
            logging.info("Connessione da %s:%s", client_add[0], client_add[1])
            client.send(bytes("Immettere nome:", code))
            indirizzi[client] = client_add
            Thread(target=amministra_client, args=(client,)).start()
            
        except Exception as e:
            logging.error("Errore nell'accettazione delle connessioni: %s", e)
            break

def broadcast(x, prefisso="", code="utf8"):
    """Invia un messaggio in broadcast a tutti i client"""
    for single_client in clients:
        try:
            single_client.send(bytes(prefisso, code)+x)
        except Exception as e:
            logging.error("Errore nell'invio del messaggio a %s: %s", clients[single_client], e)
            single_client.close()
            del clients[single_client]
        
def amministra_client(client, code="utf8"):
    """Gestisce i client connessi"""
    try:
        user = client.recv(BUFSIZ).decode(code)
        inizio = 'La connessione con %s è stata stabilita. !off per uscire.' % user
        client.send(bytes(inizio, code))
        msg = "%s si è unito alla chat!" % user
        broadcast(bytes(msg, code))
        clients[client] = user
   
        while True:
            msg = client.recv(BUFSIZ)
            
            if msg != bytes("!off", code):
                broadcast(msg, user+": ")
            else:
                client.send(bytes("!off", code))
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la Chat." % user, code))
                break
    except Exception as e:
        logging.error("Errore nella gestione del client: %s", e)
        client.close()
        if client in clients:
            del clients[client]


configura_logger()

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    logging.info("Attendendo connessioni...")
    try:
        ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except KeyboardInterrupt:
        logging.info("Chiusura server...")
    finally:
        SERVER.close()
