import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def smape(y_true,y_pred):
    a=np.asarray(y_true,dtype=float); p=np.asarray(y_pred,dtype=float); den=np.abs(a)+np.abs(p)
    ratio=np.divide(2*np.abs(p-a),den,out=np.zeros_like(den,dtype=float),where=den!=0)
    return float(np.mean(ratio)*100)

def evaluate_models(values, horizon=3):
    y=np.asarray(values,dtype=float)
    if len(y)<8: return {"available":False,"reason":f"At least 8 ordered observations are required for the current holdout evaluation; received {len(y)}."}
    test_n=max(2,min(int(horizon),len(y)//3)); train=y[:-test_n]; actual=y[-test_n:]
    preds={"naive":np.repeat(train[-1],test_n)}
    season=min(7,len(train)//2)
    if season>=2: preds["seasonal_naive"]=np.array([train[-season+i%season] for i in range(test_n)])
    x=np.arange(len(train)).reshape(-1,1); xt=np.arange(len(train),len(train)+test_n).reshape(-1,1)
    lr=LinearRegression().fit(x,train); preds["linear_regression"]=lr.predict(xt)
    if len(train)>=20:
        rf=RandomForestRegressor(n_estimators=200,min_samples_leaf=2,random_state=42).fit(x,train); preds["random_forest"]=rf.predict(xt)
    results=[]
    for name,p in preds.items():
        results.append({"model":name,"mae":float(mean_absolute_error(actual,p)),"rmse":float(np.sqrt(mean_squared_error(actual,p))),"smape":smape(actual,p),"mape":float(np.mean(np.abs((actual-p)[actual!=0]/actual[actual!=0]))*100) if np.any(actual!=0) else None,"test_count":test_n,"actual":actual.tolist(),"predicted":np.asarray(p).tolist()})
    return {"available":True,"train_count":len(train),"test_count":test_n,"validation":"chronological holdout; no random shuffle","models":results}

def forecast(values, model="naive", horizon=7):
    y=np.asarray(values,dtype=float); h=max(1,min(int(horizon),90))
    if len(y)<3: return {"available":False,"reason":"At least 3 observations are required to fit a basic forecast."}
    if model=="naive": p=np.repeat(y[-1],h)
    elif model=="seasonal_naive":
        period=min(7,len(y)//2)
        if period<2: return {"available":False,"reason":"Seasonal naive forecasting requires at least 4 observations."}
        p=np.array([y[-period+i%period] for i in range(h)])
    elif model=="linear_regression":
        x=np.arange(len(y)).reshape(-1,1); p=LinearRegression().fit(x,y).predict(np.arange(len(y),len(y)+h).reshape(-1,1))
    else: return {"available":False,"reason":"Unsupported model. Choose naive, seasonal_naive or linear_regression."}
    return {"available":True,"model":model,"horizon":h,"predictions":[max(0,float(v)) for v in p],"warning":"Forecasts are conditional estimates, not guarantees. Uncertainty intervals are not provided by this baseline implementation."}
