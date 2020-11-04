from FOGE import *

fogeInit(500,500,'qwe')

def frame_callback_function(time):
    global model
    model.rotate('x',1)
    model.rotate('y',1)
    model.rotate('z',1)

fogeRegisterKey(GLFW_KEY_ESCAPE,GLFW_PRESS,fogeClose)
fogeRegisterFrameCallack(frame_callback_function)

vs = [[-0.5,0.5,0],[0.5,0.5,0],[0.5,-0.5,0],[-0.5,-0.5,0]]

is_ = [[0,1,2],[2,3,0]]

tp = [[0,1],[1,1],[1,0],[0,0]]

t_path = 'bedrock.png'

model = fogeModel(vs,is_,tp,t_path,tex_filter_type=GL_NEAREST,tex_color_type=GL_RGBA)
#model.translate('x',0.5)

fogeMainLoop()
