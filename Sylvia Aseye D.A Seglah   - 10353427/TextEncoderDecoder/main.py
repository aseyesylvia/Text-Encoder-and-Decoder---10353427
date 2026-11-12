import base64
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox


# ------------------------------------------------------------
# TEXT ENCODER & DECODER
# Educational desktop application built with Python + Tkinter
# ------------------------------------------------------------

BG = "#0B1220"
PANEL = "#111C2F"
PANEL_LIGHT = "#17243A"
INPUT_BG = "#0D1728"
BORDER = "#263750"
TEXT = "#E8EEF8"
MUTED = "#91A2BB"
ACCENT = "#35C6A5"
ACCENT_HOVER = "#27A98C"
BLUE = "#6EA8FE"
RED = "#FF7B86"


def caesar_cipher(text, shift):
    """Shift alphabetic characters while preserving case and punctuation."""
    result = []
    shift %= 26

    for char in text:
        if "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(char)

    return "".join(result)


def atbash_cipher(text):
    """Replace each English letter with its opposite in the alphabet."""
    result = []

    for char in text:
        if "a" <= char <= "z":
            result.append(chr(ord("z") - (ord(char) - ord("a"))))
        elif "A" <= char <= "Z":
            result.append(chr(ord("Z") - (ord(char) - ord("A"))))
        else:
            result.append(char)

    return "".join(result)


def base64_encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_decode(text):
    cleaned = "".join(text.split())
    try:
        decoded = base64.b64decode(cleaned, validate=True)
        return decoded.decode("utf-8")
    except ValueError:
        raise ValueError("That does not look like valid Base64 text.")


def xor_encode(text, key):
    """XOR UTF-8 bytes and return a readable hexadecimal representation."""
    if not key:
        raise ValueError("Enter an XOR key before encoding or decoding.")

    data = text.encode("utf-8")
    key_bytes = key.encode("utf-8")
    encrypted = bytes(value ^ key_bytes[i % len(key_bytes)]
                      for i, value in enumerate(data))
    return encrypted.hex().upper()


def xor_decode(text, key):
    """Read hexadecimal XOR data, reverse the XOR operation, then decode UTF-8."""
    if not key:
        raise ValueError("Enter the same XOR key used during encoding.")

    try:
        data = bytes.fromhex(text.strip())
    except ValueError:
        raise ValueError("XOR input must be valid hexadecimal text.")

    key_bytes = key.encode("utf-8")
    decrypted = bytes(value ^ key_bytes[i % len(key_bytes)]
                      for i, value in enumerate(data))
    try:
        return decrypted.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("The key may be incorrect, or the encoded text is damaged.")


# ------------------------------------------------------------
# ADDITIONAL ALGORITHMS
# ------------------------------------------------------------

def parse_shift(key):
    """Validate the Caesar shift entered by the user."""
    try:
        shift = int(str(key).strip())
    except ValueError:
        raise ValueError("The Caesar shift must be a whole number from 0 to 25.")
    if not 0 <= shift <= 25:
        raise ValueError("The Caesar shift must be between 0 and 25.")
    return shift


def parse_rails(key):
    """Validate the number of rails for the Rail Fence cipher."""
    try:
        rails = int(str(key).strip())
    except ValueError:
        raise ValueError("The number of rails must be a whole number from 2 to 10.")
    if not 2 <= rails <= 10:
        raise ValueError("The number of rails must be between 2 and 10.")
    return rails


def vigenere_cipher(text, key, decode=False):
    """Shift each letter by the matching letter of a repeating keyword."""
    shifts = [ord(c.lower()) - ord("a") for c in key if "a" <= c.lower() <= "z"]
    if not shifts:
        raise ValueError("Enter a keyword made of letters (A-Z).")

    result = []
    position = 0
    for char in text:
        if "a" <= char <= "z" or "A" <= char <= "Z":
            shift = shifts[position % len(shifts)]
            if decode:
                shift = -shift
            base = ord("a") if char.islower() else ord("A")
            result.append(chr((ord(char) - base + shift) % 26 + base))
            position += 1
        else:
            result.append(char)

    return "".join(result)


def rot13_cipher(text):
    """Caesar cipher with a fixed shift of 13 (encoding and decoding are identical)."""
    return caesar_cipher(text, 13)


def _rail_pattern(length, rails):
    """Return the rail number each character sits on (zig-zag pattern)."""
    pattern = []
    rail, step = 0, 1
    for _ in range(length):
        pattern.append(rail)
        if rail == 0:
            step = 1
        elif rail == rails - 1:
            step = -1
        rail += step
    return pattern


