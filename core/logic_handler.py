from keras.models import load_model
import cv2


class Saver:
    def __init__(self) -> None:
        self.img = None
        self.original_img = None
        self.predict_img = None
        self.model_name = None

    def refresh_saver(self):
        self.img = None
        self.original_img = None
        self.predict_img = None


class Model_Controller:
    def __init__(self, path1=None, path2=None, path3=None) -> None:
        self.model_CNN = load_model(path1)
        self.model_CNN_LSTM = load_model(path2)
        self.model_CNN_RNN = load_model(path3)
        self.processed_img = None

    def process_img(self, img, img_size=150):
        try:
            resized_arr = cv2.resize(img, (img_size, img_size))
            gray_img = cv2.cvtColor(resized_arr, cv2.COLOR_BGR2GRAY)
            # Normalize img
            normalized_img = gray_img / 255.0
            reshaped_img = normalized_img.reshape(-1, img_size, img_size, 1)
            return reshaped_img
        except Exception as e:
            print("Error occurred during image preprocessing:", e)
            return None

    def predict(self, name, img):
        result = None
        processed_img = self.process_img(img)
        if name == "CNN":
            result = self.model_CNN.predict(processed_img)
        elif name == "CNN_LSTM":
            result = self.model_CNN_LSTM.predict(processed_img)
        elif name == "CNN_RNN":
            result = self.model_CNN_RNN.predict(processed_img)
        # print(result * 100)
        result = (result > 0.5).astype(int).reshape(-1)
        # print(result)

        return result
