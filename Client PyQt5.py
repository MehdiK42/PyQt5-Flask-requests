from PyQt5.QtWidgets import *
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Uygulama(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uçuş Logu")
        self.setGeometry(100, 100, 800, 600)
        self.arayuz_hazirla()

    def arayuz_hazirla(self):
       
        layout = QVBoxLayout()
        
        
        self.etiket1 = QLabel("Takım Numarasını Giriniz:")
        layout.addWidget(self.etiket1)
        
        
        self.kutu = QLineEdit()
        layout.addWidget(self.kutu)
        
        
        self.buton = QPushButton("Verileri Getir ve Çiz")
        self.buton.clicked.connect(self.butona_basildi) 
        layout.addWidget(self.buton)
        
        
        self.bilgi_etiketi = QLabel("Sonuçlar burada yazacak...")
        layout.addWidget(self.bilgi_etiketi)
        
        
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)

    def butona_basildi(self):
        no = self.kutu.text()
        print("İstenen Takım:", no) 
        
        
        try:
            
            adres = "http://127.0.0.1:5000/sorgula"
            paket = {"takim_id": no}
            cevap = requests.post(adres, json=paket)
            
            veriler = cevap.json()
            
            
            if len(veriler) > 0:
                
                enlemler = []
                boylamlar = []
                irtifalar = []
                
                for v in veriler:
                    enlemler.append(v["enlem"])
                    boylamlar.append(v["boylam"])
                    irtifalar.append(v["irtifa"])
                
                
                yazi = "Toplam Veri Sayısı: " + str(len(veriler)) + "\n"
                yazi += "Başlangıç: " + str(enlemler[0]) + ", " + str(boylamlar[0]) + "\n"
                yazi += "Bitiş: " + str(enlemler[-1]) + ", " + str(boylamlar[-1])
                self.bilgi_etiketi.setText(yazi)
                
                
                self.fig.clear()
                ax = self.fig.add_subplot(111, projection='3d')
                
                
                ax.plot(boylamlar, irtifalar, enlemler, marker='o')
                ax.set_xlabel('Boylam')
                ax.set_ylabel('İrtifa')
                ax.set_zlabel('Enlem')
                
                self.canvas.draw()
            else:
                self.bilgi_etiketi.setText("Bu numaraya ait veri bulunamadı!")
                
        except:
            self.bilgi_etiketi.setText("Sunucuya bağlanılamadı veya bir hata oluştu.")


app = QApplication([])
pencere = Uygulama()
pencere.show()
app.exec_()