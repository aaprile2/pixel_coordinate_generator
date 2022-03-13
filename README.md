# pixel_coordinate_generator
API to compute the pixel coordinate values for an image that is to be displayed on a 2D surface, given the dimensions of the image and the corner points of the image as it is to be displayed. Includes plotting and testing functionality as well.

## Running the API
### Using Docker image (local build)
Make sure the Dockerfile is in the working directory. Build the image using: 

```
docker image build -t [name] .
```

Then, run the application:

```
docker run --rm -it --p 8080:5000 [name]
```

**Note:** Make sure in the file _main.py_, line 13 is commented out; i.e., the host IP address is unspecified (0.0.0.0). 

### Using Docker image (Docker Hub)
Pull the image from Docker Hub:

```
docker pull aaprile22/pixel_gen:latest
```

Then, run the application:
```
docker run --rm -it --p 8080:5000 aaprile22/pixel_gen:latest
```

### Run with Python
To install dependencies, run:

```
pipenv install
```

Then, activate the virtual environment:

```
pipenv shell
```

Finally, run the application:

```
python main.py
```

**Note:** Make sure in the file _main.py_, line 12 is commented out; i.e., the host IP address is localhost (default). 

## Making Requests
A full demonstration of the API is provided in _Demo_Test.ipynb_.

### Hosts
As noted above, hosting the API with a Docker image versus a locally run Python application requires different IP addresses. 

* For the Docker applications, requests should be sent to **http://127.0.0.1:8080/[endpoint]**. Otherwise, there will be a 403 (Forbidden) error.

* For the locally run applications, requests should be sent to **http://127.0.0.1:5000/[endpoint]**. Otherwise, there will be a HTTPConnectionPool (Failed) error.


### POST: compute_coordinates
This endpoint computes pixel coordinate values for an image that is to be displayed on a 2D surface, given the dimensions of the image and the corner points of the image as it is to be displayed.

Example:

```
# Define arguments
payload = {
    'img_dim': (3, 3),
    'corner_points': [(1, 1),(3, 1), (1, 3), (3, 3)]
}

# Make POST request to compute_coordinates endpoint
response = requests.post(url + 'compute_coordinates', json = payload)

# Get JSON respose
solution = response.json()
```

The response will be a dictionary with either a key 'solution' (given valid input) or 'message' (given invalid input). 'solution' is a list of all the coordinates, starting from the top of the image plane, organized by row.

<img width="392" alt="Screen Shot 2022-03-12 at 10 54 35 PM" src="https://user-images.githubusercontent.com/49654275/158044392-64886299-487c-4b2c-a59f-d47dd23d05e6.png">

### POST: plot_solution
As an additional feature, this endpoint will generate a plot of the pixel coordinates resulting from a successful _compute_coordinates_ request. It takes the JSON response from _compute_coordinates_ directly in the payload.

Example:

```
# Make POST request to plot_solution endpoint using the above solution
response = requests.post(url + 'plot_solution', json = solution)

# Get JSON response
points = response.json()
```

The response will be a dictionary with either a key 'plot' (given valid input) or 'message' (given invalid input). 'key' is a list representing an NumPy image array. It must be converted to a NumPy array to be plotted/saved as an image.

```
# Convert points to an array
points = np.array(response.json()['plot'])

# Plot results
plt.imshow(points)
plt.axis('off')
plt.show()
```


<img width="285" alt="Screen Shot 2022-03-12 at 10 58 18 PM" src="https://user-images.githubusercontent.com/49654275/158044446-7ef9902c-8d18-43fe-b793-1c24ef06671a.png">

## Unit Testing
As an extra feature, some unit tests were defined to ensure correct response. This was implemented using Pytest, which can be installed as follows:

```
# Using pipenv
pipenv install pytest

# Using pip
pip install pytest
```

To run the tests, clone the repository and navigate to the root of the project directory, then run:

```
python -m pytest
```

You should see the following, indiciating all tests were passed:

![Screen Shot 2022-03-12 at 11 15 24 PM](https://user-images.githubusercontent.com/49654275/158044812-cad7d968-9322-47e2-abdf-1565ee889ee5.png)




