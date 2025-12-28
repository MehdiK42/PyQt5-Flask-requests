from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Basit bir POST isteği ile çalışır
@app.route('/sorgula', methods=['POST'])
def veri_getir():
    # Gelen veriyi al (takim id'si)
    gelen = request.json
    aranan_no = int(gelen['takim_id'])
    
    # Listemizi hazırlayalım
    gidecek_veriler = []
    
    # Dosyayı her seferinde açıp okuyoruz (basit mantık)
    dosya = open('logs.json', 'r')
    loglar = json.load(dosya)
    dosya.close()
    
    # İç içe döngülerle veriyi buluyoruz
    for paket in loglar:
        if "konumBilgileri" in paket:
            konum_listesi = paket["konumBilgileri"]
            
            for iha in konum_listesi:
                # Eğer aradığımız takımsa listeye ekle
                if iha["takim_numarasi"] == aranan_no:
                    # Sadece lazım olanları alalım
                    veri = {}
                    veri["enlem"] = iha["iha_enlem"]
                    veri["boylam"] = iha["iha_boylam"]
                    veri["irtifa"] = iha["iha_irtifa"]
                    
                    gidecek_veriler.append(veri)

    # Eğer hiç veri bulamadıysa boş döner
    return jsonify(gidecek_veriler)

if __name__ == '__main__':
    app.run(port=5000)