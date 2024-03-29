# -*- coding: utf-8 -*-
"""BalanzaSisRecomendacion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Ir1OAMZ8z4dPQzZO7Q-82TD-FYC0auB

Conexión a Sheets Google y paquetes de python
"""
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
import itertools
import operator
import tensorflow.compat.v1 as tf
import gspread
import gspread
mail="guerdex@guerdex.com"
clave="be53409620026d7f570fe25fc2f3853d25f9eab"
credentials={
  "type": "service_account",
  "project_id": "proyectobalanzasmart",
  "private_key_id": "cbe53409620026d7f570fe25fc2f3853d25f9eab",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4wE/wuZIo+I5p\neHWR5Kf3lwzHwClucdAQKojZUzbAwbiDeeVIDvXWKkB8b9iwy59jF6+hHdKim1VF\nTu6uhq7dWG7eqAuvgqgNzDGOBE4HPF+lO9t4vwBcXgVpGRn+jKiGfLOiYr7FJVvr\nK7x+IAj0jhIVa+Ea3SVVBoGKs8Rr356D4YZzvYTUV1vNJ9jA8p9ZfbQ8/zdjqD+v\nlDbYRzeEMB0+5smijhPAVavqPgf513R7GObKWdOB1uclO1v0H4U4XydQ36vv2K3Y\nRrXf3pOoWvqErhrr+26JpAPZAMPF5Jaq42ZfbkQL2LTs3yY3L/B/TVpBuktDqiLj\nFMTYMdpjAgMBAAECggEAPXQewyR/BSjUeinK9cn4wycX5bO6NFYgTthPJ/cBjfGC\nNh2MUkFDrcblJ18u1XQN4vDEh1O7tkH0BbdhNmVvcgoR6vc719genWRQEXzGFasT\n54r3EH18Gb1ekFx8pIrWHdIKEJhG+53XKu0j6FIwmGRPiJeXS4/G9LbSzTfJvNWW\n/3z2VaZmynejHymh/N7vlCQnJ2lIqwKBiMjMh44TuCX1GLvkqVKkIPTikYVWGakA\nfxhsX55xggqTN0U7DhR6FAT4RnmdZoQgFZpAJzecwyplNcAm+zrj21NNC12QXkLU\n2gv797QiXk9EGtMh6ToeD+czWKz8VWwUOjrkIp2QvQKBgQDin+JAiJpiaS82nMY2\nb4hXddv7mlMy7SGnq84Pjr/rRmp1h0sPhqD1ZxWIgs+OutOeBytQBcYCkicJag5Y\nMgwaRiJFvsVYehvmejluGJfunHvAI/Ttz7cPPtDuqNg6E1frGnyAoHUfWX7VZn4A\n74F8PVX40/R4/NcSislQ27GaHwKBgQDQsvCLCez2f/YJAdhgJNyUboMe0Fw+YMBg\nawqeno+mZ4YM0dZYaE07ni2eYcQ3b62rM2esbxZyuCDGmre9yxCmfDpaVCDeWPE8\nPaReKWUMcBISj2Yo01GTn8k+SzzB2zzs5NtAMn3iRtg6JcgM1/pfKpOHjJ5kki1M\nXJppTL2/PQKBgG78nnG8dN99ZAH7BZfjR4KN1g6Cpfxq5fCX03MLFjLDaZ/lgn04\nEdwdgA47AiuEk97w4+Vs7myT50pVBnFrEUJM1rwRkdSi+McHVNj2cnIJcRHIiktt\nTtnIicpYJo1Kq+QYNKFJ9BJGYjdg2pTaty+BWnliVHhsW2hZT/6pmXFBAoGASX87\nBzwvn3/g/bsQoItaw0tIEgn+8ljQZyRLUSE2Jbw/kTQ08F2LFXvXRPfZSkyiNLCd\nyjQ1C6GcqVTDcKua6YbGZhlKmgNosXZj9GVPmNm/A5pMuAPzrrGPBckpVHwJMMRI\nEou1mYKpk5DKqvtEyU8NNadoALMaENJr7rl/+WECgYANCbwACnOFF9KkrYE6kQ+p\nFD1tmfAvSp6xk7izLut83dbmxCiGiNQFfWza3J5OwrA+OBdOSctYweVZBCtUE+pi\nLpd+k2n6AckSGtcFnYLCdTrP7Vms4lqzVzZwA1rsSV9JdL2+bGvM3hhlMUL7VrXk\nzyYSpYRBtf0SxUMkhq8cdw==\n-----END PRIVATE KEY-----\n",
  "client_email": "proyectobalanzasmart@appspot.gserviceaccount.com",
  "client_id": "105104323822216977545",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/proyectobalanzasmart%40appspot.gserviceaccount.com"
}
gc = gspread.service_account_from_dict(credentials)
worksheet = gc.open('Datos_Balanza').worksheet('Ordenado')
# get_all_values gives a list of rows.
data=worksheet.get('D2:N')
print(data)
DatosUsuar=pd.DataFrame.from_records(data)  

