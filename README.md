# simple-python-3D-rasterizer

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/depth.png)

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/trig.png)

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/flatnormals.png)


## Usage

Requires Python3

`python rasterize3D.py input_file.txt`

## Supported Operations

xyz *x y z*

xyzw x y z w

trif i1 i2 i3

trig i1 i2 i3

color r g b

loadp a1,1 a1,2 a1,3 a1,4 a2,1 a2,2 … a4,4

ortho l r b t n f

translate dx dy dz

rotatex degrees, rotatey degrees, and rotatez degrees

scale sx sy sz
