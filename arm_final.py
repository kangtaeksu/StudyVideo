#!/usr/bin/env python
# coding: utf-8

# **심화도전2**
# ### **Breast cancer wisconsin 데이터를 이용한 <span style="color:darkgreen">AI분류</span> 문제**
# ---

# #### 암세포의 형태 데이터를 이용하여 암 진단 판정을 악성과 양성으로 분류하는 AI문제입니다. 
# #### AI코딩 단계에 따라 주어지는 문제를 읽고 답안을 작성하세요.
# #### ( Breast cancer wisconsin 데이터 : sklearn 내장 연습용 데이터셋 사용)
# 
#  - 데이터 : 분류(카테고리)
#  - 모델 : KNN(머신러닝 모델 비교 분석), DeepLearning
#  - 주요 전처리 : 분석 Column 추가, 표준화(standardization)
#  - 주요 학습 내용 : 이중 분류 모델 생성(binary 분류, input, output 처리, 손실함수 등), 머신러닝 모델 비교학습(리스트 활용)
# ---
# 
# **아래 측정값들을, 평균(mean), 표준오차(error), 제일 큰 값 3개의 평균(worst)으로 나타낸다. 예를 들어 radius는 mean radius, radius error, worst radius 3개 컬럼으로 나타난다.**<br>
# 
# - radius : 암세포의 반지름
# - texture : 질감
# - perimeter : 둘레
# - area : 면적
# - smoothness : 매끄러움
# - concavity : 오목함
# - concave points : 오목한 곳의 수
# - symmetry : 대칭성
# - fractal dimension : 프렉탈 차원
# - class : 라벨(y변수) 데이터로 세포의 양성/악성 여부를 binary로 표기한 데이터
#     * 0 : malignant : 악성
#     * 1 : benign : 양성
# 

# ---
# > **<span style="color:red">다음 문항을 풀기 전에 </span>아래 코드를 실행하시오.**<br>
# > **sklearn에서 제공하는 load_breast_cacncer에 대한 데이터를 불러올 예정입니다. <span style="color:darkgreen"></span>**<br>
# > ** 해당 형태로 불러온 데이터는 AIDU 환경변수와 상관없이 사용할수 있습니다.<br>
# > 분석할 feautre 데이터는 x 변수에, 라벨은 y변수에 저장 되게 됩니다.(사전 x,y 데이터 분리 실행)
# > y변수는 상기 서술된 컬럼 중 class 항목입니다.
# 
# 
# ---
# 
# 

# In[102]:


from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
x = cancer.data # 인풋으로 사용할 데이터
y = cancer.target # 아웃풋, target으로 사용할 데이터
col_names = cancer.feature_names # 인풋으로 사용할 데이터의 컬럼별 이름들
target_names = cancer.target_names # 아웃풋, target으로 사용할 데이터의 클래스 이름


# ### **Q1. pandas를 pd로 alias하여 사용할 수 있도록 불러오는 코드를 작성하고 실행하시기 바랍니다.**
# ---

# In[103]:


import pandas as pd


# ### **Q2.Matplotlib의 pyplot을 plt로 alias하여 사용할 수 있도록 불러오는 코드를 작성하고 실행하시기 바랍니다.**
# ---

# In[104]:


import matplotlib.pyplot as plt


# ### **Q3. 인풋데이터(x)와 인풋데이터 컬럼명(col_names)를 이용하여 인풋데이터의 dataframe을 제작하시기 바랍니다.**
# * **
# - 데이터 프레임의 변수 명은 bcc 로 한다.
# ---

# In[105]:


bcc = pd.DataFrame(cancer.data, columns = col_names)


# In[106]:


bcc


# ### **Q4. 데이터를 트레이닝셋 / 테스트셋으로 분할하시기 바랍니다.**
# * **
# - bcc와, y를 이용한다. ( x를 사용해도 좋지만, 이후 문제를 위해 bcc를 이용한다.)
# - train : test = 8.5 : 1.5
# - y의 클래스가 골고루 분할되도록 stratify하게 분할한다.
# - 변수명 규칙은 다음과 같다.
#     * x_train, y_train
#     * x_test, y_test
# - random state, seed 등은 2021로 설정한다.
# ---

# In[107]:


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15,  stratify = y, random_state=2021)


