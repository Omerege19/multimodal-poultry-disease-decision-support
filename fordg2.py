from tabloveri import listof 
from algoalgort import grafik 

def chck (titr ,cv ,vi ,pos ,row ,asi ):
        titrsnc ,cvsnc ,visnc ,possnc =None ,None ,None ,None 
        titralg2 ,cvalg2 ,vialg2 ,posalg2 =None ,None ,None ,None 
        try :
                arr =listof [row ]
        except Exception :
                return (None ,None ,None ,None )

        degerlist =[titr ,cv ,vi ,pos ]
        for index ,inp in enumerate (degerlist ):

                try :
                        mdeg =arr [index ,0 ]
                        tdeg =arr [index ,1 ]
                except Exception :
                        return (None ,None ,None ,None )

                try :
                        val =int (inp )
                except Exception :
                        if inp is None or str (inp ).strip ()=="":
                                if index ==0 :
                                        titrsnc =None 
                                if index ==1 :
                                        cvsnc =None 
                                if index ==2 :
                                        visnc =None 
                                if index ==3 :
                                        possnc =None 
                        else :
                                if index ==0 :
                                        titrsnc =None 
                                if index ==1 :
                                        cvsnc =None 
                                if index ==2 :
                                        visnc =None 
                                if index ==3 :
                                        possnc =None 
                        continue 

                if index ==0 :
                    if val <mdeg :
                        titrsnc =grafik (mdeg ,tdeg ,val ,asi ,"titre değeri düşük")
                        titralg2 =0 
                    elif val >tdeg :
                        titrsnc =grafik (mdeg ,tdeg ,val ,asi ,"titre değeri yüksek")
                        titralg2 =2 
                    else :
                        titrsnc =grafik (mdeg ,tdeg ,val ,asi ,"titre değeri normal")
                        titralg2 =3 
                elif index ==1 :
                    if val <mdeg :
                        cvsnc =grafik (mdeg ,tdeg ,val ,asi ,"cv değeri düşük")
                        cvalg2 =0 
                    elif val >tdeg :
                        cvsnc =grafik (mdeg ,tdeg ,val ,asi ,"cv değeri yüksek")
                        cvalg2 =2 
                    else :
                        cvsnc =grafik (mdeg ,tdeg ,val ,asi ,"cv değeri normal")
                        cvalg2 =1 
                elif index ==2 :
                    if val <mdeg :
                        visnc =grafik (mdeg ,tdeg ,val ,asi ,"vi değeri düşük")
                        vialg2 =0 
                    elif val >tdeg :
                        visnc =grafik (mdeg ,tdeg ,val ,asi ,"vi değeri yüksek")
                        vialg2 =2 
                    else :
                        visnc =grafik (mdeg ,tdeg ,val ,asi ,"vi değeri normal")
                        vialg2 =1 
                elif index ==3 :
                    if val ==tdeg :
                        possnc =grafik (mdeg ,tdeg ,val ,asi ,"pos değeri normal")
                        posalg2 =0 
                    elif val >tdeg :
                        possnc =grafik (mdeg ,tdeg ,val ,asi ,"pos değeri yüksek")
                        posalg2 =2 
                    elif val <tdeg :
                        possnc =grafik (mdeg ,tdeg ,val ,asi ,"pos değeri düşük")
                        posalg2 =1 
        return titrsnc ,cvsnc ,visnc ,possnc ,titralg2 ,cvalg2 ,vialg2 ,posalg2 


