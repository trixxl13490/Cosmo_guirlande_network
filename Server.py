import socket
import select
import threading
import time
from PyQt5 import QtCore


############################################
# Server
############################################
class Server(threading.Thread):

    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.message = 'message'
        self.to_send = 'cosmoguirlande,blackout'
        self.ticks = 200
        self.ticks_clock = False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        self.checkup = ''

    def recurring_timer(self):
        self.ticks_clock = not self.ticks_clock

    def run(self):
        while 1:
            try:
                # construction socket
                server_pi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # connexion socket avec bind, choix de port entre 1024 et 65535, ici 50000
                server_pi.bind((self.TCP_IP, self.TCP_PORT))

                # ecoute socket, 5 pour limite connexion
                server_pi.listen(5)
                print("Le serveur écoute à présent sur le port {}".format(self.TCP_PORT))

                # creation booleen & liste client
                server_on = True
                clients_connectes = []

                # test reussite connexion
                # print(infos_connexion)
                # Reception donnees
                while server_on:
                    # On va verifier que de nouveaux clients ne demandent pas a se connecter
                    # Pour cela, on ecoute la connexion_principale en lecture
                    # On attend maximum 50ms
                    connexions_demandees, wlist, xlist = select.select([server_pi], [], [], 0.05)
                    for connexion in connexions_demandees:
                        # acceptation du client, renvoi le socket qui va nous permettre de communiquer (porte de
                        # sortie du serveur, et le tuple du client
                        connexion_avec_client, infos_connexion = connexion.accept()
                        # On ajoute le socket connecté à la liste des clients
                        clients_connectes.append(connexion_avec_client)
                    # Maintenant, on ecoute la liste des clients connectes
                    # Les clients renvoyes par select sont ceux devant etre lus (recv)
                    # On attend la encore 50ms maximum
                    # On enferme l'appel à select.select dans un bloc try
                    # En effet, si la liste de clients connectes est vide, une exception
                    # Peut être levee
                    clients_a_lire = []
                    try:
                        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
                    except select.error:
                        pass
                    else:
                        # On parcourt la liste des clients a lire
                        for client in clients_a_lire:
                            # Client est de type socket
                            msg_recu = client.recv(self.BUFFER_SIZE)
                            # Peut planter si le message contient des caractères spéciaux
                            msg_recu = msg_recu.decode()
                            self.message = msg_recu
                            print("message reçu :", self.message)
                            msg = bytes(self.to_send, encoding='utf8')
                            if self.to_send != self.checkup:
                                self.checkup = msg
                                client.send(msg)
                            else:
                                pass

                # fermeture des connexions client en premier serveur en second
                print("Fermeture des connexions")
                for client in clients_connectes:
                    client.close()
                server_pi.close()
            except ConnectionResetError:
                server_pi.close()
                pass
            except ConnectionAbortedError:
                server_pi.close()
                pass
