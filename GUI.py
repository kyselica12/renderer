import PySimpleGUI as sg
from enum import Enum
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
from numpy import size

matplotlib.use('TkAgg')


class EventTypes(str, Enum):
    rotation = "rotation"
    translation = "translation"
    light = "light"
    cmd = "cmd"




class GUI:

    def __init__(self, width, height):

        layout = self.create_layout(width, height)

        self.window = sg.Window('F-rep renderer', layout,finalize=True)
        self.canvas = self.window["canvas"].TKCanvas

        self.fig = None
        self.ax = None

    def create_layout(self, width, height):
        
        def get_selection_layout3(name, range):
            pad = 20
            layout = [
                [sg.HorizontalSeparator()],
                [sg.Text(name.upper())],
                [sg.Column([
                    [sg.Column([[sg.Text("X", pad=pad)], [sg.Slider(enable_events=True,range=range, default_value=0, key=f'{name}X', orientation='horizontal',size=(10,12))]]
                     ,element_justification='c'),
                    sg.Column([[sg.Text("Y", pad=pad)], [sg.Slider(enable_events=True,range=range, default_value=0, key=f'{name}Y', orientation='horizontal',size=(10,12))]]
                     ,element_justification='c'),
                    sg.Column([[sg.Text("Z", pad=pad)], [sg.Slider(enable_events=True,range=range, default_value=0, key=f'{name}Z', orientation='horizontal',size=(10,12))]]
                     ,element_justification='c')]
                ],element_justification='c')]
            ]

            return sg.Column(layout, element_justification='c')


        canvas_column_list = [[sg.Canvas(background_color='white', size=(width,height),key='canvas')]]

        option_column = [
            [sg.Text("Transformations".upper(), font='Arial 13')],
            [sg.HorizontalSeparator()],
            [get_selection_layout3(EventTypes.rotation,(-90,90))],
            [get_selection_layout3(EventTypes.translation,(-100,100))],
            [get_selection_layout3(EventTypes.light,(-100,100))],
            [sg.HorizontalSeparator()],
            [sg.Text("Command line")],
            [sg.Input(key="test")],
        ]

        layout = [
            [sg.Column(canvas_column_list, element_justification='c'),
            sg.VerticalSeparator(),
            sg.Column(option_column, element_justification='c')]
        ]
        return layout
    


    def loop(self):
        
        while True:

            event, values = self.window.read()
            print(event, values[event])
            if event == sg.WIN_CLOSED:
                break

            elif event != EventTypes.cmd:
                name = event[:-1]
                axis = event[-1]
                yield name, axis, values[event]
            
            else:
                yield name, None, values[event]


        self.window.close()

    def draw(self, image):
        if self.canvas.children:
            for child in self.canvas.winfo_children():
                child.destroy()
        
        fig = matplotlib.figure.Figure(figsize=(7,7))
        DPI = fig.get_dpi()
        ax = fig.add_subplot(111)
        
        ax.imshow(image)
        # ax.axis('off')
        plt.tight_layout(pad=0)
        # plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
            hspace = 0, wspace = 0)
        plt.margins(0, 0)
        figure_canvas_agg = FigureCanvasTkAgg(fig, self.canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)




if __name__ == "__main__":
    gui = GUI(600,600)

    import numpy as np

    image = np.random.rand(600,600,3)



    # for x in range(255):
    #     for y in range(255):
    #         gui.canvas.create_rectangle(x,y,x,y,fill='red',outline="red")

    for n, x, v in gui.loop():
        image = np.random.rand(600,600,3)

        gui.draw(image)
        print(n,x,v)
