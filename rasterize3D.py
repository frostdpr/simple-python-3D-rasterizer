import sys
import math
from PIL import Image

def mult4by4(a, b):
    answer = []
    for outrow in range(4):
    	answer.append([])
    	for outcol in range(4):
        	answer[outrow].extend([0])
        	for i in range(4):
        		answer[outrow][outcol] += a[outrow][i] * b[i][outcol]
    return answer

def multMbyV(mat, vec):
    answer = list(vec)
    for outrow in range(4):
    	answer[outrow] = 0
    	for i in range(4):
        	answer[outrow] += mat[outrow][i] * vec[i]
    return answer

def cross(a, b):
	return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

def normalize(b):
	a = list(b)
	mag = 0
	for i in a:
		mag += i**2
	mag = mag**.5
	for i in range(len(a)):
		a[i] /= mag
	return a
def hex_2_rgb(h3x):
	hexcolor = h3x.strip("#")
	return int(hexcolor[:-4],16), int(hexcolor[2:-2],16), int(hexcolor[4:],16) 

def round(num):
	return int(num + 0.5)

def correct_vertices(input):
	return int(input) - 1 if int(input) > 0 else int(input)

def close_float(a,b):
	return abs(a-b) < .0005

def clamp(num):
	return max(0, min(float(num)*255, 255))


