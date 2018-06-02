
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

        # The name of our image
        image_name = 'simulated_agency/images/%s_%s.png' % (path, str(self.simulation.age).zfill(8))

        # Compute location of screen to grab
        x1 = self.simulation.window.winfo_rootx() + self.simulation.canvas.winfo_x()
        y1 = self.simulation.window.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.simulation.canvas.winfo_width()
        y2 = y1 + self.simulation.canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)
