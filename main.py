from flask import Flask ,jsonify ,render_template ,request ,redirect ,url_for ,session ,flash 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug .security import generate_password_hash ,check_password_hash 
from functools import wraps 
from tabloveri import tab ,listof 
from fordg2 import chck 
from ai import predict_image_pil 
from aiinf import predict_image_pilinfect 
import numpy as np 
from PIL import Image 
from io import BytesIO 
import matplotlib .pyplot as plt 
from algoalgort import grafik 
import base64 
import ast 
def bykalg (gorselgai ,gorselinf ,cvalglist ,titralglist ,clone30_titres =None ,clone30_cvs =None ,salmonella =None ):
    import ast 

    def safe_float (value ,default =0.0 ):
        if value is None :
            return default 
        try :
            if isinstance (value ,str ):

                value =value .strip ().replace ('%','').replace (',','.')
                if not value :
                    return default 
            return float (value )
        except (TypeError ,ValueError ):
            return default 

    gorselgaidict ={}
    gorselinfdict ={}

    try :
        if gorselgai and gorselgai .strip ():
            gorselgaidict =ast .literal_eval (gorselgai )
    except :
        pass 

    try :
        if gorselinf and gorselinf .strip ():
            gorselinfdict =ast .literal_eval (gorselinf )
    except :
        pass 

    ndv_score =0.0 
    try :
        print (f" gorselgaidict = {gorselgaidict}")
        print (f" gorselgaidict keys = {list(gorselgaidict.keys()) if gorselgaidict else 'boş'}")

        ndv_value =gorselgaidict .get ("NDV",None )
        print (f"NDV değeri = {ndv_value}, tip = {type(ndv_value)}")

        if ndv_value :
            if isinstance (ndv_value ,str ):
                ndv_str =ndv_value .replace ("%","").replace (" ","").strip ()
                ndv_percentage =safe_float (ndv_str ,0.0 )
                ndv_score =ndv_percentage /100.0 
                print (f"DEBUG bykalg: NDV string parse: '{ndv_value}' -> '{ndv_str}' -> {ndv_percentage}% -> {ndv_score}")
            else :
                ndv_score =safe_float (ndv_value ,0.0 )
                if ndv_score >1.0 :
                    ndv_score =ndv_score /100.0 
                print (f" NDV sayısal parse: {ndv_value} -> {ndv_score}")
        else :
            print (f" NDV değeri bulunamadı veya None/0")
    except (TypeError ,ValueError )as e :
        print (f"NDV skoru parse hatası: {e}, değer: {gorselgaidict.get('NDV', 'yok')}")
        import traceback 
        traceback .print_exc ()
        ndv_score =0.0 

    asi_isimleri =[
    "Clone30 18 hf","Clone30 25 hf","Clone30 57 hf",
    "Ma5 & 4/91 18 hf","Ma5 & 4/91 25 hf","Ma5 & 4/91 57 hf",
    "Nemovac 18 hf","Nemovac 57 hf",
    "AE 18 hf","CAV 18 hf",
    "IBD 10 hf","IBD 25 hf","IBD 57 hf",
    "REO 25 hf","REO 57 hf",
    "EDS 25 hf","EDS 57 hf"
    ]

    asi_gruplari ={
    "Ndv":[0 ,1 ,2 ],
    "Ibv":[3 ,4 ,5 ],
    "Art":[6 ,7 ],
    "Ae":[8 ],
    "Cav":[9 ],
    "Ibd":[10 ,11 ,12 ],
    "Reo":[13 ,14 ],
    "Eds":[15 ,16 ]
    }

    def tek_asi_analiz (asi_adi ,titre ,cv ):
        """Akış şemasına göre aşı analizi - Güncellenmiş versiyon"""
        rapor =f"{asi_adi}: "

        if titre is None or cv is None :
            return rapor +"Veri eksik\n"




        if titre ==0 :
            if cv ==2 :
                rapor +="Titre düşük, CV tutarsız. Aşılama homojen değil, antikor seviyesi olması gerekenin altında. Aşılama başarısız. YZ ile hastalık riski kontrol edilmeli.\n"
            elif cv ==1 :
                rapor +="Titre düşük, CV tutarlı. Aşılama yetersiz. Takip ve 7-10 gün sonra ELISA önerilir.\n"
            else :
                rapor +="Titre düşük, CV olması gerekenden düşük. Numune kalitesi yetersiz olabilir. Antikor seviyesi olması gereken aralıkta değildir.\n"

        elif titre ==1 :
            if cv ==2 :
                rapor +="Titre normal, CV tutarsız. Sürünün bir kısmı patojene maruz kalmış olabilir. Hastalık riski mevcuttur. YZ ile hastalık riski kontrol edilmeli.\n"
            elif cv ==1 :
                rapor +="Titre normal, CV tutarlı. Antikor seviyesi normal, aşılama başarılı.\n"
            else :
                rapor +="Titre normal, CV olması gerekenden düşük. Antikor seviyesi normal fakat numune kalitesi yetersiz olabilir.\n"

        elif titre ==2 :
            if cv ==2 :
                rapor +="Titre yüksek, CV tutarsız. Aşılama başarısız. Patojene maruz kalınmış olabilir. YZ ile hastalık riski kontrol edilmeli.\n"
            elif cv ==1 :
                rapor +="Titre yüksek, CV tutarlı. Yakın dönemde canlı attenüe aşı yapılmış olabilir. Sürü patojene maruz kalmış olabilir. Takip ve 7-10 gün sonra ELISA önerilir.\n"
            else :
                rapor +="Titre yüksek, CV olması gerekenden düşük. Aşı başarılıdır fakat takip önerilir.\n"
        else :
            rapor +="Veri eksik veya geçersiz.\n"

        return rapor 

    def algoritma_bazli_degerlendirme (titre ,cv ):
        """Güncellenmiş değerlendirme algoritması"""
        if titre is None or cv is None :
            return "Veri eksik veya geçersiz.",None 



        if titre ==0 :
            if cv ==2 :
                return "Titre düşük, CV tutarsız. Aşılama homojen değil, antikor seviyesi olması gerekenin altında. Aşılama başarısız. YZ ile hastalık riski kontrol edilmeli.","uyari"
            elif cv ==1 :
                return "Titre düşük, CV tutarlı. Aşılama yetersiz. Takip ve 7-10 gün sonra ELISA önerilir.","takip"
            else :
                return "Titre düşük, CV olması gerekenden düşük. Numune kalitesi yetersiz olabilir. Antikor seviyesi olması gereken aralıkta değildir.","numune_uyari"

        elif titre ==1 :
            if cv ==2 :
                return "Titre normal, CV tutarsız. Sürünün bir kısmı patojene maruz kalmış olabilir. Hastalık riski mevcuttur. YZ ile hastalık riski kontrol edilmeli.","uyari"
            elif cv ==1 :
                return "Titre normal, CV tutarlı. Antikor seviyesi normal, aşılama başarılı.","basarili"
            else :
                return "Titre normal, CV olması gerekenden düşük. Antikor seviyesi normal fakat numune kalitesi yetersiz olabilir.","numune_uyari"

        elif titre ==2 :
            if cv ==2 :
                return "Titre yüksek, CV tutarsız. Aşılama başarısız. Patojene maruz kalınmış olabilir. YZ ile hastalık riski kontrol edilmeli.","uyari"
            elif cv ==1 :
                return "Titre yüksek, CV tutarlı. Yakın dönemde canlı attenüe aşı yapılmış olabilir. Sürü patojene maruz kalmış olabilir. Takip ve 7-10 gün sonra ELISA önerilir.","takip"
            else :
                return "Titre yüksek, CV olması gerekenden düşük. Aşı başarılıdır fakat takip önerilir.","takip"
        else :
            return "Veri eksik veya geçersiz.",None 

    asi_detaylari =[]
    for grup ,indeksler in asi_gruplari .items ():
        for idx in indeksler :
            if idx <3 :

                if idx <len (clone30_titres )and idx <len (clone30_cvs )and idx <len (asi_isimleri ):
                    titre =clone30_titres [idx ]
                    cv =clone30_cvs [idx ]
                    asi_adi =asi_isimleri [idx ]

                    degerlendirme ,durum_tipi =algoritma_bazli_degerlendirme (titre ,cv )

                    asi_detaylari .append ({
                    'grup':grup ,
                    'isim':asi_adi ,
                    'titre':titre ,
                    'cv':cv ,
                    'titre_durum':degerlendirme ,
                    'cv_durum':"",
                    'durum_tipi':durum_tipi ,
                    'veri_var':titre is not None and cv is not None 
                    })
            else :

                list_idx =idx -3 
                if list_idx <len (titralglist )and list_idx <len (cvalglist )and idx <len (asi_isimleri ):
                    titre =titralglist [list_idx ]
                    cv =cvalglist [list_idx ]
                    asi_adi =asi_isimleri [idx ]

                    degerlendirme ,durum_tipi =algoritma_bazli_degerlendirme (titre ,cv )

                    asi_detaylari .append ({
                    'grup':grup ,
                    'isim':asi_adi ,
                    'titre':titre ,
                    'cv':cv ,
                    'titre_durum':degerlendirme ,
                    'cv_durum':"",
                    'durum_tipi':durum_tipi ,
                    'veri_var':titre is not None and cv is not None 
                    })


    clone30_dusuk_titre =0 
    clone30_yuksek_titre =0 
    clone30_yuksek_cv =0 
    clone30_toplam =0 

    for idx in [0 ,1 ,2 ]:
        if idx <len (clone30_titres )and idx <len (clone30_cvs ):
            titre =clone30_titres [idx ]
            cv =clone30_cvs [idx ]
            if titre is not None and cv is not None :
                clone30_toplam +=1 
                if titre ==0 :
                    clone30_dusuk_titre +=1 
                elif titre ==2 :
                    clone30_yuksek_titre +=1 
                if cv ==2 :
                    clone30_yuksek_cv +=1 

    clone30_risk_skoru =0.0 
    if clone30_toplam >0 :
        if clone30_dusuk_titre >0 :
            clone30_risk_skoru +=0.3 *(clone30_dusuk_titre /clone30_toplam )
        if clone30_yuksek_titre >0 :
            clone30_risk_skoru +=0.4 *(clone30_yuksek_titre /clone30_toplam )
        if clone30_yuksek_cv >0 :
            clone30_risk_skoru +=0.2 *(clone30_yuksek_cv /clone30_toplam )

    combined_ndv_score =max (ndv_score ,clone30_risk_skoru )

    titryrm ="Titre ve CV değerlendirmesi\n\n"
    for grup ,indeksler in asi_gruplari .items ():
        titryrm +=f"{grup} aşıları\n"
        for idx in indeksler :
            if idx <3 :

                if idx <len (clone30_titres )and idx <len (clone30_cvs )and idx <len (asi_isimleri ):
                    titryrm +=tek_asi_analiz (
                    asi_isimleri [idx ],
                    clone30_titres [idx ],
                    clone30_cvs [idx ]
                    )
            else :

                list_idx =idx -3 
                if list_idx <len (titralglist )and list_idx <len (cvalglist )and idx <len (asi_isimleri ):
                    titryrm +=tek_asi_analiz (
                    asi_isimleri [idx ],
                    titralglist [list_idx ],
                    cvalglist [list_idx ]
                    )

        if grup =="Ndv":
            titryrm +="\n--- NDV Değerlendirmesin"

            ndv_sonuclari =[]
            hastalik_supheli =False 

            for idx in [0 ,1 ,2 ]:
                if idx <len (clone30_titres )and idx <len (clone30_cvs )and idx <len (asi_isimleri ):
                    titre =clone30_titres [idx ]
                    cv =clone30_cvs [idx ]
                    asi_adi =asi_isimleri [idx ]

                    if titre is not None and cv is not None :
                        if titre ==0 :
                            if cv ==2 :
                                sonuc =f"{asi_adi}: Titre düşük, CV tutarsız. Aşılama homojen değil, antikor seviyesi olması gerekenin altında. Aşılama başarısız."
                                if ndv_score >0.5 :
                                    sonuc +=" YZ modeli tarafından Newcastle riski tespit edildi."
                                    hastalik_supheli =True 
                            elif cv ==1 :
                                sonuc =f"{asi_adi}: Titre düşük, CV tutarlı. Aşılama yetersiz. Takip ve 7-10 gün sonra ELISA önerilir."
                            else :
                                sonuc =f"{asi_adi}: Titre düşük, CV olması gerekenden düşük. Numune kalitesi yetersiz olabilir."

                        elif titre ==1 :
                            if cv ==2 :
                                sonuc =f"{asi_adi}: Titre normal, CV tutarsız. Sürünün bir kısmı patojene maruz kalmış olabilir. Hastalık riski mevcuttur."
                                if ndv_score >0.5 :
                                    sonuc +=" YZ modeli tarafından Newcastle riski tespit edildi."
                                    hastalik_supheli =True 
                            elif cv ==1 :
                                sonuc =f"{asi_adi}: Titre normal, CV tutarlı. Antikor seviyesi normal, aşılama başarılı."
                            else :
                                sonuc =f"{asi_adi}: Titre normal, CV olması gerekenden düşük. Antikor seviyesi normal fakat numune kalitesi yetersiz olabilir."

                        elif titre ==2 :
                            if cv ==2 :
                                sonuc =f"{asi_adi}: Titre yüksek, CV tutarsız. Aşılama başarısız. Patojene maruz kalınmış olabilir."
                                hastalik_supheli =True 
                            elif cv ==1 :
                                sonuc =f"{asi_adi}: Titre yüksek, CV tutarlı. Yakın dönemde canlı attenüe aşı yapılmış olabilir. Sürü patojene maruz kalmış olabilir. Takip ve 7-10 gün sonra ELISA önerilir."
                            else :
                                sonuc =f"{asi_adi}: Titre yüksek, CV olması gerekenden düşük. Aşı başarılıdır fakat takip önerilir."
                        else :
                            sonuc =f"{asi_adi}: Veri eksik veya geçersiz."

                        ndv_sonuclari .append (sonuc )

            for sonuc in ndv_sonuclari :
                titryrm +=f"{sonuc}\n"

            ndv_value_raw =gorselgaidict .get ("NDV",None )
            if ndv_value_raw :
                titryrm +=f"\nGaita AI Analizi: NDV Skoru {ndv_value_raw if isinstance(ndv_value_raw, str) else f'%{ndv_value_raw*100:.1f}'}\n"
                if ndv_score >0.5 :
                    titryrm +="  AI Değerlendirmesi: Yüksek risk tespit edildi.\n"
                    hastalik_supheli =True 
                elif ndv_score >0.3 :
                    titryrm +="  AI Değerlendirmesi: Orta risk tespit edildi.\n"
                elif ndv_score >0 :
                    titryrm +="  AI Değerlendirmesi: Düşük risk.\n"

            titryrm +="\n--- Genel Değerlendirme ---\n"

            if not ndv_sonuclari :
                titryrm +="Değerlendirme için yeterli veri bulunmamaktadır.\n"
            elif hastalik_supheli or ndv_score >0.5 :
                titryrm +="  - Sürü izolasyonu düşünülmeli\n"
                titryrm +="  - Veteriner hekim konsültasyonu gerekli\n"
                titryrm +="  - Aşılama programı gözden geçirilmeli\n"
            elif ndv_score >0.3 or any ("Titre düşük"in s or "Titre yüksek"in s for s in ndv_sonuclari ):
                titryrm +="  - 7-10 gün içinde ELISA testi yapılmalı\n"
                titryrm +="  - Aşılama programı kontrol edilmeli\n"
                titryrm +="  - Sürü gözlemi artırılmalı\n"
            elif any ("Aşılama başarılı"in s for s in ndv_sonuclari )and not hastalik_supheli and ndv_score <=0.3 :
                titryrm +="Aşılama başarılı görünüyor. Rutin takip yeterli.\n"
            else :
                titryrm +="Değerlendirme tamamlandı. Rutin takip önerilir.\n"

            titryrm +="\n"

    titryrm1 ="Görsel değerlendirme\n"

    if gorselgaidict :
        for hastalik ,s in sorted (
        gorselgaidict .items (),
        key =lambda x :safe_float (x [1 ]),
        reverse =True 
        ):
            s =safe_float (s )

            if s >0.5 :
                durum ="Yüksek risk"
            elif s >0.3 :
                durum ="Orta risk"
            else :
                durum ="Düşük risk"

            titryrm1 +=f"{hastalik}: %{s*100:.1f} – {durum}\n"
    else :
        titryrm1 +="Patolojik bulgu saptanmadı\n"

    cvyrm ="\nCV özeti\n"
    for i ,cv in enumerate (cvalglist ):
        asi_idx =i +3 
        if asi_idx <len (asi_isimleri ):
            if cv ==2 :
                cvyrm +=f"{asi_isimleri[asi_idx]}: CV tutarsız (yüksek).\n"
            elif cv ==0 :
                cvyrm +=f"{asi_isimleri[asi_idx]}: CV olması gerekenden düşük.\n"

    cvyrm1 ="Enfeksiyon değerlendirmesi\n"

    if gorselinfdict :
        for hastalik ,s in sorted (
        gorselinfdict .items (),
        key =lambda x :safe_float (x [1 ]),
        reverse =True 
        ):
            s =safe_float (s )

            if s >0.5 :
                durum ="Yüksek risk"
            elif s >0.3 :
                durum ="Orta risk"
            else :
                durum ="Düşük risk"

            cvyrm1 +=f"{hastalik}: %{s*100:.1f} – {durum}\n"
    else :
        cvyrm1 +="Enfeksiyon bulgusu saptanmadı\n"


    salmonella_risk = None
    try:
        top_key = None
        top_val = 0.0
        if gorselgaidict:
            items = sorted(
                gorselgaidict.items(),
                key=lambda x: safe_float(x[1]),
                reverse=True,
            )
            if items:
                top_key, top_val = items[0]

        checkbox_val = 0
        try:
            if salmonella is not None and str(salmonella).strip() != "":
                checkbox_val = int(str(salmonella).strip())
        except Exception:
            checkbox_val = 0

        top_is_salmonella = isinstance(top_key, str) and top_key.strip().lower().startswith("salmonella")


        if top_is_salmonella:
            if checkbox_val == 1:
                salmonella_risk = "Salmonella riski fazla"
            else:
                salmonella_risk = "Salmonella riski var"
        else:
            if checkbox_val == 1:
                salmonella_risk = "Salmonella riski var"
            else:
                salmonella_risk = None
    except Exception:
        salmonella_risk = None

    return titryrm ,titryrm1 ,cvyrm ,cvyrm1 ,asi_detaylari ,salmonella_risk 

