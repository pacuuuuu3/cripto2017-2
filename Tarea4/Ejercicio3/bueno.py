#!/usr/bin/python
# -*- coding: utf-8 -*-
binario = """ 
       p\�x�j_�!��t���NoG�oP�*&y�
�&ɝ���x0��Z���ER���m�R?�q ���c����>Y�B��5}NX�q�+���&`H�˫���VzE���G\V�����oи���[p�
"""

from hashlib import sha256


if (sha256(binario).hexdigest() == "5f4cca82a2265a42bc5c391d2c24aac767d81ea110e5ecc78429d87e42cbc0ce"):
  print "hola mundo"
else:
  print "h0l4 mund0"
