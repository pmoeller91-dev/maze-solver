from tkinter import Tk, BOTH, Canvas

class Window:
    """A class representing the main window for the maze solver."""
    def __init__(self, width: int, height: int) -> None:
        """Creates a new main window for the maze solver.

        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
        """
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.__root.title("Maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root)
        self.__canvas.pack()

        self.__running = False
    
    def redraw(self) -> None:
        """Redraws the main window."""
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self) -> None:
        """Redraws until the window is closed."""
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self) -> None:
        """Signals that the main loop should end and the window should close.
        
        Serves as a way to kick out of the ``wait_for_close()`` function and little
        else. If ``wait_for_close`` has not yet been called, has no effect.
        """
        self.__running = False
        