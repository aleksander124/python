import os

# Safeguard password
safeguard = input("Please enter the safeguard password: ")
if safeguard != 'start':
    quit()

# Format plików do zakodowania
encrypted_ext = ('.txt',)

# Weź wszystkie pliki z maszyny
file_paths = []

for root, dirs, files in os.walk('/'):
    for file in files:
        file_path, file_ext = os.path.splitext(root + '/' + file)

        # sprawdza czy plik jest takiego samego rozszerzenia co zdefiniowaliśmy
        if file_ext in encrypted_ext:
            file_paths.append(root + '/' + file)

for f in file_paths:
    print(f)