def rail_fence_encode(text, rails):
    """Write the text in a zig-zag over several rails, then read each rail in turn."""
    pattern = _rail_pattern(len(text), rails)
    order = sorted(range(len(text)), key=lambda i: pattern[i])
    return "".join(text[i] for i in order)


def rail_fence_decode(text, rails):
    pattern = _rail_pattern(len(text), rails)
    order = sorted(range(len(text)), key=lambda i: pattern[i])
    result = [""] * len(text)
    for position, original_index in enumerate(order):
        result[original_index] = text[position]
    return "".join(result)


def hex_encode(text):
    return text.encode("utf-8").hex().upper()


def hex_decode(text):
    try:
        data = bytes.fromhex("".join(text.split()))
        return data.decode("utf-8")
    except ValueError:
        raise ValueError("Input must be valid hexadecimal (0-9, A-F) that decodes to text.")


def binary_encode(text):
    return " ".join(f"{byte:08b}" for byte in text.encode("utf-8"))


def binary_decode(text):
    groups = text.split()
    try:
        if not all(set(g) <= {"0", "1"} and len(g) <= 8 for g in groups):
            raise ValueError
        return bytes(int(g, 2) for g in groups).decode("utf-8")
    except ValueError:
        raise ValueError("Input must be groups of 0s and 1s (8 bits each), separated by spaces.")


def url_encode(text):
    return urllib.parse.quote(text, safe="")


def url_decode(text):
    return urllib.parse.unquote(text)


MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
}
MORSE_REVERSE = {code: letter for letter, code in MORSE_CODE.items()}


def morse_encode(text):
    """Letters are separated by spaces and words by ' / '."""
    words = []
    unsupported = set()
    for word in text.upper().split():
        letters = []
        for char in word:
            if char in MORSE_CODE:
                letters.append(MORSE_CODE[char])
            else:
                unsupported.add(char)
        words.append(" ".join(letters))

    if unsupported:
        raise ValueError("Morse code cannot represent: " + " ".join(sorted(unsupported)))
    return " / ".join(words)


def morse_decode(text):
    words = []
    for word in text.strip().split("/"):
        letters = []
        for code in word.split():
            if code not in MORSE_REVERSE:
                raise ValueError(f"Unknown Morse code: {code}")
            letters.append(MORSE_REVERSE[code])
        words.append("".join(letters))
    return " ".join(words)


def reverse_text(text):
    return text[::-1]


# Registry: every algorithm the app offers.
#   key      -> None (no key), "shift", "rails" or "text"
#   default  -> value placed in the key box when the algorithm is chosen
ALGORITHMS = {
    "Caesar Cipher": {
        "key": "shift", "default": "3",
        "label": "SHIFT VALUE", "hint": "Enter a whole number from 0 to 25.",
        "about": "Moves every letter a fixed number of places along the alphabet.",
        "encode": lambda t, k: caesar_cipher(t, parse_shift(k)),
        "decode": lambda t, k: caesar_cipher(t, -parse_shift(k)),
    },
    "Vigenere Cipher": {
        "key": "text", "default": "KEY",
        "label": "KEYWORD", "hint": "Use letters only. Use the same keyword to decode.",
        "about": "Caesar cipher whose shift changes with each letter of a keyword.",
        "encode": lambda t, k: vigenere_cipher(t, k),
        "decode": lambda t, k: vigenere_cipher(t, k, decode=True),
    },
    "Atbash Cipher": {
        "key": None,
        "about": "Swaps each letter with its mirror (A-Z, B-Y). Encode and decode are the same.",
        "encode": lambda t, k: atbash_cipher(t),
        "decode": lambda t, k: atbash_cipher(t),
    },
    "ROT13": {
        "key": None,
        "about": "Caesar cipher fixed at 13 places. Applying it twice gives the original.",
        "encode": lambda t, k: rot13_cipher(t),
        "decode": lambda t, k: rot13_cipher(t),
    },
    "Rail Fence Cipher": {
        "key": "rails", "default": "3",
        "label": "NUMBER OF RAILS", "hint": "Enter a whole number from 2 to 10.",
        "about": "Writes the text in a zig-zag over several rails, then reads each rail.",
        "encode": lambda t, k: rail_fence_encode(t, parse_rails(k)),
        "decode": lambda t, k: rail_fence_decode(t, parse_rails(k)),
    },
    "XOR Cipher": {
        "key": "text", "default": "",
        "label": "SECRET KEY", "hint": "Use the same key when decoding.",
        "about": "Combines each byte of the text with a key using XOR. Output is hexadecimal.",
        "encode": lambda t, k: xor_encode(t, k),
        "decode": lambda t, k: xor_decode(t, k),
    },
    "Base64": {
        "key": None,
        "about": "Represents text with 64 safe characters. Common in emails and web data.",
        "encode": lambda t, k: base64_encode(t),
        "decode": lambda t, k: base64_decode(t),
    },
    "Hexadecimal": {
        "key": None,
        "about": "Writes every byte of the text as two hexadecimal digits.",
        "encode": lambda t, k: hex_encode(t),
        "decode": lambda t, k: hex_decode(t),
    },
    "Binary": {
        "key": None,
        "about": "Writes every byte of the text as eight 0s and 1s.",
        "encode": lambda t, k: binary_encode(t),
        "decode": lambda t, k: binary_decode(t),
    },
    "Morse Code": {
        "key": None,
        "about": "Dots and dashes. Letters are separated by spaces and words by ' / '.",
        "encode": lambda t, k: morse_encode(t),
        "decode": lambda t, k: morse_decode(t),
    },
    "URL Encoding": {
        "key": None,
        "about": "Replaces unsafe characters with %XX codes so text can travel in a web address.",
        "encode": lambda t, k: url_encode(t),
        "decode": lambda t, k: url_decode(t),
    },
    "Reverse Text": {
        "key": None,
        "about": "Writes the text backwards. Encode and decode are the same.",
        "encode": lambda t, k: reverse_text(t),
        "decode": lambda t, k: reverse_text(t),
    },
}


class EncoderDecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CipherLab | Text Encoder & Decoder")
        self.root.configure(bg=BG)

        self.algorithm = tk.StringVar(value="Caesar Cipher")
        self.key_value = tk.StringVar(value="3")
        self.status_text = tk.StringVar(value="Ready — choose an algorithm and enter your text.")
        self.mode_text = tk.StringVar(value="ENCODE")

        self.setup_styles()
        self.build_interface()
        self.update_key_hint()
        self.fit_window()

    def fit_window(self):
        """Size the window to its content so the text boxes are never squeezed."""
        self.root.update_idletasks()
        need_h = self.root.winfo_reqheight()
        need_w = self.root.winfo_reqwidth()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        max_h = screen_h - 80

        min_h = min(need_h + 20, max_h)
        min_w = min(max(need_w, 820), screen_w - 40)
        height = min(max(min_h, 900), max_h)
        width = min(1120, screen_w - 60)
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 3)

        self.root.minsize(min_w, min_h)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.bind("<Configure>", self.on_resize)
        self.on_resize()

    def on_resize(self, event=None):
        if event is not None and event.widget is not self.root:
            return
        tall = self.root.winfo_height() >= 860
        if tall and not self.hero_visible:
            self.hero.pack(anchor="w", fill="x")
            self.hero_visible = True
        elif not tall and self.hero_visible:
            self.hero.pack_forget()
            self.hero_visible = False

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Cipher.TCombobox",
            fieldbackground=INPUT_BG,
            background=PANEL_LIGHT,
            foreground=TEXT,
            arrowcolor=ACCENT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=10,
            font=("Segoe UI", 10)
        )
        style.map(
            "Cipher.TCombobox",
            fieldbackground=[("readonly", INPUT_BG)],
            foreground=[("readonly", TEXT)],
            selectbackground=[("readonly", PANEL_LIGHT)],
            selectforeground=[("readonly", TEXT)]
        )

    def build_interface(self):
        # Main page container
        page = tk.Frame(self.root, bg=BG)
        page.pack(fill="both", expand=True, padx=28, pady=14)

        # Header
        header = tk.Frame(page, bg=BG)
        header.pack(fill="x", pady=(0, 12))

        brand_row = tk.Frame(header, bg=BG)
        brand_row.pack(fill="x")

        logo = tk.Frame(brand_row, bg=ACCENT, width=42, height=42)
        logo.pack(side="left")
        logo.pack_propagate(False)
        tk.Label(
            logo, text="C", bg=ACCENT, fg=BG,
            font=("Segoe UI", 21, "bold")
        ).pack(expand=True)

        brand_text = tk.Frame(brand_row, bg=BG)
        brand_text.pack(side="left", padx=12)

        tk.Label(
            brand_text, text="CIPHERLAB",
            bg=BG, fg=TEXT, font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")
        tk.Label(
            brand_text, text="TEXT ENCODER  /  DECODER",
            bg=BG, fg=MUTED, font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(1, 0))

        badge = tk.Label(
            brand_row, text="●  OFFLINE TOOL",
            bg=PANEL, fg=ACCENT, padx=13, pady=8,
            font=("Segoe UI", 8, "bold")
        )
        badge.pack(side="right", pady=5)

        # Large tagline: only shown when the window is tall enough (see on_resize)
        self.hero = tk.Frame(header, bg=BG)
        self.hero_visible = False

        tk.Label(
            self.hero,
            text="Protect your words. Understand the code.",
            bg=BG, fg=TEXT, font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", pady=(18, 4))

        tk.Label(
            self.hero,
            text="Explore classic ciphers and text encoding methods in one simple workspace.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w")

        # Configuration card
        config = tk.Frame(page, bg=PANEL, highlightbackground=BORDER,
                          highlightthickness=1)
        config.pack(fill="x", pady=(0, 12))

        config_inner = tk.Frame(config, bg=PANEL)
        config_inner.pack(fill="x", padx=18, pady=12)

        tk.Label(
            config_inner, text="ALGORITHM",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.algorithm_box = ttk.Combobox(
            config_inner,
            textvariable=self.algorithm,
            values=list(ALGORITHMS),
            state="readonly",
            style="Cipher.TCombobox",
            width=25
        )
        self.algorithm_box.grid(row=1, column=0, sticky="ew", padx=(0, 18))
        self.algorithm_box.bind("<<ComboboxSelected>>", self.update_key_hint)

        self.algo_desc = tk.Label(
            config_inner, text="", bg=PANEL, fg=MUTED,
            font=("Segoe UI", 8), wraplength=430, justify="left"
        )
        self.algo_desc.grid(row=2, column=0, sticky="w", pady=(6, 0))

        self.key_label = tk.Label(
            config_inner, text="SHIFT / KEY",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")
        )
        self.key_label.grid(row=0, column=1, sticky="w", pady=(0, 8))

        self.key_entry = tk.Entry(
            config_inner, textvariable=self.key_value,
            bg=INPUT_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=ACCENT,
            font=("Segoe UI", 10)
        )
        self.key_entry.grid(row=1, column=1, sticky="ew", ipady=11, padx=(0, 18))

        self.key_hint = tk.Label(
            config_inner, text="Enter a number from 0 to 25.",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 8)
        )
        self.key_hint.grid(row=2, column=1, sticky="w", pady=(6, 0))

        config_inner.columnconfigure(0, weight=1)
        config_inner.columnconfigure(1, weight=1)

        # Work areas
        workspace = tk.Frame(page, bg=BG)
        workspace.pack(fill="both", expand=True)

        input_card = self.create_text_card(
            workspace, "INPUT TEXT", "Type or paste the text you want to process."
        )
        input_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        output_card = self.create_text_card(
            workspace, "RESULT", "Your encoded or decoded result will appear here."
        )
        output_card.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self.input_text = self.input_widget
        self.output_text = self.output_widget

        # Action bar
        action_bar = tk.Frame(page, bg=BG)
        action_bar.pack(fill="x", pady=(16, 10))
        self.action_bar = action_bar

        left_actions = tk.Frame(action_bar, bg=BG)
        left_actions.pack(side="left")

        self.make_button(left_actions, "↗  ENCODE", ACCENT, BG,
                         self.encode_text, width=13).pack(side="left", padx=(0, 8))
        self.make_button(left_actions, "↙  DECODE", BLUE, BG,
                         self.decode_text, width=13).pack(side="left", padx=(0, 8))
        self.make_button(left_actions, "⇄  USE AS INPUT", PANEL_LIGHT, TEXT,
                         self.use_result_as_input, width=15,
                         outline=BORDER).pack(side="left", padx=(0, 8))
        self.make_button(left_actions, "COPY RESULT", PANEL_LIGHT, TEXT,
                         self.copy_result, width=13,
                         outline=BORDER).pack(side="left", padx=(0, 8))
        self.make_button(left_actions, "CLEAR ALL", PANEL_LIGHT, TEXT,
                         self.clear_all, width=11,
                         outline=BORDER).pack(side="left")

        # Status strip
        status = tk.Frame(page, bg=PANEL, highlightbackground=BORDER,
                          highlightthickness=1)
        status.pack(fill="x", pady=(4, 0))
        self.status_bar = status

        tk.Label(
            status, text="●", bg=PANEL, fg=ACCENT,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(12, 7), pady=9)

        tk.Label(
            status, textvariable=self.status_text,
            bg=PANEL, fg=MUTED, font=("Segoe UI", 8)
        ).pack(side="left", pady=9)

        tk.Label(
            status, text="CIPHERLAB  •  PYTHON PROJECT",
            bg=PANEL, fg="#60728D", font=("Segoe UI", 8, "bold")
        ).pack(side="right", padx=12)

        # Footer note
        footer = tk.Label(
            page,
            text="Learning tool only: these classic ciphers are for education, not for protecting sensitive information.",
            bg=BG, fg="#71829A", font=("Segoe UI", 8)
        )
        footer.pack(anchor="w", pady=(10, 0))

        # Reserve space for the buttons, status bar and footer FIRST, so the
        # text boxes can never push them off the bottom of the window.
        for widget in (workspace, action_bar, status, footer):
            widget.pack_forget()
        footer.pack(side="bottom", anchor="w", pady=(10, 0))
        status.pack(side="bottom", fill="x", pady=(4, 0))
        action_bar.pack(side="bottom", fill="x", pady=(16, 10))
        workspace.pack(fill="both", expand=True)

        # Keyboard shortcuts
        self.root.bind("<Control-e>", lambda _e: self.encode_text())
        self.root.bind("<Control-d>", lambda _e: self.decode_text())

    def create_text_card(self, parent, title, subtitle):
        card = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER,
                        highlightthickness=1)

        heading = tk.Frame(card, bg=PANEL)
        heading.pack(fill="x", padx=15, pady=(14, 3))

        tk.Label(
            heading, text=title, bg=PANEL, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            card, text=subtitle, bg=PANEL, fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        text_box = tk.Text(
            card, wrap="word", undo=True,
            bg=INPUT_BG, fg=TEXT, insertbackground=ACCENT,
            selectbackground="#285A70", selectforeground=TEXT,
            relief="flat", padx=12, pady=12, width=20, height=7,
            font=("Consolas", 10),
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        text_box.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        if title == "INPUT TEXT":
            self.input_widget = text_box
        else:
            self.output_widget = text_box

        return card

    def make_button(self, parent, text, bg, fg, command,
                    width=12, outline=None):
        button = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=ACCENT_HOVER,
            activeforeground=BG, relief="flat", bd=0,
            padx=12, pady=11, width=width,
            cursor="hand2", font=("Segoe UI", 8, "bold"),
            highlightthickness=1 if outline else 0,
            highlightbackground=outline or bg
        )
        return button

    def update_key_hint(self, _event=None):
        info = ALGORITHMS[self.algorithm.get()]
        self.algo_desc.config(text=info["about"])

        if info["key"] is None:
            self.key_label.config(text="KEY")
            self.key_hint.config(text="This algorithm does not require a key.")
            self.key_value.set("")
            self.key_entry.config(state="disabled")
        else:
            self.key_label.config(text=info["label"])
            self.key_hint.config(text=info["hint"])
            self.key_entry.config(state="normal")
            self.key_value.set(info["default"])

    def get_input(self):
        return self.input_text.get("1.0", "end-1c")

    def show_output(self, result, action):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.status_text.set(f"Success — text {action} using {self.algorithm.get()}.")

    def process(self, mode):
        """Run the selected algorithm. mode is 'encode' or 'decode'."""
        text = self.get_input()
        if not text:
            message = ("Please enter some text first." if mode == "encode"
                       else "Paste the encoded text into the input area.")
            messagebox.showinfo("Input required", message)
            return

        try:
            algorithm = ALGORITHMS[self.algorithm.get()]
            result = algorithm[mode](text, self.key_value.get())
            self.show_output(result, mode + "d")
        except (ValueError, UnicodeError) as error:
            messagebox.showerror(f"Could not {mode}", str(error))
            self.status_text.set(f"{mode.capitalize()} failed — check your input and settings.")

    def encode_text(self):
        self.process("encode")

    def decode_text(self):
        self.process("decode")

    def use_result_as_input(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Nothing to move", "There is no result to use yet.")
            return

        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", result)
        self.output_text.delete("1.0", "end")
        self.status_text.set("Result moved to the input box.")

    def copy_result(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Nothing to copy", "There is no result to copy yet.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()
        self.status_text.set("Result copied to clipboard.")

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.status_text.set("Workspace cleared — ready for new text.")


if __name__ == "__main__":
    window = tk.Tk()
    app = EncoderDecoderApp(window)
    window.mainloop()
