import unittest
from unittest.mock import MagicMock
from Gui import BaseStation
from UI.WebSockeCommunicationt import WebSocket
from UI.CameraMondeVideoFeed import CameraMonde
from UI.MapRender import DrawPlayground
import numpy as np
import websockets
import cv2



class TestMethods(unittest.TestCase):

    def setUp(self):
        self.station = BaseStation
        self.web_socket = WebSocket
        self.camera_monde = CameraMonde
        self.draw_playgroung = DrawPlayground(MagicMock, MagicMock)

    def test_Playground_empty(self):
        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        self.assertIs(self.draw_playgroung.data.all(), test_data.all())

    def test__draw_Playground(self):
        returned_data = self.draw_playgroung.draw_playground_empty()
        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        for i in range(50, 350):
            for j in range(20, 180):
                if (i - 56) % 16 == 0 or (j - 36) % 16 == 0:
                    test_data[i, j] = [0, 0, 0]
                else:
                    test_data[i, j] = [255, 255, 255]
        self.assertIs(returned_data.all(), test_data.all())

    def test_draw_robot(self):
        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        for i in range(50, 350):
            for j in range(20, 180):
                if (i - 56) % 16 == 0 or (j - 36) % 16 == 0:
                    test_data[i, j] = [0, 0, 0]
                else:
                    test_data[i, j] = [255, 255, 255]
        i = 8
        j = 3
        i = (i * 16) + 57  # 121 si i = 4
        j = (j * 16) + 37  # 85 si j = 3
        for k in range(i, i + 31):
            for l in range(j, j + 31):
                test_data[k, l] = [255, 20, 147]
        returned_data = self.draw_playgroung.draw_playground_empty()
        returned_data = self.draw_playgroung.draw_robot(8, 3)
        self.assertEqual(returned_data.all(), test_data.all())

    def test_de_draw_robot(self):
        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        for i in range(50, 350):
            for j in range(20, 180):
                if (i - 56) % 16 == 0 or (j - 36) % 16 == 0:
                    test_data[i, j] = [0, 0, 0]
                else:
                    test_data[i, j] = [255, 255, 255]
        i = 8
        j = 3
        i = (i * 16) + 57  # 121 si i = 4
        j = (j * 16) + 37  # 85 si j = 3
        for k in range(i, i + 31):
            for l in range(j, j + 31):
                test_data[k, l] = [255, 20, 147]
        i = 8
        j = 3
        i = (i * 16) + 57
        j = (j * 16) + 37
        for k in range(i, i + 31):
            for l in range(j, j + 31):
                if k == i + 15 or l == j + 15:
                    test_data[k, l] = [0, 0, 0]
                else:
                    test_data[k, l] = [255, 255, 255]
        self.draw_playgroung.draw_playground_empty()
        self.draw_playgroung.draw_robot(8, 3)
        returned_data = self.draw_playgroung.de_draw_robot(8, 3)
        self.assertIs(returned_data.all(), test_data.all())

    def test_camera_monde(self):
        capture = cv2.VideoCapture(0)
        frame = capture.read()
        test_data = np.zeros((600, 512, 3), dtype=np.uint8)
        self.assertIsNot(frame[1], test_data)

    async def test_ping(self):
        async with websockets.connect(
                'ws://localhost:7654/pong') as websocket:
            pong = await websocket.recv()
            self.assertEqual(pong, "pong")


if __name__ == '__main__':
    unittest.main()
