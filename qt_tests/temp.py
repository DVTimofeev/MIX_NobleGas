import sys

import numpy as np
from enum import Enum, IntEnum
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import rcParams

class MouseButton(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    BACK = 8
    FORWARD = 9

class _Mode(str, Enum):
    NONE = ""
    PAN = "pan/zoom"
    ZOOM = "zoom rect"


class Snapper:
    """Snaps to data points"""

    def __init__(self, data, callback):
        self.data = data
        self.callback = callback

    def snap(self, x, y):
        pos = np.array([x, y])
        distances = np.linalg.norm(self.data - pos, axis=1)
        dataidx = np.argmin(distances)
        datapos = self.data[dataidx,:]
        self.callback(datapos[0], datapos[1])
        return datapos


class SnappingNavigationToolbar(NavigationToolbar2QT):
    """Navigation toolbar with data snapping"""

    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates)
        self.snapper = None

    def set_snapper(self, snapper):
        self.snapper = snapper

    def mouse_move(self, event):
        # if self.snapper and event.xdata and event.ydata:
            # event.xdata, event.ydata = self.snapper.snap(event.xdata, event.ydata)
        # print(event.xdata, event.ydata)
        super().mouse_move(event)
        pass

    def distance(a, b):
        return (sum([(k[0] - k[1]) ** 2 for k in zip(a, b)]) ** 0.5)

    def onclick(self, event):
        super().mouse_click(event)
        print(event.xdata, event.ydata)

    def press_pan(self, event):
        """Callback for mouse button press in pan/zoom mode."""
        print(event.xdata, event.ydata)

    def drag_pan(self, event):
        print(event.xdata, event.ydata)

    def on_press(event):
        print('you pressed', event.button, event.xdata, event.ydata)

    def _zoom_pan_handler(self, event):
        # if self.mode == _Mode.NONE:
        #     if event.name == "button_press_event":
        #         print(f'pressing at x={event.xdata}; y={event.ydata}')
        #     elif event.name == "button_release_event":
        #         print(f'releasing at x={event.xdata}; y={event.ydata}')

        if self.mode == _Mode.PAN:
            if event.name == "button_press_event":
                self.press_pan(event)
            elif event.name == "button_release_event":
                self.release_pan(event)
        if self.mode == _Mode.ZOOM:
            if event.name == "button_press_event":
                self.press_zoom(event)
            elif event.name == "button_release_event":
                self.release_zoom(event)

    def release_pan(self, event):
        """Callback for mouse button press in pan/zoom mode."""
        print(event.xdata, event.ydata)

    # def button_press_handler(self, event, canvas=None, toolbar=None):
    #     """
    #     The default Matplotlib button actions for extra mouse buttons.
    #     Parameters are as for `key_press_handler`, except that *event* is a
    #     `MouseEvent`.
    #     """
    #     print(event.xdata, event.ydata)
    #
    #     if canvas is None:
    #         canvas = event.canvas
    #     if toolbar is None:
    #         toolbar = canvas.toolbar
    #     if toolbar is not None:
    #         button_name = str(MouseButton(event.button))
    #         if button_name in rcParams['keymap.back']:
    #             toolbar.back()
    #         elif button_name in rcParams['keymap.forward']:
    #             toolbar.forward()



class Highlighter:
    def __init__(self, ax):
        self.ax = ax
        self.marker = None
        self.markerpos = None

    def draw(self, x, y):
        """draws a marker at plot position (x,y)"""
        if (x, y) != self.markerpos:
            if self.marker:
                self.marker.remove()
                del self.marker
            self.marker = self.ax.scatter(x, y, color='yellow')
            self.markerpos = (x, y)
            self.ax.figure.canvas.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        canvas = FigureCanvas(Figure(figsize=(5,3)))
        layout.addWidget(canvas)
        toolbar = SnappingNavigationToolbar(canvas, self)
        self.addToolBar(toolbar)

        data = np.random.randn(100, 2)
        ax = canvas.figure.subplots()
        ax.scatter(data[:,0], data[:,1])
        canvas.mpl_connect('button_press_event', SnappingNavigationToolbar.on_press)

        self.highlighter = Highlighter(ax)
        snapper = Snapper(data, self.highlighter.draw)
        toolbar.set_snapper(snapper)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()