def dda(a, b, color,z_buffer, interp,w,h):
	stepdir = abs(a[0] - b[0]) > abs(a[1] - b[1]) # true->x step false->y step
	swap = b[0] - a[0] < 0 if(stepdir) else b[1] - a[1] < 0 # true->swap needed
	if(swap): #make smaller one of stepdir be first point
		a,b = b,a
	x,y, z = a[0], a[1], a[2] #set x and y to initial point
	stepx = b[0]-a[0] if(stepdir)  else a[0]-b[0]
	stepy = b[1]-a[1] if(not stepdir)  else a[1]-b[1]
	stepz = b[2]-a[2] if(not stepdir)  else a[2]-b[2]
	length = stepx if stepx >= stepy else stepy
	if(length < 0):
		length *= -1
	dx = (b[0] - a[0]) / float(length) #find x and y step amount
	dy = (b[1] - a[1]) / float(length)
	dz = (b[2] - a[2]) / float(length)
	if(interp):
		R,G,B = a[3], a[4], a[5]
		dR,dG,dB = (b[3]-a[3])/length, (b[4]-a[4])/length, (b[5]-a[5])/length
	else:
		R,G,B = color[0], color[1], color[2]
		dR,dG,dB = 0,0,0
	if((x // 1 != x and stepdir)): #calculate offset values for x and y if needed
		orat = int(a[0]) + 1.0 - a[0]
		x += orat * dx
		y +=  orat * dy
		z += orat * dz
		R,G,B = R+dR*orat,G+dG*orat,B+dB*orat
	elif(y // 1 != y and not stepdir):
		orat = int(a[1]) + 1.0 - a[1]
		x += orat * dx
		y +=  orat * dy
		z += orat * dz
		R,G,B = R+dR*orat,G+dG*orat,B+dB*orat
	
	while(x < b[0] if stepdir else y < b[1]):
		#print(R,G,B,A)
		if(z < 1 and z > 0 and 0<=x<width and 0<=y<height and z <= z_buffer[round(x)][round(y)]):
			#print(x,y,z)
			#print(round(x),round(y))
			putpixel((round(x),round(y)), (int(R),int(G),int(B),255))
			z_buffer[round(x)][round(y)] = z
		x,y,z,R,G,B= x+dx,y+dy,z+dz,R+dR,G+dG,B+dB
def dda_list(a, b):
	ret = []
	if(a[1] == b[1]):
		return ret
	stepdir = False 
	swap = b[0] - a[0] < 0 if(stepdir) else b[1] - a[1] < 0 
	if(swap): 
		a,b = b,a
	x,y,z= a[0], a[1], a[2] 
	stepx = b[0]-a[0] if(stepdir)  else a[0]-b[0]
	stepy = b[1]-a[1] if(not stepdir)  else a[1]-b[1]
	stepz = b[2]-a[2] if(not stepdir)  else a[2]-b[2]
	length =  stepy
	if(length < 0):
		length *= -1
	dx = (b[0] - a[0]) / float(length) #find x and y step amount
	dy = (b[1] - a[1]) / float(length)
	dz = (b[2] - a[2]) / float(length)
	R,G,B = a[4], a[5], a[6]
	dR,dG,dB = (b[4]-a[4])/length, (b[5]-a[5])/length, (b[6]-a[6])/length
	if( y // 1 != y and not stepdir ): #calculate offset values for x and y if needed
		orat = int(a[1]) + 1.0 - a[1]
		x += orat * dx
		y +=  orat * dy
		z += orat * dz
		R,G,B = R+dR*orat,G+dG*orat,B+dB*orat
	while(y < b[1]):
		ret.append([x,y,z,R,G,B])
		x,y,z,R,G,B= x+dx,y+dy,z+dz,R+dR,G+dG,B+dB
	#print(ret)
	return ret
def trig(a, b, c, color,z_buffer,w,h, interp):
	common = []
	common.extend(dda_list(c,b))
	common.extend(dda_list(a,c))
	common.extend(dda_list(b,a))
	for i in common:
		#print(i)
		for j in range(common.index(i), len(common)):
			if close_float(i[1], common[j][1]) and i != common[j] and not close_float(i[0], common[j][0]):
				dda(i,common[j], color, z_buffer, interp,w,h)
				#print(i,common[j])

if len(sys.argv) == 1:
	print("Must provide at least 1 argument")
	sys.exit()

for i in range (1, len(sys.argv)):
	filereader = open(sys.argv[i],"r")
	vertices, color, mv_mat, proj_mat, z_buffer = [], [255,255,255], [[1,0,0,0], [0,1,0,0],[0,0,1,0],[0,0,0,1]], [[1,0,0,0], [0,1,0,0],[0,0,1,0],[0,0,0,1]], []
	view_w, view_h = 0, 0
	for line in filereader.readlines():
		if len(line.strip()) != 0:
			words = line.strip().split()
			keyword = words[0]
		else:
			keyword = ""	
		if keyword == "png":
			width, height = int(words[1]), int(words[2])
			img = Image.new("RGBA", (width,height), (0,0,0,0))
			view_w, view_h = width/2, height/2
			putpixel = img.im.putpixel	
			filename = words[3]
			z_buffer = [[1.0 for j in range(height)] for i in range(width)]
		elif keyword == "xyz":
			vertices.extend([[float(words[1]),float(words[2]), float(words[3]), 1, color[0],color[1],color[2]]])
			#print(vertices)
		elif keyword == "xyzw":
			vertices.extend([[float(words[1]),float(words[2]), float(words[3]), float(words[4]), color[0],color[1],color[2]]])
		elif keyword == "trif" or keyword == "trig":
			temp = []
			for i in range(1,4):
				temp.extend([vertices[correct_vertices(words[i])]])
			#apply mv matrix, proj matrix and viewport transformation
			for i in range(3): 
				temp[i] = multMbyV(mult4by4(proj_mat,mv_mat), temp[i])
				for j in range(4):
					temp[i][j] = temp[i][j] / temp[i][3] #div by w
				temp[i][0] = (temp[i][0]+1)*view_w;
				temp[i][1] = (temp[i][1]+1)*view_h;
			trig(temp[0], temp[1], temp[2],color,z_buffer,width,height,False) if keyword[3] == "f" else trig(temp[0], temp[1], temp[2],color,z_buffer,width,height,True)
		elif keyword == "color":
			color = []
			for i in range(1,4):
				color.append(clamp(words[i]))
		elif keyword == "loadmv":
			mv_mat = []
			for i in range(1,17,4):
				temp = []
				for j in range(i, i + 4):
					temp.append(float(words[j]))
				mv_mat.extend([temp])
		elif keyword == "loadp":
			proj_mat = []
			for i in range(1,17,4):
				temp = []
				for j in range(i, i + 4):
					temp.append(float(words[j]))
				proj_mat.extend([temp])
			#print(proj_mat)
		elif keyword == "frustum":
			l,r,b,t,n,f = float(words[1]),float(words[2]), float(words[3]), float(words[4]),float(words[5]), float(words[6])
			proj_mat = [[2*n/(r-l),0,(r+l)/(r-l),0],[0,2*n/(t-b),(t+b)/(t-b),0],[0,0,-(f+n)/(f-n),-(2*f*n)/(f-n)],[0,0,-1,0]]
		elif keyword == "ortho":
			l,r,b,t,n,f = float(words[1]),float(words[2]), float(words[3]), float(words[4]),float(words[5]), float(words[6])
			n = 2*n-f
			proj_mat = [[2/(r-l),0,0,-(r+l)/(r-l)],[0,2/(t-b),0,-(t+b)/(t-b)],[0,0,-2/(f-n),-(f+n)/(f-n)],[0,0,0,1]]
			#print(proj_mat)
		elif keyword == "translate":
			for i in range(3):
				mv_mat[i][3] = float(words[i+1]) + mv_mat[i][3]
		elif keyword == "rotatex" or keyword == "rotatey" or keyword == "rotatez" :
			c,s = math.cos(math.radians(float(words[1]))), math.sin(math.radians(float(words[1])))
			if keyword[6] == "x":
				mv_mat = mult4by4(mv_mat,[[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]])
			elif keyword[6] == "y":
				mv_mat = mult4by4(mv_mat,[[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]] )
			elif keyword[6] == "z":
				mv_mat = mult4by4(mv_mat,[[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]])
		elif keyword == "rotate":
			c,s = math.cos(math.radians(float(words[1]))), math.sin(math.radians(float(words[1])))
			xyz = normalize([float(words[2]),float(words[3]),float(words[4])])
			x,y,z = xyz[0],xyz[1],xyz[2]
			mv_mat = mult4by4(mv_mat,[[x**2*(1-c)+c, x*y*(1-c)-z*s, x*z*(1-c)+y*s,0],[y*x*(1-c)+z*s,y**2*(1-c)+c,y*z*(1-c)-x*s,0],[x*z*(1-c)-y*s,y*z*(1-c)+x*s,z**2*(1-c)+c,0],[0,0,0,1]])
		elif keyword == "scale":
			for i in range(3):
				mv_mat[i][i] = float(words[i+1])* mv_mat[i][i]
		elif keyword == "lookat":
			eye_index, center_index = correct_vertices(words[1]), correct_vertices(words[2])
			eye = [vertices[eye_index][0], vertices[eye_index][1], vertices[eye_index][2]]
			center = [vertices[center_index][0], vertices[center_index][1], vertices[center_index][2]]
			f = normalize([center[0]-eye[0], center[1]-eye[1], center[2]-eye[2]])
			UP = normalize([float(words[3]),float(words[4]),float(words[5])])
			s = cross(f, UP)
			u = cross(normalize(s),f)
			mv_mat = mult4by4([[s[0],s[1],s[2],0],[u[0],u[1],u[2],0],[-f[0],-f[1],-f[2],0],[0,0,0,1]], [[1,0,0,-eye[0]],[0,1,0,-eye[1]],[0,0,1,-eye[2]],[0,0,0,1]])
	img.save(filename)
	