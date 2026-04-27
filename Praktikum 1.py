import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from collections import Counter, defaultdict

# ─── Daftar kata kunci ───────────────────────────────────────────────────────
RESERVED_WORDS = {
    # C
    'auto','break','case','char','const','continue','default','do','double',
    'else','enum','extern','float','for','goto','if','inline','int','long',
    'register','restrict','return','short','signed','sizeof','static','struct',
    'switch','typedef','union','unsigned','void','volatile','while',
    # C++
    'alignas','alignof','and','and_eq','asm','bitand','bitor','bool','catch',
    'char16_t','char32_t','class','compl','concept','const_cast','constexpr',
    'consteval','constinit','decltype','delete','dynamic_cast','explicit',
    'export','false','friend','mutable','namespace','new','noexcept','not',
    'not_eq','nullptr','operator','or','or_eq','private','protected','public',
    'reinterpret_cast','requires','static_assert','static_cast','template',
    'this','throw','true','try','typeid','typename','using','virtual','wchar_t',
    'xor','xor_eq','override','final',
    # Python
    'def','import','from','as','pass','in','is','lambda','yield','with',
    'except','finally','raise','elif','global','nonlocal','assert','del',
    'None','True','False','await','async',
    # JavaScript
    'var','let','function','typeof','instanceof','const',
}

MATH_OPS = {
    '+=','-=','*=','/=','%=','**','//','==','!=','<=','>=',
    '&&','||','<<','>>','->','::',
    '+','-','*','/','%','=','<','>','!','&','|','^','~',
}

PUNCT = set('{}()[];,.:@#')
PREPROCESSOR_WORDS = {
    'include', 'define', 'ifdef', 'ifndef', 'endif',
    'if', 'elif', 'else', 'undef', 'pragma', 'error', 'line'
}

CATEGORY_ORDER = [
    'Preprocessor',
    'Reserve Word',
    'Variabel / Identifier',
    'Kalimat Matematika',
    'Simbol & Tanda Baca',
    'Angka / Literal',
    'String Literal',
    'Komentar',
    'Tidak Dikenal',
]

# ─── Tokenizer ───────────────────────────────────────────────────────────────
def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        ch = code[i]

        # Lewati whitespace
        if ch in ' \t\n\r':
            i += 1
            continue

        # Komentar // ...
        if code[i:i+2] == '//':
            val = ''
            while i < len(code) and code[i] != '\n':
                val += code[i]; i += 1
            tokens.append((val, 'Komentar'))
            continue

        # Komentar /* ... */
        if code[i:i+2] == '/*':
            val = '/*'; i += 2
            while i < len(code) and code[i:i+2] != '*/':
                val += code[i]; i += 1
            val += '*/'; i += 2
            tokens.append((val, 'Komentar'))
            continue

        # Direktif preprocessor C/C++ atau komentar Python # ...
        if ch == '#':
            line_start = code.rfind('\n', 0, i) + 1
            prefix = code[line_start:i]

            # Jika # muncul di awal baris (setelah spasi), cek apakah ini preprocessor
            if prefix.strip() == '':
                j = i + 1
                while j < len(code) and code[j] in ' \t':
                    j += 1
                word = ''
                while j < len(code) and code[j].isalpha():
                    word += code[j]
                    j += 1

                if word in PREPROCESSOR_WORDS:
                    val = ''
                    while i < len(code) and code[i] != '\n':
                        val += code[i]
                        i += 1
                    tokens.append((val, 'Preprocessor'))
                    continue

            val = ''
            while i < len(code) and code[i] != '\n':
                val += code[i]; i += 1
            tokens.append((val, 'Komentar'))
            continue

        # String literal " atau '
        if ch in ('"', "'"):
            quote = ch; val = ch; i += 1
            while i < len(code) and code[i] != quote:
                if code[i] == '\\':
                    val += code[i]; i += 1
                val += code[i]; i += 1
            val += code[i] if i < len(code) else ''; i += 1
            tokens.append((val, 'String Literal'))
            continue

        # Angka
        if ch.isdigit() or (ch == '.' and i+1 < len(code) and code[i+1].isdigit()):
            val = ''
            dot_count = 0
            while i < len(code):
                if code[i].isdigit():
                    val += code[i]
                    i += 1
                elif code[i] == '.' and dot_count == 0:
                    dot_count += 1
                    val += code[i]
                    i += 1
                else:
                    break

            # Suffix numerik sederhana (u, l, f, dsb)
            while i < len(code) and code[i].lower() in 'ulf':
                val += code[i]; i += 1
            tokens.append((val, 'Angka / Literal'))
            continue

        # Identifier atau reserved word
        if ch.isalpha() or ch == '_':
            val = ''
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                val += code[i]; i += 1
            tipe = 'Reserve Word' if val in RESERVED_WORDS else 'Variabel / Identifier'
            tokens.append((val, tipe))
            continue

        # Operator 2 karakter
        two = code[i:i+2]
        if two in MATH_OPS:
            tokens.append((two, 'Kalimat Matematika'))
            i += 2; continue

        # Operator 1 karakter
        if ch in MATH_OPS:
            tokens.append((ch, 'Kalimat Matematika'))
            i += 1; continue

        # Simbol / tanda baca
        if ch in PUNCT:
            tokens.append((ch, 'Simbol & Tanda Baca'))
            i += 1; continue

        # Tidak dikenal
        tokens.append((ch, 'Tidak Dikenal'))
        i += 1

    return tokens

