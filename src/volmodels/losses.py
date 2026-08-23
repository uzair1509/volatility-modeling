import numpy as np

def mse(forecast, actual):
  return np.mean((forecast - actual)**2)

def mae(forecast, actual):
  return np.mean(np.abs(forecast - actual))

def qlike(forecast, actual):
   eps = 1e-8 #prevent div by 0
   act = np.maximum(actual, eps)
   frc = np.maximum(forecast, eps)
   return np.mean(act/frc - np.log(act/frc) - 1)
