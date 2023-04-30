import numpy as np
import cv2


class Processor:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.actions_history = []

    def _open_image(self, filename=None):
        """Open an image and return it"""
        try:
            return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        except:
            raise Exception("Could not open image: {}".format(filename))

    def open_image(self, filename=None):
        """Open a image to edit it"""
        try:
            _image = self._open_image(filename)
            if _image is not None:
                self.image = _image
                self.original_image = self.image.copy()
                self.actions_history.insert(0, self.image)
            else:
                raise Exception("Could not open image: {}".format(filename))
        except:
            raise Exception("Could not open image: {}".format(filename))

    def revert_image(self):
        """Set image to default"""
        self.actions_history.append(self.image)
        self.image = self.original_image.copy()

    def undo_image(self):
        """Undo image action"""
        if len(self.actions_history) > 0:
            self.image = self.actions_history.pop(-1)

    def save_image(self, location):
        """Save image in a image file"""
        try:
            cv2.imwrite(location, self.image)
        except:
            raise Exception("Specify the file format!")

    def flip_image(self, option):
        """Flip the imagen"""
        self.actions_history.append(self.image)

        if option == 'HORIZONTAL':
            self.image = cv2.flip(self.image, 1)
        elif option == 'VERTICAL':
            self.image = cv2.flip(self.image, 0)

    def grayscale_filter(self):
        """Escala de grises"""
        self.actions_history.append(self.image)

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)

    def brightness_filter(self, bias):
        """Modify the brightness"""
        self.actions_history.append(self.image)
        self.image = cv2.addWeighted(self.image, 1, np.zeros(self.image.shape, self.image.dtype), 0, bias*500-250)

    def contrast_filter(self, gain):
        """Modify the contrast"""
        self.actions_history.append(self.image)
        self.image = cv2.addWeighted(self.image, gain*10, np.zeros(self.image.shape, self.image.dtype), 0, 0)

    def negative_filter(self):
        """Set image to negative"""
        self.actions_history.append(self.image)

        self.image = 255 - self.image

    def rotate_image(self, degrees):
        """Rotate the imagen"""
        try:
            temp_img = self.image.copy()
            height = temp_img.shape[0]
            width = temp_img.shape[1]
            m = cv2.getRotationMatrix2D((width // 2, height // 2), degrees, 1)
            self.actions_history.append(self.image)
            self.image = cv2.warpAffine(temp_img, m, (width, height))
        except:
            raise Exception("Degrees need to be a real number!")

    def move_image(self, option, amount):
        """Move the imagen"""
        try:
            height = self.image.shape[0]
            width = self.image.shape[1]
            if option == 'HORIZONTAL':
                m = np.float32([[1, 0, amount], [0, 1, 0]])
            elif option == 'VERTICAL':
                m = np.float32([[1, 0, 0], [0, 1, amount]])
            else:
                m = np.float32([[1, 0, 0], [0, 1, 0]])

            self.actions_history.append(self.image)
            self.image = cv2.warpAffine(self.image, m, (width, height))
        except:
            raise Exception("Amount need to be a real number!")

    def resize_image(self, option, amount):
        """Resize the imagen"""
        try:
            h, w, _ = self.image.shape
            if option == 'WIDTH':
                w += amount
            elif option == 'HEIGHT':
                h += amount

            try:
                self.actions_history.append(self.image)
                self.image = cv2.resize(self.image, (w, h), interpolation=cv2.INTER_CUBIC)
            except:
                raise Exception("The size must be greater than 0!")
        except:
            raise Exception("Amount need to be a real number!")

    def operations(self, option, another=None):
        """Do operations"""
        if another is None:
            return
        another = self._open_image(another)
        h, w, _ = self.image.shape
        another = cv2.resize(another, (w, h), interpolation=cv2.INTER_CUBIC)
        self.actions_history.append(self.image)
        if option == 'Sum':
            self.image = cv2.add(self.image, another)
        elif option == 'Subtract':
            self.image = cv2.subtract(self.image, another)
        elif option == 'AND':
            self.image = cv2.bitwise_and(self.image, another)
        elif option == 'OR':
            self.image = cv2.bitwise_or(self.image, another)
