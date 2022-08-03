# -*- coding: utf-8 -*-

DEFAULT_LEFT_MARGIN: int = 10
DEFAULT_TOP_MARGIN: int = 10
DEFAULT_CONTAINER_LEFT_MARGIN: int = DEFAULT_LEFT_MARGIN * 2
DEFAULT_CONTAINER_TOP_MARGIN: int = DEFAULT_TOP_MARGIN * 2

DEFAULT_ROW_HEIGHT: int = 24                        # Default height for controls

DEFAULT_LABEL_WIDTH: int = 60
DEFAULT_LABEL_TOP_OFFSET: int = 4
DEFAULT_INPUT_CONTROL_WIDTH: int = 96               # Default width for input controls, like (entry, combobox, ...)

DEFAULT_BUTTON_HEIGHT: int = DEFAULT_ROW_HEIGHT
DEFAULT_BUTTON_WIDTH: int = DEFAULT_INPUT_CONTROL_WIDTH
DEFAULT_BUTTON_LEFT_MARGIN: int = int(DEFAULT_LEFT_MARGIN / 2)

MARGIN_ONLY: int = 0

DEFAULT_GRID_ROWS_HEIGHT = (DEFAULT_ROW_HEIGHT,                 # 1º row
                            DEFAULT_ROW_HEIGHT,                 # 2º row
                            DEFAULT_ROW_HEIGHT,                 # 3º row
                            DEFAULT_ROW_HEIGHT,                 # 4º row
                            MARGIN_ONLY,                        # 5º row=0 will allow more margin before row of buttons
                            DEFAULT_BUTTON_HEIGHT,              # 6º row
                            int(DEFAULT_ROW_HEIGHT / 2))        # 7º row

DEFAULT_GRID_COLUMNS_WIDTH = (DEFAULT_LABEL_WIDTH,  # 1º column
                              DEFAULT_INPUT_CONTROL_WIDTH,  # 2º column
                              DEFAULT_LABEL_WIDTH,  # 3º column
                              DEFAULT_INPUT_CONTROL_WIDTH)       # 4º column

# Add: height of the rows plus margins of the controls plus margin of the container to get the height of the container
DEFAULT_CONTAINER_HEIGHT = sum(DEFAULT_GRID_ROWS_HEIGHT) \
                           + (len(DEFAULT_GRID_ROWS_HEIGHT) + 1) * DEFAULT_TOP_MARGIN \
                           + DEFAULT_CONTAINER_LEFT_MARGIN
# Add: width of the columns plus margins of the controls plus margin of the container to get the width of the container
DEFAULT_CONTAINER_WIDTH = sum(DEFAULT_GRID_COLUMNS_WIDTH) \
                          + (len(DEFAULT_GRID_COLUMNS_WIDTH) + 1) * DEFAULT_LEFT_MARGIN\
                          + DEFAULT_CONTAINER_LEFT_MARGIN

BACKGROUND_COLOR: int = -16777188   # clGradientInactiveCaption


class FakeGridLayout:
    """
    Class to simulate a Grid (rows x columns) inside the Container based on the Place layout manager,
      thus calculating for each control absolute coordinates (x, y).
    """
    def __init__(self,
                 rows_height_: () = DEFAULT_GRID_ROWS_HEIGHT,
                 columns_width_: () = DEFAULT_GRID_COLUMNS_WIDTH):
        self.__rows_height = rows_height_
        self.__columns_width = columns_width_

    def get_place(self,
                  row_number_: int,
                  col_number_: int) -> ():
        """
        Calculates the exact coordinates (x, y) to place the control inside the parent container, obtained from a
          fake-grid mimicked by GRID_ROWS_HEIGHT and GRID_COLUMNS_WIDTH
        :param row_number_: where the control will be placed inside the container
        :param col_number_: where the control will be placed inside the container
        :return: coordinates (x, y) to Place the control inside the container
        """
        x_ = sum(self.__columns_width[:col_number_ - 1]) + DEFAULT_LEFT_MARGIN * col_number_
        y_ = sum(self.__rows_height[:row_number_ - 1]) + DEFAULT_TOP_MARGIN * row_number_
        return x_, y_
