''' GENERATE PLOT OF SOLUTION '''

from flask import request, abort
from flask_restful import Resource
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np


#### Plot resource for plotting solutions ####
class Plot(Resource):
    ''' POST request for plotting points '''
    def post(self):
        # Get form data
        self.data = request.get_json()

        # Plot points; if error, abort
        try:
            self.points = np.array(self.data['solution'])

            # Plot points
            fig= plt.figure()
            for i in range(self.points.shape[0]):
                for j in range(self.points.shape[1]):
                    plt.plot(self.points[i, j, 0], self.points[i, j, 1], 'bo')
            
            # Turn off plot display
            plt.close(fig)

            # Draw the figure
            fig.canvas.draw()

            # Save figure into NumPy array
            img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(fig.canvas.get_width_height()[::-1] + (3,))

            # Return plot as list of pixel coordinates
            return {'plot': img.tolist()}, 201
        except:
            abort(400, 'BadRequest: Could not plot data. Make sure your points array is valid.')