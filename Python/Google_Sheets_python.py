import numpy as np
import pandas as pd
import collections
from mpl_toolkits.mplot3d import Axes3D
from IPython import display
from matplotlib import pyplot as plt
import sklearn
import sklearn.manifold
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import itertools
import operator
#import tensorflow.compat.v1 as tf
import gspread
#agregar credenciales ocultas
gc = gspread.service_account_from_dict(credentials)
worksheet = gc.open('Datos_Balanza').worksheet('Ordenado')
# get_all_values gives a list of rows.
data=worksheet.get('D2:N')
DatosUsuar=pd.DataFrame.from_records(data)  
ratings=worksheet.get('Q2:T11')
# Convert to a DataFrame and render.      
DatosUsuar=DatosUsuar.set_axis(['Documento', 'manzana', 'platano', 'beterraga','zanahoria', 'maiz', 'limon', 'cebolla', 'papa', 'camote', 'tomate'], axis=1)
DatosUsuar.head(10)
rating=pd.DataFrame.from_records(ratings)
rating=rating.set_axis(['Producto ID', 'Producto', 'Veces comprado', 'Usuarios compradores'], axis=1)
rating=rating.sort_values('Veces comprado')
comprado = rating["Veces comprado"].astype(int)
comprado = comprado.tolist()
product = rating["Producto"].tolist()
Documento=worksheet.col_values(4)
Productos=worksheet.get('E1:N1')
Productos = str(Productos)[1:-1]
usuario_un=[{'Documento':'18978998','manzana':'1', 'platano':'0', 'beterraga':'1', 'zanahoria':'0', 'maiz':'0', 'limon':'0', 'cebolla':'1', 'papa':'0', 'camote':'0', 'tomate':'1'}]
entrada_food=pd.DataFrame(usuario_un)
data1=worksheet.get('E2:N')
DatosUsuar1=pd.DataFrame.from_records(data1)
ratings_train, ratings_test = train_test_split(DatosUsuar1, test_size = 0.2, random_state=42)
sim_matrix = 1 - sklearn.metrics.pairwise.cosine_distances(DatosUsuar1)
sim_matrix_train = sim_matrix[0:8,0:8]
sim_matrix_test = sim_matrix[8:10,8:10]
sim_train=pd.DataFrame(sim_matrix_train)
derived_df = ratings_train.drop([8,9], axis=1)
derived_df = derived_df.astype(float)
derived_df= derived_df.sort_values(0)
users_predictions =derived_df.dot(sim_train)/np.array([np.abs(sim_matrix_train).sum(axis=1)]).T
pd.DataFrame(data=users_predictions, index=['a','b','c','d','e','f','g'])

USUARIO_EJEMPLO ='87654321'
USUARIO_EJEMPLO=str(USUARIO_EJEMPLO)
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip('[[')
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip(']]')
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip("'")
print("Para usuario: ",USUARIO_EJEMPLO) # debe existir en nuestro dataset de train!
datas = DatosUsuar[DatosUsuar['Documento'] == USUARIO_EJEMPLO]
usuario_ver=datas.index[datas['Documento'] == USUARIO_EJEMPLO]
z=usuario_ver.tolist()

def red():
  print(usuario_ver)
  user0=users_predictions.index.argsort()[usuario_ver]
  compara=[]
  # Veamos los tres recomendados con mayor puntaje en la predic para este usuario
  for i, aRepo in enumerate(user0[-3:]):
      selRepo = DatosUsuar[DatosUsuar['Documento']==(aRepo+1)]
      compara.append(users_predictions[usuario_ver])
      #print(selRepo['Documento'] , 'puntaje:\n', users_predictions[usuario_ver][aRepo])
  compara=(str(compara)[13:-1].replace("  ",","))
  compara=compara.replace("\n",",")
  compara=compara.split(',')
  plain_list_iter = iter(compara)
  plain_list_dict_object = itertools.zip_longest(plain_list_iter, plain_list_iter, fillvalue=None)
  comparacion = dict(plain_list_dict_object)
  comparacion_sort= sorted(comparacion.items(), key=operator.itemgetter(1), reverse=True)
  user =str(user0)[1:-1]
  for name in enumerate(comparacion_sort):
    if user in name[1][0]:
      print('detect')
    else:
      #print(name[1][0], ':', comparacion[name[1][0]])
      similar=name[1][0]
      break
  first = users_predictions.loc[[int(similar)]]
  maxi=(str(first.max(axis = 1))[5:-15])
  maxi=float(maxi)
  rating_orden=rating.sort_index()
  #print("Datos:\n",datas)
  print("Similar:\n",first)
  recomendacion=[]
  for index in range(first.shape[1]):
      valor=float(first.iloc[: , index].values)
      valor=("{:.6f}".format(valor))
      if float(valor)==maxi:    
        recomendacion.append(rating_orden.iloc[index, 1])
  print('\nProductos recomendados: ',str(recomendacion).replace("'","")[1:-1])
if len(z) == 0:
  popular =worksheet.get('V11')
  recomendacion=[popular]
  recomendacion=str(recomendacion).replace("[['"," ")[1:-1]
  recomendacion=str(recomendacion).replace("']"," ")[1:-1]
  print('\nProductos recomendados: ',recomendacion)
else:
  recomendacion=[]
  red()
