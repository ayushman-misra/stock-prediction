import tkinter as tk
from tkinter import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pandas_datareader import data
import datetime
from pylab import *
from sklearn.model_selection import train_test_split

def fun(stock,test,days,lconf,message):

    global f
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    f = data.DataReader(stock, 'tiingo', start, end,access_key='75470926fd68a503e3b08f0ec2341febb165d09b')
    f.reset_index(inplace=True)
    f.set_index('date',inplace=True)
    f=f[['adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',]]
    no_days=int(days)
    f['newclose']=f['adjClose'].shift(-no_days)
    x=f.drop(['adjClose','newclose'],axis=1)
    y=f['newclose'].dropna()
    x1=x[:-no_days]
    x_pr=x[-no_days:]
    x_tr,x_ts,y_tr,y_ts=train_test_split(x1,y,test_size=float(test))
    alg=LinearRegression()
    alg.fit(x_tr,y_tr)
    lconf.config(text=str(alg.score(x_ts,y_ts)))
    prd=alg.predict(x_pr)
    message.config(text=str(prd))
    lastday=f.iloc[-1].name
    f['forecast']=np.nan
    for i in prd:
        lastday+=datetime.timedelta(1)
        f.loc[lastday]=[np.nan for _ in range(6)]+[i]

def sgr():
     f['adjClose'].plot()
     f['forecast'].plot()
     plt.show()


rt=Tk()

rt.title("Stock Predictor")

label=tk.Label(rt,anchor=W,font=('verdana',15),text='Welcome to Stock Prediction Portal',bg='cyan')
label.grid(row=0,columnspan=8)

label=Label(rt,font=('verdana',15),text='Select the Stock')
label.grid(row=2,column=0)

stock=StringVar()
stock.set('Select Stock')
om=OptionMenu(rt,stock,'googl','msft')
om.grid(row=2,column=1)

l1=Label(rt,font=('verdana',15),text='Test Size')
l1.grid(row=3,column=0)

test=DoubleVar()
test.set('Select Test Size')
om1=OptionMenu(rt,test,0.1,0.2,0.3)
om1.grid(row=3,column=1)

l2=Label(rt,font=('verdana',15),text='Number Of Days')
l2.grid(row=4,column=0)

nd=Entry(rt,font=('verdana',15))
nd.grid(row=4,column=1)

b1=tk.Button(rt,text='Predict',font=('verdana',15),bg='grey',command=lambda :fun(stock.get(),test.get(),nd.get(),l4,pm))
b1.grid(row=5,column=0)

b2=tk.Button(rt,text='Show Graph',font=('verdana',15),bg='grey',command=sgr)
b2.grid(row=6,column=0)

l3=Label(rt,font=('verdana',15,'bold'),text='Acurracy Percentage')
l3.grid(row=7,column=0)

l4=Label(rt,font=('verdana',15))
l4.grid(row=7,column=1)

pm=Message(rt,font=('verdana',10))
pm.grid(row=10,columnspan=7)

rt.mainloop()
