import numpy as np
import pandas as pd

def detect_anomalies(df: pd.DataFrame, window=7, threshold=3.5):
    if len(df)<max(8,window+2): return {"available":False,"reason":f"At least {max(8,window+2)} ordered observations are required."}
    s=df.visitors.astype(float); prior=s.shift(1).rolling(window,min_periods=max(3,window//2)).median(); residual=s-prior
    abs_dev=(s-prior).abs().shift(1).rolling(window,min_periods=max(3,window//2)).median(); robust_z=0.6745*residual/abs_dev.replace(0,np.nan)
    found=[]
    for i,z in enumerate(robust_z):
        if pd.notna(z) and abs(float(z))>=threshold:
            expected=float(prior.iloc[i]); observed=float(s.iloc[i]); score=abs(float(z))
            found.append({"timestamp":df.timestamp.iloc[i].isoformat(),"observed":observed,"expected":expected,"deviation":observed-expected,"robust_z":float(z),"method":"rolling median + MAD robust z-score","severity":"high" if score>=6 else "medium"})
    return {"available":True,"method":"rolling median + MAD robust z-score","anomalies":found,"interpretation":"Anomalies indicate unusual observations, not proof of attacks or malicious activity."}
