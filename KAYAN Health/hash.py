from werkzeug.security import generate_password_hash 
print(generate_password_hash("1234", method="pbkdf2:sha256"))

passwords = [
    "house123", 
    "wilson123",
    "lopez123",
    "perez123",
    "ramirez123",
    "recepcion123"
]

for p in passwords: print(p, "=>", generate_password_hash(p, method="pbkdf2:sha256"))