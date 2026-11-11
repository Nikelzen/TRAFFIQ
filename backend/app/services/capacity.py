def calculate_capacity(forecast_values, headroom_percent: float, capacity_limit: float | None = None):
    if not forecast_values: return {"available":False,"reason":"No forecast values are available."}
    if not 0 <= headroom_percent <= 300: raise ValueError("Headroom must be between 0 and 300 percent.")
    peak=max(float(v) for v in forecast_values); recommended=peak*(1+headroom_percent/100)
    return {"available":True,"forecast_peak":peak,"headroom_percent":headroom_percent,"recommended_capacity":recommended,"capacity_limit":capacity_limit,"overload_intervals":[i for i,v in enumerate(forecast_values) if capacity_limit is not None and float(v)>capacity_limit],"unit":"visitors per forecast interval","limitation":"This estimates visitor-volume capacity only; it does not infer CPU, memory, bandwidth or server instances."}
