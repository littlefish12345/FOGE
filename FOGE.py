from OpenGL.GL import *
from glfw.GLFW import *
from PIL import Image
import numpy

window = None
key_function_map = {}
draw_obj = []

class fogeError(Exception): #错误类
    def __init__(self,error_str):
        self.error_str=_error_str
    def __str__(self):
        return self.error_str

def __fogeDrawObj__():
    global draw_obj,shader
    for obj in draw_obj:
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,obj.texture)
        shader.use()
        glBindVertexArray(obj.VAO)
        glDrawElements(GL_TRIANGLES,obj.indices_num,GL_UNSIGNED_INT,None)
        glBindVertexArray(0)

def __fogeProcessKeyInput__(window): #处理键盘输入
    global key_function_map
    for key in key_function_map.keys():
        if glfwGetKey(window,key) == key_function_map[key][0]:
            key_function_map[key][1]()

class __fogeShader__: #着色器类
    def __init__(self,vertex_shader_path,fragment_shader_path):
        try:
            vertex_shader_source_file = open(vertex_shader_path,'r') #读取顶点着色器源文件
            vertex_shader_source = vertex_shader_source_file.read()
        except FileNotFoundError:
            glfwTerminate()
            raise fogeError('Unable to read vertex shader source file')
        finally:
            vertex_shader_source_file.close()

        try:
            fragment_shader_source_file = open(fragment_shader_path,'r')  #读取顶点着色器源文件
            fragment_shader_source = fragment_shader_source_file.read()
        except FileNotFoundError:
            glfwTerminate()
            raise fogeError('Unable to read fragment shader source file')
        finally:
            fragment_shader_source_file.close()

        vertex_shader = glCreateShader(GL_VERTEX_SHADER) #编译片段着色器
        glShaderSource(vertex_shader,vertex_shader_source)
        glCompileShader(vertex_shader)
        vertex_compile_success = glGetShaderiv(vertex_shader,GL_COMPILE_STATUS)
        if not vertex_compile_success:
            log = glGetShaderInfoLog(vertex_shader)
            logging.critical(log)
            raise fogeError('Unable to compile vertex shader')

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER) #编译片段着色器
        glShaderSource(fragment_shader,fragment_shader_source)
        glCompileShader(fragment_shader)
        fragment_compile_success = glGetShaderiv(fragment_shader,GL_COMPILE_STATUS)
        if not fragment_compile_success:
            log = glGetShaderInfoLog(fragment_shader)
            logging.critical(log)
            raise fogeError('Unable to compile fragment shader')

        shader_program = glCreateProgram() #链接着色器
        glAttachShader(shader_program,vertex_shader)
        glAttachShader(shader_program,fragment_shader)
        glLinkProgram(shader_program)
        shader_program_link_success = glGetProgramiv(shader_program,GL_LINK_STATUS)
        if not shader_program_link_success:
            log = glGetProgramInfoLog(shader_program)
            logging.critical(log)
            raise fogeError('Unable to link shader')

        self.shader_program = shader_program

    def use(self): #使用这个着色器
        glUseProgram(self.shader_program)

    def get_location(self,name): #获取顶点着色器locaion
        return glGetAttribLocation(self.shader_program,name)

def fogeClose(): #关闭foge
    global window
    glfwSetWindowShouldClose(window,True)

def fogeRegisterKey(key,status,function): #注册键响应回调函数
    global key_function_map
    key_function_map[key] = (status,function)

def fogeInit(width,height,title):
    global window,shader
    if not glfwInit(): #初始化glfw
        raise fogeError('Unable to load glfw')

    window = glfwCreateWindow(width,height,title,None,None) #创建窗口
    if not window:
        glfwTerminate()
        raise fogeError('Unable to create the window')
    glfwMakeContextCurrent(window)

    shader = __fogeShader__('./shader/Vertex.glsl','./shader/Fragment.glsl')

