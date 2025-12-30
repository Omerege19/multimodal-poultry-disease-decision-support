import pandas as pd 
import numpy as np 
satir =[
["GP","vector + 3x live (Clone 30)","NDV","18W",4000 ,11000 ,30 ,70 ,300 ,400 ,"100%"],
["GP","vector + 3x live (Clone 30) + inact","NDV","25W",12000 ,26000 ,20 ,60 ,300 ,400 ,"100%"],
["GP","vector + 3x live (Clone 30) + inact","NDV","57W",10000 ,23000 ,20 ,60 ,300 ,400 ,"100%"],
["GP","4x live (Ma5 & 4/91)","IBV","18W",3000 ,9000 ,30 ,70 ,300 ,450 ,"100%"],
["GP","4x live (Ma5 & 4/91)","IBV","25W",6000 ,16000 ,30 ,70 ,300 ,450 ,"100%"],
["GP","4x live (Ma5 & 4/91) + inact","IBV","57W",8000 ,20000 ,30 ,70 ,300 ,450 ,"100%"],
["GP","2x live (Nemovac)","ART","18W",3000 ,12000 ,20 ,60 ,90 ,450 ,"100%"],
["GP","2x live (Nemovac) + inact","ART","25W",7000 ,25000 ,20 ,60 ,150 ,1000 ,"100%"],
["GP","2x live (Nemovac) + inact","ART","57W",7000 ,25000 ,20 ,60 ,150 ,1000 ,"100%"],
["GP","1x live","CAV","18W",4000 ,8000 ,30 ,70 ,90 ,450 ,"100%"],
["GP","1x live","CAV","25W",6000 ,16000 ,30 ,70 ,90 ,450 ,"100%"],
["GP","no vaccination","FAV","18W",None ,None ,None ,None ,None ,None ,None ],
["GP","1x live (intermediate) + inact","IBD","25W",5000 ,12000 ,15 ,"40 (50)",100 ,650 ,"100%"],
["GP","1x live (intermediate) + inact","IBD","57W",8000 ,18000 ,15 ,"40 (50)",300 ,1500 ,"100%"],
["GP","1x inact","IBD","25W",8000 ,18000 ,15 ,"40 (50)",300 ,1500 ,"100%"],
["GP","1x inact","REO","25W",8000 ,14000 ,20 ,50 ,None ,None ,"100%"],
["GP","1x inact","REO","57W",None ,None ,None ,None ,None ,None ,"not sufficient data"],
["GP","1x inact","EDS","25W",2000 ,8000 ,30 ,70 ,50 ,"350-400","100%"],
["GP","1x inact","EDS","57W",2000 ,8000 ,30 ,70 ,40 ,"250-300",">80%"]
]

baslik =[
"Type of birds","Vaccination program","Disease","Age",
"Lower titer","Upper titer","Lower %CV","Upper %CV",
"Lower VI","Upper VI","% pos"
]




clone3018w =np .array ([[4000 ,11000 ],[30 ,70 ],[90 ,400 ],[100 ,100 ]])
clone3025w =np .array ([[12000 ,26000 ],[20 ,60 ],[300 ,2000 ],[100 ,100 ]])
clone3057w =np .array ([[12000 ,23000 ],[20 ,60 ],[300 ,1100 ],[100 ,100 ]])

ma5518w =np .array ([[3000 ,9000 ],[30 ,70 ],[50 ,400 ],[100 ,100 ]])
ma525w =np .array ([[6000 ,16000 ],[30 ,60 ],[90 ,450 ],[100 ,100 ]])
ma557w =np .array ([[6000 ,16000 ],[30 ,60 ],[90 ,450 ],[100 ,100 ]])

nemovac18w =np .array ([[4500 ,12000 ],[30 ,70 ],[100 ,500 ],[100 ,100 ]])
nemovac25w =np .array ([[7000 ,25000 ],[20 ,60 ],[150 ,1000 ],[100 ,100 ]])
nemovac57w =np .array ([[7000 ,25000 ],[20 ,60 ],[100 ,1000 ],[100 ,100 ]])

xlive18wAE =np .array ([[5000 ,13000 ],[20 ,60 ],[100 ,500 ],[80 ,100 ]])
xlive18wCAV =np .array ([[3000 ,8000 ],[30 ,70 ],[50 ,300 ],[80 ,100 ]])

intermediate10w =np .array ([[5000 ,12000 ],[15 ,40 ],[100 ,650 ],[100 ,100 ]])
intermediate25w =np .array ([[8000 ,20000 ],[10 ,40 ],[300 ,1500 ],[100 ,100 ]])
intermediate57w =np .array ([[8000 ,18000 ],[15 ,40 ],[300 ,1500 ],[100 ,100 ]])

inact25wREO =np .array ([[8000 ,15000 ],[20 ,50 ],[200 ,800 ],[100 ,100 ]])
inact57wREO =np .array ([[5000 ,14000 ],[0 ,0 ],[0 ,0 ],[100 ,100 ]])

inact25wEDS =np .array ([[2000 ,8000 ],[30 ,70 ],[50 ,400 ],[80 ,100 ]])
inact57wEDS =np .array ([[2000 ,8000 ],[30 ,70 ],[40 ,300 ],[80 ,100 ]])





listof =[clone3018w ,clone3025w ,clone3057w ,
ma5518w ,ma525w ,ma557w ,nemovac18w 
,nemovac25w ,nemovac57w ,xlive18wAE ,
xlive18wCAV ,intermediate10w ,intermediate25w ,intermediate57w ,
inact25wREO ,inact57wREO ,inact25wEDS ,inact57wEDS ]

tab =pd .DataFrame (satir ,columns =baslik )

print (tab )