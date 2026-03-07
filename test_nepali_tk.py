import tkinter as tk

root = tk.Tk()
root.title("Nepali Test")

label1 = tk.Label(root, text="जिल्ला प्रशासन कार्यालय", font=("Noto Sans Devanagari", 24))
label1.pack(padx=20, pady=20)

label2 = tk.Label(root, text="जिल्ला प्रशासन कार्यालय", font=("Kalimati", 24))
label2.pack(padx=20, pady=20)

entry = tk.Entry(root, font=("Noto Sans Devanagari", 24), width=30)
entry.insert(0, "जिल्ला प्रशासन कार्यालय")
entry.pack(padx=20, pady=20)

root.mainloop()