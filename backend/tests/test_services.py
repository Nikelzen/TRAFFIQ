import pandas as pd
import pytest
from app.services.ingestion import parse_csv
from app.services.calculus import polynomial_analysis
from app.services.forecasting import evaluate_models, smape
from app.services.capacity import calculate_capacity
from app.services.anomalies import detect_anomalies

def test_csv_valid():
    df=parse_csv(b"timestamp,visitors\n2026-01-01T00:00:00Z,4\n2026-01-01T01:00:00Z,8\n")
    assert df.visitors.tolist()==[4,8]
def test_csv_missing_values_rejected():
    with pytest.raises(Exception):parse_csv(b"timestamp,visitors\n2026-01-01T00:00:00Z,\n")
def test_csv_negative_rejected():
    with pytest.raises(Exception):parse_csv(b"timestamp,visitors\n2026-01-01T00:00:00Z,-1\n")
def test_calculus_quadratic_has_peak():
    r=polynomial_analysis([0,1,2,3,4],[0,3,4,3,0],2)
    assert len(r['critical_points'])==1 and r['critical_points'][0]['classification']=='local maximum'
def test_forecast_insufficient_data():
    assert evaluate_models([1,2,3])['available'] is False
def test_smape_zero_safe():
    assert smape([0,0],[0,1])>=0
def test_capacity():
    r=calculate_capacity([100,120],20,110)
    assert r['recommended_capacity']==144 and r['overload_intervals']==[1]
def test_anomaly_insufficient_data():
    assert detect_anomalies(pd.DataFrame({'timestamp':[],'visitors':[]}))['available'] is False
