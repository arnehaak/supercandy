

import statsmodels.api as sm
import statsmodels.formula.api as sm_formula


def fit_logreg_fancy(X, winpercentage, features):

  # TODO: Implement
  logistic_model = sm_formula.logit('winpercentage ~ xxx', data)
  result = logistic_model.fit()


def fit_logreg_linear(X, winpercentage, features):

  logit_model = sm.Logit(winpercentage, X)
  
  #logit_model.endog_names[:] = ['winpercentage']
  logit_model.exog_names[:]  = features
  
  clf = logit_model.fit()
  
  return clf
  