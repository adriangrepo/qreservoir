
from PyQt4 import QtGui

#see http://jdreaver.com/posts/2014-10-31-double-slider.html
class DoubleSlider(QtGui.QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set integer max and min on parent. These stay constant.
        super().setMinimum(0)
        self._max_int = 10000
        super().setMaximum(self._max_int)

        # The "actual" min and max values seen by user.
        self._min_value = 0.0
        self._max_value = 100.0
        
    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range

    def setValue(self, value):
        super().setValue(int(value / self._value_range * self._max_int))
        
    def setMinimum(self, value):
        self.setRange(value, self._max_value)

    def setMaximum(self, value):
        self.setRange(self._min_value, value)

    def setRange(self, minimum, maximum):
        old_value = self.value()
        self._min_value = minimum
        self._max_value = maximum
        self.setValue(old_value)  # Put slider in correct position
        
    def proportion(self):
        return (self.value() - self._min_value) / self._value_range