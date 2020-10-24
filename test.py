from FOGE_rewrite import *

fogeInit(500,500,'qwe')

fogeRegisterKey(GLFW_KEY_ESCAPE,GLFW_PRESS,fogeClose)

vs = [[-0.5,0.5,0.5],[0.5,0.5,0.5],[0.5,-0.5,0.5],[-0.5,-0.5,0.5],
      [-0.5,0.5,-0.5],[0.5,0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,-0.5]]

is_ = [[0,1,3],[1,2,3],
       [4,5,7],[5,6,7],
       [0,4,7],[0,3,7],
       [1,5,6],[1,2,6],
       [0,1,5],[0,4,5],
       [3,2,6],[3,7,6]]

tp = [[0,1],[1,1],[1,0],[0,0],
      [0,1],[1,1],[1,0],[0,0]]

t_path = 'dirt.png'

model = fogeModel(vs,is_,tp,t_path,tex_filter_type=GL_NEAREST)
#model.loadTextureFile()

fogeMainLoop()
