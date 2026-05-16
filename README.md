# ⚔️ SABRR.. NANTI JUGA NYERANG — Turn-Based RPG Dungeon Crawler

![Start Screen](Screenshot%202026-05-16%20232844.png)

**SABRR.. NANTI JUGA NYERANG** adalah sebuah proyek eksperimental game bergenre *Turn-Based Strategy RPG* yang dibangun menggunakan bahasa pemrograman **Python** dan *library* **Pygame**. Game ini berfokus pada manajemen sumber daya *party*, strategi pemilihan aksi, dan ketahanan (*survival*) di dalam penjelajahan sebuah *dungeon* yang berbahaya.

---

## 🎮 Mekanisme Sistem Permainan (Game Mechanics)

Sebagai seorang *Game Designer*, sistem inti permainan ini dirancang untuk memberikan tantangan taktis yang menuntut kalkulasi matang dari pemain melalui mekanik berikut:

* **Fixed Trio Party:** Pemain langsung diberikan kendali penuh atas 3 anggota *party* dengan kelas (*class*) yang unik sejak awal permainan.
* **Dungeon Crawler Gauntlet:** Pemain dipaksa memasuki *dungeon* dan harus menyelesaikan setiap tahapan (*stage*) dengan cara mengalahkan seluruh monster yang menghadang.
* **Persistent HP System (Mekanik Utama):** Sisa HP (*Health Points*) dari setiap anggota *party* **tidak akan dipulihkan (reset)** saat berhasil melewati suatu *stage*. Kerusakan yang diterima bersifat permanen hingga pemain mencapai lantai terakhir.
* **Ultimate Objective:** Mempertahankan seluruh anggota tim agar tetap hidup demi menghadapi *Final Boss* di *stage* tertinggi. Kehilangan satu anggota akan merusak sinergi taktis *party*.
* **Attacking Balance:** Untuk menjaga keadilan sistem pertarungan, *scaling* nilai *Basic Attack* (Pukul) dasar dibuat sama rata untuk semua anggota *party*.

---

## 🎭 Komposisi Kelas & Desain Kemampuan (Class Balancing)

Pertarungan dirancang dengan sistem sinergi tiga kelas klasik (Segitiga Strategi) untuk menghadapi musuh:

| Kelas (Class) | Jenis Serangan | Kemampuan Kunci (Skill & CORE) | Peran Taktis |
| :--- | :--- | :--- | :--- |
| **Slayer** | *Single Target* | • **Skill:** *High Single-Target Damage*<br>• **CORE:** *Ultra-High Burst Damage* | *Boss Killer* / Pengeksekusi target tunggal dengan HP besar. |
| **Mage** | *Area of Effect (AoE)* | • **Skill:** *Splash Damage* (100% target utama, 50% target sekitar)<br>• **CORE:** *Massive AoE Damage* ke seluruh musuh | *Wave Clearer* / Penghancur rombongan monster kroco. |
| **Healer** | *Support / Utility* | • **Skill:** *Single-Target Healing*<br>• **CORE:** *Party-Wide Ultimate Healing* | *Sustainer* / Penjaga stabilitas HP permanen tim antar *stage*. |

---

## 📸 Tangkapan Layar Game (Screenshots)

### 🩸 Suasana Dungeon & Progres Tahapan
Game ini menggunakan estetika visual *dark pixel art* yang didukung dengan tipografi bergaya *grunge* untuk memperkuat atmosfer eksplorasi lantai *dungeon*.

| Layar Selamat Datang | Layar Progres Tahapan |
|---|---|
| ![Welcome Screen](Screenshot%202026-05-16%20232910.png) | ![Stage 1 Screen](Screenshot%202026-05-16%20232853.png) |

### ⚔️ Antarmuka Pertarungan (Battle UI & Gameplay)
Antarmuka pertarungan dirancang seefisien mungkin untuk memberikan kejelasan informasi *state* permainan secara *real-time* kepada pemain.

![Battle Gameplay](Screenshot%202026-05-16%20232917.png)

* **Manajemen Informasi:** Indikator giliran aktif (*Turn Indicator*) dan jumlah Energi ditampilkan jelas di sisi atas layar.
* **Sistem Navigasi:** Pilihan aksi (**PUKUL**, **SKILL**, **CORE**) diletakkan di sudut kanan bawah menggunakan kontrol yang intuitif.
* **Status Party:** Bar kesehatan (HP) ditempatkan tepat di bawah masing-masing *sprite* karakter untuk memudahkan evaluasi strategi bertahan hidup.

---

## 🛠️ Spesifikasi Teknis & Dependensi

* **Bahasa Pemrograman:** Python 3.x
* **Library Utama:** Pygame
* **Arsitektur Sistem:** Sistem berbasis giliran (*Turn-Based State Machine*), kalkulasi formula *damage* dinamis, dan manajemen *render layer* untuk aset *pixel art*.

---
👨‍💻 **Didesain dan Dikembangkan oleh:** [Firmas Ferdiansya](https://github.com/dariusatera)
