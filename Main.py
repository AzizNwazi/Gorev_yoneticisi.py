import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QFileDialog
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox
from PyQt5.QtGui import QColor,QFont ,QBrush

class GorevYoneticisi(QWidget): #Qwidget sınıfından kalıtım
    def __init__(self):
        super().__init__()

        # Görev listesi
        self.gorevler = []

        # Kullanıcı arayüzünü oluştur
        self.initUi()

    def initUi(self):

        # Pencere boyutunu ayarla
        self.setFixedSize(1000, 800)

        # Arayüz öğelerini oluştur
        self.gorev_alani = QLabel('Görev Yönetimi')
        self.gorev_girdi_alani = QLineEdit()
        self.ekle_butonu = QPushButton('Görev Ekle')
        self.gorev_listesi = QListWidget()
        self.tamamlandi_butonu = QPushButton('Görevi Tamamla ✓')
        self.sil_butonu = QPushButton('Görevi Sil')
        self.kaydet = QPushButton("Dosya Kaydet")
        self.temizle = QPushButton("Temizle")

        # Yazı tipini ve boyutunu ayarla
        font = QFont("Consolas", 12)  # Örnek: Consolas ya da Arial yazı tipi, 12 boyut
        self.gorev_alani.setFont(font)
        self.gorev_girdi_alani.setFont(font)
        self.ekle_butonu.setFont(font)
        self.gorev_listesi.setFont(font)
        self.tamamlandi_butonu.setFont(font)
        self.sil_butonu.setFont(font)
        self.kaydet.setFont(font)
        self.temizle.setFont(font)


        # Layout'ları oluştur ve eksenlere yerleştir , butonların ve nesnelerin ortalanmasını, esnemesini sağlar
        v_box = QVBoxLayout(self)
        v_box.addWidget(self.gorev_alani)

        h_box = QHBoxLayout()
        h_box.addWidget(self.gorev_girdi_alani)
        h_box.addWidget(self.ekle_butonu)

        v_box.addLayout(h_box)
        v_box.addWidget(self.gorev_listesi)

        h_box = QHBoxLayout()
        h_box.addWidget(self.tamamlandi_butonu)
        h_box.addWidget(self.sil_butonu)
        h_box.addWidget(self.kaydet)
        h_box.addWidget(self.temizle)

        v_box.addLayout(h_box)

        # Butonlara tıklama olaylarını bağla
        self.ekle_butonu.clicked.connect(self.ekle_fonk)
        self.tamamlandi_butonu.clicked.connect(self.tamamlandi_fonk)
        self.sil_butonu.clicked.connect(self.sil_fonk)
        self.gorev_listesi.itemClicked.connect(self.secili_gorevi_guncelle)
        self.kaydet.clicked.connect(self.dosya_kaydet)
        self.temizle.clicked.connect(self.tum_gorevleri_temizle)

        # Pencere arkaplan rengi
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(100, 200, 200))  # R, G, B değerleri
        self.setPalette(palette)

        # Uygulamayı başlat
        self.setWindowTitle('Görev Yöneticisi')
        self.show()

        self.tamamlandi_butonu.setStyleSheet('background-color: GREEN ; color: white;')

    # Yeni görev ekleme fonksiyonu
    def ekle_fonk(self):
        gorev_metni = self.gorev_girdi_alani.text().strip()

        if gorev_metni:
            self.gorevler.append({'text': gorev_metni, 'completed': False})
            self.gorev_listesini_guncelle()
            self.gorev_girdi_alani.clear()


    # Görevi tamamlama fonksiyonu
    def tamamlandi_fonk(self):
        secili_item = self.gorev_listesi.currentItem()

        if secili_item:
            index = self.gorev_listesi.row(secili_item)
            self.gorevler[index]['completed'] = True

            self.gorev_listesini_guncelle()


    # Görevi silme fonksiyonu
    def sil_fonk(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item:
            sonuc = QMessageBox.question(self, 'Uyarı', 'Seçili görevi silmek istiyor musunuz?',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if sonuc == QMessageBox.Yes:
                index = self.gorev_listesi.row(secili_item)
                del self.gorevler[index]
                self.gorev_listesini_guncelle()


    # Görev listesini güncelleme fonksiyonu
    def gorev_listesini_guncelle(self):
        self.gorev_listesi.clear()
        for gorev in self.gorevler:
            metin_itemi = f"[{'✓ Tamamlandı' if gorev['completed'] else '❑ Tamamlanmadı'}] {gorev['text']}"


            self.gorev_listesi.addItem(metin_itemi)


    # Seçili görevi güncelleme fonksiyonu
    def secili_gorevi_guncelle(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item:
            index = self.gorev_listesi.row(secili_item)
            gorev_metni = self.gorevler[index]['text']
            self.gorev_girdi_alani.setText(gorev_metni)


    # Tüm görevleri temizleme fonksiyonu
    def tum_gorevleri_temizle(self):
        sonuc = QMessageBox.question(self, 'Uyarı', 'Tüm görevleri silmek istiyor musunuz?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if sonuc == QMessageBox.Yes:
            self.gorevler.clear()
            self.gorev_listesini_guncelle()
            self.gorev_girdi_alani.clear()


    # Görevleri dosyaya kaydetme fonksiyonu
    def dosya_kaydet(self):
        dosya_ismi, _ = QFileDialog.getSaveFileName(self, "Dosya Kaydet", os.getenv("HOME"))

        try:
            with open(dosya_ismi, "w") as file:
                print("Kaydedilen Görevler:\n")
                for gorev in self.gorevler:

                    file.write(str(gorev))
                    file.write("\n")
                    print(gorev)

                for gorev in self.gorevler:
                    file.write(f"{gorev['text']}\n")

        except Exception as e:
            print(f"Dosya kaydederken bir hata oluştu: {e}")

# Uygulamayı başlat
app = QApplication(sys.argv)
gorevYoneticisi = GorevYoneticisi()
sys.exit(app.exec_())