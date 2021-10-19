import numpy as np
import yaml
import os
import matplotlib.pyplot as plt


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

def onSegment(p, q, r): 
  if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
       (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
    return True
  return False

def orientation(p, q, r): 
  # to find the orientation of an ordered triplet (p,q,r) 
  # function returns the following values: 
  # 0 : Colinear points 
  # 1 : Clockwise points 
  # 2 : Counterclockwise 
    
  # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
  # for details of below formula.  
    
  val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
  if (val > 0): 
    # Clockwise orientation 
    return 1
  elif (val < 0): 
    # Counterclockwise orientation 
    return 2
  else:        
    # Colinear orientation 
    return 0


# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1, q1, p2, q2): 
      
  # Find the 4 orientations required for  
  # the general and special cases 
  o1 = orientation(p1, q1, p2) 
  o2 = orientation(p1, q1, q2) 
  o3 = orientation(p2, q2, p1) 
  o4 = orientation(p2, q2, q1) 

  # General case 
  if ((o1 != o2) and (o3 != o4)): 
    return True

  # Special Cases 

  # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
  if ((o1 == 0) and onSegment(p1, p2, q1)): 
    return True

  # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
  if ((o2 == 0) and onSegment(p1, q2, q1)): 
    return True

  # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
  if ((o3 == 0) and onSegment(p2, p1, q2)): 
    return True

  # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
  if ((o4 == 0) and onSegment(p2, q1, q2)): 
    return True

  # If none of the cases 
  return False


def isInside(polygon, point):
  """
  Input:
    polygon: a list of Point objects
    n: number of vertices, must larger than 3
    point: query point object

  Output:
    True if the point is inside the polygon, False otherwise
  """
  n = len(polygon)
  # There must be at least 3 vertices in polygon
  if n < 3:
    return False
  
  # Create a point for line segment from p to infinite 
  INF = 10000
  extreme = Point(INF, point.y)

  # Count intersections of the above line with sides of polygon 
  count = 0
  i = 0


  while True:
    next_idx = (i+1)%n
    # print('i, next idx', i, next_idx)
    # Check if the line segment from 'p' to 'extreme' intersects 
    # with the line segment from 'polygon[i]' to 'polygon[next]' 
    if doIntersect(polygon[i], polygon[next_idx], point, extreme):
      # If the point 'p' is colinear with line segment 'i-next', 
      # then check if it lies on segment. If it lies, return true, 
      # otherwise false 
      if orientation(polygon[i], point, polygon[next_idx],) == 0:
        return onSegment(polygon[i], point, polygon[next_idx])
      # print('intersect! ', polygon[i].x, polygon[i].y, polygon[next_idx].x, polygon[next_idx].y)
      count += 1
    i = next_idx

    if i == 0:
      break

  # calculate the y-value overlap count
  overlap_count = 0
  for i in range(n):
    if polygon[i].y == point.y and polygon[i].x > point.x:
      # eliminate the foollowing two cases: pay attention to bound check
      # \ /    o
      #  o    / \
      left_idx = i-1 if i-1>= 0 else n-1
      right_idx = i+1 if i+1 < n else 0
      left_y, right_y = polygon[left_idx].y, polygon[right_idx].y
      if (not (left_y > point.y and right_y > point.y)) and (not (left_y < point.y and right_y < point.y)):
        overlap_count += 1

  # print('count - overlap_count', count, overlap_count, count - overlap_count)
  
  if count == 0:
    return False
  else:
    return (count - overlap_count) % 2 == 1

def check_vertex_overlap(idx):
  yaml_path = '/media/yuliang/Drive/Fall2020/research_Dmitry/dataset-1.0/dataset-1.0/annotations/'
  yaml_idx = str(idx)
  yaml_path = os.path.join(yaml_path, yaml_idx.zfill(3) + '_annotation.yaml')
  with open(yaml_path) as f:
    data = yaml.load(f, Loader=yaml.Loader)

  # print('data', data)
  # data 
  # {'filename': '003_image.png', 
  # 'annotation': 
  #   [{'type': 'weed', 
  #     'points': {'x': [1175.0, 1131.0, 1132.0, 1178.0, 1238.0, 1294.0, 1294.0], 
  #                'y': [763.0, 770.0, 844.0, 950.0, 947.0, 874.0, 807.0]}}, 
  #    {'type': 'weed', 
  #    'points': {'x': [1047.0, 850.0, 817.0, 727.0, 772.0, 939.0], 
  #               'y': [749.0, 889.0, 895.0, 700.0, 619.0, 655.0]}}, 
  #    {'type': 'weed', 
  #     'points': {'x': [849.0, 804.0, 810.0, 998.0, 1134.0, 1108.0, 1000.0, 933.0], 
  #                'y': [521.0, 542.0, 610.0, 583.0, 543.0, 470.0, 459.0, 464.0]}}, 
  #    {'type': 'crop', 
  #     'points': {'x': [794.0, 760.0, 624.0, 614.0, 822.0, 873.0], 
  #                'y': [439.0, 454.0, 425.0, 406.0, 346.0, 355.0]}}, 
  #    {'type': 'crop', 
  #     'points': {'x': [941.0, 705.0, 693.0, 769.0, 897.0, 928.0], 
  #                'y': [271.0, 219.0, 99.0, 5.0, 2.0, 113.0]}}, 
  #    {'type': 'weed', 
  #     'points': {'x': [691.0, 666.0, 582.0, 555.0, 648.0], 
  #                'y': [298.0, 164.0, 140.0, 255.0, 326.0]}}, 
  #    {'type': 'weed', 
  #     'points': {'x': [672.0, 631.0, 531.0, 618.0, 655.0, 674.0], 
  #                'y': [870.0, 835.0, 905.0, 955.0, 965.0, 961.0]}}, 
  #    {'type': 'weed', 
  #     'points': {'x': [851.0, 804.0, 809.0, 789.0, 675.0, 681.0, 688.0, 766.0, 812.0, 847.0], 
  #                'y': [519.0, 543.0, 592.0, 606.0, 602.0, 483.0, 465.0, 457.0, 433.0, 463.0]}}]}

  inside_count = 0
  # take one vertex in the polygon 1
  annotation = data['annotation']
  # pos_query = annotation[0]['points']
  # query_point = Point(pos_query['x'][6], pos_query['y'][6])
  # query_length = len(pos_query['x'])

  num_total_poly = len(annotation)
  # query poly
  for m in range(num_total_poly):
    pos_query = annotation[m]['points']
    query_length = len(pos_query['x'])
    # query point
    for k in range(query_length):
      query_point = Point(pos_query['x'][k], pos_query['y'][k])
      # target poly
      for i in range(num_total_poly):
        if i != m:
          polygon_i = []
          n_i = len(annotation[i]['points']['x'])

          for j in range(n_i):
            pos_j = annotation[i]['points']
            polygon_i.append( Point(pos_j['x'][j], pos_j['y'][j]) )
          result = isInside(polygon_i, query_point)
          # print('mth query poly, kth query point, ith polygon, is inside', m, k, i, result)

          if result:
            inside_count += 1
            print('mth query poly, kth query point, ith polygon, is inside', m, k, i, result)
            print('True info:', query_point.x, query_point.y, polygon_i[0].x, polygon_i[0].y)

  print('inside count', inside_count)


def main():
  # polygon = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
  # n = len(polygon)
  # p = Point(10, 10.0000000001)
  # print(isInside(polygon, n, p))

  # polygon1 = [Point(1, 0), Point(-1, 0), Point(0, 2)]
  # n1 = len(polygon1)
  # p1 = Point(0.5, 1.000001)
  # print(isInside(polygon1, n1, p1))
  
  # check_vertex_overlap(19)
  # print(orientation(Point()))


  print('INDIVIDUAL TEST')
  idx = 7
  yaml_path = '/media/yuliang/Drive/Fall2020/research_Dmitry/dataset-1.0/dataset-1.0/annotations/'
  yaml_idx = str(idx)
  yaml_path = os.path.join(yaml_path, yaml_idx.zfill(3) + '_annotation.yaml')
  with open(yaml_path) as f:
    data = yaml.load(f, Loader=yaml.Loader)

  # polygon2 = [Point(587.0, 248.0), Point(546.0, 233.0), Point(527.0, 244.0), 
  #             Point(524.0, 278.0), Point(538.0, 321.0), Point(587.0, 345.0), 
  #             Point(647.0, 355.0), Point(645.0, 319.0)]
  # n2 = len(polygon2)
  # p2 = Point(373.0, 345.0)
  # print(isInside(polygon2, n2, p2))


  points = data['annotation'][7]['points']
  polygon3 = []
  for i in range(len(points['x'])):
    polygon3.append(Point(points['x'][i], points['y'][i]))
  n3 = len(polygon3)
  p3 = Point(561.0, 321.0)
  print(isInside(polygon3, p3))


  x_plot = []
  y_plot = []
  for p in polygon3:
    # plt.plot(p.x, p.y, 'bo-')
    x_plot.append(p.x)
    y_plot.append(p.y)
  plt.plot(x_plot+[polygon3[0].x, polygon3[-1].x], y_plot+[polygon3[0].y, polygon3[-1].y], 'bo-')
  plt.plot(p3.x, p3.y, 'ro')
  plt.gca().invert_yaxis()
  plt.show()

  # for p in polygon2:
  #   # plt.plot(p.x, p.y, 'bo-')
  #   x_plot.append(p.x)
  #   y_plot.append(p.y)
  # plt.plot(x_plot+[polygon2[0].x, polygon2[-1].x], y_plot+[polygon2[0].y, polygon2[-1].y], 'bo-')
  # plt.plot(p2.x, p2.y, 'ro')
  # plt.gca().invert_yaxis()
  # plt.show()

if __name__ == "__main__":
  main()
