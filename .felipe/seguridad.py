# Datos iniciales
ciphertext = [1252, 1079, 319, 337, 231, 1100, 507, 1100, 231, 213, 192]
n = 1273
d = 713

# Descifrar cada bloque
plaintext_numbers = [pow(c, d, n) for c in ciphertext]

# Convertir a caracteres ASCII
plaintext_message = ''.join(chr(p) for p in plaintext_numbers)

print("Numeros descifrados:", plaintext_numbers)
print("Mensaje descifrado:", plaintext_message)
