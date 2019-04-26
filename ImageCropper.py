import cv2
import numpy as np
import math
import os

def euclideanDist(x1, y1, x2, y2):
  x1 = float(x1)
  y1 = float(y1)
  x2 = float(x2)
  y2 = float(y2)
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def analyze_points(rect_points):
  # Return bottom left, top left, top right, bottom right
  # sort by x (divide left and right)
  xSort = rect_points[rect_points[:,0].argsort()]
  print(xSort)

  leftPoints = xSort[:2, :]
  print(leftPoints)
  leftPoints = leftPoints[leftPoints[:,1].argsort()]
  tl, bl = leftPoints[0], leftPoints[1]
  rightPoints = xSort[2:, :]
  rightPoints = rightPoints[rightPoints[:,1].argsort()]
  tr, br = rightPoints[0], rightPoints[1]
  print(leftPoints[:,1])
  print(rightPoints[:,1])
  print("Order: bottom left, top left, top right, bottom right")
  print("%d,%d; %d,%d; %d,%d; %d,%d" % (bl[0], bl[1], tl[0], tl[1], tr[0], tr[1], br[0], br[1]))
  width = euclideanDist(bl[0], bl[1], br[0], br[1])
  height = euclideanDist(bl[0], bl[1], tl[0], tl[1])
  return np.float32([bl, tl, tr, br]), int(width), int(height)


def crop(rectPoints, srcDir="input/test.jpg", destDir="output/test"):
  img = cv2.imread(srcDir)

  # Return bottom left, top left, top right, bottom right
  src, width, height = analyze_points(rectPoints)
  print("width: %d, height: %d" % (width, height))

  dest1 = np.array([[0, height-1],
                    [0, 0],
                    [width-1, 0],
                    [width-1, height-1]], dtype="float32")
  
  dest2 = np.array([[0, 0],
                    [height-1, 0],
                    [height-1, width-1],
                    [0, width-1]], dtype="float32")

  dest3 = np.array([[width-1, 0],
                    [width-1, height-1],
                    [0, height-1],
                    [0, 0]], dtype="float32")

  dest4 = np.array([[height-1, width-1],
                    [0, width-1],
                    [0, 0],
                    [height-1, 0]], dtype="float32")

  # the perspective transformation matrix
  M1 = cv2.getPerspectiveTransform(src, dest1)
  M2 = cv2.getPerspectiveTransform(src, dest2)
  M3 = cv2.getPerspectiveTransform(src, dest3)
  M4 = cv2.getPerspectiveTransform(src, dest4)

  # directly warp the rotated rectangle to get the straightened rectangle
  warped1 = cv2.warpPerspective(img, M1, (width, height))
  cv2.imwrite(destDir + "_1.jpg", warped1)

  warped2 = cv2.warpPerspective(img, M2, (height, width))
  cv2.imwrite(destDir + "_2.jpg", warped2)

  warped3 = cv2.warpPerspective(img, M3, (width, height))
  cv2.imwrite(destDir + "_3.jpg", warped3)

  warped4 = cv2.warpPerspective(img, M4, (height, width))
  cv2.imwrite(destDir + "_4.jpg", warped4)

def main():
  if not os.path.exists("input"):
      os.makedirs("input")
  if not os.path.exists("output"):
      os.makedirs("output")
  cnt = np.array([
          [1132, 143],
          [1624, 333],
          [1962, 1424],
          [1580, 1563]
      ])

  crop(cnt, "./input/test.jpg", "./output/test")

if __name__ == '__main__':
  main()