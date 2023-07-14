#LIBRERIE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 

from PyQt6 import uic, QtWidgets,QtCore
import sys
import time
import threading
import os 

radice_percorso = os.getcwd() #Cerca le risorse nella stessa cartella del file. #N.B. Eseguire lo script nella sua cartella.

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        uic.loadUi(radice_percorso+"/seccatore_UI.ui",self)
        self.Fatto_pulsante.clicked.connect(self.analisi)
        self.setStyleSheet("background-image: url("+radice_percorso+"/sfondo.svg);")
        self.invio = False

    #ANALISI input utente e aprtura browser
    def analisi(self):
        print("Pulsante premuto")
        self.contatto = self.Contatto.text()
        self.messaggio = self.Messaggio.text()
        self.elemento_xpath = '//*[@title="'+self.contatto+'"]' #Percorso XPATH relativo
        try:
            self.intervallo = float(self.Intervallo.text()) 
        except ValueError:
            print("Intervallo non valido, imposto configurazione standard")
            self.intervallo = 1.0
        print(self.contatto,self.messaggio,self.intervallo)

        #APERTURA BROWSER
        self.driver = webdriver.Chrome()
        self.driver.get("https://web.whatsapp.com/")

        #TROVA CONTATTO E INVIA MESSAGGIO
        if not self.invio:
            self.invio = True
            threading.Thread(target=self.invia_messaggio).start()

    #TROVA elementi
    def invia_messaggio(self):
        while self.invio:
            try:    
                chat=self.driver.find_element(By.XPATH,self.elemento_xpath)
                print("TROVATO")
                self.driver.minimize_window()
                chat.click()
                barra = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
                barra.click()
                barra.send_keys(self.messaggio)
                barra.send_keys(Keys.ENTER)
            except:
                print(f"Elemento {self.elemento_xpath} non trovato")
            time.sleep(self.intervallo)

    
    def closeEvent(self,event): #Alla chiusura
        self.invio=False
        if self.driver is not None:
            self.driver.quit()
        event.accept() #Chiusura completata
    
                  

#CONFIGURAZIONE
app = QtWidgets.QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.setFixedSize(905,291)
mainWindow.setWindowTitle("Spammer")
mainWindow.show()
sys.exit(app.exec())