ratings=worksheet.get('Q2:T11')
# Convert to a DataFrame and render.      
DatosUsuar=DatosUsuar.set_axis(['Documento', 'manzana', 'platano', 'beterraga','zanahoria', 'maiz', 'limon', 'cebolla', 'papa', 'camote', 'tomate'], axis=1)
DatosUsuar.head(10)

"""# Nueva sección"""

rating=pd.DataFrame.from_records(ratings)
rating=rating.set_axis(['Producto ID', 'Producto', 'Veces comprado', 'Usuarios compradores'], axis=1)
rating=rating.sort_values('Veces comprado')

comprado = rating["Veces comprado"].astype(int)
comprado = comprado.tolist()
product = rating["Producto"].tolist()
plt.bar(product,comprado)
plt.ylabel("Cantidad de compras")
plt.xlabel("Productos")
plt.title("Productos vs Cantidad de compras")
plt.show()

Documento=worksheet.col_values(4)
print('Usuarios:',len(Documento)-1)
Productos=worksheet.get('E1:N1')
Productos = str(Productos)[1:-1]
#print(Productos)
print('Productos:',10)

usuario_todo=[{'Documento':'18978998','manzana':'1', 'platano':'0', 'beterraga':'1', 'zanahoria':'0', 'maiz':'0', 'limon':'0', 'cebolla':'1', 'papa':'0', 'camote':'0', 'tomate':'1'},
            {'Documento':'12568491','manzana':'0', 'platano':'1', 'beterraga':'0', 'zanahoria':'1', 'maiz':'0', 'limon':'1', 'cebolla':'0', 'papa':'0', 'camote':'0', 'tomate':'1'},
            {'Documento':'15876789','manzana':'0', 'platano':'1', 'beterraga':'0', 'zanahoria':'0', 'maiz':'1', 'limon':'1', 'cebolla':'0', 'papa':'1', 'camote':'1', 'tomate':'0'},
            {'Documento':'12848915','manzana':'1', 'platano':'0', 'beterraga':'0', 'zanahoria':'0', 'maiz':'1', 'limon':'1', 'cebolla':'1', 'papa':'0', 'camote':'1', 'tomate':'1'}]

usuario_un=[{'Documento':'18978998','manzana':'1', 'platano':'0', 'beterraga':'1', 'zanahoria':'0', 'maiz':'0', 'limon':'0', 'cebolla':'1', 'papa':'0', 'camote':'0', 'tomate':'1'}]
entrada_food=pd.DataFrame(usuario_un)
print('Productos-Usuarios:\n',entrada_food)

data1=worksheet.get('E2:N')
print(data1)
DatosUsuar1=pd.DataFrame.from_records(data1)
ratings_train, ratings_test = train_test_split(DatosUsuar1, test_size = 0.2, random_state=42)
#print(ratings_train.shape)
#print(ratings_test.shape)
DatosUsuar1

rating

sim_matrix = 1 - sklearn.metrics.pairwise.cosine_distances(DatosUsuar1)
print(sim_matrix.shape)

plt.imshow(sim_matrix);
plt.title("Similitud del coseno")
plt.xlabel("Productos")
plt.ylabel("Productos")
plt.colorbar()
plt.show()

sim_matrix_train = sim_matrix[0:8,0:8]
sim_matrix_test = sim_matrix[8:10,8:10]
print("train:\n",sim_matrix_train.shape)
print("test:\n",sim_matrix_test.shape)

sim_train=pd.DataFrame(sim_matrix_train)
print(sim_train.shape)
sim_train

derived_df = ratings_train.drop([8,9], axis=1)
derived_df = derived_df.astype(float)
derived_df= derived_df.sort_values(0)
plt.hist(sim_matrix)

plt.hist(sim_matrix_test)

users_predictions =derived_df.dot(sim_train)/np.array([np.abs(sim_matrix_train).sum(axis=1)]).T
pd.DataFrame(data=users_predictions, index=['a','b','c','d','e','f','g'])
print(users_predictions.shape)

plt.rcParams['figure.figsize'] = (20.0, 5.0)
plt.imshow(users_predictions);
plt.title("Similitud entre usuarios por productos pesados")
plt.xlabel("Usuarios")
plt.ylabel("Usuarios")
plt.colorbar()
plt.show()

#USUARIO_EJEMPLO =worksheet.get('V2')
USUARIO_EJEMPLO =int(input())
USUARIO_EJEMPLO=str(USUARIO_EJEMPLO)
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip('[[')
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip(']]')
USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip("'")
print("Para usuario: ",USUARIO_EJEMPLO) # debe existir en nuestro dataset de train!
datas = DatosUsuar[DatosUsuar['Documento'] == USUARIO_EJEMPLO]
usuario_ver=datas.index[datas['Documento'] == USUARIO_EJEMPLO]
z=usuario_ver.tolist()
def red():
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
  #print("Similar:\n",first)
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