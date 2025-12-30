import torch 
import torch .nn .functional as F 
from torchvision import transforms ,models 
from PIL import Image 

device =torch .device ("cuda"if torch .cuda .is_available ()else "cpu")


model =models .efficientnet_b0 (weights =None )


num_features =model .classifier [1 ].in_features 
model .classifier =torch .nn .Sequential (
torch .nn .Dropout (0.4 ),
torch .nn .Linear (num_features ,4 )
)


model .load_state_dict (torch .load ("model.pth",map_location =device ),strict =False )

model .to (device )
model .eval ()


print ("Model yüklendi ve hazır.")


class_names =["Coccidiosis","Healthy","NDV","Salmonella"]


transform =transforms .Compose ([
transforms .Resize ((240 ,240 )),
transforms .ToTensor (),
])


def predict_image_pil (image ,topk =4 ):
    """
    image: PIL.Image formatında görsel
    topk: en yüksek kaç tahmin dönecek
    """
    img_tensor =transform (image ).unsqueeze (0 ).to (device )

    with torch .no_grad ():
        outputs =model (img_tensor )
        probs =F .softmax (outputs ,dim =1 )
        top_probs ,top_idxs =probs .topk (topk ,dim =1 )

    result ={}

    for i in range (topk ):
        cls_name =class_names [top_idxs [0 ][i ].item ()]
        percentage =round (top_probs [0 ][i ].item ()*100 ,2 )
        result [cls_name ]=f"%{percentage}"

    return result 



model1 =models .efficientnet_b1 (weights =None )


num_features =model1 .classifier [1 ].in_features 
model1 .classifier =torch .nn .Sequential (
torch .nn .Dropout (0.4 ),
torch .nn .Linear (num_features ,4 )
)

