#!/usr/bin/python
# -*- coding: utf-8 -*-


import cairo
#import Image
import gtk
import gobject

from numpy import cos, sin, pi, sort, array, zeros, diff,\
  ones, reshape, linspace, argsort, arctan2, sqrt, square

from numpy.random import random, normal

FNAME = './img/xx'
NMAX = int(2*1e8)

SIZE = 1000
ONE = 1./SIZE

PI = pi
TWOPI = 2.*pi
PI5 = 0.5*pi
MID = 0.5

INIT_BRANCH = 20.*ONE
BRANCH_ANGLE = 0.2*PI
BRANCH_DIMINISH = ONE/40
BRANCH_SPLIT_DIMINISH = 0.71

BRANCH_PROB = 0.005

SEARCH_ANGLE_MAX = pi*0.01
SEARCH_ANGLE_EXP = 0.1


BACK = [1]*3
FRONT = [0, 0, 0, 0.5]
TRUNK_STROKE = [0, 0, 0, 1]
TRUNK = [1, 1, 1, 1]
TRUNK_SHADE = [0,0,0,0.5]
#TRUNK_SHADE = [1,1,1,0.5]
LEAF = [0,0,1,0.5]



LINEWIDTH = ONE*2

DRAW_ITT = 10


class Render(object):

  def __init__(self, n):

    self.n = n

    self.__init_cairo()

    window = gtk.Window()
    window.resize(self.n, self.n)

    window.connect("destroy", self.__write_image_and_exit)
    darea = gtk.DrawingArea()
    darea.connect("expose-event", self.expose)
    window.add(darea)
    window.show_all()

    self.darea = darea
    self.num_img = 0

  def clear_canvas(self):

    self.ctx.set_source_rgb(*BACK)
    self.ctx.rectangle(0, 0, 1, 1)
    self.ctx.fill()

  def __write_image_and_exit(self, *args):

    self.sur.write_to_png('on_exit.png')
    gtk.main_quit(*args)

  def __init_cairo(self):

    sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.n, self.n)
    ctx = cairo.Context(sur)
    ctx.scale(self.n, self.n)
    ctx.set_source_rgb(*BACK)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    self.sur = sur
    self.ctx = ctx

  def init_step(self, e):

    self.itt = 0
    self.step = e
    # gobject.timeout_add(5,self.step_wrap)
    gobject.idle_add(self.step_wrap)
    self.steps = 0

  def circle(self, x, y, r):

    self.ctx.arc(x, y, r, 0, pi*2.)
    self.ctx.fill()

  def expose(self, *args):

    if not self.itt % DRAW_ITT:
      cr = self.darea.window.cairo_create()
      cr.set_source_surface(self.sur, 0, 0)
      cr.paint()

  def step_wrap(self, *args):

    res = self.step()
    self.expose()
    self.steps += 1
    self.itt += 1

    return res


class Branch():

  def __init__(self,x,y,r,a,s=ONE,g=0):

    self.x = x
    self.y = y
    self.r = r
    self.a = a
    self.s = s

    self.i = 0 # steps
    self.g = g # generation

  def step(self):

    #self.r *= BRANCH_DIMINISH
    self.r = self.r - BRANCH_DIMINISH

    angle = normal()*SEARCH_ANGLE_MAX
    #self.a += (1.-1./((ge+1)**SEARCH_ANGLE_EXP))*angle
    self.a += ((1./(ONE + INIT_BRANCH - self.r))**SEARCH_ANGLE_EXP)*angle

    dx = cos(self.a)*self.s
    dy = sin(self.a)*self.s
    self.x += dx
    self.y += dy
    self.i += 1

def main():

  render = Render(SIZE)
  render.ctx.set_source_rgba(*FRONT)
  render.ctx.set_line_width(LINEWIDTH)

  Q = []
  Q.append(Branch(MID,0.8,INIT_BRANCH,-PI*0.5,ONE))

  def draw_leaf(b):

    rx = render.ctx
    rx.set_source_rgba(*LEAF)

    x = b.x
    y = b.y
    s = b.s

    GRAINS = 100
    LEAF_LENGTH = INIT_BRANCH

    x1 = x + cos(-PI)*LEAF_LENGTH
    x2 = x + cos(0)*LEAF_LENGTH
    y1 = y + sin(-PI)*LEAF_LENGTH
    y2 = y + sin(0)*LEAF_LENGTH
    dd = sqrt(square(x1-x2) + square(y1-y2))

    the = -PI

    scales = random(GRAINS)*dd*random()
    xxp = x1 - scales*cos(the)
    yyp = y1 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,ONE,ONE)
      rx.fill()

  def draw_branch(b):
    a = b.a
    r = b.r
    x = b.x
    y = b.y
    s = b.s

    rx = render.ctx

    GRAINS = 20

    x1 = x + cos(a-0.5*PI)*r
    x2 = x + cos(a+0.5*PI)*r
    y1 = y + sin(a-0.5*PI)*r
    y2 = y + sin(a+0.5*PI)*r
    dd = sqrt(square(x-x2) + square(y-y2))

    ## TRUNK STROKE
    rx.set_source_rgba(*TRUNK)
    rx.move_to(x1,y1)
    rx.line_to(x2,y2)
    rx.stroke()

    ## OUTLINE
    rx.set_source_rgba(*TRUNK_STROKE)
    rx.rectangle(x1,y1,ONE,ONE)
    rx.fill()
    rx.rectangle(x1,y1,ONE,ONE)
    rx.fill()

    rx.rectangle(x2,y2,ONE,ONE)
    rx.fill()
    rx.rectangle(x2,y2,ONE,ONE)
    rx.fill()

    ## TRUNK SHADE
    the = 0.5*PI + a

    scales = random(GRAINS)*dd*random()
    xxp = x2 - scales*cos(the)
    yyp = y2 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,ONE,ONE)
      rx.fill()

    ## TRUNK SHADE 2
    GRAINS = 3
    dd = sqrt(square(x-x1) + square(y-y1))
    the = a - 0.5*PI

    scales = random(GRAINS)*dd*random()
    xxp = x1 - scales*cos(the)
    yyp = y1 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,ONE,ONE)
      rx.fill()

  def step():

    q_remove = []
    q_new = []
    for i,b in enumerate(Q):
      b.step()
      draw_branch(b)

      if b.r<=ONE:
        q_remove.append(i)
        #draw_leaf(b)
        continue

      if random()<BRANCH_PROB:

        x = b.x
        y = b.y
        a = b.a
        r = b.r
        g = b.g

        new_r = BRANCH_SPLIT_DIMINISH*r
        b1 = Branch(x,y,new_r,a+random()*BRANCH_ANGLE,ONE,g+1)
        b2 = Branch(x,y,new_r,a-random()*BRANCH_ANGLE,ONE,g+1)
        q_new.append(b2)
        q_new.append(b1)
      else:
        q_remove.append(i)
        q_new.append(b)

    q_remove.reverse()
    for r in q_remove:
      del(Q[r])

    Q.extend(q_new)

    if Q:
      return True
    else:
      return False

  render.init_step(step)

  gtk.main()


if __name__ == '__main__':

  if False:

    import pstats
    import cProfile
    fn = './profile/profile'
    cProfile.run('main()', fn)
    p = pstats.Stats(fn)
    p.strip_dirs().sort_stats('cumulative').print_stats()

  else:

    main()
