# flake8: noqa
# runScript in shell
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc.settings")

import django
django.setup()

# your imports, e.g. Django models
#from tccStudentRegistration.models import *
# from tccStudentRegistration.importCSV import *
#from datawarehouseManager.dataMining import *
from datawarehouseManager.models import *
from sklearn.preprocessing import StandardScaler
from pandas import pandas as pd
scaler = StandardScaler()
print("working")

fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False,semestreEvasao__isnull=False)
df = pd.DataFrame(list(fatoEvasaoLista.values()))
df = df.drop("coeficienteEvasao",axis=1)
df = df.drop("alunoEvasao_id",axis=1)
df = df.drop("cursoEvasao_id",axis=1)
df = df.drop("semestreEvasao_id",axis=1)
df = df.drop("quantidadeEvasao",axis=1)
df = df.drop("id",axis=1)
print(df)
scaler.fit(df.drop("situacaoEvasao_id",axis=1))
scaled_features = scaler.transform(df.drop("situacaoEvasao_id",axis=1))
df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])
print(df_feat)

from sklearn.model_selection import train_test_split
x = df_feat
y = df['situacaoEvasao_id']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(x_train,y_train)

pred = knn.predict(x_test)

print(pred)


from sklearn.metrics import classification_report,confusion_matrix

print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))