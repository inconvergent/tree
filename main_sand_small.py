#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi


NMAX = int(2*1e7)

SIZE = 512
ONE = 1./SIZE


#PI5 = 0.5*pi
MID = 0.5


INIT_BRANCH = 0.03
GRAIN_MULT = 5

BRANCH_DIMINISH = ONE*0.03

BRANCH_SPLIT_DIMINISH = 0.71
BRANCH_PROB_SCALE = 1.43


BRANCH_SPLIT_ANGLE = 0.3*pi
BRANCH_ANGLE_MAX = 4.*pi/SIZE
BRANCH_ANGLE_EXP = 1.5

BACK = [1,1,1,1]

OUTLINE = [0, 0, 0, 0.5]
TRUNK_STROKE = [0, 0, 0, 0.05]
TRUNK = [1, 1, 1, 1]


def main():
  from fn import Fn
  from modules.tree import Tree
  from sand import Sand

  sand = Sand(SIZE)
  sand.set_bg(BACK)

  fn = Fn(prefix='./res/tree-', postfix='.png')

  while True:
    sand.set_bg(BACK)
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

    i = 1
    while tree.Q:
      i += 1
      tree.step()
      tree.draw_brances_sand(
          sand,
          GRAIN_MULT,
          OUTLINE,
          TRUNK,
          TRUNK_STROKE
          )

      if not i%200:
        print(i, len(tree.Q))

    name = fn.name()
    print(name)
    sand.write_to_png(name)

if __name__ == '__main__':
    main()