app =Flask (__name__ )
app .secret_key ='lmmmaai'
app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///tavuk.db'
app .config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
print ("DB:",app .config ["SQLALCHEMY_DATABASE_URI"])
db =SQLAlchemy (app )
from functools import wraps 
def guvenlik (f ):
    @wraps (f )
    def inner (*args ,**kwargs ):
        try :
            return f (*args ,**kwargs )
        except Exception as e :
            print ("SAVUNMA HATASI:",e )
            raise 
    return inner 

class BilgiKartlari (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    baslik =db .Column (db .String (100 ),nullable =False )
    icerik =db .Column (db .Text ,nullable =False )
    def __repr__ (self ):
        return f'<BilgiKartlari {self.id}>'





class Card (db .Model ):
    __tablename__ ="card"
    id =db .Column (db .Integer ,primary_key =True )
    user_id =db .Column (db .Integer ,nullable =False )
    musteriadi =db .Column (db .String (120 ),nullable =False )
    kumes =db .Column (db .String (120 ),nullable =False )
    yas =db .Column (db .String (50 ),nullable =False )
    surukodu =db .Column (db .String (50 ),nullable =False )


    clone3018wtid =db .Column (db .LargeBinary ,nullable =True )
    clone3018wcvd =db .Column (db .LargeBinary ,nullable =True )
    clone3018wvid =db .Column (db .LargeBinary ,nullable =True )
    clone3018wposd =db .Column (db .LargeBinary ,nullable =True )

    clone3025wtid =db .Column (db .LargeBinary ,nullable =True )
    clone3025wcvd =db .Column (db .LargeBinary ,nullable =True )
    clone3025wvid =db .Column (db .LargeBinary ,nullable =True )
    clone3025wposd =db .Column (db .LargeBinary ,nullable =True )

    clone3057wtid =db .Column (db .LargeBinary ,nullable =True )
    clone3057wcvd =db .Column (db .LargeBinary ,nullable =True )
    clone3057wvid =db .Column (db .LargeBinary ,nullable =True )
    clone3057wposd =db .Column (db .LargeBinary ,nullable =True )

    ma518wtid =db .Column (db .LargeBinary ,nullable =True )
    ma518wcvd =db .Column (db .LargeBinary ,nullable =True )
    ma518wvid =db .Column (db .LargeBinary ,nullable =True )
    ma518wposd =db .Column (db .LargeBinary ,nullable =True )

    ma525wtid =db .Column (db .LargeBinary ,nullable =True )
    ma525wcvd =db .Column (db .LargeBinary ,nullable =True )
    ma525wvid =db .Column (db .LargeBinary ,nullable =True )
    ma525wposd =db .Column (db .LargeBinary ,nullable =True )

    ma557wtid =db .Column (db .LargeBinary ,nullable =True )
    ma557wcvd =db .Column (db .LargeBinary ,nullable =True )
    ma557wvid =db .Column (db .LargeBinary ,nullable =True )
    ma557wposd =db .Column (db .LargeBinary ,nullable =True )

    nemovac18wtid =db .Column (db .LargeBinary ,nullable =True )
    nemovac18wcvd =db .Column (db .LargeBinary ,nullable =True )
    nemovac18wvid =db .Column (db .LargeBinary ,nullable =True )
    nemovac18wposd =db .Column (db .LargeBinary ,nullable =True )

    nemovac25wtid =db .Column (db .LargeBinary ,nullable =True )
    nemovac25wcvd =db .Column (db .LargeBinary ,nullable =True )
    nemovac25wvid =db .Column (db .LargeBinary ,nullable =True )
    nemovac25wposd =db .Column (db .LargeBinary ,nullable =True )

    nemovac57wtid =db .Column (db .LargeBinary ,nullable =True )
    nemovac57wcvd =db .Column (db .LargeBinary ,nullable =True )
    nemovac57wvid =db .Column (db .LargeBinary ,nullable =True )
    nemovac57wposd =db .Column (db .LargeBinary ,nullable =True )

    xlive18wAEwtid =db .Column (db .LargeBinary ,nullable =True )
    xlive18wAEwcvd =db .Column (db .LargeBinary ,nullable =True )
    xlive18wAEwvid =db .Column (db .LargeBinary ,nullable =True )
    xlive18wAEwposd =db .Column (db .LargeBinary ,nullable =True )

    xlive18wCAVwtid =db .Column (db .LargeBinary ,nullable =True )
    xlive18wCAVwcvd =db .Column (db .LargeBinary ,nullable =True )
    xlive18wCAVwvid =db .Column (db .LargeBinary ,nullable =True )
    xlive18wCAVwposd =db .Column (db .LargeBinary ,nullable =True )

    intermediate10wtid =db .Column (db .LargeBinary ,nullable =True )
    intermediate10wcvd =db .Column (db .LargeBinary ,nullable =True )
    intermediate10wvid =db .Column (db .LargeBinary ,nullable =True )
    intermediate10wposd =db .Column (db .LargeBinary ,nullable =True )

    intermediate25wtid =db .Column (db .LargeBinary ,nullable =True )
    intermediate25wcvd =db .Column (db .LargeBinary ,nullable =True )
    intermediate25wvid =db .Column (db .LargeBinary ,nullable =True )
    intermediate25wposd =db .Column (db .LargeBinary ,nullable =True )

    intermediate57wtid =db .Column (db .LargeBinary ,nullable =True )
    intermediate57wcvd =db .Column (db .LargeBinary ,nullable =True )
    intermediate57wvid =db .Column (db .LargeBinary ,nullable =True )
    intermediate57wposd =db .Column (db .LargeBinary ,nullable =True )

    inact25wREOwtid =db .Column (db .LargeBinary ,nullable =True )
    inact25wREOwcvd =db .Column (db .LargeBinary ,nullable =True )
    inact25wREOwvid =db .Column (db .LargeBinary ,nullable =True )
    inact25wREOwposd =db .Column (db .LargeBinary ,nullable =True )

    inact57wREOwtid =db .Column (db .LargeBinary ,nullable =True )
    inact57wREOwcvd =db .Column (db .LargeBinary ,nullable =True )
    inact57wREOwvid =db .Column (db .LargeBinary ,nullable =True )
    inact57wREOwposd =db .Column (db .LargeBinary ,nullable =True )

    inact25wEDSwtid =db .Column (db .LargeBinary ,nullable =True )
    inact25wEDSwcvd =db .Column (db .LargeBinary ,nullable =True )
    inact25wEDSwvid =db .Column (db .LargeBinary ,nullable =True )
    inact25wEDSwposd =db .Column (db .LargeBinary ,nullable =True )

    inact57wEDSwtid =db .Column (db .LargeBinary ,nullable =True )
    inact57wEDSwcvd =db .Column (db .LargeBinary ,nullable =True )
    inact57wEDSwvid =db .Column (db .LargeBinary ,nullable =True )
    inact57wEDSwposd =db .Column (db .LargeBinary ,nullable =True )


    islenmisResm =db .Column (db .String ,nullable =True )
    islenmisResm1 =db .Column (db .String ,nullable =True )
    titryrm =db .Column (db .String ,nullable =True )
    titryrm1 =db .Column (db .String ,nullable =True )
    cvyrm =db .Column (db .String ,nullable =True )
    cvyrm1 =db .Column (db .String ,nullable =True )
    salmonella_risk =db .Column (db .String ,nullable =True )
    asi_detaylari =db .Column (db .Text ,nullable =True )


    def __repr__ (self ):
        return f'<Card {self.id}>'


class Profil (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    profil =db .Column (db .Text ,nullable =False )
    def __repr__ (self ):
        return f'<Card {self.id}>'


class User (db .Model ):

    id =db .Column (db .Integer ,primary_key =True ,autoincrement =True )
    username =db .Column (db .String (30 ),nullable =False )
    password =db .Column (db .String (40 ),nullable =False )

    def __repr__ (self ):
        return f'<User {self.id}>'

with app .app_context ():
    db .create_all ()
    if BilgiKartlari .query .count ()==0 :
        cards =[
        BilgiKartlari (
        baslik ="Bumblefoot",
        icerik ="Kümes hayvanlarında sık karşılaşılmakta olan, ayak lezyonlarına sebep olan hastalıklardan biri olan, pododermatitin(bumblefoot); çoğunlukla plantar metatarsal ya da dijital taban yastığında meydana gelen deri bütünlüğü bozuklukları ile ortaya çıktığı bildirilmektedir. Bu durum, yüzeysel veya derin ülserasyonlarla birlikte ayağın derin dokularını etkileyen enfeksiyöz bir sürecin gelişmesine yol açabilmektedir. Ayakta oluşan bahsedilen lezyonların, özellikle yabani ve kafes kuşlarının genel sağlığı ve refahı üzerinde önemli olumsuz etkiler oluşturduğu gözlemlenmektedir. Tedavi edilmediği durumlarda ise topallık, sistemik enfeksiyonlar, verim kaybı ve hatta ekstremitenin kaybı gibi ciddi sonuçlara neden olabildiği ifade edilmektedir."
        ),
        BilgiKartlari (
        baslik ="Coryza",
        icerik ="İnfeksiyöz koriza, tavuklarda Avibacterium paragallinarum türünün sebep olduğu akut bir solunum yolu hastalığıdır. Klinik belirtiler arasında aktivite azalması, burun akıntısı, hapşırma ve yüz bölgesinde şişlik yer almaktadır. Ön tanı, duyarlı tavuklarda tipik klinik bulgulara dayanarak konulmaktadır."
        ),
        BilgiKartlari (
        baslik ="CRD",
        icerik ="CRD hastalığının birincil etiyolojilk etkeni Mycoplasma gallisepticum'dur. Bu enfeksiyon dünya genelinde yaygındır ve tüm yaş gruplarındaki kuşlar arasında yüksek derecede bulaşıcıdır. Enfekte kuşlar yaşamları boyunca taşıyıcı olarak kalmakta ve diğer kuş popülasyonları için risk oluşturmaktadır."
        ),
        BilgiKartlari (
        baslik ="Fowlpox",
        icerik ="Fowlpox enfeksiyonu, tavuklar ve hindilerde yavaş yayılan ve ekonomik açıdan önemli bir hastalık olarak bilinmektedir; çünkü yumurta üretiminde kayıplara ve ölümlere neden olabilmektedir."
        ),
        BilgiKartlari (
        baslik ="NDV",
        icerik ="Newcastle hastalığı (ND), Paramiksovirüs ailesinden Avian Paramyxovirus Tip-1 (APMV-1) virüsünün neden olduğu dünya genelinde yaygın olarak görülen ve evcil kümes hayvanları da dahil olmak üzere kuşları etkileyen, çok bulaşıcı ve genellikle şiddetli seyirli bir kanatlı hayvan hastalığıdır ve hastalığın etkeni Newcastle hastalığı virüsü olarak bilinmektedir (NDV). NDV potansiyel olarak evcil ve vahşi tüm kuş türlerini enfekte edebilir"),
        ]

        db .session .add_all (cards )
        db .session .commit ()

@app .route ('/',methods =['GET','POST'])
def login ():

        error =''
        if request .method =='POST':
            form_login =request .form ['username']
            form_password =request .form ['password']

            users_db =User .query .all ()
            for user in users_db :
                if form_login ==user .username and form_password ==user .password :
                    session ['user_id']=user .id 
                    session ['username']=form_login 

                    return redirect ('/index')
                else :
                    error ='Incorrect login or password'
            return render_template ('login.html',error =error )

        else :
            return render_template ('login.html')

@app .route ('/reg',methods =['GET','POST'])
def reg ():
    error =""
    if request .method =='POST':
        username =request .form .get ('username','').strip ()
        password =request .form .get ('password','')
        users_db =User .query .all ()
        existing =User .query .filter_by (username =username ).first ()
        if existing :
            error ="Lütfen başka bir kullanıcı adı seçiniz"
            return render_template ('registration.html',error =error )
        user =User (username =username ,password =password )
        db .session .add (user )
        db .session .commit ()
        return redirect ('/')
    else :
        return render_template ('registration.html')



@app .route ('/index')
@guvenlik 
def index ():
    useridchck =session .get ('user_id')
    cards =Card .query .filter_by (user_id =useridchck ).order_by (Card .id ).all ()







    return render_template ('index.html',cards =cards )

@app .route ('/card/<int:id>')
@guvenlik 
def card (id ):
    import json 

    card =Card .query .get (id )

    field_map =[
    ('clone3018wtid','Clone30 18hf titre'),('clone3018wcvd','Clone30 18hf cv'),('clone3018wvid','Clone30 18hf vi'),('clone3018wposd','Clone30 18hf pos'),
    ('clone3025wtid','Clone30 25hf titre'),('clone3025wcvd','Clone30 25hf cv'),('clone3025wvid','Clone30 25hf vi'),('clone3025wposd','Clone30 25hf pos'),
    ('clone3057wtid','Clone30 57hf titre'),('clone3057wcvd','Clone30 57hf cv'),('clone3057wvid','Clone30 57hf vi'),('clone3057wposd','Clone30 57hf pos'),
    ('ma518wtid','Ma5 18hf titre'),('ma518wcvd','Ma5 18hf cv'),('ma518wvid','Ma5 18hf vi'),('ma518wposd','Ma5 18hf pos'),
    ('ma525wtid','Ma5 25hf titre'),('ma525wcvd','Ma5 25hf cv'),('ma525wvid','Ma5 25hf vi'),('ma525wposd','Ma5 25hf pos'),
    ('ma557wtid','Ma5 57hf titre'),('ma557wcvd','Ma5 57hf cv'),('ma557wvid','Ma5 57hf vi'),('ma557wposd','Ma5 57hf pos'),
    ('nemovac18wtid','Nemovac 18hf titre'),('nemovac18wcvd','Nemovac 18hf cv'),('nemovac18wvid','Nemovac 18hf vi'),('nemovac18wposd','Nemovac 18hf pos'),
    ('nemovac25wtid','Nemovac 25hf titre'),('nemovac25wcvd','Nemovac 25hf cv'),('nemovac25wvid','Nemovac 25hf vi'),('nemovac25wposd','Nemovac 25hf pos'),
    ('nemovac57wtid','Nemovac 57hf titre'),('nemovac57wcvd','Nemovac 57hf cv'),('nemovac57wvid','Nemovac 57hf vi'),('nemovac57wposd','Nemovac 57hf pos'),
    ('xlive18wAEwtid','Live 18hf AE titre'),('xlive18wAEwcvd','Live 18hf AE cv'),('xlive18wAEwvid','Live 18hf AE vi'),('xlive18wAEwposd','Live 18hf AE pos'),
    ('xlive18wCAVwtid','Live 18hf CAV titre'),('xlive18wCAVwcvd','Live 18hf CAV cv'),('xlive18wCAVwvid','Live 18hf CAV vi'),('xlive18wCAVwposd','Live 18hf CAV pos'),
    ('intermediate10wtid','Intermediate 10hf titre'),('intermediate10wcvd','Intermediate 10hf cv'),('intermediate10wvid','Intermediate 10hf vi'),('intermediate10wposd','Intermediate 10hf pos'),
    ('intermediate25wtid','Intermediate 25hf titre'),('intermediate25wcvd','Intermediate 25hf cv'),('intermediate25wvid','Intermediate 25hf vi'),('intermediate25wposd','Intermediate 25hf pos'),
    ('intermediate57wtid','Intermediate 57hf titre'),('intermediate57wcvd','Intermediate 57hf cv'),('intermediate57wvid','Intermediate 57hf vi'),('intermediate57wposd','Intermediate 57hf pos'),
    ('inact25wREOwtid','Inact 25hf REO titre'),('inact25wREOwcvd','Inact 25hf REO cv'),('inact25wREOwvid','Inact 25hf REO vi'),('inact25wREOwposd','Inact 25hf REO pos'),
    ('inact57wREOwtid','Inact 57hf REO titre'),('inact57wREOwcvd','Inact 57hf REO cv'),('inact57wREOwvid','Inact 57hf REO vi'),('inact57wREOwposd','Inact 57hf REO pos'),
    ('inact25wEDSwtid','Inact 25hf EDS titre'),('inact25wEDSwcvd','Inact 25hf EDS cv'),('inact25wEDSwvid','Inact 25hf EDS vi'),('inact25wEDSwposd','Inact 25hf EDS pos'),
    ('inact57wEDSwtid','Inact 57hf EDS titre'),('inact57wEDSwcvd','Inact 57hf EDS cv'),('inact57wEDSwvid','Inact 57hf EDS vi'),('inact57wEDSwposd','Inact 57hf EDS pos')
    ]

    img_data ={}
    for attr ,label in field_map :
        val =getattr (card ,attr ,None )
        if val :
            try :
                img_data [label ]=base64 .b64encode (val ).decode ('utf-8')
            except Exception :
                pass 


    asi_detaylari =[]
    if card .asi_detaylari :
        try :
            asi_detaylari =json .loads (card .asi_detaylari )
        except :
            asi_detaylari =[]

    return render_template ('card.html',card =card ,img_data =img_data ,asi_detaylari =asi_detaylari )
@app .route ('/create')
@guvenlik 
def create ():
    return render_template ('create_card.html')

@app .route ("/api/info/<int:info_id>")
@guvenlik 
def api_info (info_id ):
    card =BilgiKartlari .query .get (info_id )

    if not card :
        return jsonify ({"error":"not found"}),404 

    return jsonify ({
    "title":card .baslik ,
    "description":card .icerik 
    })

@app .route ('/form_create',methods =['GET','POST'])
@guvenlik 
def form_create ():
    if request .method =='POST':



        islenmisResm =""
        islenmisResm1 =""
        musteriadi =request .form .get ('musteriadi','').strip ()
        kumes =request .form .get ('kumes','').strip ()
        yas =request .form .get ('yas','').strip ()
        surukodu =request .form .get ('surukodu','').strip ()

        clone3018wti =request .form .get ('clone3018ti','').strip ()
        clone3018wcv =request .form .get ('clone3018cv','').strip ()
        clone3018wvi =request .form .get ('clone3018vi','').strip ()
        clone3018wpos =request .form .get ('clone3018pos','').strip ()


        clone3025wti =request .form .get ('clone3025ti','').strip ()
        clone3025wcv =request .form .get ('clone3025cv','').strip ()
        clone3025wvi =request .form .get ('clone3025vi','').strip ()
        clone3025wpos =request .form .get ('clone3025pos','').strip ()


        clone3057wti =request .form .get ('clone3057ti','').strip ()
        clone3057wcv =request .form .get ('clone3057cv','').strip ()
        clone3057wvi =request .form .get ('clone3057vi','').strip ()
        clone3057wpos =request .form .get ('clone3057pos','').strip ()


        ma518wti =request .form .get ('ma518ti','').strip ()
        ma518wcv =request .form .get ('ma518cv','').strip ()
        ma518wvi =request .form .get ('ma518vi','').strip ()
        ma518wpos =request .form .get ('ma518pos','').strip ()


        ma525wti =request .form .get ('ma525ti','').strip ()
        ma525wcv =request .form .get ('ma525cv','').strip ()
        ma525wvi =request .form .get ('ma525vi','').strip ()
        ma525wpos =request .form .get ('ma525pos','').strip ()


        ma557wti =request .form .get ('ma557ti','').strip ()
        ma557wcv =request .form .get ('ma557cv','').strip ()
        ma557wvi =request .form .get ('ma557vi','').strip ()
        ma557wpos =request .form .get ('ma557pos','').strip ()

        nemovac18wti =request .form .get ('nemovac18ti','').strip ()
        nemovac18wcv =request .form .get ('nemovac18cv','').strip ()
        nemovac18wvi =request .form .get ('nemovac18vi','').strip ()
        nemovac18wpos =request .form .get ('nemovac18pos','').strip ()

        nemovac25wti =request .form .get ('nemovac25ti','').strip ()
        nemovac25wcv =request .form .get ('nemovac25cv','').strip ()
        nemovac25wvi =request .form .get ('nemovac25vi','').strip ()
        nemovac25wpos =request .form .get ('nemovac25pos','').strip ()

        nemovac57wti =request .form .get ('nemovac57ti','').strip ()
        nemovac57wcv =request .form .get ('nemovac57cv','').strip ()
        nemovac57wvi =request .form .get ('nemovac57vi','').strip ()
        nemovac57wpos =request .form .get ('nemovac57pos','').strip ()

        xlive18wAEti =request .form .get ('xlive18wAEti','').strip ()
        xlive18wAEcv =request .form .get ('xlive18wAEcv','').strip ()
        xlive18wAEvi =request .form .get ('xlive18wAEvi','').strip ()
        xlive18wAEpos =request .form .get ('xlive18wAEpos','').strip ()

        xlive18wCAVti =request .form .get ('xlive18wCAVti','').strip ()
        xlive18wCAVcv =request .form .get ('xlive18wCAVcv','').strip ()
        xlive18wCAVvi =request .form .get ('xlive18wCAVvi','').strip ()
        xlive18wCAVpos =request .form .get ('xlive18wCAVpos','').strip ()

        intermediate10wti =request .form .get ('intermed10wti','').strip ()
        intermediate10wcv =request .form .get ('intermed10wcv','').strip ()
        intermediate10wvi =request .form .get ('intermed10wvi','').strip ()
        intermediate10wpos =request .form .get ('intermediate10wpos','').strip ()

        intermediate25wti =request .form .get ('intermed25wti','').strip ()
        intermediate25wcv =request .form .get ('intermed25wcv','').strip ()
        intermediate25wvi =request .form .get ('intermed25wvi','').strip ()
        intermediate25wpos =request .form .get ('intermediate25wpos','').strip ()

        intermediate57wti =request .form .get ('intermed57wti','').strip ()
        intermediate57wcv =request .form .get ('intermed57wcv','').strip ()
        intermediate57wvi =request .form .get ('intermed57wvi','').strip ()
        intermediate57wpos =request .form .get ('intermediate57wpos','').strip ()

        xinact25wREOti =request .form .get ('xinact25wREOti','').strip ()
        xinact25wREOcv =request .form .get ('xinact25wREOcv','').strip ()
        xinact25wREOvi =request .form .get ('xinact25wREOvi','').strip ()
        xinact25wREOpos =request .form .get ('xinact25wREOpos','').strip ()

        xinact57wREOti =request .form .get ('xinact57wREOti','').strip ()
        xinact57wREOcv =request .form .get ('xinact57wREOcv','').strip ()
        xinact57wREOvi =request .form .get ('xinact57wREOvi','').strip ()
        xinact57wREOpos =request .form .get ('xinact57wREOpos','').strip ()

        xinact25wEDSti =request .form .get ('xinact25wEDSti','').strip ()
        xinact25wEDScv =request .form .get ('xinact25wEDScv','').strip ()
        xinact25wEDSvi =request .form .get ('xinact25wEDSvi','').strip ()
        xinact25wEDSpos =request .form .get ('xinact25wEDSpos','').strip ()

        xinact57wEDSti =request .form .get ('xinact57wEDSti','').strip ()
        xinact57wEDScv =request .form .get ('xinact57wEDScv','').strip ()
        xinact57wEDSvi =request .form .get ('xinact57wEDSvi','').strip ()
        xinact57wEDSpos =request .form .get ('xinact57wEDSpos','').strip ()

        resm =request .files .get ('resimInput')
        resm1 =request .files .get ('resimInput1')

        salmonella =request .form .get ('salmonella','').strip ()
        if resm1 :
            print ("Görsel bulgu dosyası yüklendi.")
        islenmisResm =""
        islenmisResm1 =""
        if resm :
            try :
                resmicerk =resm .read ()
                resmsteam =BytesIO (resmicerk )
                resmdegisken =Image .open (resmsteam )
            except Exception :
                resmdegisken =None 
            if resmdegisken and predict_image_pil :
                try :
                    islenmisResm =str (predict_image_pil (resmdegisken ))
                    print (islenmisResm )
                except Exception as e :
                    islenmisResm =f"AI processing failed: {str(e)}"
            elif resmdegisken :
                islenmisResm ="AI module not available"
            else :
                islenmisResm ="Image processing error"


        if resm1 :
            try :
                resmicerk1 =resm1 .read ()
                resm1steam =BytesIO (resmicerk1 )
                resm1degisken =Image .open (resm1steam )
            except Exception as e :
                print (f"Görsel okuma hatası: {str(e)}")
                resm1degisken =None 
            if resm1degisken :
                try :

                    result_dict =predict_image_pilinfect (resm1degisken )


                    islenmisResm1 =str (result_dict ).replace ("'",'"')

                    islenmisResm1 =str (result_dict )
                    print (f"Infection AI sonucu: {islenmisResm1}")
                except Exception as e :
                    print (f"Infection AI işleme hatası: {str(e)}")
                    import traceback 
                    traceback .print_exc ()
                    islenmisResm1 =f"AI processing failed: {str(e)}"
            else :
                islenmisResm1 ="Image processing error"

        clone3018wtid ,clone3018wcvd ,clone3018wvid ,clone3018wposd ,clone3018wtitralg ,clone3018wcvalg ,clone3018wvidalg ,clone3018wposdalg =chck (clone3018wti ,clone3018wcv ,clone3018wvi ,clone3018wpos ,0 ,"Clone30 18 week")
        clone3025wtid ,clone3025wcvd ,clone3025wvid ,clone3025wposd ,clone3025wtitralg ,clone3025wcvalg ,clone3025wvidalg ,clone3025wposdalg =chck (clone3025wti ,clone3025wcv ,clone3025wvi ,clone3025wpos ,1 ,"Clone30 25 week")
        clone3057wtid ,clone3057wcvd ,clone3057wvid ,clone3057wposd ,clone3057wtitralg ,clone3057wcvalg ,clone3057wvidalg ,clone3057wposdalg =chck (clone3057wti ,clone3057wcv ,clone3057wvi ,clone3057wpos ,2 ,"Clone30 57 week")
        ma518wtid ,ma518wcvd ,ma518wvid ,ma518wposd ,ma518wtitralg ,ma518wcvalg ,ma518wvidalg ,ma518wposdalg =chck (ma518wti ,ma518wcv ,ma518wvi ,ma518wpos ,3 ,"Ma5 & 4/91 18 week")
        ma525wtid ,ma525wcvd ,ma525wvid ,ma525wposd ,ma525wtitralg ,ma525wcvalg ,ma525wvidalg ,ma525wposdalg =chck (ma525wti ,ma525wcv ,ma525wvi ,ma525wpos ,4 ,"Ma5 & 4/91 25 week")
        ma557wtid ,ma557wcvd ,ma557wvid ,ma557wposd ,ma557wtitralg ,ma557wcvalg ,ma557wvidalg ,ma557wposdalg =chck (ma557wti ,ma557wcv ,ma557wvi ,ma557wpos ,5 ,"Ma5 & 4/91 57 week")
        nemovac18wtid ,nemovac18wcvd ,nemovac18wvid ,nemovac18wposd ,nemovac18wtitralg ,nemovac18wcvalg ,nemovac18wvidalg ,nemovac18wposdalg =chck (nemovac18wti ,nemovac18wcv ,nemovac18wvi ,nemovac18wpos ,6 ,"Nemovac 18 week")
        nemovac25wtid ,nemovac25wcvd ,nemovac25wvid ,nemovac25wposd ,nemovac25wtitralg ,nemovac25wcvalg ,nemovac25wvidalg ,nemovac25wposdalg =chck (nemovac25wti ,nemovac25wcv ,nemovac25wvi ,nemovac25wpos ,7 ,"Nemovac 25 week")
        nemovac57wtid ,nemovac57wcvd ,nemovac57wvid ,nemovac57wposd ,nemovac57wtitralg ,nemovac57wcvalg ,nemovac57wvidalg ,nemovac57wposdalg =chck (nemovac57wti ,nemovac57wcv ,nemovac57wvi ,nemovac57wpos ,8 ,"Nemovac 57 week")
        xlive18wAEtid ,xlive18wAEcvd ,xlive18wAEvid ,xlive18wAEposd ,xlive18wAETitralg ,xlive18wAEcvalg ,xlive18wAEvidalg ,xlive18wAEposdalg =chck (xlive18wAEti ,xlive18wAEcv ,xlive18wAEvi ,xlive18wAEpos ,9 ,"1x live AE 18 week")
        xlive18wCAVtid ,xlive18wCAVcvd ,xlive18wCAVvid ,xlive18wCAVposd ,xlive18wCAVTitralg ,xlive18wCAVcvalg ,xlive18wCAVvidalg ,xlive18wCAVposdalg =chck (xlive18wCAVti ,xlive18wCAVcv ,xlive18wCAVvi ,xlive18wCAVpos ,10 ,"1x live CAV 18 week")
        intermediate10wtid ,intermediate10wcvd ,intermediate10wvid ,intermediate10wposd ,intermediate10wtitralg ,intermediate10wcvalg ,intermediate10wvidalg ,intermediate10wposdalg =chck (intermediate10wti ,intermediate10wcv ,intermediate10wvi ,intermediate10wpos ,11 ,"1x live intermediate 10 week")
        intermediate25wtid ,intermediate25wcvd ,intermediate25wvid ,intermediate25wposd ,intermediate25wtitralg ,intermediate25wcvalg ,intermediate25wvidalg ,intermediate25wposdalg =chck (intermediate25wti ,intermediate25wcv ,intermediate25wvi ,intermediate25wpos ,12 ,"1x live intermediate 25 week")
        intermediate57wtid ,intermediate57wcvd ,intermediate57wvid ,intermediate57wposd ,intermediate57wtitralg ,intermediate57wcvalg ,intermediate57wvidalg ,intermediate57wposdalg =chck (intermediate57wti ,intermediate57wcv ,intermediate57wvi ,intermediate57wpos ,13 ,"1x live intermediate 57 week")
        xinact25wREOtid ,xinact25wREOcvd ,xinact25wREOvid ,xinact25wREOposd ,xinact25WREOtitralg ,xinact25WREOcvalg ,xinact25WREOvidalg ,xinact25WREOposdalg =chck (xinact25wREOti ,xinact25wREOcv ,xinact25wREOvi ,xinact25wREOpos ,14 ,"1x inact REO 25 week")
        xinact57wREOtid ,xinact57wREOcvd ,xinact57wREOvid ,xinact57wREOposd ,xinact57WREOtitralg ,xinact57WREOcvalg ,xinact57WREOvidalg ,xinact57WREOposdalg =chck (xinact57wREOti ,xinact57wREOcv ,xinact57wREOvi ,xinact57wREOpos ,15 ,"1x inact REO 57 week")
        xinact25wEDStid ,xinact25wEDScvd ,xinact25wEDSvid ,xinact25wEDSposd ,xinact25WEDStitralg ,xinact25WEDScvalg ,xinact25WEDSvidalg ,xinact25WEDSposdalg =chck (xinact25wEDSti ,xinact25wEDScv ,xinact25wEDSvi ,xinact25wEDSpos ,16 ,"1x inact EDS 25 week")
        xinact57wEDStid ,xinact57wEDScvd ,xinact57wEDSvid ,xinact57wEDSposd ,xinact57WEDStitralg ,xinact57WEDScvalg ,xinact57WEDSvidalg ,xinact57WEDSposdalg =chck (xinact57wEDSti ,xinact57wEDScv ,xinact57wEDSvi ,xinact57wEDSpos ,17 ,"1x inact EDS 57 week")
        asilist =[
        "ma518w","ma525w","ma557w",
        "nemovac18w","nemovac25w","nemovac57w",
        "xlive18wAEw","xlive18wCAVw",
        "intermediate10w","intermediate25w","intermediate57w",
        "xinact25WREOw","xinact57WREOw",
        "xinact25WEDSw","xinact57WEDSw"
        ]
        titralglist =[


        ma518wtitralg ,
        ma525wtitralg ,
        ma557wtitralg ,

        nemovac18wtitralg ,
        nemovac25wtitralg ,
        nemovac57wtitralg ,

        xlive18wAETitralg ,
        xlive18wCAVTitralg ,

        intermediate10wtitralg ,
        intermediate25wtitralg ,
        intermediate57wtitralg ,

        xinact25WREOtitralg ,
        xinact57WREOtitralg ,

        xinact25WEDStitralg ,
        xinact57WEDStitralg 
        ]
        cvalglist =[


        ma518wcvalg ,
        ma525wcvalg ,
        ma557wcvalg ,

        nemovac18wcvalg ,
        nemovac25wcvalg ,
        nemovac57wcvalg ,

        xlive18wAEcvalg ,
        xlive18wCAVcvalg ,

        intermediate10wcvalg ,
        intermediate25wcvalg ,
        intermediate57wcvalg ,

        xinact25WREOcvalg ,
        xinact57WREOcvalg ,

        xinact25WEDScvalg ,
        xinact57WEDScvalg 
        ]

        clone30_titres =[clone3018wtitralg ,clone3025wtitralg ,clone3057wtitralg ]
        clone30_cvs =[clone3018wcvalg ,clone3025wcvalg ,clone3057wcvalg ]

        titryrm ,titryrm1 ,cvyrm ,cvyrm1 ,asi_detaylari ,salmonella_risk =bykalg (
        islenmisResm ,islenmisResm1 ,cvalglist ,titralglist ,
        clone30_titres =clone30_titres ,clone30_cvs =clone30_cvs ,salmonella =salmonella 
        )


        import json 
        asi_detaylari_json =json .dumps (asi_detaylari ,ensure_ascii =False )


        listofstuff =[clone3018wtid ,clone3018wcvd ,clone3018wvid ,clone3018wposd ,
        clone3025wtid ,clone3025wcvd ,clone3025wvid ,clone3025wposd ,
        clone3057wtid ,clone3057wcvd ,clone3057wvid ,clone3057wposd ,
        ma518wtid ,ma518wcvd ,ma518wvid ,ma518wposd ,
        ma525wtid ,ma525wcvd ,ma525wvid ,ma525wposd ,
        ma557wtid ,ma557wcvd ,ma557wvid ,ma557wposd ,
        nemovac18wtid ,nemovac18wcvd ,nemovac18wvid ,nemovac18wposd ,
        nemovac25wtid ,nemovac25wcvd ,nemovac25wvid ,nemovac25wposd ,
        nemovac57wtid ,nemovac57wcvd ,nemovac57wvid ,nemovac57wposd ,
        xlive18wAEtid ,xlive18wAEcvd ,xlive18wAEvid ,xlive18wAEposd ,
        xlive18wCAVtid ,xlive18wCAVcvd ,xlive18wCAVvid ,xlive18wCAVposd ,
        intermediate10wtid ,intermediate10wcvd ,intermediate10wvid ,intermediate10wposd ,
        intermediate25wtid ,intermediate25wcvd ,intermediate25wvid ,intermediate25wposd ,
        intermediate57wtid ,intermediate57wcvd ,intermediate57wvid ,intermediate57wposd ,
        xinact25wREOtid ,xinact25wREOcvd ,xinact25wREOvid ,xinact25wREOposd ,
        xinact57wREOtid ,xinact57wREOcvd ,xinact57wREOvid ,xinact57wREOposd ,
        xinact25wEDStid ,xinact25wEDScvd ,xinact25wEDSvid ,xinact25wEDSposd ,
        xinact57wEDStid ,xinact57wEDScvd ,xinact57wEDSvid ,xinact57wEDSposd ,

        ]






        card =Card (
        user_id =session .get ('user_id',0 ),
        musteriadi =musteriadi ,
        kumes =kumes ,
        yas =yas ,
        surukodu =surukodu ,
        clone3018wtid =clone3018wtid ,
        clone3018wcvd =clone3018wcvd ,
        clone3018wvid =clone3018wvid ,
        clone3018wposd =clone3018wposd ,
        clone3025wtid =clone3025wtid ,
        clone3025wcvd =clone3025wcvd ,
        clone3025wvid =clone3025wvid ,
        clone3025wposd =clone3025wposd ,
        clone3057wtid =clone3057wtid ,
        clone3057wcvd =clone3057wcvd ,
        clone3057wvid =clone3057wvid ,
        clone3057wposd =clone3057wposd ,
        ma518wtid =ma518wtid ,
        ma518wcvd =ma518wcvd ,
        ma518wvid =ma518wvid ,
        ma518wposd =ma518wposd ,
        ma525wtid =ma525wtid ,
        ma525wcvd =ma525wcvd ,
        ma525wvid =ma525wvid ,
        ma525wposd =ma525wposd ,
        ma557wtid =ma557wtid ,
        ma557wcvd =ma557wcvd ,
        ma557wvid =ma557wvid ,
        ma557wposd =ma557wposd ,
        nemovac18wtid =nemovac18wtid ,
        nemovac18wcvd =nemovac18wcvd ,
        nemovac18wvid =nemovac18wvid ,
        nemovac18wposd =nemovac18wposd ,
        nemovac25wtid =nemovac25wtid ,
        nemovac25wcvd =nemovac25wcvd ,
        nemovac25wvid =nemovac25wvid ,
        nemovac25wposd =nemovac25wposd ,
        nemovac57wtid =nemovac57wtid ,
        nemovac57wcvd =nemovac57wcvd ,
        nemovac57wvid =nemovac57wvid ,
        nemovac57wposd =nemovac57wposd ,
        xlive18wAEwtid =xlive18wAEtid ,
        xlive18wAEwcvd =xlive18wAEcvd ,
        xlive18wAEwvid =xlive18wAEvid ,
        xlive18wAEwposd =xlive18wAEposd ,
        xlive18wCAVwtid =xlive18wCAVtid ,
        xlive18wCAVwcvd =xlive18wCAVcvd ,
        xlive18wCAVwvid =xlive18wCAVvid ,
        xlive18wCAVwposd =xlive18wCAVposd ,
        intermediate10wtid =intermediate10wtid ,
        intermediate10wcvd =intermediate10wcvd ,
        intermediate10wvid =intermediate10wvid ,
        intermediate10wposd =intermediate10wposd ,
        intermediate25wtid =intermediate25wtid ,
        intermediate25wcvd =intermediate25wcvd ,
        intermediate25wvid =intermediate25wvid ,
        intermediate25wposd =intermediate25wposd ,
        intermediate57wtid =intermediate57wtid ,
        intermediate57wcvd =intermediate57wcvd ,
        intermediate57wvid =intermediate57wvid ,
        intermediate57wposd =intermediate57wposd ,
        inact25wREOwtid =xinact25wREOtid ,
        inact25wREOwcvd =xinact25wREOcvd ,
        inact25wREOwvid =xinact25wREOvid ,
        inact25wREOwposd =xinact25wREOposd ,
        inact57wREOwtid =xinact57wREOtid ,
        inact57wREOwcvd =xinact57wREOcvd ,
        inact57wREOwvid =xinact57wREOvid ,
        inact57wREOwposd =xinact57wREOposd ,
        inact25wEDSwtid =xinact25wEDStid ,
        inact25wEDSwcvd =xinact25wEDScvd ,
        inact25wEDSwvid =xinact25wEDSvid ,
        inact25wEDSwposd =xinact25wEDSposd ,
        inact57wEDSwtid =xinact57wEDStid ,
        inact57wEDSwcvd =xinact57wEDScvd ,
        inact57wEDSwvid =xinact57wEDSvid ,
        inact57wEDSwposd =xinact57wEDSposd ,
        titryrm =titryrm ,
        titryrm1 =titryrm1 ,
        cvyrm =cvyrm ,
        cvyrm1 =cvyrm1 ,
        salmonella_risk =salmonella_risk ,
        islenmisResm =islenmisResm ,
        islenmisResm1 =islenmisResm1 ,
        asi_detaylari =asi_detaylari_json )

        db .session .add (card )
        db .session .commit ()
        return redirect ('/index')
    else :
        return render_template ('create_card.html',islenmisResm =islenmisResm )





if __name__ =="__main__":
    app .run (debug =True )