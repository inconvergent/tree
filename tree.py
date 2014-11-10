#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy.random import normal, random
from numpy import cos,sin

class Branch(object):

  def __init__(self,x,y,r,a,s,g):

    self.x = x
    self.y = y
    self.r = r
    self.a = a
    self.s = s

    self.i = 0
    self.g = g

  def step(self):

    #self.r *= BRANCH_DIMINISH
    self.r = self.r - self.branch_diminish

    angle = normal()*self.branch_angle_max

    #da = (1.-1./((self.g+1)**SEARCH_ANGLE_EXP))*angle
    #da = ((1./(ONE + INIT_BRANCH - self.r))**SEARCH_ANGLE_EXP)*angle
    #da = (1.-1./(ONE + INIT_BRANCH - self.r)**SEARCH_ANGLE_EXP)*angle

    scale = self.one+self.root_r-self.r
    da = (1.+scale/self.root_r)**self.branch_angle_exp
    self.a += da*angle

    dx = cos(self.a)*self.s
    dy = sin(self.a)*self.s

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
               branch_angle_max,
               branch_angle_exp):

    self.root_x = root_x
    self.root_y = root_y
    self.root_r = root_r
    self.stepsize = stepsize

    self.one = one

    self.branch_diminish = branch_diminish
    self.branch_angle_max = branch_angle_max
    self.branch_angle_exp = branch_angle_exp

    self.branch_prob_scale = branch_prob_scale

    self.Q = []

    branch = Branch(root_x,
                    root_y,
                    root_r,
                    root_a,
                    stepsize,
                    0,
                    branch_diminish,
                    branch_angle_max,
                    branch_angle_exp)

    self.Q.append(branch)

  def step(self):

    q_remove = []
    q_new = []
    for i,b in enumerate(self.Q):

      b.step()

      if b.r<=self.one:
        q_remove.append(i)
        continue

      branch_prob = (self.init_branch-b.r+self.one)*self.branch_prob_scale

      if random()<branch_prob:

        x = b.x
        y = b.y
        a = b.a
        r = b.r
        g = b.g

        new_r = self.branch_split_diminish*r
        b1 = Branch(x,y,new_r,
                    a+random()*self.branch_split_angle,
                    self.stepsize,
                    g+1,
                    self.one,
                    self.init_branch,
                    self.branch_diminish,
                    self.search_angle_max,
                    self.search_angle_exp)

        b2 = Branch(x,y,new_r,
                    a+random()*self.branch_split_angle,
                    self.stepsize,
                    g+1,
                    self.one,
                    self.init_branch,
                    self.branch_diminish,
                    self.search_angle_max,
                    self.search_angle_exp)


        q_new.append(b2)
        q_new.append(b1)

      else:

        q_remove.append(i)
        q_new.append(b)

    q_remove.reverse()

    for r in q_remove:
      del(self.Q[r])

    self.Q.extend(q_new)

