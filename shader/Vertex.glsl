#version 330 core
layout (location = 0) in vec3 inPos;
layout (location = 1) in vec2 inTexPos;

out vec2 outTexPos;

uniform mat4 transform;

void main()
{
	gl_Position = transform*vec4(inPos, 1.0);
	outTexPos = inTexPos;
}