import tkinter as tk
from tkinter import messagebox, scrolledtext

gejala_tht = {
    "G1": "Nafas abnormal", "G2": "Suara serak", "G3": "Perubahan kulit",
    "G4": "Telinga penuh", "G5": "Nyeri bicara menelan", "G6": "Nyeri tenggorokan",
    "G7": "Nyeri leher", "G8": "Pendarahan hidung", "G9": "Telinga berdenging",
    "G10": "Airliur menetes", "G11": "Perubahan suara", "G12": "Sakit kepala",
    "G13": "Nyeri pinggir hidung", "G14": "Serangan vertigo", "G15": "Getah bening",
    "G16": "Leher bengkak", "G17": "Hidung tersumbat", "G18": "Infeksi sinus",
    "G19": "Beratbadan turun", "G20": "Nyeri telinga", "G21": "Selaput lendir merah",
    "G22": "Benjolan leher", "G23": "Tubuh tak seimbang", "G24": "Bolamata bergerak",
    "G25": "Nyeri wajah", "G26": "Dahi sakit", "G27": "Batuk",
    "G28": "Tumbuh dimulut", "G29": "Benjolan dileher", "G30": "Nyeri antara mata",
    "G31": "Radang gendang telinga", "G32": "Tenggorokan gatal", "G33": "Hidung meler",
    "G34": "Tuli", "G35": "Mual muntah", "G36": "Letih lesu", "G37": "Demam"
}

aturan_penyakit = {
    "Tonsilitis": ["G37", "G12", "G5", "G27", "G6", "G21"],
    "Sinusitis Maksilaris": ["G37", "G12", "G27", "G17", "G33", "G36", "G29"],
    "Sinusitis Frontalis": ["G37", "G12", "G27", "G17", "G33", "G36", "G21", "G26"],
    "Sinusitis Edmoidalis": ["G37", "G12", "G27", "G17", "G33", "G36", "G21", "G30", "G13", "G26"],
    "Sinusitis Sfenoidalis": ["G37", "G12", "G27", "G17", "G33", "G36", "G29", "G7"],
    "Abses Peritonsiler": ["G37", "G12", "G6", "G15", "G2", "G29", "G10"],
    "Faringitis": ["G37", "G5", "G6", "G7", "G15"],
    "Kanker Laring": ["G5", "G27", "G6", "G15", "G2", "G19", "G1"],
    "Deviasi Septum": ["G37", "G17", "G20", "G8", "G18", "G25"],
    "Laringitis": ["G37", "G5", "G15", "G16", "G32"],
    "Kanker Leher & Kepala": ["G5", "G22", "G8", "G28", "G3", "G11"],
    "Otitis Media Akut": ["G37", "G20", "G35", "G31"],
    "Contact Ulcers": ["G5", "G2"],
    "Abses Parafaringeal": ["G5", "G16"],
    "Barotitis Media": ["G12", "G20"],
    "Kanker Nafasoring": ["G17", "G8"],
    "Kanker Tonsil": ["G6", "G29"],
    "Neuronitis Vestibularis": ["G35", "G24"],
    "Meniere": ["G20", "G35", "G14", "G4"],
    "Tumor Syaraf Pendengaran": ["G12", "G34", "G23"],
    "Kanker Leher Metastatik": ["G29"],
    "Osteosklerosis": ["G34", "G9"],
    "Vertigo Postular": ["G24"]
}

