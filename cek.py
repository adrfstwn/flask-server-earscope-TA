import cv2

# Ambil daftar codec yang didukung
codecs = ['H264', 'XVID', 'MP4V', 'MJPG', 'AVC1', 'VP80']

for codec in codecs:
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter('test.mp4', fourcc, 20.0, (640, 480))

    if out.isOpened():
        print(f"✅ OpenCV mendukung codec: {codec}")
    else:
        print(f"❌ OpenCV TIDAK mendukung codec: {codec}")

    out.release()
