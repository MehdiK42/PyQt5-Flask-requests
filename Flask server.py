from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/sorgula', methods=['POST'])
def veri_getir():
    
    gelen = request.json
    aranan_no = int(gelen['takim_id'])
    
    
    gidecek_veriler = []
    
   
    dosya = open('logs.json', 'r')
    loglar = json.load(dosya)
    dosya.close()
    
    
    for paket in loglar:
        if "konumBilgileri" in paket:
            konum_listesi = paket["konumBilgileri"]
            
            for iha in konum_listesi:
               
                if iha["takim_numarasi"] == aranan_no:
                    
                    veri = {}
                    veri["enlem"] = iha["iha_enlem"]
                    veri["boylam"] = iha["iha_boylam"]
                    veri["irtifa"] = iha["iha_irtifa"]
                    
                    gidecek_veriler.append(veri)

   
    return jsonify(gidecek_veriler)

if __name__ == '__main__':
    app.run(port=5000)