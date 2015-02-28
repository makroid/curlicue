#Simple python curlicue tool

This is a simple tool to visualize curves that are calculated via summation:

  `z_n = \sum_{i=1}^n exp(2*pi*j*f(s,i))`

In the upper text-field, a valid "C"-expression can be entered for f(s,i), e.g.
  
  `f(s,i) = s * i * i`
  
`ì` is the loop-variable (range: 1 to Iterations),
`s` is a free parameter,
`j` is the imaginary unit

##Requirements

* python2.x + gtk
* matplotlib
* scipy
* python2.x development files
  
##Tour

![combined](http://i.imgur.com/d12azA3.png?1)
