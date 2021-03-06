#!/usr/bin/env python
# coding: utf-8

# **심화도전1**
# ### **boston house prices 데이터를 이용한 <span style="color:darkgreen"> AI 예측</span>문제 **
# ---

# #### Boston의 지역특성과 가격 데이터를 이용하여 , Boston 집값을 예측하는 AI문제입니다. 
# #### AI코딩 단계에 따라 주어지는 문제를 읽고 답안을 작성하세요.
# #### (boston house prices 데이터 : sklearn 내장 연습용 데이터셋 사용)
# 
#  - 데이터 : 회귀(수치)
#  - 모델 : 다중 회귀 분석 심화(선형, lidge, Lasso, elastic,), DeepLearning
#  - 주요 전처리 : 분석 Column 추가, 표준화(standardization), min-max Scaling
#  - 주요 학습 내용 : 다중 회귀 분석 심화 내용, 회귀 예측 모델 생성(input, output 처리, 손실함수 등)
# ---

# **boston house prices 데이터 컬럼 설명 (sklearn 내장 연습용 데이터셋)**
# - CRIM : 자치시(town)별 1인당 범죄율
# - ZN : 25,000 평방피트를 초과하는 거주지역의 비율
# - INDUS : 비소매상업지역이 점유하고 있는 토지의 비율
# - CHAS : 찰스강 근처는 1, 그렇지 않으면 0
# - NOX : 10ppm당 일산화질소 농도
# - RM : 주택 1가구당 평균 방의 개수
# - AGE : 1940년 이전에 건축된 소유주택의 비율
# - DIS : 5개의 보스턴 직업센터까지의 접근성 지수
# - RAD : 방사형 도로까지의 접근성 지수
# - TAX : 10,000달러 당 재산 새율
# - PTRATIO : 자치시(town)별 학생/교사 비율
# - B : 1000(Bk-0.63)^2, Bk는 자치시별 흑인의 비율
# - LSTAT : 모집단의 하위계층 비율
# - MEDV : 집주인이 실제 거주하는 집들의 주택가격 중앙값 (단위 $1,000)

# ---
# ---
# > **<span style="color:red">다음 문항을 풀기 전에 </span>아래 코드를 실행해주시기 바랍니다.**<br>
# > - AIDU 사용을 위한 AIDU 환경변수를 선언을 하는 코드. <span style="color:darkgreen"></span><br>
# ---
# 

# In[25]:


from sklearn.datasets import load_boston
boston = load_boston()
x = boston.data # 인풋으로 사용할 데이터
y = boston.target # 아웃풋, target으로 사용할 데이터
col_names = boston.feature_names # 인풋으로 사용할 데이터의 컬럼별 이름들


# ### **Q1. Pandas를 pd로 alias하여 사용할 수 있도록 불러오는 코드를 작성하고 실행하시기 바랍니다.**
# ---

# In[26]:


import pandas as pd


# ### **Q2. Numpy를 np로 alias하여 사용할 수 있도록 불러오는 코드를 작성하고 실행하시기 바랍니다.**
# ---

# In[27]:


import numpy as np


# ### **Q3. 인풋데이터(x)와 인풋데이터 컬럼명(col_names)를 이용하여 인풋데이터의 dataframe을 제작하시기 바랍니다.**
# * **
# - 데이터 프레임의 변수 명은 bhp 로 한다.
# ---

# In[28]:


bhp = pd.DataFrame(boston.data, columns= col_names)


# ### **Q4. 데이터 프레임 bhp에 새로운 컬럼 MEDV를 제작하시기 바랍니다.**
# * **
# - 컬럼의 값은 y를 사용한다. (주택 가격)
# ---

# In[29]:


bhp['MEDV'] = y
bhp


# ### **Q5. 데이터를 트레이닝셋 / 테스트셋으로 분할하시기 바랍니다.**
# * **
# - x와 y를 이용해도 좋지만, 데이터 프레임 bhp를 이용하여 분할하면 이후 코드가 편리해진다.
# - train : test = 8.5 : 1.5
# - 컬럼 CHAS 를 이용하여 stratify 하게 분할한다.
# - 변수명 규칙은 다음과 같다.
#     * x_train, y_train
#     * x_test, y_test
# - random state, seed 등은 2021로 설정한다.
# 
# ---

# In[30]:


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, stratify = bhp['CHAS'], random_state=2021)


# ### **Q6. 트레이닝셋을 트레이닝셋 / 벨리데이션셋으로 분할하시기 바랍니다.**
# * **
# - x_train과 y_train을 이용한다.
# - train : valid = 7 : 1.5
# - x_train의 컬럼 CHAS 를 이용하여 stratify 하게 분할한다.
# - 변수명 규칙은 다음과 같다.
#     * x_train, y_train
#     * x_valid, y_valid
# - random state, seed 등은 2021로 설정한다.
# 
# ---

