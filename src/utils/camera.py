"""
Camera Manager - Handles camera input and processing
"""

import cv2
import numpy as np
import mediapipe as mp

class CameraManager:
    def __init__(self):
        self.cap = None
        self.frame = None
        self.processed_frame = None
        
        # Initialize MediaPipe
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = None
        self.hands = None
        
    def initialize(self):
        """Initialize camera and MediaPipe"""
        try:
            # Try to open camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                return False
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Initialize MediaPipe
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5
            )
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def capture_frame(self):
        """Capture a frame from camera"""
        if self.cap is None:
            return False
        
        ret, frame = self.cap.read()
        if ret:
            # Flip frame horizontally for mirror effect
            self.frame = cv2.flip(frame, 1)
            self.processed_frame = self.frame.copy()
            return True
        return False
    
    def detect_faces(self):
        """Detect faces in current frame"""
        if self.frame is None:
            return []
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = self.frame.shape
                
                # Convert relative coordinates to absolute
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                faces.append({
                    'x': x, 'y': y, 'width': width, 'height': height,
                    'confidence': detection.score[0]
                })
        
        return faces
    
    def detect_hands(self):
        """Detect hands in current frame"""
        if self.frame is None:
            return []
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        hands = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get hand center point
                h, w, _ = self.frame.shape
                landmarks = []
                
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    landmarks.append((x, y))
                
                # Calculate center of hand
                center_x = sum(point[0] for point in landmarks) // len(landmarks)
                center_y = sum(point[1] for point in landmarks) // len(landmarks)
                
                hands.append({
                    'center': (center_x, center_y),
                    'landmarks': landmarks
                })
        
        return hands
    
    def detect_dominant_color(self, region=None):
        """Detect dominant color in frame or region"""
        if self.frame is None:
            return None
        
        # Use center region if no region specified
        if region is None:
            h, w = self.frame.shape[:2]
            region = self.frame[h//3:2*h//3, w//3:2*w//3]
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        
        # Define color ranges in HSV
        color_ranges = {
            'red': [(0, 50, 50), (10, 255, 255)],
            'red2': [(170, 50, 50), (180, 255, 255)],  # Red wraps around
            'blue': [(100, 50, 50), (130, 255, 255)],
            'green': [(40, 50, 50), (80, 255, 255)],
            'yellow': [(20, 50, 50), (40, 255, 255)],
            'purple': [(130, 50, 50), (170, 255, 255)]
        }
        
        max_pixels = 0
        dominant_color = None
        
        for color, (lower, upper) in color_ranges.items():
            if color == 'red2':
                continue  # Handle red separately
            
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Special handling for red (it wraps around in HSV)
            if color == 'red':
                mask2 = cv2.inRange(hsv, np.array(color_ranges['red2'][0]), 
                                  np.array(color_ranges['red2'][1]))
                mask = cv2.bitwise_or(mask, mask2)
            
            pixel_count = cv2.countNonZero(mask)
            
            if pixel_count > max_pixels and pixel_count > 1000:  # Minimum threshold
                max_pixels = pixel_count
                dominant_color = color
        
        return dominant_color
    
    def get_frame_for_display(self):
        """Get frame ready for display (converted to RGB)"""
        if self.processed_frame is None:
            return None
        
        # Convert BGR to RGB for pygame
        return cv2.cvtColor(self.processed_frame, cv2.COLOR_BGR2RGB)
    
    def cleanup(self):
        """Clean up camera resources"""
        if self.cap:
            self.cap.release()
        if self.face_detection:
            self.face_detection.close()
        if self.hands:
            self.hands.close()
