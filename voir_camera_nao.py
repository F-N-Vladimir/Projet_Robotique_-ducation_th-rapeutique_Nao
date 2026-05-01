#!/usr/bin/env python3
# voir_camera_nao.py - Simple visualisation de la caméra NAO

import subprocess
import cv2
import os
import time

print("="*50)
print("CAMERA NAO - VISUALISATION EN DIRECT")
print("="*50)
print("Appuyez sur 'q' pour quitter")
print("="*50)

try:
    # Créer un script pour le flux NAO
    nao_stream_script = "/tmp/nao_viewer.py"
    with open(nao_stream_script, 'w') as f:
        f.write("""#!/usr/bin/env python2.7
import sys
import os
import time
sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy

ROBOT_IP = "11.0.0.79"
ROBOT_PORT = 9559
TEMP_IMG = "/tmp/nao_view.jpg"

video_proxy = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
resolution = 2  # 640x480
color_space = 10  # JPEG
fps = 20
name_id = video_proxy.subscribeCamera("viewer", 0, resolution, color_space, fps)

try:
    while True:
        image = video_proxy.getImageRemote(name_id)
        if image:
            jpeg_data = image[6]
            with open(TEMP_IMG, 'wb') as img_file:
                img_file.write(jpeg_data)
            print("F")
        time.sleep(0.05)
finally:
    video_proxy.unsubscribe(name_id)
""")
        os.chmod(nao_stream_script, 0o755)
    
    # Lancer le flux
    process = subprocess.Popen(["python2.7", nao_stream_script], stdout=subprocess.PIPE)
    
    frame_file = "/tmp/nao_view.jpg"
    cv2.namedWindow("Camera NAO - Vue en direct", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera NAO - Vue en direct", 800, 600)
    
    while True:
        if os.path.exists(frame_file):
            frame = cv2.imread(frame_file)
            if frame is not None:
                # Ajouter du texte
                cv2.putText(frame, "Camera NAO - Appuyez sur 'q' pour quitter", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.imshow("Camera NAO - Vue en direct", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        time.sleep(0.03)
    
    process.terminate()
    cv2.destroyAllWindows()
    
except Exception as e:
    print(f"Erreur: {e}")
