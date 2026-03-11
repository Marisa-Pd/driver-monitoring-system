# Driver Monitoring System

ระบบตรวจจับพฤติกรรมอันตรายขณะขับรถ 
โดยใช้ Raspberry Pi และ OpenCV

## อุปกรณ์ที่ใช้
- Raspberry Pi 4
- กล้อง Web Camera
- Buzzer
- LCD Display 16x2

## ฟีเจอร์
- ตรวจจับการหลับตาด้วย Haar Cascade + EAR
- ตรวจจับโทรศัพท์ด้วย Haar Cascade
- ตรวจจับการออกนอกเลนด้วย Hough Line Transform

## วิธีติดตั้ง
pip install -r requirements.txt

## วิธีรัน
python main.py
