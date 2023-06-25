import cv2
import pytesseract

# Set up the video capture from the front camera
cap = cv2.VideoCapture(1)
harcascade = "C:\camnumplate\haskelchick.xml"
# Load the trained haarcascade classifier for license plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

s=""
# Set up Tesseract OCR engine
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

while True:
    # Read frames from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect license plates in the frame
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Process each detected license plate
    for (x, y, w, h) in plates:
        # Extract the license plate region from the frame
        plate_roi = frame[y:y+h, x:x+w]

        # Preprocess the license plate region
        gray_plate = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        gray_plate = cv2.GaussianBlur(gray_plate, (5, 5), 0)

        # Perform thresholding to enhance the text
        _, threshold_plate = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform text extraction using Tesseract OCR
        #plate_number = pytesseract.image_to_string(threshold_plate, config='--psm 7')
        custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        plate_number = pytesseract.image_to_string(gray_plate, config=custom_config)
        custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text  = pytesseract.image_to_string(threshold_plate ,lang='eng',config=custom_config)
        print(text)
        # Draw a rectangle around the license plate on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        s=plate_number
        # Draw the extracted plate number on the frame
        cv2.putText(frame, plate_number, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        print("resutl ahey"+s)

    # Display the resulting frame
    cv2.imshow('License Plate Detection', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("reslt id "+s)
        break

# Release the video capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
print("ye le pappu ")
print(plate_number)
