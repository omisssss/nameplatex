import cv2
import pytesseract
import mysql.connector

harcascade = "C:/camnumplate/haskelchick.xml"
haskade = "https://inf-c2b0d1f4-5cb9-4d75-8487-6149e9767b5e-no4xvrhsfq-uc.a.run.app/detect"

cap = cv2.VideoCapture(1)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
best_number_plate_text = None
best_frame = None
best_score = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y:y + h, x:x + w]
            number_plate_text = pytesseract.image_to_string(img_roi, config='--psm 7')

            if number_plate_text and len(number_plate_text) > best_score:
                best_number_plate_text = number_plate_text
                best_frame = img_roi.copy()
                best_score = len(number_plate_text)

    cv2.imshow("Result", img)

    if best_frame is not None:
        cv2.imshow("Best Frame", best_frame)
        cv2.imwrite("best_captured_frame.jpg", best_frame)
        print("Best Detected Number Plate:", best_number_plate_text)

        # MySQL operations
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="your_database"
            )

            cursor = conn.cursor()
            insert_query = "INSERT INTO log_table (vehicle_number) VALUES (%s)"
            cursor.execute(insert_query, (best_number_plate_text,))
            conn.commit()
            print("Vehicle approved, Gate opened, stored in log_table.")

            # Your additional MySQL operations here
            # ...

            cursor.close()
            conn.close()

        except mysql.connector.Error as error:
            print("Error: ", error)
    else:
        print("No number plate detected")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()