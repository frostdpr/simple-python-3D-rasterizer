# simple-python-3D-rasterizer

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/depth.png)

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/trig.png)

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/flatnormals.png)


## Usage

Requires Python3

`python rasterize3D.py input_file.txt`

## Supported Operations

#### xyz *x y z*

Adds the point *x y z 1* to the vertex list.

![]()

#### xyzw *x y z w*

Adds the point *x y z w* to the vertex list.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/xyzw.png)

#### trif *i1 i2 i3*

Draws a triangle defined by vertices given by indices *i1 i2 i3*. With the color given by the last color command. Defaults to white.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/trif.png)

#### trig *i1 i2 i3*

Draws a gouraud shaded triangle.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/trig.png)

#### color *r g b*

Sets the current color to *r g b*, floating point between 0 and 1.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/color.png)

#### loadp *a1,1 a1,2 a1,3 a1,4 a2,1 a2,2 … a4,4*

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/loadp.png)

#### loadmv *a1,1 a1,2 a1,3 a1,4 a2,1 a2,2 … a4,4*

![]()

#### ortho *l r b t n f*

Sets the projection to be an orthogonal projection.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/ortho.png)

#### frustum *l r b t n f* 

Sets the projection to be an perspective projection.

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/frustum.png)

#### lookat *eye center upx upy upz*

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/lookat.png)

#### translate *dx dy dz*

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/translate.png)

#### rotatex *degrees*, rotatey *degrees*, and rotatez *degrees*

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/rotatex.png)

#### scale *sx sy sz*

![](https://raw.githubusercontent.com/frostdpr/simple-python-3D-rasterizer/master/output/scale.png)
