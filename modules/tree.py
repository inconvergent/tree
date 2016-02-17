#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy.random import normal, random, randint
from numpy import cos,sin

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

class Tree(object):

  def __init__(self,
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
               branch_angle_exp):

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

    branch = Branch(self,
                    self.root_x,
                    self.root_y,
                    self.root_r,
                    self.root_a,
                    0)

    self.Q.append(branch)

  def step(self):

    q_remove = []
    q_new = []
    for i,b in enumerate(self.Q):

      b.step()

      if b.r<=self.one:
        q_remove.append(i)
        continue

      branch_prob = (self.root_r-
                     b.r+self.one)*self.branch_prob_scale

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

