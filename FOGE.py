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
        if obj.type == 'triangle':
            glBindVertexArray(obj.VAO)
            glDrawArrays(GL_TRIANGLES,0,3)
            glBindVertexArray(0)

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

    vertexShaderSourceFile = open('./shader/Vertex.glsl','r')
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

    fragmentShaderSourceFile = open('./shader/Fragment.glsl','r')
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

def fogeMainloop():
    global window,shaderProgram
    while not glfwWindowShouldClose(window):
        __fogeProcessKeyInput__(window)
        glClearColor(0,0,0,1)
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
