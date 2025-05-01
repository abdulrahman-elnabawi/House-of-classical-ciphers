import tkinter as tk
from tkinter import ttk
import numpy as np

# ------ Functions for Classical Ciphers ------

# Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def caesar_crack(text):
    possibilities = ""
    for shift in range(1, 26):
        decrypted = caesar_decrypt(text, shift)
        possibilities += f"Shift {shift}: {decrypted}\n"
    return possibilities

# Affine Cipher
def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr(((a * (ord(char) - offset) + b) % 26) + offset)
        else:
            result += char
    return result

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(text, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Invalid key: 'a' has no modular inverse."
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((a_inv * ((ord(char) - offset - b)) % 26) + offset)
        else:
            result += char
    return result

def affine_crack(text):
    possibilities = ""
    for a in range(1, 26):
        if mod_inverse(a, 26) is not None:
            for b in range(26):
                decrypted = affine_decrypt(text, a, b)
                possibilities += f"a={a}, b={b}: {decrypted}\n"
    return possibilities

# Vigenere Cipher
def vigenere_encrypt(text, key):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            key_shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - offset + key_shift) % 26 + offset)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            key_shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - offset - key_shift) % 26 + offset)
            key_index += 1
        else:
            result += char
    return result

def vigenere_crack(text):
    return "Cracking Vigenere needs Kasiski Examination. (Not implemented here)"

# Playfair Cipher
def generate_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = ""
    for char in key:
        if char not in matrix:
            matrix += char
    for char in alphabet:
        if char not in matrix:
            matrix += char
    return [list(matrix[i*5:(i+1)*5]) for i in range(5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:
            result += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace(" ", "")
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            result += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def playfair_crack(text):
    return "Cracking Playfair is complex and needs dictionary attack. (Not implemented here)"

# Hill Cipher
def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        encrypted = np.dot(key_matrix, pair) % 26
        result += chr(encrypted[0]+65) + chr(encrypted[1]+65)
    return result

def hill_decrypt(text, key_matrix):
    determinant = int(np.round(np.linalg.det(key_matrix))) % 26
    determinant_inv = mod_inverse(determinant, 26)
    if determinant_inv is None:
        return "Key matrix not invertible modulo 26."

    adjugate = np.round(determinant * np.linalg.inv(key_matrix)).astype(int) % 26
    inverse_matrix = (determinant_inv * adjugate) % 26

    text = text.upper().replace(" ", "")
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        decrypted = np.dot(inverse_matrix, pair) % 26
        result += chr(decrypted[0]+65) + chr(decrypted[1]+65)
    return result

def hill_crack(text):
    return "Hill cipher cracking requires known plaintext attack. (Not implemented here)"

# Monoalphabetic Cipher
def mono_encrypt(text, key_map):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += key_map[char]
            else:
                result += key_map[char.upper()].lower()
        else:
            result += char
    return result

def mono_decrypt(text, key_map):
    inv_map = {v: k for k, v in key_map.items()}
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += inv_map[char]
            else:
                result += inv_map[char.upper()].lower()
        else:
            result += char
    return result

def mono_crack(text):
    return "Cracking monoalphabetic cipher requires frequency analysis. (Not fully implemented)"

# ------ Main Application GUI ------

# إعداد النافذة
root = tk.Tk()
root.title("Classical Ciphers")
root.geometry("900x600")
root.configure(bg="#333333")

# المتغيرات
cipher_var = tk.StringVar()
operation_var = tk.StringVar()
input_text = tk.StringVar()
key_entry = tk.StringVar()
additional_entry = tk.StringVar()

# دوال التنفيذ
def execute():
    cipher = cipher_var.get()
    operation = operation_var.get()
    text = text_box.get("1.0", "end-1c")
    key = key_entry.get()
    additional = additional_entry.get()
    
    output = ""

    try:
        if cipher == "Caesar":
            shift = int(key)
            if operation == "Encrypt":
                output = caesar_encrypt(text, shift)
            elif operation == "Decrypt":
                output = caesar_decrypt(text, shift)
            else:
                output = caesar_crack(text)
        
        elif cipher == "Affine":
            a = int(key)
            b = int(additional)
            if operation == "Encrypt":
                output = affine_encrypt(text, a, b)
            elif operation == "Decrypt":
                output = affine_decrypt(text, a, b)
            else:
                output = affine_crack(text)

        elif cipher == "Vigenere":
            if operation == "Encrypt":
                output = vigenere_encrypt(text, key)
            elif operation == "Decrypt":
                output = vigenere_decrypt(text, key)
            else:
                output = vigenere_crack(text)

        elif cipher == "Playfair":
            if operation == "Encrypt":
                output = playfair_encrypt(text, key)
            elif operation == "Decrypt":
                output = playfair_decrypt(text, key)
            else:
                output = playfair_crack(text)

        elif cipher == "Hill":
            key_matrix = np.array([[int(x) for x in key.split()[:2]], 
                                   [int(x) for x in key.split()[2:]]])
            if operation == "Encrypt":
                output = hill_encrypt(text, key_matrix)
            elif operation == "Decrypt":
                output = hill_decrypt(text, key_matrix)
            else:
                output = hill_crack(text)

        elif cipher == "Monoalphabetic":
            key_map = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", key.upper()))
            if operation == "Encrypt":
                output = mono_encrypt(text, key_map)
            elif operation == "Decrypt":
                output = mono_decrypt(text, key_map)
            else:
                output = mono_crack(text)

    except Exception as e:
        output = f"Error: {e}"

    result_box.delete("1.0", "end")
    result_box.insert("1.0", output)

# إعداد واجهة المستخدم
cipher_label = ttk.Label(root, text="Select Cipher:", foreground="white", background="#333333")
cipher_label.pack(pady=10)

cipher_options = ["Caesar", "Affine", "Vigenere", "Playfair", "Hill", "Monoalphabetic"]
cipher_menu = ttk.Combobox(root, textvariable=cipher_var, values=cipher_options, state="readonly", width=30)
cipher_menu.pack(pady=10)
cipher_menu.set("Caesar")

operation_label = ttk.Label(root, text="Select Operation:", foreground="white", background="#333333")
operation_label.pack(pady=10)

operation_options = ["Encrypt", "Decrypt", "Crack"]
operation_menu = ttk.Combobox(root, textvariable=operation_var, values=operation_options, state="readonly", width=30)
operation_menu.pack(pady=10)
operation_menu.set("Encrypt")

# نصوص الإدخال
text_label = ttk.Label(root, text="Enter Text:", foreground="white", background="#333333")
text_label.pack(pady=10)

text_box = tk.Text(root, height=6, width=50)
text_box.pack(pady=10)

key_label = ttk.Label(root, text="Enter Key:", foreground="white", background="#333333")
key_label.pack(pady=10)

key_input = ttk.Entry(root, textvariable=key_entry)
key_input.pack(pady=10)

additional_label = ttk.Label(root, text="Enter Additional Info (if needed):", foreground="white", background="#333333")
additional_label.pack(pady=10)

additional_input = ttk.Entry(root, textvariable=additional_entry)
additional_input.pack(pady=10)

execute_button = ttk.Button(root, text="Execute", command=execute)
execute_button.pack(pady=20)

# صندوق النتيجة
result_label = ttk.Label(root, text="Result:", foreground="white", background="#333333")
result_label.pack(pady=10)

result_box = tk.Text(root, height=6, width=50)
result_box.pack(pady=10)

# تشغيل البرنامج
root.mainloop()
