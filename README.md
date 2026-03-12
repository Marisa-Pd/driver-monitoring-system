# 🚗 Driver Monitoring System
ระบบตรวจจับพฤติกรรมอันตรายขณะขับรถแบบ Real-time
พัฒนาด้วย Raspberry Pi และ OpenCV เป็น Final Year Project

---

## 📌 ที่มาและปัญหาที่แก้ไข (Background)
อุบัติเหตุบนท้องถนนส่วนใหญ่เกิดจากความง่วงและการเสียสมาธิขณะขับรถ
โปรเจกต์นี้จึงพัฒนาระบบที่ใช้กล้องวิเคราะห์พฤติกรรมผู้ขับแบบ Real-time
และแจ้งเตือนทันทีเมื่อตรวจพบความเสี่ยง

---

## ⚙️ เทคโนโลยีที่ใช้ (Tech Stack)
| หมวด | เทคโนโลยี |
|------|-----------|
| Hardware | Raspberry Pi 4, Pi Camera, Buzzer, LCD 16x2 |
| Language | Python 3 |
| Library | OpenCV, RPi.GPIO |
| Algorithm | Haar Cascade Classifier, Hough Line Transform, Canny Edge Detection |

---

## 🔍 การทำงานของระบบ (How It Works)

### 1. ตรวจจับการหลับตา
- ใช้ Haar Cascade Classifier ที่เทรนมาสำหรับตรวจจับดวงตา
- คำนวณค่า Eye Aspect Ratio (EAR) จากสัดส่วนของเปลือกตาในแต่ละเฟรม
- ถ้า EAR ต่ำกว่าเกณฑ์ต่อเนื่องเกินจำนวนเฟรมที่กำหนด → ตัดสินว่าหลับใน

### 2. ตรวจจับการใช้โทรศัพท์
- ใช้ Haar Cascade Classifier ที่เทรนมาสำหรับจำรูปร่างโทรศัพท์
- ตรวจสอบทุกเฟรมว่ามี Pattern ของโทรศัพท์ปรากฏในภาพหรือไม่

### 3. ตรวจจับการออกนอกเลน
- กรอง Noise ด้วย Canny Edge Detection ก่อน
- ใช้ Hough Line Transform ตรวจหาเส้นถนนในภาพ
- คำนวณมุม Slope ของเส้นเพื่อประเมินว่ารถเบี่ยงออกจากเลนหรือไม่

---

## 🚨 เงื่อนไขการแจ้งเตือน (Alert Logic)
ระบบแจ้งเตือนเมื่อตรวจพบพฤติกรรมอันตราย **อย่างน้อย 2 อย่างพร้อมกัน**
เพื่อลด False Positive และป้องกันการแจ้งเตือนที่ไม่จำเป็น

| สถานการณ์ | การแจ้งเตือน |
|-----------|-------------|
| หลับตา + ออกนอกเลน | 🔊 Buzzer + 📺 LCD |
| เล่นโทรศัพท์ + ออกนอกเลน | 🔊 Buzzer + 📺 LCD |
| หลับตา + เล่นโทรศัพท์ | 🔊 Buzzer + 📺 LCD |

---

## 📁 โครงสร้างไฟล์ (File Structure)
```
driver-monitoring-system/
│
├── code_project_final.py     # ไฟล์หลักสำหรับรันระบบ
├── eyes_detection.py         # โมดูลตรวจจับการหลับตา
├── phone_detection.py       # โมดูลตรวจจับโทรศัพท์
├── lane_detection.py        # โมดูลตรวจจับเส้นเลน
│
├── haarcascade/
│   ├── haarcascade_eye.xml
│   └── haarcascade_phone.xml
│
├── requirements.txt
└── README.md
```

---

## 🛠️ วิธีติดตั้งและรัน (Installation)

**1. Clone Repository**
```bash
git clone https://github.com/ชื่อMarisa-Pd/driver-monitoring-system.git
cd driver-monitoring-system
```

**2. ติดตั้ง Library**
```bash
pip install -r requirements.txt
```

**3. รันระบบ**
```bash
code_project_final.py
```

---

## 📌 สิ่งที่ได้เรียนรู้ (What I Learned)
- การใช้ Computer Vision แก้ปัญหาจริงในชีวิตประจำวัน
- การ Tune Parameter ของ Algorithm ให้เหมาะกับสภาพแสงและสิ่งแวดล้อมจริง
- การออกแบบ Alert Logic เพื่อลด False Positive
- การทำงานร่วมกับ Hardware จริงบน Raspberry Pi

---

## 👤 ผู้พัฒนา (Developer)
**ชื่อ** — [Marisa Phongdee]  
**สาขา** — [วิศวกรรมอิเล็กทรอนิกส์และระบบคอมพิวเตอร์]  
**มหาวิทยาลัย** — [มหาวิทยาลัยศิลปากร]  
**ปีที่พัฒนา** — 2567
