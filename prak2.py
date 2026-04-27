import tkinter as tk

def cek_string(s):
    state = "S"

    for c in s:
        # print(state, c)
        if c not in "01":
            return "REJECT (invalid char)"

        if state == "S":
            if c == "1":
                state = "B"
            else:
                state = "A"

        elif state == "A":
            if c == "0":
                state = "C"
            else:
                state = "B"

        elif state == "B":
            if c == "1":
                state = "B"
            else:
                state = "A"

        elif state == "C":
            state = "C"

    if state == "B":
        return "ACCEPT"
    else:
        return "REJECT"


def proses():
    input_str = entry.get()
    hasil = cek_string(input_str)
    label_result.config(text=hasil)

window = tk.Tk()
window.title("FSM Checker")
window.geometry("350x200")

label = tk.Label(window, text="Masukkan string (0/1):")
label.pack()

entry = tk.Entry(window, width=30)
entry.pack()

button = tk.Button(window, text="Check", command=proses)
button.pack(pady=10)

label_result = tk.Label(window, text="")
label_result.pack()

window.mainloop()
