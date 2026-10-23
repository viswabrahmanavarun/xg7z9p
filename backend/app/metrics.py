from typing import List, Dict
import numpy as np

def _align_series(forecast: List[Dict], actual: List[Dict]):
    """Align forecast and actual series by startTime.
    Returns two numpy arrays of generation values in the same order.
    """
    # Build dicts keyed by startTime for quick lookup
    actual_dict = {item["startTime"]: item["generation"] for item in actual}
    forecast_vals = []
    actual_vals = []
    for f in forecast:
        ts = f["startTime"]
        if ts in actual_dict:
            forecast_vals.append(f["generation"])
            actual_vals.append(actual_dict[ts])
    return np.array(forecast_vals), np.array(actual_vals)

def compute_metrics(forecast: List[Dict], actual: List[Dict]):
    """Calculate MAE, RMSE and bias (mean error) between forecast and actual.
    Returns tuple (mae, rmse, bias).
    """
    if not forecast or not actual:
        raise ValueError("Empty series provided")
    f_arr, a_arr = _align_series(forecast, actual)
    if f_arr.size == 0:
        raise ValueError("No overlapping timestamps between forecast and actual")
    errors = f_arr - a_arr
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors ** 2)))
    bias = float(np.mean(errors))
    return mae, rmse, bias