def proses_diagnosa():
    pilihan_indeks = listbox_gejala.curselection()
    
    if not pilihan_indeks:
        messagebox.showwarning("Peringatan", "Harap pilih minimal satu gejala yang dialami!")
        return

    gejala_dialami = []
    for i in pilihan_indeks:
        teks_item = listbox_gejala.get(i)
        kode = teks_item.split(" - ")[0]
        gejala_dialami.append(kode)

    hasil_diagnosa = []
    for penyakit, list_gejala_aturan in aturan_penyakit.items():
        gejala_cocok = set(gejala_dialami).intersection(set(list_gejala_aturan))
        jumlah_cocok = len(gejala_cocok)
        
        if jumlah_cocok > 0:
            persentase = (jumlah_cocok / len(list_gejala_aturan)) * 100
            hasil_diagnosa.append({
                "penyakit": penyakit,
                "persentase": persentase,
                "jumlah_cocok": jumlah_cocok,
                "total_syarat": len(list_gejala_aturan)
            })

    hasil_diagnosa = sorted(hasil_diagnosa, key=lambda x: x["persentase"], reverse=True)

    teks_hasil.config(state=tk.NORMAL)
    teks_hasil.delete(1.0, tk.END)
    
    teks_hasil.insert(tk.END, "=== HASIL DIAGNOSA ===\n\n")
    
    if not hasil_diagnosa:
        teks_hasil.insert(tk.END, "Tidak dapat mendiagnosa penyakit dari gejala yang dipilih.\n")
    else:
        teks_hasil.insert(tk.END, "Kemungkinan penyakit yang Anda alami:\n\n")
        for idx, hasil in enumerate(hasil_diagnosa):
            if idx < 5: 
                teks_hasil.insert(tk.END, f"{idx+1}. {hasil['penyakit']}\n")
                teks_hasil.insert(tk.END, f"   Tingkat kecocokan: {hasil['persentase']:.1f}% ({hasil['jumlah_cocok']}/{hasil['total_syarat']} gejala)\n\n")
        
        if hasil_diagnosa[0]["persentase"] == 100.0:
            teks_hasil.insert(tk.END, f"KESIMPULAN: Diagnosa sangat kuat mengarah pada penyakit {hasil_diagnosa[0]['penyakit']}.")
        else:
            teks_hasil.insert(tk.END, f"KESIMPULAN: Diagnosa tertinggi adalah {hasil_diagnosa[0]['penyakit']}, namun gejala tidak sepenuhnya lengkap/spesifik.")
            
    teks_hasil.config(state=tk.DISABLED)

def reset_pilihan():
    listbox_gejala.selection_clear(0, tk.END)
    teks_hasil.config(state=tk.NORMAL)
    teks_hasil.delete(1.0, tk.END)
    teks_hasil.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Sistem Pakar Diagnosa THT")
window.geometry("600x650")
window.configure(padx=20, pady=20)

label_judul = tk.Label(window, text="Aplikasi Sistem Pakar Penyakit THT", font=("Arial", 16, "bold"))
label_judul.pack(pady=(0, 10))

label_instruksi = tk.Label(window, text="Pilih gejala yang Anda alami (bisa pilih lebih dari satu):", font=("Arial", 10))
label_instruksi.pack(anchor="w")

frame_listbox = tk.Frame(window)
frame_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

scrollbar = tk.Scrollbar(frame_listbox)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_gejala = tk.Listbox(frame_listbox, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, font=("Arial", 11), height=12)
for kode, nama in gejala_tht.items():
    listbox_gejala.insert(tk.END, f"{kode} - {nama}")
listbox_gejala.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_gejala.yview)

frame_tombol = tk.Frame(window)
frame_tombol.pack(pady=10)

btn_diagnosa = tk.Button(frame_tombol, text="Diagnosa Penyakit", command=proses_diagnosa, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_diagnosa.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(frame_tombol, text="Reset Pilihan", command=reset_pilihan, bg="#f44336", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_reset.grid(row=0, column=1, padx=5)

label_hasil = tk.Label(window, text="Hasil Analisa:", font=("Arial", 10, "bold"))
label_hasil.pack(anchor="w", pady=(10, 0))

teks_hasil = scrolledtext.ScrolledText(window, height=10, font=("Consolas", 10), state=tk.DISABLED, bg="#f9f9f9")
teks_hasil.pack(fill=tk.BOTH, expand=True)

window.mainloop()