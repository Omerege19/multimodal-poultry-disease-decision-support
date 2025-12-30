
import numpy as np 
import matplotlib 
matplotlib .use ('Agg')
import matplotlib .pyplot as plt 
from io import BytesIO 
import ast 
def grafik (aralikbas ,aralikbit ,gosterilensayi ,asi ,sozelsonuc ):
    aralikgen =aralikbit -aralikbas 
    fig ,ax =plt .subplots (figsize =(15 ,3 ))
    gorsel =BytesIO ()
    ax .barh (y =[0 ],width =aralikgen ,left =aralikbas ,
    height =0.5 ,
    color ='lightgray',
    edgecolor ='black',
    label =f'[{aralikbas}, {aralikbit}] Aralığı.{asi} aşısı')

    ax .axvline (x =gosterilensayi ,
    color ='red',
    linestyle ='--',
    linewidth =2 ,
    label =f'Sayı: {gosterilensayi}')

    ax .set_xlim (aralikbas -20000 ,aralikbit +20000 )
    ax .set_title (sozelsonuc ,fontsize =14 )
    plt .legend (loc ='upper left',bbox_to_anchor =(0.05 ,1.2 ))
    plt .tight_layout ()
    plt .savefig (gorsel ,format ="png",dpi =270 )
    plt .close (fig )
    gorsel .seek (0 )
    return gorsel .getvalue ()

