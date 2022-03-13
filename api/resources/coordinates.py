''' COMPUTE COORDINATES '''

from flask import request, abort
from flask_restful import Resource
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np


#### Coordinates resource for computing points ####
class Coordinates(Resource):
    ''' Initialization; validate input '''
    def __init__(self):
        # Get form data
        data = request.get_json()
        
        # Check arguments
        if 'img_dim' not in data.keys() or 'corner_points' not in data.keys():
            abort(500, 'ValueError: img_dim and corner_points required.')
        
        # Unpack values
        self.img_dim = data['img_dim']
        self.corner_points = data['corner_points']

        # Check image dimension values
        if len(self.img_dim) != 2 or any(d <= 0 or type(d) is not int for d in self.img_dim) or self.img_dim == (1, 1):
           abort(501, 'ValueError: Image dimensions invalid. Required format: (height > 0, width > 0).')
        
        # Check corner points values
        # Check dimensions
        if np.array(self.corner_points).shape != (4, 2):
            abort(502, 'ValueError: Corner points invalid; must provide four 2D points. Required format: [(x1, y1), .... , (x4, y4)].')
        
        # Check if valid rectangle
        def is_valid_rectangle(points):
            # Sort points by x coordinate to establish order (bottom-left, top-left, bottom-right, top-right)
            bl, tl, br, tr = sorted(points)

            # Check if x and y values are equal, which implies a rectangle and alignment
            return bl[0] == tl[0] and br[0] == tr[0] and bl[1] == br[1] and tl[1] == tr[1]

        if not is_valid_rectangle(self.corner_points):
            abort(503, 'ValueError: Corners do not define a rectangle aligned with axes.')


    ''' POST request for computing coordinates '''
    def post(self):
        # Compute min and max of corner_points
        min_x, min_y = list(map(min, zip(*self.corner_points)))
        max_x, max_y = list(map(max, zip(*self.corner_points)))

        # Get evenly spaced intervals along x and y axes
        x_ind = np.linspace(min_x, max_x, self.img_dim[1])
        y_ind = np.linspace(max_y, min_y, self.img_dim[0])

        # Create a meshgrid 
        X, Y = np.meshgrid(x_ind, y_ind)

        # Stack meshgrid components along 3rd dimension and return
        return {'solution': np.dstack([X, Y]).tolist()}, 201