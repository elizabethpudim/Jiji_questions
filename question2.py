import numpy as np

def mse(y_true, y_pred):
  return np.square(y_true - y_pred).mean()

def rmse(y_true, y_pred):
  mse = np.square(y_true - y_pred).mean()
  return np.sqrt(mse)

#or we can use mean_squared_error(y_true, y_pred) as well from scikit-learn
