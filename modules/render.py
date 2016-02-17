#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
import gtk
import gobject

from numpy import cos, sin, pi, sqrt, square
from numpy.random import random

class Render(object):

  def __init__(self, n, front, back, trunk, trunk_stroke, grains):

    self.n = n
    self.one = 1./self.n

    self.front = front
    self.back = back
    self.trunk = trunk
    self.trunk_stroke = trunk_stroke
    self.grains = grains

    self.__init_cairo()

  def clear_canvas(self):

    self.ctx.set_source_rgba(*self.back)
    self.ctx.rectangle(0, 0, 1, 1)
    self.ctx.fill()

  def __init_cairo(self):

    sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.n, self.n)
    ctx = cairo.Context(sur)
    ctx.scale(self.n, self.n)

    self.sur = sur
    self.ctx = ctx

    self.clear_canvas()

  def circle(self, x, y, r):

    self.ctx.arc(x, y, r, 0, pi*2.)
    self.ctx.fill()

  def branch(self,b):

    a = b.a
    r = b.r
    x = b.x
    y = b.y

    rx = self.ctx

    one = self.one

    x1 = x + cos(a-0.5*pi)*r
    x2 = x + cos(a+0.5*pi)*r
    y1 = y + sin(a-0.5*pi)*r
    y2 = y + sin(a+0.5*pi)*r
    dd = sqrt(square(x-x2) + square(y-y2))

    ## TRUNK STROKE
    rx.set_source_rgba(*self.trunk)
    for _ in xrange(10):
      rx.move_to(x1,y1)
      rx.line_to(x2,y2)
      rx.stroke()

    ## OUTLINE
    rx.set_source_rgba(*self.trunk_stroke)
    rx.rectangle(x1,y1,one,one)
    rx.fill()
    rx.rectangle(x1,y1,one,one)
    rx.fill()

    rx.rectangle(x2,y2,one,one)
    rx.fill()
    rx.rectangle(x2,y2,one,one)
    rx.fill()

    ## TRUNK SHADE RIGHT
    the = 0.5*pi + a

    # TODO: shade increments
    scales = random(self.grains)*dd*random()
    xxp = x2 - scales*cos(the)
    yyp = y2 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,one,one)
      rx.fill()

    ## TRUNK SHADE LEFT
    dd = sqrt(square(x-x1) + square(y-y1))
    the = a - 0.5*pi

    scales = random(int(self.grains/5.))*dd*random()
    xxp = x1 - scales*cos(the)
    yyp = y1 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,one,one)
      rx.fill()

  def branch2(self,b):

    a = b.a
    r = b.r
    x = b.x
    y = b.y

    rx = self.ctx

    one = self.one

    x1 = x + cos(a-0.5*pi)*r
    x2 = x + cos(a+0.5*pi)*r
    y1 = y + sin(a-0.5*pi)*r
    y2 = y + sin(a+0.5*pi)*r
    dd = sqrt(square(x-x2) + square(y-y2))

    ## TRUNK STROKE
    rx.set_source_rgba(*self.trunk)
    for _ in xrange(10):
      rx.move_to(x1,y1)
      rx.line_to(x2,y2)
      rx.stroke()

    ## OUTLINE
    rx.set_source_rgba(*self.trunk_stroke)
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
    scales = random(self.grains)*dd*random()
    xxp = x2 - scales*cos(the)
    yyp = y2 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,one,one)
      rx.fill()

    ## TRUNK SHADE LEFT
    dd = sqrt(square(x-x1) + square(y-y1))
    the = a - 0.5*pi

    scales = random(int(self.grains/5.))*dd*random()
    xxp = x1 - scales*cos(the)
    yyp = y1 - scales*sin(the)

    for xx,yy in zip(xxp,yyp):
      rx.rectangle(xx,yy,one,one)
      rx.fill()


class Animate(Render):

  def __init__(self, n, front, back, trunk, trunk_stroke, grains,
               steps_itt, step):

    Render.__init__(self, n, front, back, trunk, trunk_stroke, grains)

    window = gtk.Window()
    window.resize(self.n, self.n)

    self.steps_itt = steps_itt
    self.step = step

    window.connect("destroy", self.__destroy)
    darea = gtk.DrawingArea()
    darea.connect("expose-event", self.expose)
    window.add(darea)
    window.show_all()

    self.darea = darea

    self.steps = 0
    gobject.idle_add(self.step_wrap)

  def __destroy(self,*args):

    gtk.main_quit(*args)

  def expose(self,*args):

    cr = self.darea.window.cairo_create()
    cr.set_source_surface(self.sur,0,0)
    cr.paint()

  def step_wrap(self):

    res = self.step(self.steps_itt,self)
    self.steps += 1
    self.expose()

    return res

