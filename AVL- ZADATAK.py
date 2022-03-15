import sys, os, pathlib
from PyQt5 import QtCore, QtWidgets

lista= []
podaci = []
polje = []
fizikalne_velicine = []
ime_datoteke = ''
odabrana_datoteka = ''
znakovi = ''
broj_datoteka = 0
redak = 0
stupac = 0
end = 0
nastavak = 0
brzina = 0
indeks = 0
brojilo = 0
kraj = 0
pocetak = 0
prethodni = 0

def popis():
    global broj_datoteka, ime_datoteke
    # WINDOWS - očitavanje i mjenjanje putanje direktorija
    os.chdir(os.getcwd()+'\\Data')
    # UBUNTU - očitavanje i mjenjanje putanje direktorija
    #os.chdir(os.getcwd()+'/Data')
    # definiranje putanje
    currentDirectory = pathlib.Path('.')
    # definiranje ekstenzije
    currentPattern = "*.GID"
    # učitavanje datoteke
    for currentFile in currentDirectory.glob(currentPattern):  
        ime_datoteke = str(currentFile)
        lista.append(ime_datoteke)
        broj_datoteka += 1
    return

def ucitavanje(ime):
    global podaci, brzina, redak, stupac, nastavak, end, indeks, brojilo, fizikalne_velicine, kraj, pocetak, prethodni
    # WINDOWS - putanja datoteke
    putanja = str(os.getcwd()+'\\'+ime)
    # UBUNTU - putanja datoteke
    #putanja = str(os.getcwd()+'/'+ime)
    file = open(putanja, 'r')
    #učitavanje podataka iz datoteke redak po redak
    for line in file:  
        podaci.append(line)
    for i in podaci:
        znakovi = i.upper()
        znakovi1 = znakovi.find('SPEED')
        if znakovi1 >= 0:
            brzina = float(znakovi[znakovi1+8:])
        znakovi2 = znakovi.find('CHANNEL')
        if znakovi2 >= 0 or nastavak == 1:
            stupac += znakovi.count(',')
            if znakovi.count('&') == 1:
                nastavak = 1
                razlika = stupac- prethodni
                prethodni = stupac
            else:
                stupac += 1
                razlika = stupac - prethodni
                nastavak = 0
            kraj = 0  
            for i in range(0, razlika):
                pocetak = znakovi.find("'", kraj)
                kraj = znakovi.find("'", pocetak+1)
                fizikalne_velicine.append(znakovi[pocetak+1:kraj])
                kraj += 1
        znakovi3 = znakovi.find('END')
        if znakovi3 >= 0 or end == 1:
            if end == 1:
                redak += 1
            else:
                global indeks
                indeks = brojilo + 1
                end = 1
        brojilo += 1
    file.close()
    
class Controller:
    def __init__(self):
        pass

    def show_initial(self):
        self.initial = InitialWindow()
        self.initial.switch_window.connect(self.show_main)
        self.initial.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.close()
        self.initial.close()
        self.window.show()

class InitialWindow(QtWidgets.QWidget):
    global odabrana_datoteka
    popis()
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = 'GIDAS Reader Visualizer - Initial Screen'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()
        layout = QtWidgets.QVBoxLayout()
        
    def createGridLayout(self):
        global odabrana_datoteka
        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1, 4)
        
        self.label = QtWidgets.QLabel('GIDAS File:')
        
        self.combo = QtWidgets.QComboBox(self)
        for i in range(0,broj_datoteka):
            ime_datoteke = lista[i]
            self.combo.addItem(str(ime_datoteke))
        self.combo.activated[str].connect(self.onActivated)
        odabrana_datoteka = lista[0]
        
        self.button = QtWidgets.QPushButton('Visualize')
        self.button.clicked.connect(self.initial)

        layout.addWidget(self.label,0,0)
        layout.addWidget(self.combo,0,1)
        layout.addWidget(self.button,1,0)
        self.setLayout(layout)
        
    def onActivated(self, text):
        global odabrana_datoteka
        odabrana_datoteka = text

    def initial(self):
        self.switch_window.emit()
        
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = 'GIDAS Reader Visualizer - Viewer'
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

    def createGridLayout(self):
        ucitavanje(odabrana_datoteka)
        
        self.createTable()
        
        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1,1)
        
        self.label = QtWidgets.QLabel('Speed:')
        
        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)
        
        layout1 = QtWidgets.QGridLayout()
        self.horizontalGroupBox = QtWidgets.QGroupBox()
        self.textbox = QtWidgets.QLabel(str(brzina))
        layout1.addWidget(self.textbox)
        self.horizontalGroupBox.setLayout(layout1)

        layout.addWidget(self.label,0,0)
        layout.addWidget(self.horizontalGroupBox,0,1)
        layout.addWidget(self.tableWidget,1,1)
        layout.addWidget(self.button,2,0)
        self.setLayout(layout)
        
    def createTable(self):
        global polje, stupac
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(redak)
        self.tableWidget.setColumnCount(stupac)
        self.tableWidget.setHorizontalHeaderLabels(fizikalne_velicine)
        for i in range(indeks, len(podaci)):
            polje.clear()
            polje.extend(podaci[i].split())
            for j in range(0, stupac):
                self.tableWidget.setItem(i-indeks,j, QtWidgets.QTableWidgetItem(str(polje[j])))
                
    def switch(self):
        self.switch_window.emit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_initial()
    # WINDOWS
    sys.exit(app.exec_())
    # UBUNTU
    #app.exec_()

if __name__ == '__main__':
    main()