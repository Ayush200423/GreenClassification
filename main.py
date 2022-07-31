from cv2_object_detection import ObjectDetection
from database import Database

class Controller:
    def __init__(self):
        self.db = Database()
        print('<-------- Login -------->')
        self.username = input('Username: ')
        self.password = input('Password: ')
        try:
            self.db.add_user(self.username, self.password)
        except:
            if self.db.authenticate_user(self.username, self.password):
                print('Authenticated')
                self.video()
            else:
                print("Error: Wrong Password.")
                quit()
        else:
            self.video()

    def video(self):
        model_path = "dnn_model/yolov4-tiny.weights"
        config_path = "dnn_model/yolov4-tiny.cfg"
        detection = ObjectDetection(model_path, config_path)
        detection.detect_items(self.username)


Controller()