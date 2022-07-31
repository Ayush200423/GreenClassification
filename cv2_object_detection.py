import cv2
import math

from bin_contents import contents
from database import Database

class ObjectDetection:
    def __init__(self, model_path, config_path):
        self.classes = []
        self.temporary_count = 0
        # Dnn
        net = cv2.dnn.readNet(model_path, config_path)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(320, 320), scale=1/255)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cv2.namedWindow("Input Frame")

        self.db = Database()
        self.get_classes()

    def get_classes(self):
        with open("dnn_model/classes.txt", "r") as file_classes:
            for class_name in file_classes.readlines():
                class_name = class_name.strip('\n')
                self.classes.append(class_name)

    def detect_items(self, username):
        while True:
            # Get the frames
            _, frame = self.cap.read()

            class_ids, confidence_scores, bounding_boxes = self.model.detect(frame)
            for class_id, confidence_score, bounding_box in zip(class_ids, confidence_scores, bounding_boxes):
                (x, y, w, h) = bounding_box
                for key, value in contents.items():
                    if class_id in value:
                        cv2.putText(frame, f"{key} {math.floor(confidence_score * 1000)/10}%", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                        if key == 'Recycling / Reusable' or key == 'Electronic Waste':
                            self.temporary_count += 1
                            if self.temporary_count > 10:
                                self.db.change_points(self.db.get_points(username) + 1, username)
                                self.temporary_count = 0
                                if self.db.get_points(username) >= 10:
                                    self.db.change_points(0, username)
                                    print('GreenClassification will donate $0.10 to organizations working towards a cleaner environment.')
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == 27:
                self.destroy_program()
    
    def destroy_program(self):
        self.cap.release()
        cv2.destroyAllWindows()