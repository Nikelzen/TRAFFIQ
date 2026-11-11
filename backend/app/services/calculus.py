import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid

def polynomial_analysis(times, values, degree=2):
    x=np.asarray(times,dtype=float); y=np.asarray(values,dtype=float)
    if len(x) < 3: raise ValueError("At least 3 observations are required for polynomial analysis.")
    if len(x) != len(y) or not np.isfinite(x).all() or not np.isfinite(y).all(): raise ValueError("Input arrays must be finite and have equal lengths.")
    degree=max(1,min(int(degree),len(x)-2,5))
    origin=float(x.min()); scale=float(x.max()-x.min()) or 1.0
    z=(x-origin)/scale
    coeff=np.polyfit(z,y,degree); p=np.poly1d(coeff); dp=np.polyder(p)/scale; ddp=np.polyder(p,2)/(scale**2)
    grid=np.linspace(x.min(),x.max(),max(100,len(x)*10)); zg=(grid-origin)/scale
    first_roots=np.roots(np.polyder(p)); critical=[]
    for root in first_roots:
        if abs(root.imag)<1e-8 and 0 <= root.real <= 1:
            t=origin+root.real*scale; eps=max(scale*1e-5,1e-7); left=float(dp((t-eps-origin)/scale)); right=float(dp((t+eps-origin)/scale))
            kind="local maximum" if left>0 and right<0 else "local minimum" if left<0 and right>0 else "stationary point"
            critical.append({"time":float(t),"fitted_value":float(p(root.real)),"classification":kind})
    inflections=[]
    for root in np.roots(np.polyder(p,2)):
        if abs(root.imag)<1e-8 and 0 < root.real < 1:
            t=origin+root.real*scale; eps=1e-5; l=float(ddp(root.real-eps)); r=float(ddp(root.real+eps))
            if l*r<0: inflections.append({"time":float(t),"fitted_value":float(p(root.real))})
    return {"degree":degree,"coefficients_normalized":coeff.tolist(),"grid":grid.tolist(),"fitted":p(zg).tolist(),"first_derivative":dp(zg).tolist(),"second_derivative":ddp(zg).tolist(),"residuals":(y-p(z)).tolist(),"critical_points":critical,"inflection_points":inflections,"area_trapezoidal":float(trapezoid(y,x)),"area_note":"Trapezoidal numerical approximation of the area under the fitted observation curve; discrete visitor totals are a separate sum."}
