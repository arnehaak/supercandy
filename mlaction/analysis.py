
import numpy as np


def compute_confmat(clf, X, winpercentage, threshold = 0.5, normalize=None):

  y_pred   = np.array(clf.predict(X) >= threshold, dtype=float)
  y_actual = winpercentage >= 0.5  # This is always 0.5
  confmat = np.histogram2d(y_actual, y_pred, bins=2)[0]
  
  if normalize == "true":
    confmat /= np.sum(confmat, axis = 1)
  elif normalize == "pred":
    confmat /= np.sum(confmat, axis = 0)
  elif normalize == "all":
    confmat /= np.sum(confmat[:])
           
  return confmat

  