#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
import logging

# Configura il logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ricezione_messaggi():
    """Funzione per ricevere messaggi dal server."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if not msg:
                break
            msg_list.insert(tk.END, msg)
        except OSError: 
            logging.info("Connessione chiusa.")
            break

def invia_messaggi(event=None):
    """Funzione per inviare messaggi al server."""
    mex = my_msg.get()
    my_msg.set("")
    try:
        client_socket.send(bytes(mex, "utf8"))
        if mex == "!off":
            client_socket.close()
            pannello.quit()
    except OSError:
        logging.error("Errore (invio messaggio)")

def on_closing(event=None):
    """Funzione chiamata quando si chiude la finestra."""
    my_msg.set("!off")
    invia_messaggi()

#creo la finestra principale
pannello = tk.Tk()
pannello.title("Nuova conversazione")
pannello.configure(bg="lightblue")

#creo il campo di input per inviare i messaggi
frame_messaggi = tk.Frame(pannello, bg="lightblue")
my_msg = tk.StringVar()
my_msg.set("Scrivi qui.")
scrollbar = tk.Scrollbar(frame_messaggi)

msg_list = tk.Listbox(frame_messaggi, height=20, width=70, yscrollcommand=scrollbar.set, bg="white")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
frame_messaggi.pack()

entry_field = tk.Entry(pannello, textvariable=my_msg, bg="white")
entry_field.bind("<Return>", invia_messaggi)
entry_field.pack()

send_button = tk.Button(pannello, text="SEND", command=invia_messaggi, bg="lightgreen")
send_button.pack()

pannello.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Server host: ')
PORT = input('Porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#thread per ricevere i messaggi dal server
receive_thread = Thread(target=ricezione_messaggi)
receive_thread.start()

#avvio della gui
tk.mainloop()
