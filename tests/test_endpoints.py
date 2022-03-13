''' PYTEST TEST DEFINITIONS '''

#### Test 1: Validating compute_coordinates input ####
def test_input(client):
    # Invalid coordinate dimensions
    payload = {
    'img_dim': (0, 1),
    'corner_points': [(1, 1),(3, 1), (1, 3), (3, 3)]
    }
    res1 = client.post('compute_coordinates', json = payload)
    assert res1.status_code == 501

    # Invalid number of points
    payload = {
    'img_dim': (3, 3),
    'corner_points': [(1, 1),(3, 1), (1, 3), (3, 3), (3, 4)]
    }
    res2 = client.post('compute_coordinates', json = payload)
    assert res2.status_code == 502

    # Invalid rectangle
    payload = {
    'img_dim': (3, 3),
    'corner_points': [(1, 1),(3, 1), (1, 3), (4, 3)]
    }
    res3 = client.post('compute_coordinates', json = payload)
    assert res3.status_code == 503

    # Valid rectangle
    payload = {
    'img_dim': (3, 3),
    'corner_points': [(1, 1),(3, 1), (1, 3), (3, 3)]
    }
    res4 = client.post('compute_coordinates', json = payload)
    assert res4.status_code == 201


#### Test 2: Checking compute_coordinates output ####
def test_coords(client):
    # Example 1
    payload = {
    'img_dim': (3, 3),
    'corner_points': [(1, 1),(3, 1), (1, 3), (3, 3)]
    }
    res1 = client.post('compute_coordinates', json = payload)
    assert res1.status_code == 201
    json1 = res1.json
    assert 'solution' in json1.keys()
    assert json1['solution'] == [[[1.0, 3.0], [2.0, 3.0], [3.0, 3.0]],[[1.0, 2.0], [2.0, 2.0], [3.0, 2.0]], [[1.0, 1.0], [2.0, 1.0], [3.0, 1.0]]]

    # Example 2
    payload = {
    'img_dim': (4, 5),
    'corner_points': [(1.5, 8.0),(4.0, 8.0), (1.5, 1.5), (4.0, 1.5)]
    }
    res2 = client.post('compute_coordinates', json = payload)
    assert res2.status_code == 201
    json2 = res2.json
    assert 'solution' in json2.keys()
    assert json2['solution'] == [[[1.5, 8.0],[2.125, 8.0],[2.75, 8.0],[3.375, 8.0],[4.0, 8.0]],[[1.5, 5.833333333333334],[2.125, 5.833333333333334],[2.75, 5.833333333333334],[3.375, 5.833333333333334],[4.0, 5.833333333333334]],[[1.5, 3.666666666666667],[2.125, 3.666666666666667],[2.75, 3.666666666666667],[3.375, 3.666666666666667],[4.0, 3.666666666666667]],[[1.5, 1.5], [2.125, 1.5], [2.75, 1.5], [3.375, 1.5], [4.0, 1.5]]]


#### Test 3: Testing plot_solution output ####
def test_plots(client):
    # Success example
    payload = {
        'solution': [[[1.0, 3.0], [2.0, 3.0], [3.0, 3.0]],[[1.0, 2.0], [2.0, 2.0], [3.0, 2.0]], [[1.0, 1.0], [2.0, 1.0], [3.0, 1.0]]]
    }
    res1 = client.post('plot_solution', json = payload)
    assert res1.status_code == 201
    json1 = res1.json
    assert 'plot' in json1.keys()

    # Fail example
    payload = {
        'message': 'ValueError: Image dimensions invalid. Required format: (height > 0, width > 0).'
    }
    res2 = client.post('plot_solution', json = payload)
    assert res2.status_code == 400
    json2 = res2.json
    assert 'message' in json2.keys()





