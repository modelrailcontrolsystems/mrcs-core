"""
Created on 1 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

Simple linear regression
"""


# --------------------------------------------------------------------------------------------------------------------

class LinearRegression(object):
    """
    simple linear regression
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, data: list[tuple[float, float]]):
        self.__data = data


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def fit(self) -> tuple[float, float]:
        n = len(self)

        if n < 2:
            raise ValueError(f'Insufficient data points: {self.data}.')

        if len({x for x, _ in self.data}) < 2:
            raise ValueError(f'All data points have the same x value: {self.data}.')

        # init...
        sum_x = 0.0
        sum_y = 0.0

        sum_x2 = 0.0
        sum_xy = 0.0

        # sum....
        for x, y in self.__data:
            sum_x += x
            sum_y += y

            sum_x2 += x * x
            sum_xy += x * y

        # compute...
        avg_x = sum_x / n
        avg_y = sum_y / n

        d_x = (sum_x2 * n) - (sum_x * sum_x)
        d_y = (sum_xy * n) - (sum_x * sum_y)

        slope = d_y / d_x
        intercept = avg_y - (slope * avg_x)

        return slope, intercept


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def data(self):
        return self.__data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'LinearRegression:{{data:{self.data}}}'