# ─── Warna per kategori ───────────────────────────────────────────────────────
WARNA = {
    'Preprocessor':          '#283593',   # indigo
    'Reserve Word':          '#1565C0',   # biru tua
    'Simbol & Tanda Baca':   '#2E7D32',   # hijau
    'Variabel / Identifier': '#E65100',   # oranye
    'Kalimat Matematika':    '#C62828',   # merah
    'Angka / Literal':       '#6A1B9A',   # ungu
    'String Literal':        '#00838F',   # teal
    'Komentar':              '#757575',   # abu‑abu
    'Tidak Dikenal':         '#B71C1C',   # merah gelap
}

# ─── GUI ─────────────────────────────────────────────────────────────────────
class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer - Tugas Praktikum #1")
        self.root.geometry("950x680")
        self.root.configure(bg='#F5F5F5')

        self.tokens = []
        self.auto_job = None
        self.category_lists = {}
        self._build_ui()

    # ── Bangun antarmuka ──────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg='#1565C0', pady=10)
        header.pack(fill='x')
        tk.Label(header, text="Lexical Analyzer",
                 font=('Consolas', 18, 'bold'), bg='#1565C0', fg='white').pack()
        tk.Label(header, text="Klasifikasi Token Program Komputer",
                 font=('Consolas', 10), bg='#1565C0', fg='#BBDEFB').pack()

        # ── Konten utama ──
        main = tk.Frame(self.root, bg='#F5F5F5')
        main.pack(fill='both', expand=True, padx=12, pady=10)

        # Panel atas: input
        top = tk.LabelFrame(main, text=" Input Program (Atas) ", font=('Consolas', 10, 'bold'),
                             bg='#F5F5F5', fg='#1565C0', padx=8, pady=8)
        top.pack(fill='both', expand=True, padx=0, pady=(0, 8))

        self.txt_input = scrolledtext.ScrolledText(
            top, font=('Consolas', 11), wrap='none', height=14,
            relief='solid', bd=1, bg='#FAFAFA')
        self.txt_input.pack(fill='both', expand=True)
        self.txt_input.bind('<KeyRelease>', self.schedule_auto_analyze)

        # Tombol
        btn_frame = tk.Frame(top, bg='#F5F5F5', pady=6)
        btn_frame.pack(fill='x')

        tk.Button(btn_frame, text="▶  Analisis", command=self.run_analyze,
                  bg='#1565C0', fg='white', font=('Consolas', 10, 'bold'),
                  relief='flat', padx=12, pady=4, cursor='hand2').pack(side='left', padx=2)
        tk.Button(btn_frame, text="C / C++ Contoh", command=lambda: self.load_example('c'),
                  bg='#37474F', fg='white', font=('Consolas', 9),
                  relief='flat', padx=8, pady=4, cursor='hand2').pack(side='left', padx=2)
        tk.Button(btn_frame, text="Python Contoh", command=lambda: self.load_example('py'),
                  bg='#37474F', fg='white', font=('Consolas', 9),
                  relief='flat', padx=8, pady=4, cursor='hand2').pack(side='left', padx=2)
        tk.Button(btn_frame, text="Buka File", command=self.open_file,
                  bg='#37474F', fg='white', font=('Consolas', 9),
                  relief='flat', padx=8, pady=4, cursor='hand2').pack(side='left', padx=2)
        tk.Button(btn_frame, text="Bersihkan", command=self.clear_all,
                  bg='#B71C1C', fg='white', font=('Consolas', 9),
                  relief='flat', padx=8, pady=4, cursor='hand2').pack(side='right', padx=2)

        # Panel bawah: output terkelompok dalam kotak kategori
        bottom = tk.LabelFrame(main, text=" Hasil Token per Kategori (Bawah) ",
                               font=('Consolas', 10, 'bold'),
                               bg='#F5F5F5', fg='#1565C0', padx=8, pady=8)
        bottom.pack(fill='both', expand=True)

        # Area scrollable untuk kotak-kotak kategori
        self.canvas = tk.Canvas(bottom, bg='#F5F5F5', highlightthickness=0)
        self.cards_frame = tk.Frame(self.canvas, bg='#F5F5F5')
        self.cards_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor='nw')
        scroll_y = ttk.Scrollbar(bottom, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll_y.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')

        self.cards_frame.bind('<Configure>', self._on_cards_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Status bar
        self.status_var = tk.StringVar(value="Masukkan kode lalu klik Analisis.")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                              font=('Consolas', 9), bg='#1565C0', fg='white',
                              anchor='w', padx=10)
        status_bar.pack(fill='x', side='bottom')

    # ── Aksi ─────────────────────────────────────────────────────────────────
    def run_analyze(self):
        code = self.txt_input.get('1.0', 'end').strip()
        if not code:
            messagebox.showwarning("Kosong", "Masukkan kode program terlebih dahulu!")
            return
        self.tokens = tokenize(code)
        self.update_table()

    def _on_cards_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.cards_window, width=event.width)

    def schedule_auto_analyze(self, event=None):
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
        self.auto_job = self.root.after(350, self.auto_analyze)

    def auto_analyze(self):
        self.auto_job = None
        code = self.txt_input.get('1.0', 'end').strip()
        if not code:
            self.tokens = []
            self.update_table()
            return
        self.tokens = tokenize(code)
        self.update_table()

    def update_table(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.category_lists.clear()

        grouped_unique = defaultdict(list)
        seen_by_category = defaultdict(set)
        for val, tipe in self.tokens:
            if val not in seen_by_category[tipe]:
                seen_by_category[tipe].add(val)
                grouped_unique[tipe].append(val)

        kategori_urut = [k for k in CATEGORY_ORDER if k in grouped_unique]
        kategori_lain = sorted(k for k in grouped_unique.keys() if k not in CATEGORY_ORDER)
        kategori_semua = kategori_urut + kategori_lain

        for idx, kat in enumerate(kategori_semua):
            card = tk.LabelFrame(
                self.cards_frame,
                text=f" {kat} ({len(grouped_unique[kat])}) ",
                font=('Consolas', 9, 'bold'),
                fg=WARNA.get(kat, '#424242'),
                bg='#FFFFFF',
                padx=6,
                pady=6,
            )
            card.grid(row=idx // 2, column=idx % 2, padx=6, pady=6, sticky='nsew')

            lb_frame = tk.Frame(card, bg='#FFFFFF')
            lb_frame.pack(fill='both', expand=True)

            listbox = tk.Listbox(
                lb_frame,
                font=('Consolas', 9),
                height=8,
                relief='solid',
                bd=1,
                activestyle='none',
                exportselection=False,
            )
            listbox.pack(side='left', fill='both', expand=True)

            sb = ttk.Scrollbar(lb_frame, orient='vertical', command=listbox.yview)
            sb.pack(side='right', fill='y')
            listbox.configure(yscrollcommand=sb.set)

            for i, token in enumerate(grouped_unique[kat], 1):
                listbox.insert('end', f"{i}. {token}")

            self.category_lists[kat] = listbox

        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)

        counts = Counter(t for _, t in self.tokens)
        if self.tokens:
            total_unik = sum(len(v) for v in grouped_unique.values())
            ringkasan = "  |  ".join(f"{k}: {v}" for k, v in counts.items())
            self.status_var.set(
                f"Token mentah: {len(self.tokens)}  |  Token unik: {total_unik}  |  {ringkasan}"
            )
        else:
            self.status_var.set("Masukkan kode lalu klik Analisis.")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("File Kode", "*.c *.cpp *.py *.js *.java *.txt"), ("Semua", "*.*")])
        if path:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                self.txt_input.delete('1.0', 'end')
                self.txt_input.insert('1.0', f.read())
            self.auto_analyze()

    def clear_all(self):
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
        self.txt_input.delete('1.0', 'end')
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.category_lists.clear()
        self.tokens = []
        self.status_var.set("Masukkan kode lalu klik Analisis.")

    def load_example(self, lang):
        contoh = {
            'c': """\
#include <stdio.h>

int main() {
    int x = 10;
    float y = 3.14;
    /* Cek kondisi */
    if (x > 5) {
        x = x + y * 2;
    }
    return 0;
}""",
            'py': """\
def hitung(x, y):
    total = x + y
    if total > 10:
        return total * 2
    else:
        return 0

# Panggil fungsi
hasil = hitung(5, 7)
print(hasil)
"""
        }
        self.txt_input.delete('1.0', 'end')
        self.txt_input.insert('1.0', contoh[lang])
        self.auto_analyze()

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()