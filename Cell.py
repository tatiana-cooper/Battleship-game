class Cell:
    """
    The class represented the cell on the player's field.
    """

    def __init__(self):
        self.__is_damaged = False

    @property
    def is_damaged(self):
        """
        This method shows if Cell is damaged
        :return: __is_damaged
        """
        return self.__is_damaged

    def shoot_at(self):
        """
        The method changes damaged state of Cell to True
        :return: bool
        """
        self.__is_damaged = True

    def view(self):
        """
        Display view of Cell by state (is damaged or not).
        :return: view of Cell by state
        """
        if self.__is_damaged is False:
            return '| '
        else:
            return '|○'
