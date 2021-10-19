import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import yaml

from isInsidePoly import *

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

annotation_path = '/media/yuliang/Drive/Fall2020/research_Dmitry/dataset-1.0/dataset-1.0/annotations/'


def load_image(idx):
  img_path = os.path.join(annotation_path, str(idx).zfill(3) + "_annotation.png")
  img = cv2.imread(img_path)
  H, W, C = img.shape
  print(f'Successfully loaded img {str(idx).zfill(3) + "_annotation.png"}, shape: {H, W, C}')
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img

def load_yaml(idx):
  yaml_path = os.path.join(annotation_path, str(idx).zfill(3) + "_annotation.yaml")
  with open(yaml_path) as f:
    data = yaml.load(f, Loader=yaml.Loader)
  print(f'Successfully loaded yaml file {str(idx).zfill(3) + "_annotation.yaml"}') 
  return data

def get_polygon_set(annotation_dict):
  ''' 
  Gather polygon list S.

  Inputs:
    annotation_dict: a dictionary file read from the yaml annotation file.

  Returns:
    polygon_list_verbose: a list whose each element is a dictionary with two keys,
      'type' and 'points'.
    polygon_list: a list whose each element is a list of Point objects (vertices).
  '''
  polygon_list_verbose, polygon_list = [], []
  annotation = annotation_dict['annotation']
  num_polygons = len(annotation)
  for i in range(num_polygons):
    polygon_list_verbose.append(annotation[i])

    polygon_temp = []
    num_vertices = len(polygon_list_verbose[i]['points']['x'])
    for j in range(num_vertices):
      x_temp = polygon_list_verbose[i]['points']['x'][j]
      y_temp = polygon_list_verbose[i]['points']['y'][j]
      polygon_temp.append(Point(x_temp, y_temp))
    polygon_list.append(polygon_temp)
  return polygon_list_verbose, polygon_list

def get_box_set(polygon_list_verbose):
  '''
    Get boxes from S, follow the sequence of the polygon set.
    Data format: [ ... [xmin, ymin, xmax, ymax]_{i} ... ]
  '''
  boxes = []
  num_polygons = len(polygon_list_verbose)

  for i in range(num_polygons):
    x_set, y_set = polygon_list_verbose[i]['points']['x'], polygon_list_verbose[i]['points']['y']
    xmin, ymin, xmax, ymax = np.min(x_set), np.min(y_set), np.max(x_set), np.max(y_set)
    boxes.append([xmin, ymin, xmax, ymax])
  return boxes

def get_labels(polygon_list_verbose):
  labels = []
  num_polygons = len(polygon_list_verbose)

  for i in range(num_polygons):
    if polygon_list_verbose[i]['type'] == 'weed':
      labels.append(2)
    elif polygon_list_verbose[i]['type'] == 'crop':
      labels.append(1)
  return labels

def find_overlap_pixels_and_save():
  for img_idx in range(1, 61):
    # img_idx = 34
    plt.cla()
    mask = load_image(img_idx)  
    data = load_yaml(img_idx)  
    polygon_list_verbose, polygon_list = get_polygon_set(data)
    boxes = get_box_set(polygon_list_verbose)

    H, W, C = mask.shape
    out = np.zeros((H, W))
    
    num_polygons = len(polygon_list)
    overlap_vertices_x = []
    overlap_vertices_y = []
    for i in range(H):
      for j in range(W):
        if mask[i, j][1] == 255 or mask[i, j][0] == 255:
          count = 0
          overlap_p = []
          for p in range(num_polygons):
            # pay attention to the order here. j,i or i,j
            if isInside(polygon_list[p], Point(j, i)):
              # print(f'pixel i, j {i, j}, is inside polygon {p}')
              count += 1
              overlap_p.append(p)
          if count > 1:
            # print(f'pixel j i {j, i} is inside {count} polygons {overlap_p}')
            overlap_vertices_x.append(j)
            overlap_vertices_y.append(i)

    plt.imshow(mask)

    # visualize polygons
    # Color: https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    # Marker: https://matplotlib.org/api/markers_api.html
    color_list = ['b', 'c', 'm', 'y', 'w', 'tab:blue','tab:orange', 
                  'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 
                  'tab:gray', 'tab:olive', 'tab:cyan', 'bisque', 'darkred', 'olive',
                  'lavender', 'steelblue', 'deepskyblue', 'plum', 'cadetblue',
                  'azure', 'teal', 'salmon', 'coral']
    for i, polygon in enumerate(polygon_list_verbose):
      plt.plot(polygon['points']['x'] + [polygon['points']['x'][0], polygon['points']['x'][-1]], 
              polygon['points']['y'] + [polygon['points']['y'][0], polygon['points']['y'][-1]], 
              color=color_list[i], marker='o')

    # visualize overlap pixels
    for i in range(len(overlap_vertices_x)):
      plt.plot(overlap_vertices_x[i], overlap_vertices_y[i], 
              color='yellow', marker='^')

    # plt.show()
    save_path = '/media/yuliang/Drive/Fall2020/research_Dmitry/week9/overlap_test/'
    plt.savefig(os.path.join(save_path, str(img_idx).zfill(3) + '_overlap.png'))

