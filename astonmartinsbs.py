import cv2
import pytesseract
import mysql.connector
from mysql.connector import Error
import re
import time

harcascade = "C:\camnumplate\haskelchick.xml"
haskade="https://inf-c2b0d1f4-5cb9-4d75-8487-6149e9767b5e-no4xvrhsfq-uc.a.run.app/detect"

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1)




cap.set(3, 640) # width
cap.set(4, 480) #height

min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)



    cv2.imshow("Result", img)

    if  cv2.waitKey(1) & 0xFF == ord('s') :
       # time.sleep(1)
        print("saving ")
        #cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        
        cv2.imshow("chaan image ",img_roi)
        imgx =img_roi
        cv2.putText(img_roi, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        #cv2.imshow("Results",img)
        #imgx=img_roi
        #imgx=img
        cv2.waitKey(20)
        cv2.imshow("Results",img)
        count += 1 
        cv2.waitKey(1) & 0xFF == ord('q')
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break   
 


# Load the image

#print("imagetread done")
cv2.imshow('Original Image', imgx)

resize_test_license_plate = cv2.resize(  imgx, None, fx = 2, fy = 2,  interpolation = cv2.INTER_CUBIC)
cv2.imshow('resixe Image', resize_test_license_plate)
# Convert the image to grayscale
grayscale_resize_test_license_plate = cv2.cvtColor(  resize_test_license_plate, cv2.COLOR_BGR2GRAY)
# Apply a Gaussian blur to the image
cv2.imshow('grayscale Image',  grayscale_resize_test_license_plate)
gray_img = cv2.GaussianBlur(  grayscale_resize_test_license_plate, (5, 5), 0)

#gray_img = cv2.GaussianBlur(  grayscale_resize_test_license_plate, (4, 5), 0)
 
#print(gray_img)

# Apply a threshold to the image
#imgx = cv2.threshold(gray_img, 100, 255, cv2.THRESH_BINARY)[1]  # modfified code

imgx = cv2.threshold(grayscale_resize_test_license_plate, 100, 255, cv2.THRESH_TOZERO)[1]
#threshold_img = cv2.threshold(blurred_img, 100, 255, cv2.THRESH_BINARY)[1]   # ptoginsl code
#threshold_img=cv2.threshold(blurred_img, 0,255,cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]
 
# Extract text from the image

cv2.imshow("thisfinaliamge",imgx)
      
 #  rgb = cv2.cvtColor(threshold_img, cv2.COLOR_BGR2RGB)
#custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
text  = pytesseract.image_to_string(gray_img ,lang='eng',config=custom_config)


#text = pytesseract.image_to_string("C:\om image processing\sampleimage2.jpg")
#print("imagetread done text coversion Results are  as follows ....")
# Print the extracted text 
print("result")
print (len(text))
print(text)
pop=text.replace(" ", "")

#--------------------------------------------------------
# Replace "O" with 0 in positions 2, 3, 6, 7, 8, 9
def transform_string(input_string):
   
    if input_string.startswith(('HH', 'NH','TH','PH')):
        input_string = 'MH' + input_string[2:].strip()
    transformed_string = ''
    for i, char in enumerate(input_string):
        if i in (2, 3, 6, 7, 8, 9) and char == 'O':
            transformed_string += '0'
        elif i in (2, 3, 6, 7, 8, 9) and char == 'S':
            transformed_string += '5'
    
        else:
            transformed_string += char
    return transformed_string[:10]

# example usage
input_str = pop
output_str = transform_string(input_str)
print(output_str) # output: 'MH03BW1263'


#==========================================================
vehicle_number = output_str.strip()





print (len(vehicle_number))
# Display the original and processed images
cv2.imshow('resultant Image', imgx)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)
cursor = conn.cursor()


#vehicle_number='"'+text3+'"'




# Check if vehicle number is present in users table
select_query = "SELECT vehicle_number, vehicle_type, total_amt,user_type FROM users WHERE vehicle_number = '"+vehicle_number+"'"
#print(select_query)
#cursor.execute(select_query, (vehicle_number,))
cursor.execute(select_query, )
result = cursor.fetchone()

if result:
    # Store vehicle number in log_table
    insert_query = "INSERT INTO log_table (vehicle_number) VALUES (%s)"
    cursor.execute(insert_query, (vehicle_number,))
    
    conn.commit()
    print("Vehicle aprroved ,Gate opened . stored in log_table.")

    # Check vehicle type and increment total_amt accordingly
    vehicle_type = result[1]
    total_amt = result[2]
    user_type=result[3]
   #print("tuj lamBO AHEY "+user_type)
    if vehicle_type == 'TwoWheeler' and user_type=="Staff" :
        total_amt += 4
    elif vehicle_type == 'FourWheeler' and user_type=="Student":
        total_amt += 15
    elif vehicle_type == 'FourWheeler' and user_type=="Staff":
        total_amt += 0    

    # Update total_amt in users table
    update_query = "UPDATE users SET total_amt = %s WHERE vehicle_number = %s"
    cursor.execute(update_query, (total_amt, vehicle_number))
    conn.commit()
    print(f"Total amount updated to {total_amt} for vehicle number {vehicle_number}.")
else:
    print("Vehicle  not found  you are not approved .")

# Close MySQL connection
cursor.close()
conn.close()