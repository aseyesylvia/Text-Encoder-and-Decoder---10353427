# CipherLab - Text Encoder & Decoder

**Assignment 3** - A desktop application built with Python and Tkinter that encodes and decodes text using 12 different algorithms.

## Features

- Clean dark-themed graphical interface
- 12 algorithms, each with a short description shown in the app
- Key / shift box that adapts to the chosen algorithm
- Friendly error messages for wrong keys or invalid input
- **Use as Input** button to chain algorithms (e.g. Caesar, then Base64)
- Copy result and clear buttons

| Algorithm | Type | Key |
|-----------|------|-----|
| Caesar Cipher | Substitution cipher | Shift 0-25 |
| Vigenere Cipher | Substitution cipher | Keyword |
| Atbash Cipher | Substitution cipher | None |
| ROT13 | Substitution cipher | None |
| Rail Fence Cipher | Transposition cipher | Rails 2-10 |
| XOR Cipher | Symmetric cipher (hex output) | Secret key |
| Base64 | Encoding | None |
| Hexadecimal | Encoding | None |
| Binary | Encoding | None |
| Morse Code | Encoding | None |
| URL Encoding | Encoding | None |
| Reverse Text | Transformation | None |

## Requirements

- Python 3.8 or newer
- Tkinter (included with the standard Python installer on Windows and macOS; on Linux: `sudo apt install python3-tk`)
- No other libraries needed

## Run the application

```bash
python main.py
```

1. Choose an algorithm from the dropdown.
2. Enter a shift or key if the algorithm needs one.
3. Type or paste text into **Input Text**.
4. Click **Encode** or **Decode** (or press Ctrl+E / Ctrl+D). The answer appears in **Result**.

## Run the tests

```bash
python -m unittest -v
```

## How the code is organised

- Each algorithm has its own `encode` and `decode` function in `main.py`.
- The `ALGORITHMS` dictionary lists every algorithm with its key type, description and functions. Adding a new algorithm only needs two functions and one new entry.
- `EncoderDecoderApp` builds the interface and calls whichever algorithm is selected.

## Note

These ciphers are for learning. They are not secure and should not be used to protect sensitive data.

## Author

Courage Kofi Abusah - University of Professional Studies, Accra (UPSA)
