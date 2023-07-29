import cv2
from pyzbar.pyzbar import decode

def scan_barcodes(frame):
    # Convert the frame to grayscale for barcode detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pyzbar to scan for barcodes
    barcodes = decode(gray)

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        barcode_rect_points = barcode.polygon

        print(f"Barcode Type: {barcode_type}, Data: {barcode_data}")
        if barcode_rect_points:
            # Draw the barcode boundary box
            n = len(barcode_rect_points)
            for i in range(n):
                cv2.line(frame, barcode_rect_points[i], barcode_rect_points[(i+1) % n], (0, 255, 0), 3)

    return frame

if __name__ == "__main__":
    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture video frame-by-frame
        ret, frame = video_capture.read()

        # If the frame is captured successfully
        if ret:
            # Detect and scan barcodes
            frame_with_barcodes = scan_barcodes(frame)

            # Display the frame with barcode information
            cv2.imshow('Barcode Scanner', frame_with_barcodes)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()