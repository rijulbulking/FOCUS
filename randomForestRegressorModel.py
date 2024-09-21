import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

n = int(input('Elapsed second: '))


data = pd.read_csv('network_data_log.csv')
X = data[['elapsed_time']]
Y_inbound = data['inbound_data']
Y_outbound = data['outbound_data']



inboundModel = RandomForestRegressor()
inboundModel.fit(X, Y_inbound)
inboundPrediction = inboundModel.predict([ [n-1] ])

outboundModel = RandomForestRegressor()
outboundModel.fit(X, Y_outbound)
outboundPrediction = outboundModel.predict([ [ n-1] ])

print(f'Actual download: {Y_inbound.iloc[n-1]}')
print(f'Predicted download: {inboundPrediction}')
print(f'Actual upload: {Y_outbound.iloc[n-1]}')
print(f'Predicted upload: {outboundPrediction}')

joblib.dump(inboundModel, 'inboundModel.joblib')
joblib.dump(outboundModel, 'outboundModel.joblib')


# # Assuming the columns are named 'elapsed_time', 'inbound_data', and 'outbound_data'
# X = data[['elapsed_time']]  # Features (independent variable)
# y_inbound = data['inbound_data']  # Target for inbound data
# y_outbound = data['outbound_data']  # Target for outbound data

# # Split the data into training and testing sets
# X_train, X_test, y_train_inbound, y_test_inbound = train_test_split(X, y_inbound, test_size=0.2, random_state=42)
# X_train, X_test, y_train_outbound, y_test_outbound = train_test_split(X, y_outbound, test_size=0.2, random_state=42)

# # Create and train the Random Forest Regressor for inbound data
# model_inbound = RandomForestRegressor(n_estimators=100, random_state=42)
# model_inbound.fit(X_train, y_train_inbound)

# # Predict inbound data
# y_pred_inbound = model_inbound.predict(X_test)

# # Print predicted and actual values for inbound data
# print("Predicted Inbound Data:", y_pred_inbound)
# print("Actual Inbound Data:", y_test_inbound.values)

# # Evaluate the model for inbound data
# mse_inbound = mean_squared_error(y_test_inbound, y_pred_inbound)
# print(f'Mean Squared Error for Inbound Data: {mse_inbound}')

# # Create and train the Random Forest Regressor for outbound data
# model_outbound = RandomForestRegressor(n_estimators=100, random_state=42)
# model_outbound.fit(X_train, y_train_outbound)

# # Predict outbound data
# y_pred_outbound = model_outbound.predict(X_test)

# # Print predicted and actual values for outbound data
# print("Predicted Outbound Data:", y_pred_outbound)
# print("Actual Outbound Data:", y_test_outbound.values)

# # Evaluate the model for outbound data
# mse_outbound = mean_squared_error(y_test_outbound, y_pred_outbound)
# print(f'Mean Squared Error for Outbound Data: {mse_outbound}')