def convert_masks(img_idx):
  mask = load_image(img_idx)  
  data = load_yaml(img_idx)  
  polygon_list_verbose, polygon_list = get_polygon_set(data)
  boxes = get_box_set(polygon_list_verbose)
  labels = get_labels(polygon_list_verbose)

  H, W, C = mask.shape
  out = np.zeros((H, W), dtype=mask.dtype)
  
  num_polygons = len(polygon_list)
  for i in range(H):
    for j in range(W):
      if mask[i, j][1] == 255 or mask[i, j][0] == 255:
        inside_count = 0
        inside_idx = -1
        for p in range(num_polygons):
          # pay attention to the order here. j,i or i,j
          if isInside(polygon_list[p], Point(j, i)):
            # print(f'pixel i, j {i, j}, is inside polygon {p}')
            inside_count += 1
            inside_idx = p
        # omit overlap areas
        if inside_count == 1:
          # print(f'pixel j i {j, i} is inside {inside_count} polygons {overlap_p}')
          # assign instance label, should be positive, (1~num_polygons)
          out[i, j] = inside_idx+1
  return out, boxes, labels

def save_image(data, fn):
  '''
    Use plt lib to save images without axis and margins.
  '''
  sizes = np.shape(data)
  height = float(sizes[0])
  width = float(sizes[1])
    
  fig = plt.figure()
  fig.set_size_inches(width/height, 1, forward=False)
  ax = plt.Axes(fig, [0., 0., 1., 1.])
  ax.set_axis_off()
  fig.add_axes(ax)

  ax.imshow(data)
  plt.savefig(fn, dpi = height) 
  plt.close()

def get_label_and_box_only(img_idx):
  mask = load_image(img_idx)  
  data = load_yaml(img_idx)  
  polygon_list_verbose, polygon_list = get_polygon_set(data)
  boxes = get_box_set(polygon_list_verbose)
  labels = get_labels(polygon_list_verbose)
  return boxes, labels


def main():
  # save_path = '/media/yuliang/Drive/Fall2020/research_Dmitry/week10/instance_masks/'
  # for img_idx in range(1, 61):
  #   out, boxes, labels = convert_masks(img_idx)
  #   cv2.imwrite(os.path.join(save_path, str(img_idx).zfill(3) + '_instance.png'), out)

  boxes = []
  labels = []

  for i in range(1, 61):
    boxes_i, labels_i = get_label_and_box_only(i)
    boxes.append(boxes_i)
    labels.append(labels_i)

  boxes_np = np.zeros((len(boxes),len(max(boxes, key=lambda x: len(x))), 4))
  print('boxes_np', boxes_np.shape)
  for i,j in enumerate(boxes):
    # print('check', boxes_np[i].shape, len(j), j)
    boxes_np[i][0:len(j)] = np.array(j)

  labels_np = np.zeros((len(labels),len(max(labels, key=lambda x: len(x)))))
  print('labels_np', labels_np.shape)
  for i,j in enumerate(labels):
    labels_np[i][0:len(j)] = np.array(j)

  boxes_np = boxes_np.reshape(boxes_np.shape[0], -1)
  np.savetxt("boxes.txt", boxes_np, newline="\n", fmt="%.1f")
  np.savetxt("labels.txt", labels_np, newline="\n", fmt="%d")

if __name__ == "__main__":
  main()