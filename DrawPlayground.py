import numpy as np


class DrawPlayground:
    data = np.zeros((400, 200, 3), dtype=np.uint8)

    def __init__(self, playground_window, position_text):
        self.textImage = playground_window
        self.textField = position_text
        return_playground = self.draw_playground_empty()
        self.post_playgroung(return_playground)


    def draw_playground_empty(self):
        #idraw = [56, 72, 88, 104, 120, 136, 152, 168, 184, 200, 216, 232, 248, 264, 280, 296, 312, 328, 344]
        #jdraw = [36, 52, 68, 84, 100, 116, 132, 148, 164]
        for i in range(50, 350):
            for j in range(20, 180):
                if (i-56) % 16 == 0 or (j-36) % 16 == 0:
                    self.data[i, j] = [0, 0, 0]
                else:
                    self.data[i, j] = [255, 255, 255]
        return self.data

    def draw_robot(self, i, j):
        self.textField.value = "[ i = %d to %d, j = %d to %d]" % (i, i + 1, j, j + 1)
        i = (i * 16) + 57 #121 si i = 4
        j = (j * 16) + 37 #85 si j = 3
        for k in range(i, i+31):
            for l in range(j, j+31):
                self.data[k, l] = [255, 20, 147]
        return self.data

    def de_draw_robot(self, i, j):
        i = (i * 16) + 57
        j = (j * 16) + 37
        for k in range(i, i+31):
            for l in range(j, j+31):
                if k == i + 15 or l == j + 15:
                    self.data[k, l] = [0, 0, 0]
                else:
                    self.data[k, l] = [255, 255, 255]
        return self.data

    def post_playgroung(self, data):
        self.textImage.value = data
