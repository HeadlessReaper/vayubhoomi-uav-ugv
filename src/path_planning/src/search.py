#!/usr/bin/env python3

import math
import copy
from scipy.spatial import distance
from shapely.geometry import Polygon, Point
#import matplotlib.pyplot as plt


def check_distance(point1, point2):
    
    sum = 0
    for i in range(len(point1)):
        sum += math.pow(point1[i] - point2[i], 2)
    
    sum = math.sqrt(sum)

    if round(sum, 2) < 0.1:
        return True
    else:
        return False
        

def check(point1, point2):
    '''
    Checks if they are the same point or not
    '''
    for i in range(len(point1)):
        if round(point1[i], 1) != round(point2[i], 1):
            return False
    return True


def round_point(point):
    '''
    Rounds all the 2 co-ordinates of a point
    '''
    for i in range(len(point)):
        for j in range(len(point[i])):
            point[i][j] = round(point[i][j], 2)
    return point


def check_in(points, polygon, visited):
    '''
    Removes all prohibited points from points and returns
    '''
    points = round_point(points)
    temp = copy.deepcopy(points)
    for i in range(len(points)):
        '''if (points[i][0] > 2.5 and points[i][0] < 7.5) and (points[i][1] > 1.5 and points[i][1] < 8.5):
            temp.remove(points[i])'''
        '''elif points[i] in prohibited:
            #print('b')
            temp.remove(points[i])'''
        point = Point(points[i][0], points[i][1])
        if polygon.contains(point):
            temp.remove(points[i])
        elif len(visited) != 0:
            for j in range(len(visited)):
                if check(points[i], visited[j]):
                    temp.remove(points[i])
    return temp
    

def heuristic(points, start, destination):
    '''
    Calculates heuristic for each point
    '''
    l = []
    for i in range(len(points)):
        dist = distance.cityblock(destination, points[i]) #distance.cityblock(start, points[i]) +
        l.append(dist)
    return l


def neighbours(point):
    '''
    Finds all the points at a distapoint = [build[num][0], build[num][1], build[num][2]]nce of 0.1m from the given point
    '''
    points = []
    for i in range(360):
        y = point[1] + 0.1 * math.sin((i * 2 * math.pi) / 180)
        x = point[0] + 0.1 * math.cos((i * 2 * math.pi) / 180)
        points.append([x, y])
    return points


def best(points, polygon, start, end, visited):
    '''
    Chooses the point which is least distance that is not prohibited
    '''
    points = check_in(points, polygon, visited)
    distances = heuristic(points, start, end)
    loc = distances.index(min(distances))
    return points[loc]


def search(nodes, poly):
    '''
    Main function that searches
    '''
    #nodes = [[4.34, -0.67], [4.34, -4.17], [-3.16, -4.17], [-3.16, -0.67], [4.34, -0.67]]
    '''points = []
    for i in poly:
        points.append(tuple(i))'''
    #polygon = Polygon(points)
    polygon = poly
    #plt.plot(*polygon.exterior.xy)
    # Creates a list of prohibited point
    '''prohibited = []
    x = 2.5
    y = 1.5
    while x < 7.49:
        while y < 8.49:
            prohibited.append([round(x, 2), round(y, 2)])
            y += 0.01
        x += 0.01
    # Path to be traversed
    #print(prohibited)'''
    visited = []
    path = []
    for i in range(len(nodes) - 1):
        '''if i == 0:
            # Start has to be origin for first iteration
            start = [0, 0]
        else:'''
        start = nodes[i]
        destination = nodes[i + 1]
        visited = []
        # Calculates points for first iteration
        points = neighbours(start)
        loc = best(points, polygon, start, destination, visited)
        path.append(loc)
        visited.append(loc)
        while True:
            # If the current location is the destination, loop is done
            if check_distance(loc, destination):                
                print('aaaaaaaaaaaaaaaaaaaaa')
                #path.append('aaaaaaaaaaaaaaaaaaaaaa')
                path.append(loc)
                break
            else:
                points = neighbours(loc)
                loc = best(points, polygon, start, destination, visited)
                path.append(loc)
                print(loc, start, destination)
                visited.append(loc)
        continue

    return path   

'''
queue = search([[0, 0], [4.34, -0.67]], [[4.34, -0.67], [4.34, -4.17], [-3.16, -4.17], [-3.16, -0.67], [4.34, -0.67]])
queue_2 = search([[4.34, -0.67], [4.34, -4.17], [-3.16, -4.17], [-3.16, -0.67], [4.34, -0.67]], [[4.34, -0.67], [4.34, -4.17], [-3.16, -4.17], [-3.16, -0.67], [4.34, -0.67]])
orig = len(queue_2)
b = copy.deepcopy(queue_2)
b = b[1:]
for j in range(5):
    c = copy.deepcopy(b)
    for i in range(len(b)):
        c[i].append(j + 1)
        queue_2.append(c[i])
   
for i in queue:
	i.append(1)   
queue_2 = queue_2[orig:]
queue.extend(queue_2)
build = search([[0, 0], [3.34, -1.67]], [[3.34, -1.67], [3.34, -5.17], [-4.16, -5.17], [-4.16, -1.67], [3.34, -1.67]])
build_2 = search([[3.34, -1.67], [3.34, -5.17], [-4.16, -5.17], [-4.16, -1.67], [3.34, -1.67]], [[3.34, -1.67], [3.34, -5.17], [-4.16, -5.17], [-4.16, -1.67], [3.34, -1.67]])
orig = len(build_2)
b_2 = copy.deepcopy(build_2)
b_2 = b_2[1:]
for j in range(5):
    c_2 = copy.deepcopy(b_2)
    for i in range(len(b_2)):
        c_2[i].append(j + 1)
        build_2.append(c_2[i])
   
for i in build:
	i.append(1)   
build_2 = build_2[orig:]
build.extend(build_2)
print(len(build), len(queue))
print(build[43], queue[43])'''