# ### **Q5. 트레이닝 데이터를 트레이닝셋 / 벨리데이션셋으로 분할하시기 바랍니다.**
# * **
# - x_train, y_train을 이용한다.
# - train : validation = 7 : 3
# - y_train의 클래스가 골고루 분할되도록 stratify하게 분할한다.
# - 변수명 규칙은 다음과 같다.
#     * x_train, y_train
#     * y_valid, y_valid
# - random state, seed 등은 2021로 설정한다.
# ---

# In[110]:



x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.255,  stratify = y_train, random_state=2021)
x_train.shape


# ### **Q6. x_train, x_valid, x_test의 인덱스를 초기화 하시기 바랍니다.**
# * **
# - 현재 x들은 전부 dataframe이고, 원본 bcc의 인덱스를 그대로 가지고 있다.
# - 맨 첫번째 row부터 순서대로 인덱스를 갖도록 한다
# - 인덱스는 정수 인덱스이며, 0부터 시작한다.
# ---

# In[111]:


bcc.reset_index()


# ### **Q7. x_train, x_valid, x_test의 모든 컬럼을 각각 표준화(standardization) 스케일링 하시기 바랍니다.**
# * **
# - **모든 전처리 규칙은 트레이닝셋으로 부터 선정한다.**
# - 스케일링한 x들은 각각 아래의 변수에 따로 선언해둔다.
#     * x_train_sc
#     * x_valid_sc
#     * x_test_sc
# ---

# In[112]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() 

scaler.fit(x_train)
x_train_sc = scaler.transform(x_train)

scaler.fit(x_valid)
x_valid_sc = scaler.transform(x_valid)

scaler.fit(x_test)
x_test_sc = scaler.transform(x_test)


# ### **Q8. KNN 모델들을 학습시키시기 바랍니다.**
# * **
# - 트레이닝 셋 (x_train_sc, y_train)을 이용하여 학습시킨다.
# - KNN의 이웃수(k)를 2부터 15까지 늘려가며 총 14개의 모델을 학습시킨다.
# - 학습시킨 트리들은 리스트를 만들어 knns 변수에 담아둔다.
# - y를 예측할 경우, 이웃들의 거리값은 반영하지 않는다.(weights 파라미터는 uniform을 사용한다.)
# - 각 모델을 knns 라는 list에 순차적으로 저장하시기 바랍니ㅣ다.
# ---

# In[113]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

k_param = range(2,16)
knns = []

for k in k_param:
    knn = KNeighborsClassifier(n_neighbors=k, weights = "uniform")
    knns.append(knn.fit(x_train_sc, y_train))


# ### **Q9. KNN 모델들의 성능을 리스트에 담아 accs에 선언하시기 바랍니다.**
# * **
# - k가 2인 knn모델부터 순서대로 평가하여 리스트에 담는다.
# - 벨리데이션 셋 위에서 성능을 평가한다. (x는 스케일링 된 값이어야 한다.)
# - 성능지표로는 accuracy를 사용한다.
# ---

# In[114]:


accs=[]
for i in range(14):
    print(knns[i].score(x_valid_sc, y_valid))
    accs.append(knns[i].score(x_valid_sc, y_valid))


# ### **Q10. KNN모델들의 k(이웃수)에 따른 accuracy를 시각화 하고, 가장 성능이 좋은 k 값을 선택하시기 바랍니다.**
# * **
# - 위의 Q9에서 제작한 리스트 accs를 이용한다.
# - line plot 이나 scatter plot을 이용한다.
# - 동일 성능의 k가 여러개라면, 가장 작은 k를 선택한다.
# ---

# In[145]:


plt.plot(accs)
plt.xlabel("k")
plt.ylabel("Validation Accuracy")
plt.title("Breast Cancer Classifier Accuracy")
plt.show()

a = accs.index(max(accs))
k = knns[a]


# ### **Q11. 선택된 KNN모델의 테스트셋 위에서의 accuracy를 출력하시기 바랍니다.**
# * **
# - 성능 확인 시 입력데이터는 스케일링 된 데이터인 x_test_sc를 사용해야 한다.
# ---

# In[146]:


k.score(x_test_sc, y_test)


# ### **Q12. 해당 모델의 classificaiton report를 출력하고, malignant의 precision 값을 출력하시오**
# ---
#   - 테스트셋 위의 성능 평가를 바탕으로 문제를 푼다.
#   - 성능 확인 시 입력데이터는 스케일링 된 데이터인 x_test_sc를 사용해야 한다.
# ---

