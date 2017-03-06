-----------------------------------------------------------------------------
-- Prueba de la función generadora de números aleatorios de Lua.
-- El generador de números aleatorios está en la biblioteca Math del lenguaje.

-- Observaciones: 
-- La probabilidad de los números se aproxima más a 6/(pi)^2 cuando el intervalo-- (y el número de posibles números) es pequeño. En cuanto aumenta, la probabilidad disminuye
----------------------------------------------------------------------------

-- calcula la probabilidad de que dos números aleatorios sean coprimos
function probabilidad(a,b)
  prod = 1
  local raiz_cota = math.sqrt(a*b) -- la cota superior es el producto de ambos números  
  for i = 2, raiz_cota do 
    prod = prod * (1 - (1/i)^2)
  end
  return prod
end

-- genera los números pseudoaleatorios
for i = 1, 500 do
  print(i)
  a = math.random(2*i)
  b = math.random(2*i)
  resultado = probabilidad(a,b)
  proba = 6/(math.pi)^2 -- constante con el valor de los primeros digitos de pi
  print(" Probabilidad obtenida: " .. resultado)
  print(" Probabilidad esperada: " .. proba)
end

