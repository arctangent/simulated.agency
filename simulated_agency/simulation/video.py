
class VideoRecorder(object):
    '''
    Provides object drawing functionality
    '''

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.save_image = self.save_image

    def save_image(self, path):
        ''' Basic save image '''

        simulation = self.simulation
        canvas = simulation.canvas
        window = simulation.window

        # The name of our image
        image_name = 'simulated_agency/images/%s_%s.png' % (path, str(simulation.age).zfill(8))

        # Compute location of screen to grab
        x1 = window.winfo_rootx() + canvas.winfo_x()
        y1 = window.winfo_rooty() + canvas.winfo_y()
        x2 = x1 + canvas.winfo_width()
        y2 = y1 + canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)