def fogeMainLoop():
    global window
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glClearColor(0,0,0,1)
    while not glfwWindowShouldClose(window):
        width,height = glfwGetFramebufferSize(window)
        glViewport(0,0,width,height)
        __fogeProcessKeyInput__(window)
        glClear(GL_COLOR_BUFFER_BIT)
        __fogeDrawObj__()
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()

class fogeModel: #模型
    def __init__(self,vertex_list=[],indices=[],texture_pos=[],texture_path='',usage=GL_STATIC_DRAW,tex_wrap_type=GL_REPEAT,tex_filter_type=GL_LINEAR,tex_color_type=GL_RGB):
        global draw_obj
        draw_obj.append(self)
        self.show = False
        self.VAO = glGenVertexArrays(1) #生成VAO
        if vertex_list and indices and texture_pos and texture_path:
            self.show = True
            self.loadModel(vertex_list,indices,usage)
            self.loadTexture(texture_pos,texture_path,usage,tex_wrap_type,tex_filter_type,tex_color_type)

    def loadModel(self,vertex_list,indices,usage=GL_STATIC_DRAW): #加载模型
        global shader
        vertex_location = shader.get_location(b'inPos') #获取顶点坐标locaion

        glBindVertexArray(self.VAO) #绑定VAO

        all_indices = [] #生成EBO和顶点VBO数据
        for i in indices:
            all_indices = all_indices+i
            
        all_vertex_list = []
        for i in vertex_list:
            all_vertex_list  = all_vertex_list+i

        self.indices_num = len(all_indices)

        vertex_data = numpy.array(all_vertex_list,numpy.float32) #生成和加载顶点VBO
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
        glBufferData(GL_ARRAY_BUFFER,vertex_data,usage)

        indices_data = numpy.array(all_indices,numpy.uint32) #生成和加载EBO
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices_data,usage)

        glVertexAttribPointer(vertex_location,3,GL_FLOAT,GL_FALSE,0,None) #设定顶点坐标读取模式
        glEnableVertexAttribArray(vertex_location) #启用顶点数组
        
        glBindVertexArray(0) #解绑VAO
        glBindBuffer(GL_ARRAY_BUFFER,0) #解绑VBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,0) #解绑EBO

    def loadTexture(self,texture_pos,texture_path,usage=GL_STATIC_DRAW,tex_wrap_type=GL_REPEAT,tex_filter_type=GL_LINEAR,tex_color_type=GL_RGB): #加载贴图
        global shader
        tex_location = shader.get_location(b'inTexPos') #获取贴图坐标locaion

        glBindVertexArray(self.VAO) #绑定VAO
        
        all_texture_pos = [] #生成贴图坐标VBO数据
        for i in texture_pos:
            all_texture_pos  = all_texture_pos+i

        texture_pos_data = numpy.array(all_texture_pos,numpy.float32) #生成和加载贴图坐标VBO
        self.tVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.tVBO)
        glBufferData(GL_ARRAY_BUFFER,texture_pos_data,usage)

        glVertexAttribPointer(tex_location,2,GL_FLOAT,GL_FALSE,0,None) #设定贴图坐标读取模型
        glEnableVertexAttribArray(tex_location) #启用贴图坐标数组

        glBindVertexArray(0) #解绑VAO
        glBindBuffer(GL_ARRAY_BUFFER,0) #解绑VBO

        img = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM) #加载贴图文件
        img_data = numpy.array(list(img.getdata()),numpy.int8) #生成贴图数据
        self.texture = glGenTextures(1) #生成贴图对象
        glBindTexture(GL_TEXTURE_2D,self.texture)

        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,tex_wrap_type) #设置贴图环绕方式
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,tex_wrap_type)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,tex_filter_type) #设置贴图过滤方式
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,tex_filter_type)

        glTexImage2D(GL_TEXTURE_2D,0,tex_color_type,img.size[0],img.size[1],0,tex_color_type,GL_UNSIGNED_BYTE,img_data) #传输贴图数据

        glBindTexture(GL_TEXTURE_2D,0) #解绑提额图对象
