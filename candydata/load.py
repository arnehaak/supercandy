
import os
import io
import codecs
import pandas as pd


def load_data():

  filename = os.path.join(os.path.dirname(__file__), 'candy-data.csv')
 
  # Encoding is broken: It looks like UTF-16 Big Endian with BOM, but
  # the ’ character is not encoded properly.
  
  with open(filename, 'rb') as f:
    encoded_text = f.read()
  bom = codecs.BOM_UTF16_BE
  assert encoded_text.startswith(bom)
  encoded_text = encoded_text[len(bom):]
  decoded_text = encoded_text.decode('utf-16be')

  # Fix broken character
  decoded_text = decoded_text.replace('Õ', '’')
  
  # Encode to UTF-8
  encoded_utf8 = io.BytesIO()
  encoded_utf8.write(decoded_text.encode('utf-8'))  
  encoded_utf8.seek(0)
  
  return pd.read_csv(encoded_utf8, encoding='utf-8')
