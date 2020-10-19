from FOGE import *

fogeInit(500,500,'qwe')

fogeRegisterKey(GLFW_KEY_ESCAPE,GLFW_PRESS,fogeClose)
triangle = fogeTriangle([-0.5,-0.5,0],[0,-0.5,0],[-0.25,0.5,0],GL_STATIC_DRAW)
triangle = fogeTriangle([0.5,-0.5,0],[0,-0.5,0],[0.25,0.5,0],GL_STATIC_DRAW)

fogeMainloop()
