from OpenGL.GL import *
from glfw.GLFW import *
import logging
import numpy
import sys

window = None
key_function_map = {}
draw_obj = []

def __fogeProcessKeyInput__(window): #处理键盘输入
    global key_function_mal
    for key in key_function_map.keys():
        if glfwGetKey(window,key) == key_function_map[key][0]:
            key_function_map[key][1]()

def __fogeDrawObj__():
    global draw_obj
    for obj in draw_obj:
        glBindVertexArray(obj.VAO)
        if obj.type == 'triangle':
            glDrawArrays(GL_TRIANGLES,0,3)
        else:
            glDrawElements(GL_TRIANGLES,obj.indices_num,GL_UNSIGNED_INT,None)
        glBindVertexArray(0)

class __fogeShader__:
    def __init__(self,vertex_path,fragment_path):
        vertexShaderSourceFile = open(vertex_path,'r')
        vertexShaderSource = vertexShaderSourceFile.read()
        vertexShaderSourceFile.close()
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader,vertexShaderSource)
        glCompileShader(vertexShader)
        vertexCompileSuccess = glGetShaderiv(vertexShader,GL_COMPILE_STATUS)
        if not vertexCompileSuccess:
            infoLog = glGetShaderInfoLog(vertexShader)
            logging.critical(infoLog)
            raise 'Unable to compile vertex shader'

        fragmentShaderSourceFile = open(fragment_path,'r')
        fragmentShaderSource = fragmentShaderSourceFile.read()
        fragmentShaderSourceFile.close()
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader,fragmentShaderSource)
        glCompileShader(fragmentShader)
        fragmentCompileSuccess = glGetShaderiv(fragmentShader,GL_COMPILE_STATUS)
        if not fragmentCompileSuccess:
            infoLog = glGetShaderInfoLog(fragmentShader)
            logging.critical(infoLog)
            raise 'Unable to compile vertex shader'

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram,vertexShader)
        glAttachShader(shaderProgram,fragmentShader)
        glLinkProgram(shaderProgram)
        shaderProgramCompileSuccess = glGetProgramiv(shaderProgram,GL_LINK_STATUS)
        if not shaderProgramCompileSuccess:
            infoLog = ''
            glGetProgramInfoLog(shaderProgram,infoLog)
            logging.critical(infoLog)
            raise 'Unable to link shader'
        
        self.shaderProgram = shaderProgram
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
        
    def use(self):
        glUseProgram(self.shaderProgram)


def fogeInit(width,height,title): #foge初始化
    global window,shaderProgram
    def change_framebuffer_size_callback(window,width,height): #改变窗口大小时的回调函数
        glViewport(0,0,width,height)
    if not glfwInit():
        raise 'Unable to load glfw'
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR,3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR,3)
    glfwWindowHint(GLFW_OPENGL_PROFILE,GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT,GL_TRUE)

    window = glfwCreateWindow(width,height,title,None,None)
    if window == None:
        raise 'Unable to create window'
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window,change_framebuffer_size_callback)

def fogeMainloop():
    global window,shaderProgram
    glClearColor(0,0,0,1)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    while not glfwWindowShouldClose(window):
        __fogeProcessKeyInput__(window)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shaderProgram)
        __fogeDrawObj__()
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()

def fogeClose():
    global window
    glfwSetWindowShouldClose(window,True)

def fogeRegisterKey(key,status,function):
    global key_function_map
    key_function_map[key] = (status,function)

class forgeModel:
    def __init__(self,vertice_list=None,indices=None,usage=GL_STATIC_DRAW):
        global draw_obj
        self.type = 'model'
        draw_obj.append(self)
        if vertice_list and indices:
            self.indices_num = len(indices)*3
            self.VAO = glGenVertexArrays(1)
            self.VBO = glGenBuffers(1)
            self.EBO = glGenBuffers(1)
            glBindVertexArray(self.VAO)
            
            all_indices = []
            for i in indices:
                all_indices = all_indices+i
            all_list = []
            for i in vertice_list:
                all_list = all_list+i

            glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
            glBufferData(GL_ARRAY_BUFFER,numpy.array(all_list,dtype='float32'),usage)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER,numpy.array(all_indices,dtype='uint32'),usage)
            glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER,0)
            glBindVertexArray(0)

class fogeTriangle:
    def __init__(self,vertice1,vertice2,vertice3,usage):
        global draw_obj
        self.type = 'triangle'
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
        glBufferData(GL_ARRAY_BUFFER,numpy.array(vertice1+vertice2+vertice3,dtype='float32'),usage)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindVertexArray(0)
        draw_obj.append(self)