# In[31]:


x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=3/14, stratify = bhp['CHAS'], random_state=2021)
pd.DataFrame(x_valid)


# ### **Q7. 데이터의 NOX와 RM은 민맥스(min-max) 스케일링 하시기 바랍니다.**
# * **
# - 모든 스케일링 규칙은 트레이닝 셋을 이용하여 정한다.
# - 트레이닝셋, 벨리데이션셋, 테스트셋 전부 스케일링 한다.
# ---

# In[32]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(bhp[['NOX']])
nox = scaler.transform(bhp[['NOX']])
nox1 = pd.DataFrame(nox, columns=['NOX'])

scaler.fit(bhp[['RM']])
rm = scaler.transform(bhp[['RM']])
rm1 = pd.DataFrame(rm, columns=['RM'])

bhp


# ### **Q8. 데이터의 RAD와 B는 표준화(standardization) 스케일링 하시기 바랍니다.**
# * **
# - 모든 스케일링 규칙은 트레이닝 셋을 이용하여 정한다.
# - 트레이닝셋, 벨리데이션셋, 테스트셋 전부 스케일링 한다.
# ---

# In[33]:



from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() 
scaler.fit(bhp[['RAD']])
rad = scaler.transform(bhp[['RAD']])
rad1 = pd.DataFrame(rad, columns=['RAD'])
rad1
 
scaler.fit(bhp[['B']])
b = scaler.transform(bhp[['B']])
b1 = pd.DataFrame(b, columns=['B'])

bhp


# ### **Q9. 트레이닝 셋을 이용하여 선형회귀 모델을 학습시키시기 바랍니다.**
# * **
# - linear regression의 normal equation으로 coefficient들을 추정한다.
# - 학습된 모델은 lr 에 선언해둔다.
# ---

# In[34]:


from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x_train, y_train)
lr.coef_


# ### **Q10. 트레이닝 셋을 이용하여 ridge regression 모델을 학습시키시기 바랍니다.**
# * **
# - regularization term의 penalty intensity 는 5로 설정한다.
# - 학습된 모델은 ridge 에 선언해둔다.
# ---

# In[35]:


from sklearn.linear_model import Ridge
ridge =Ridge(alpha = 5)
ridge.fit(x_train, y_train)
ridge.coef_


# ### **Q11. 트레이닝 셋을 이용하여 lasso regression 모델을 학습시키시기 바랍니다.**
# * **
# - regularization term의 penalty intensity 는 1로 설정한다.
# - 학습된 모델은 lasso 에 선언해둔다.
# ---

# In[36]:


from sklearn.linear_model import Lasso
lasso = Lasso(alpha=1)
lasso.fit(x_train, y_train)
lasso.coef_


# ### **Q12. 트레이닝 셋을 이용하여 elastic net regression 모델을 학습시키시기 바랍니다.**
# * **
# - regularization term의 penalty intensity는 아래와 같이 설정한다
#     * l1 penalty intensity : 0.5
#     * l2 penalty intensity : 3 
# - 학습된 모델은 elastic 에 선언해둔다.
# ---

# In[37]:


from sklearn.linear_model import ElasticNet
#alpha : a + b를 의미. 여기서 a란, L1으로 얼마나 정규화시킬지의 값, b란, L2로 얼마나 정규화시킬지의 값을 의미
#l1_ratio : "L1의 정규화값 / (L1의 정규화값 + L2의 정규화값)"을 의미. 만약 0.8이라면 8/10 이기 때문에 L1은 8만큼, L2는 2만큼 정규화시킴을 의미
elasticnet = ElasticNet(alpha=3.5, l1_ratio=0.8571, random_state=2021)
elasticnet.fit(x_train, y_train)


# ### **Q13. 벨리데이션 셋을 이용하여 학습된 네 모델의 성능을 출력하시기 바랍니다.**
# * **
# - 평가를 위한 손실함수는 rmse를 이용한다.
# ---

# In[38]:


from sklearn.metrics import mean_squared_error
y_valid_pred1=lr.predict(x_valid)
valid_rmse_lr=np.sqrt(mean_squared_error(y_valid, y_valid_pred1))
print("lr Valid RMSE:%.4f" % valid_rmse_lr)

y_valid_pred2=ridge.predict(x_valid)
valid_rmse_ridge=np.sqrt(mean_squared_error(y_valid, y_valid_pred2)) 
print("ridge Valid RMSE:%.4f" % valid_rmse_ridge)

y_valid_pred3=lasso.predict(x_valid)
valid_rmse_lasso=np.sqrt(mean_squared_error(y_valid, y_valid_pred3)) 
print("lasso Valid RMSE:%.4f" % valid_rmse_lasso)

