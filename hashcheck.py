import bcrypt

# Password provided by the user
password = "acculance2022".encode('utf-8')

# Hashed password provided for verification (note the '2a' prefix for compatibility with Python bcrypt)
hashed_password = b'$2a$10$fOCvclDtRbpeeM5RZ38SvebitmgbUI0U8Yiw9YsHFHQGS12R1gTym'

# Checking if the password matches the hash
if bcrypt.checkpw(password, hashed_password):
    print("The password matches the given hash.")
else:
    print("The password does not match the given hash.")
