import cv2

def capture_image(filename="temp_capture.jpg"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Webcam non accessible")
        return None

    print("[INFO] Appuie sur ESPACE pour capturer")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)

        if key == 32:  # touche espace
            cv2.imwrite(filename, frame)
            print("[INFO] Image capturée :", filename)
            break

        elif key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

    return filename
