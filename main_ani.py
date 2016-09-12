#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi


SIZE = 1200
ONE = 1./SIZE


MID = 0.5

INIT_BRANCH = SIZE*0.03*ONE
GRAINS = int(SIZE*0.02)

BRANCH_DIMINISH = ONE/32

BRANCH_SPLIT_DIMINISH = 0.71
BRANCH_PROB_SCALE = 1./(INIT_BRANCH)/SIZE*20

BRANCH_SPLIT_ANGLE = 0.3*pi
BRANCH_ANGLE_MAX = 5.*pi/SIZE
BRANCH_ANGLE_EXP = 2

## COLORS AND SHADES
BACK = [1,1,1,1]
FRONT = [0, 0, 0, 0.5]
TRUNK_STROKE = [0, 0, 0, 1]
TRUNK = [1, 1, 1, 1]
TRUNK_SHADE = [0,0,0,0.5]


def main():

  from iutils.render import Animate
  from modules.tree import Tree

  tree = Tree(
    MID,
    0.95,
    INIT_BRANCH,
    -pi*0.5,
    ONE,
    ONE,
    BRANCH_SPLIT_ANGLE,
    BRANCH_PROB_SCALE,
    BRANCH_DIMINISH,
    BRANCH_SPLIT_DIMINISH,
    BRANCH_ANGLE_MAX,
    BRANCH_ANGLE_EXP
  )

  def wrap(render):

    tree.step()
    tree.draw_brances(render, GRAINS, TRUNK, TRUNK_STROKE)

    if tree.Q:
      return True
    else:
      return False

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(ONE)
  render.start()


if __name__ == '__main__':
    main()

