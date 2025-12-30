import torch 
import torch .nn .functional as F 
from torchvision import transforms ,models 
from PIL import Image 
import os 

device =torch .device ("cuda"if torch .cuda .is_available ()else "cpu")


model =None 
model_loaded =False 

try :
    model =models .efficientnet_b4 (weights =None )

    num_features =model .classifier [1 ].in_features 
    model .classifier =torch .nn .Sequential (
    torch .nn .Dropout (0.5 ),
    torch .nn .Linear (num_features ,5 )
    )

    if os .path .exists ("modelinfect.pth"):
        model .load_state_dict (torch .load ("modelinfect.pth",map_location =device ),strict =False )
        model .to (device )
        model .eval ()
        model_loaded =True 
        print ("Infection model yüklendi ve hazır.")
    else :
        print ("Uyarı: modelinfect.pth dosyası bulunamadı!")
except Exception as e :
    print (f"Infection model yükleme hatası: {str(e)}")
    model_loaded =False 

class_names =["Bumblefoot",
"Coryza",
"CRD",
"Fowlpox",
"Healthy"]


transform =transforms .Compose ([
transforms .Resize ((380 ,380 )),
transforms .ToTensor (),
transforms .Normalize (mean =[0.485 ,0.456 ,0.406 ],std =[0.229 ,0.224 ,0.225 ])
])


def predict_image_pilinfect (image ,topk =5 ):
    """
    image: PIL.Image formatında görsel
    topk: en yüksek kaç tahmin dönecek
    Returns: Dictionary with class names as keys and probability values (0-1) as values
    """
    if not model_loaded or model is None :
        raise Exception ("Model yüklenemedi veya hazır değil")

    if image is None :
        raise ValueError ("Görsel None olamaz")

    try :

        if image .mode !='RGB':
            image =image .convert ('RGB')

        img_tensor =transform (image ).unsqueeze (0 ).to (device )

        with torch .no_grad ():
            outputs =model (img_tensor )
            probs =F .softmax (outputs ,dim =1 )
            top_probs ,top_idxs =probs .topk (topk ,dim =1 )

        result ={}

        for i in range (topk ):
            cls_name =class_names [top_idxs [0 ][i ].item ()]

            probability =top_probs [0 ][i ].item ()
            result [cls_name ]=probability 

        return result 
    except Exception as e :
        raise Exception (f"Tahmin yapılırken hata oluştu: {str(e)}")