y_valid_pred4=elasticnet.predict(x_valid)
valid_rmse_elastic=np.sqrt(mean_squared_error(y_valid, y_valid_pred4)) 
print("elastic net Valid RMSE:%.4f" % valid_rmse_elastic)


# ### **Q14. 테스트 셋을 이용하여 학습된 네 모델의 성능을 출력하시기 바랍니다.**
# * **
# - 손실함수는 mean absolute error를 이용한다.
# ---

# In[39]:


from sklearn.metrics import mean_absolute_error

y_test_pred1=lr.predict(x_test)
test_mae_lr=mean_absolute_error(y_test, y_test_pred1)
print("lr Test MAE:%.4f" % test_mae_lr)

y_test_pred2=ridge.predict(x_test)
test_mae_ridge=mean_absolute_error(y_test, y_test_pred2) 
print("ridge Test MAE:%.4f" % test_mae_ridge)

y_test_pred3=lasso.predict(x_test)
test_mae_lasso=mean_absolute_error(y_test, y_test_pred3) 
print("lasso Test MAE:%.4f" % test_mae_lasso)

y_test_pred4=elasticnet.predict(x_test)
test_mae_elastic=mean_absolute_error(y_test, y_test_pred4) 
print("elasticNet Test MAE:%.4f" % test_mae_elastic)


# ### **Q15. 테스트 셋에서 CHAS가 1일 때, 학습된 네 모델의 성능을 출력하시기 바랍니다.**
# * **
# - 손실함수는 mean absolute error를 이용한다.
# ---

# In[40]:


for i in range(len(x_test)):
    x_test[i][3] = 1
from sklearn.metrics import mean_absolute_error

y_test_pred1=lr.predict(x_test)
test_mae_lr=mean_absolute_error(y_test, y_test_pred1) #훈련 데이터의 평가 점수
print("lr Test MAE:%.4f" % test_mae_lr)

y_test_pred2=ridge.predict(x_test)
test_mae_ridge=mean_absolute_error(y_test, y_test_pred2) #훈련 데이터의 평가 점수
print("ridge Test MAE:%.4f" % test_mae_ridge)

y_test_pred3=lasso.predict(x_test)
test_mae_lasso=mean_absolute_error(y_test, y_test_pred3) #훈련 데이터의 평가 점수
print("lasso Test MAE:%.4f" % test_mae_lasso)

y_test_pred4=elasticnet.predict(x_test)
test_mae_elastic=mean_absolute_error(y_test, y_test_pred4) #훈련 데이터의 평가 점수
print("elasticNet Test MAE:%.4f" % test_mae_elastic)


# > **<span style="color:red">다음 문항을 풀기 전에 </span>아래 코드를 실행하시기 바랍니다.**
# >

# In[41]:


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, BatchNormalization
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.callbacks import ModelCheckpoint


# ### **Q16. 아래 조건에 맞추어 뉴럴네트워크 모델을 학습시키시기 바랍니다.**
# * **
# - Tensorflow framework를 사용한다.
# - 히든레이어는 아래와 같은 규칙에 맞추어 구성합니다.
#     * 2개 이상의 fully connected layer를 사용할 것
#     * FC layer뒤에는 batch normalization을 진행한다.
# - ModelCheckpoint 콜백으로 validation performance가 좋은 모델을 best_model.h5 파일로 저장한다.
# - 학습과정의 로그를 history에 선언하여 남긴다.
# - epochs는 200번을 진행한다.
# ---

# In[43]:


from tensorflow.keras.optimizers import Adam

model = Sequential()

model.add(Dense(64, activation='relu', input_shape=(13,)))
model.add(BatchNormalization())
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(1))

model.compile(loss='mse', optimizer=Adam(lr=0.001), metrics=['mse'])


modelpath = "best_model.h5"
checkpointer = ModelCheckpoint( filepath=modelpath, monitor='val_loss', verbose=1,
                               save_best_only=True)

history = model.fit(x_valid, y_valid, epochs=200, validation_split=0.2, callbacks=checkpointer)


# ### **Q17. 다음 조건에 맞추어 뉴럴네트워크의 학습 로그를 시각화 하시기 바랍니다.**
# * **
# - 필요한 라이브러리가 있다면 따로 불러온다.
# - epochs에 따른 loss의 변화를 시각화 한다.
# - train loss와 validation loss를 전부 시각화하고, 구별가능해야 한다.
# - 그래프의 타이틀은 'Loss'로 표시한다.
# - x축에는 'epochs'라고 표시하고 y축에는 'MSE'라고 표시한다.
# ---

# In[44]:


import matplotlib.pyplot as plt

h = history
plt.plot(h.history['mse'])
plt.plot(h.history['val_loss'])
plt.title('loss')
plt.xlabel('epochs')
plt.ylabel("MSE")
plt.show()


# In[ ]:




