#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy.random import normal, random, randint

from numpy import pi
from numpy import cos
from numpy import sin
from numpy import square
from numpy import sqrt
from numpy import array
from numpy import ones


class Branch(object):

  def __init__(self,tree,x,y,r,a,g):

    self.tree = tree

    self.x = x
    self.y = y
    self.r = r
    self.a = a

    self.shade = 0

    self.i = 0
    self.g = g

    self.left = 0.5
    self.right = 0.5

  def step(self):

    #self.r *= BRANCH_DIMINISH
    self.r = self.r - self.tree.branch_diminish

    angle = normal()*self.tree.branch_angle_max

    #da = (1.-1./((self.g+1)**SEARCH_ANGLE_EXP))*angle
    #da = ((1./(ONE + INIT_BRANCH - self.r))**SEARCH_ANGLE_EXP)*angle
    #da = (1.-1./(ONE + INIT_BRANCH - self.r)**SEARCH_ANGLE_EXP)*angle

    scale = self.tree.one+self.tree.root_r-self.r
    da = (1.+scale/self.tree.root_r)**self.tree.branch_angle_exp
    self.a += da*angle

    dx = cos(self.a)*self.tree.stepsize
    dy = sin(self.a)*self.tree.stepsize

    self.x += dx
    self.y += dy
    self.i += 1

    # self.left += (1.0-2.0*random())*0.3
    # if self.left<0.2:
    #   self.left = 0.2
    # if self.left>0.95:
    #   self.left = 0.95
    # self.right += (1.0-2.0*random())*0.3
    # if self.right<0.2:
    #   self.right = 0.2
    # if self.right>0.95:
    #   self.right = 0.95

class Tree(object):

  def __init__(
    self,
    root_x,
    root_y,
    root_r,
    root_a,
    one,
    stepsize,
    branch_split_angle,
    branch_prob_scale,
    branch_diminish,
    branch_split_diminish,
    branch_angle_max,
    branch_angle_exp
  ):

    self.root_x = root_x
    self.root_y = root_y
    self.root_r = root_r
    self.root_a = root_a
    self.stepsize = stepsize
    self.one = one

    self.branch_split_angle = branch_split_angle
    self.branch_diminish = branch_diminish
    self.branch_split_diminish = branch_split_diminish
    self.branch_angle_max = branch_angle_max
    self.branch_angle_exp = branch_angle_exp

    self.branch_prob_scale = branch_prob_scale

    self.init()

  def init(self):

    self.Q = []

    branch = Branch(
      self,
      self.root_x,
      self.root_y,
      self.root_r,
      self.root_a,
      0
    )

    self.Q.append(branch)

  def step(self):

    q_remove = []
    q_new = []
    for i,b in enumerate(self.Q):

      b.step()

      if b.r<=self.one:
        q_remove.append(i)
        continue

      branch_prob = (self.root_r-b.r+self.one)*self.branch_prob_scale

      if random()<branch_prob:

        x = b.x
        y = b.y
        a = b.a
        r = b.r
        g = b.g

        new_r = self.branch_split_diminish*r

        ra = ((-1)**randint(2))*random()*self.branch_split_angle
        q_new.append(Branch(self,
                     x,
                     y,
                     new_r,
                     a + ra,
                     g+1))

      else:

        q_remove.append(i)
        q_new.append(b)

    q_remove.reverse()

    for r in q_remove:
      del(self.Q[r])

    self.Q.extend(q_new)

  # def branch(self,b):
  #
  #   a = b.a
  #   r = b.r
  #   x = b.x
  #   y = b.y
  #
  #   rx = self.ctx
  #
  #   one = self.one
  #
  #   x1 = x + cos(a-0.5*pi)*r
  #   x2 = x + cos(a+0.5*pi)*r
  #   y1 = y + sin(a-0.5*pi)*r
  #   y2 = y + sin(a+0.5*pi)*r
  #   dd = sqrt(square(x-x2) + square(y-y2))
  #
  #
  #   ## TRUNK STROKE
  #   rx.set_source_rgba(*self.trunk)
  #   for _ in range(10):
  #     rx.move_to(x1,y1)
  #     rx.line_to(x2,y2)
  #     rx.stroke()
  #
  #   ## OUTLINE
  #   rx.set_source_rgba(*self.trunk_stroke)
  #   rx.rectangle(x1,y1,one,one)
  #   rx.fill()
  #   rx.rectangle(x1,y1,one,one)
  #   rx.fill()
  #
  #   rx.rectangle(x2,y2,one,one)
  #   rx.fill()
  #   rx.rectangle(x2,y2,one,one)
  #   rx.fill()
  #
  #   ## TRUNK SHADE RIGHT
  #   the = 0.5*pi + a
  #
  #   # TODO: shade increments
  #   scales = random(self.grains)*dd*random()
  #   xxp = x2 - scales*cos(the)
  #   yyp = y2 - scales*sin(the)
  #
  #   for xx,yy in zip(xxp,yyp):
  #     rx.rectangle(xx,yy,one,one)
  #     rx.fill()
  #
  #   ## TRUNK SHADE LEFT
  #   dd = sqrt(square(x-x1) + square(y-y1))
  #   the = a - 0.5*pi
  #
  #   scales = random(int(self.grains/5.))*dd*random()
  #   xxp = x1 - scales*cos(the)
  #   yyp = y1 - scales*sin(the)
  #
  #   for xx,yy in zip(xxp,yyp):
  #     rx.rectangle(xx,yy,one,one)
  #     rx.fill()

  def draw_brances(self, render, grains, trunk, trunk_stroke):
    one = self.one
    rx = render.ctx

    for b in self.Q:
      a = b.a
      r = b.r
      x = b.x
      y = b.y

      x1 = x + cos(a-0.5*pi)*r
      x2 = x + cos(a+0.5*pi)*r
      y1 = y + sin(a-0.5*pi)*r
      y2 = y + sin(a+0.5*pi)*r
      dd = sqrt(square(x-x2) + square(y-y2))

      ## TRUNK STROKE
      render.set_front(trunk)
      for _ in range(10):
        rx.move_to(x1,y1)
        rx.line_to(x2,y2)
        rx.stroke()

      ## OUTLINE
      render.set_front(trunk_stroke)
      rx.rectangle(x1,y1,one,one)
      rx.fill()
      rx.rectangle(x1,y1,one,one)
      rx.fill()

      rx.rectangle(x2,y2,one,one)
      rx.fill()
      rx.rectangle(x2,y2,one,one)
      rx.fill()

      rx.rectangle(x1,y1,one,one)
      rx.fill()
      rx.rectangle(x2,y2,one,one)
      rx.fill()

      ## TRUNK SHADE RIGHT
      the = 0.5*pi + a

      # TODO: shade increments
      scales = random(grains)*dd*random()
      xxp = x2 - scales*cos(the)
      yyp = y2 - scales*sin(the)

      for xx,yy in zip(xxp,yyp):
        rx.rectangle(xx,yy,one,one)
        rx.fill()

      ## TRUNK SHADE LEFT
      dd = sqrt(square(x-x1) + square(y-y1))
      the = a - 0.5*pi

      scales = random(int(grains/5.))*dd*random()
      xxp = x1 - scales*cos(the)
      yyp = y1 - scales*sin(the)

      for xx,yy in zip(xxp,yyp):
        rx.rectangle(xx,yy,one,one)
        rx.fill()

  def draw_brances_sand(self, sand, grain_mult, outline, trunk, trunk_stroke):

    for b in self.Q:
      a = b.a
      r = b.r
      x = b.x
      y = b.y

      x1 = x + cos(a-0.5*pi)*r
      x2 = x + cos(a+0.5*pi)*r
      y1 = y + sin(a-0.5*pi)*r
      y2 = y + sin(a+0.5*pi)*r
      dd = sqrt(square(x-x2) + square(y-y2))
      num_grains = int(dd/self.one)

      if num_grains<2:
        num_grains = 2

      ## TRUNK STROKE
      t1 = array([
        [x1, y1]
        ], 'float')
      t2 = array([
        [x2, y2]
        ], 'float')
      sand.set_rgba(trunk)
      sand.paint_strokes(t1, t2, 10*num_grains*grain_mult)

      ## OUTLINE
      sand.set_rgba(outline)
      d = array([
          [x1, y1],
          [x2, y2]
          ], 'float')
      sand.paint_filled_circles(d, ones(2)*self.one*1.3, 10)

      for _ in range(4):

        ## TRUNK SHADE RIGHT
        the = 0.5*pi + a + (1.0-2.0*random())*0.03
        s1 = array([ [x2, y2] ], 'float')
        s2 = s1-array([ [cos(the), sin(the)] ], 'float')*dd*random()
        sand.set_rgba(trunk_stroke)
        sand.paint_strokes(s1, s2, num_grains*grain_mult)

        ## TRUNK SHADE LEFT
        the = a - 0.5*pi + (1.0-2.0*random())*0.03
        s1 = array([ [x1, y1] ], 'float')
        s2 = s1-array([ [cos(the), sin(the)] ], 'float')*dd*random()
        sand.set_rgba(trunk_stroke)
        sand.paint_strokes(s1, s2, int(num_grains*grain_mult*0.20))