# In[147]:


y_test_sc = k.predict(x_test_sc)
from sklearn.metrics import classification_report

target_names = ['y_test','y_test_sc'] # target values

# Print classification report after a train/test split:
print(classification_report(y_test,y_test_sc, target_names=target_names))


# In[148]:


from sklearn.metrics import precision_score
precision_score(y_test,y_test_sc, pos_label = 0)
#앞이 실제 뒤가 예측


# ### **Q13. Q8에서 Q11 까지의 학습 과정을 scaling 되지 않은 원본데이터로 학습하여 별도의 모델을 만드시기 바랍니다.**
# * **
# - 해당 모델의 classificaiton report를 출력하고, malignant의 precision 값을 출력하시오
#     - 테스트셋 위의 성능 평가를 바탕으로 문제를 푼다.
#     - 성능 확인 시 입력데이터는 스케일링 하지 않은 데이터인 x_valid를 사용해야 한다.
# ---

# In[149]:


y_valid_sc = k.predict(x_valid)
target_names = ['y_valid','y_valid_sc'] # target values
# Print classification report after a train/test split:
print(classification_report(y_valid,y_valid_sc, target_names=target_names))

precision_score(y_valid,y_valid_sc, pos_label = 0)


# ### **Q14. 스케일링하지 않은 데이터의 예측 모델 성능과, 스케일링한 데이터의 예측모델 성능을 출력하여 비교하시기 바랍니다.**
# * **
# - 기존 만든 best_knn 모델의 score를 사용하여 성능을 출력할 것
# - 스케일링한 학습 모델은 데이터 : x_test_sc 활용
# - 스케일링하지 않은 모델은 데이터 x_test 활용
# ---

# In[150]:


print(k.score(x_test_sc, y_test))
print(k.score(x_test, y_test))


# > **<span style="color:red">다음 문항을 풀기 전에 </span>아래 코드를 실행하세요.**
# >

# In[151]:


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.callbacks import EarlyStopping


# ### **Q16. 아래 조건에 맞추어 뉴럴네트워크 모델을 학습시키시기 바랍니다**
# * **
# - Tensorflow framework를 사용한다.
# - 히든레이어는 아래와 같은 규칙에 맞추어 구성합니다.
#     * 3개 이상의 fully connected layer를 사용할 것
#     * Drop out과 batchnormalization을 각각 한번 이상 사용한다.
# - Early stopping을 이용하여, validation loss가 10번 이상 개선되지 않으면 학습을 중단 시키고, 가장 성능이 좋았을 때의 가중치를 복구한다.
# - 학습과정의 로그(loss, accuracy)를 history에 선언하여 남긴다.
# - y를 별도로 원핫인코딩 하지 않고 분류모델을 학습시킬 수 있도록 한다.
# - 0,1로 구분된 binary 분류모델에 맞는 loss function인 binary_crossentropy를 사용하도록 한다.
# - epochs는 2000번을 지정한다.
# ---

# In[157]:


import os
from keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

model = Sequential()

model.add(Dense(64, activation='relu', input_shape=(30,)))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['acc'])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)



checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1,
                                                save_best_only=True)
history = model.fit(x_train, y_train, epochs=2000,  

                 batch_size=10, verbose=2, validation_split=0.2,   

                 callbacks=[es,cp_callback])

model.load_weights(checkpoint_path)


# ### **Q17. 다음 조건에 맞추어 뉴럴네트워크의 학습 로그를 시각화 하시오.**
# * **
# - 필요한 라이브러리가 있다면 따로 불러온다.
# - epochs에 따른 accuracy의 변화를 시각화 한다.
# - train accuracy와 validation accuracy를 전부 시각화하고, 구별가능해야 한다.
# - 그래프의 타이틀은 'Accuracy'로 표시한다.
# - x축에는 'epochs'라고 표시하고 y축에는 'accuracy'라고 표시한다.
# - 위에서 학습한 머신러닝 모델과 성능을 비교해보시오. 
# ---

# In[160]:


h = history
plt.plot(h.history['acc'])
plt.plot(h.history['val_acc'])
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel("accuracy")
plt.show()


# In[ ]:




