import pandas as pd
import numpy as np
from statistics import mean

fs = 5000
def calculate_performance(vibration_data, optimal_range=(5, 15)):
    # Assuming 'vibration_data' is a DataFrame with columns 'time' and 'vibration'
    # Optimal range is defined as a tuple (lower_bound, upper_bound)
    
    # Generate a time series based on the sampling frequency
    time_series = np.linspace(0, len(vibration_data) / fs, len(vibration_data))

    # Create DataFrame from the vibration data
    vibration_data = pd.DataFrame({
        'time': time_series,
        'vibration': vibration_data
    })

    # Calculate deviation from the optimal range
    outside_optimal = ~vibration_data['vibration'].between(*optimal_range)
    deviation = vibration_data['vibration'][outside_optimal] - optimal_range[1]
    deviation[deviation < 0] = optimal_range[0] - deviation[deviation < 0]

    # Performance could be inversely proportional to the average deviation
    average_deviation = mean(deviation) if not deviation.empty else 0
    performance_score = 1 / (1 + average_deviation)

    return performance_score


# def calculate_failure(vibration_data, critical_threshold=20):
#     # Assuming 'vibration_data' is a DataFrame with columns 'time' and 'vibration'
#     # critical_threshold defines the vibration level that is considered critical

#     # Count occurrences where vibration exceeds the critical threshold
#     failure_risk_count = (vibration_data['vibration'] > critical_threshold).sum()

#     # Calculate failure probability (simplified example)
#     total_readings = len(vibration_data)
#     failure_probability = failure_risk_count / total_readings

#     return failure_probability
