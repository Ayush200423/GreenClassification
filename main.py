from cv2_object_detection import ObjectDetection

def main():
    model_path = "dnn_model/yolov4-tiny.weights"
    config_path = "dnn_model/yolov4-tiny.cfg"

    detection = ObjectDetection(model_path, config_path)
    detection.detect_items()

if __name__ == '__main__':
    main()