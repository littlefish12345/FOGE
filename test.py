from FOGE import *

fogeInit(500,500,'qwe')

fogeRegisterKey(GLFW_KEY_ESCAPE,GLFW_PRESS,fogeClose)
'''
triangle = fogeTriangle([-0.5,-0.5,0],[0,-0.5,0],[-0.25,0.5,0],GL_STATIC_DRAW)
triangle = fogeTriangle([0.5,-0.5,0],[0,-0.5,0],[0.25,0.5,0],GL_STATIC_DRAW)
'''
vs = [[-0.5,0.5,0.5],[0.5,0.5,0.5],[0.5,-0.5,0.5],[-0.5,-0.5,0.5],
      [-0.5,0.5,-0.5],[0.5,0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,-0.5]]
is_ = [[0,1,3],[1,2,3],
       [4,5,7],[5,6,7],
       [0,4,7],[0,3,7],
       [1,5,6],[1,2,6],
       [0,1,5],[0,4,5],
       [3,2,6],[3,7,6]]
model = forgeModel(vs,is_)

fogeMainloop()
