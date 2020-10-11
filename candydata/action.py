
import pandas as pd
import numpy as np


def get_featvecs(df, features, featvecs_only = False):

  df = df.copy(deep=True)
    
  X = df[features].to_numpy()  
  X[X==0] = -1
  
  if featvecs_only:
    return X
  else:
    names = df['competitorname'].tolist()
    wp    = df['winpercent'].to_numpy() / 100.0
    return names, X, wp
  
  
def unpackbits(x, num_bits):
  # Bit unpacking with arbirtry number of bits (Numpy's internal function is
  # limit to 8 bits).
  
  xshape = list(x.shape)
  x = x.reshape([-1, 1])
  mask = 2**np.arange(num_bits).reshape([1, num_bits])
  bitmatrix = (x & mask).astype(bool).astype(int).reshape(xshape + [num_bits])
  bitmatrix = np.flip(bitmatrix, axis = 1)
  return bitmatrix
 

def generate_all_candy_df(features): 
    
  num_rows = 2 ** len(features)

  data = unpackbits(np.arange(num_rows), len(features))
      
  df_initializer = dict()

  for col_idx, feature in enumerate(features):
    df_initializer[feature] = data[:, col_idx]
    
  df_initializer['wp_est']  = float('nan')
  df_initializer['comment'] = ['' for _ in range(num_rows)]

  return pd.DataFrame(data = df_initializer)
  
  
def encode_binvec_as_int(binvec):
  assert binvec.dtype == np.bool
  assert len(binvec.shape) == 1
  binvec = binvec.reshape(1, -1)
  assert binvec.shape[0] == 1
  num_bits = binvec.shape[1]
  assert num_bits <= 16
  
  curr_features = np.hstack([np.zeros([1, 16 - num_bits]), binvec]).astype(np.uint8)
  
  return np.packbits(curr_features.reshape(-1, 2, 8)[:, ::-1]).view(np.uint16)[0]

 
def generate_unique_featvec_df(df, features): 

  # Determine unique feature vectors
  known_candies = dict()

  for _, row in df.iterrows():    
    featvec_encoded = encode_binvec_as_int(row[features].to_numpy().astype(np.bool))

    wp_curr = row['winpercent']
    
    if featvec_encoded in known_candies:
      curr_entry = known_candies[featvec_encoded]
      curr_entry['comment'] += ", " + row['competitorname']
      curr_entry['wp_min'] = min(wp_curr, curr_entry['wp_min'])
      curr_entry['wp_max'] = max(wp_curr, curr_entry['wp_max'])
    else:
      known_candies[featvec_encoded] = {
        'comment': row['competitorname'],
        'wp_min':  wp_curr,
        'wp_max':  wp_curr
        }

  known_featvecs_encoded = list(known_candies.keys())
  
  candies_grouped = [entry['comment'] for entry in known_candies.values()]
  wp_min = [entry['wp_min'] for entry in known_candies.values()]
  wp_max = [entry['wp_max'] for entry in known_candies.values()]
        
  data = unpackbits(np.asarray(known_featvecs_encoded), len(features))
      
  df_initializer = dict()

  for col_idx, feature in enumerate(features):
    df_initializer[feature] = data[:, col_idx]
    
  df_initializer['comment'] = candies_grouped
  df_initializer['wp_min']  = wp_min
  df_initializer['wp_max']  = wp_max

  return pd.DataFrame(data = df_initializer)
  
  
def match_candies(df_allcandy, df_orig, features):

  # Determine unique feature vectors
  known_candies = dict()

  for _, row in df_orig.iterrows():    
    featvec_encoded = encode_binvec_as_int(row[features].to_numpy().astype(np.bool))

    if featvec_encoded in known_candies:
      known_candies[featvec_encoded] += ", " + row['competitorname']
    else:
      known_candies[featvec_encoded] = row['competitorname']
  
  # Insert comments into the data frame of all possible candies
  for idx_row, row in df_allcandy.iterrows():  
    featvec_encoded = encode_binvec_as_int(row[features].to_numpy().astype(np.bool))

    if featvec_encoded in known_candies:
      df_allcandy.loc[idx_row, 'comment'] = known_candies[featvec_encoded]
    else:
      df_allcandy.loc[idx_row, 'comment'] = '(unique)'
        