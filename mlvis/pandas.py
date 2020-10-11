
def is_class_match(wp_gt, wp_est, thresh):
  return ( (wp_gt < thresh) and (wp_est < thresh) ) or ( (wp_gt >= thresh) and (wp_est >= thresh) )

  
def apply_class_mismatch_highlighting(row, cols, thresh, color):
  col_wp_gt, col_wp_est = cols
  styles = {col: '' for col in row.index}
  if not is_class_match(row[col_wp_gt], row[col_wp_est], thresh):
    styles[col_wp_gt]  = 'background-color: %s' % color
    styles[col_wp_est] = 'background-color: %s' % color
  return styles

  
def highlight_class_mismatches(df, cols, thresh, color='orange'):
  return df.style.apply(lambda x: apply_class_mismatch_highlighting(x, cols, thresh, color), axis=1)

  
  
  
def apply_differences_highlighting(row, cols, thresh, color):
  col_a, col_b = cols
  styles = {col: '' for col in row.index}
  if abs(row[col_a] - row[col_b]) > thresh:
    styles[col_a] = 'background-color: %s' % color
    styles[col_b] = 'background-color: %s' % color
  return styles

  
def highlight_differences(df, cols, thresh, color='orange'):
  return df.style.apply(lambda x: apply_differences_highlighting(x, cols, thresh, color), axis=1)
