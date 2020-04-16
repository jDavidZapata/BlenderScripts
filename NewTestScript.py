import bpy 
from random import randint

#bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.select_by_type(extend=False, type='MESH')

bpy.ops.object.delete(use_global=False)

amount = 30

for i in range(amount):
    x = randint(-6,6)
    y = randint(-6,6)
    z = randint(-2,2)
    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
    bpy.ops.mesh.primitive_uv_sphere_add(location=(-x,-y,-z))
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].render_levels = 2
    bpy.context.object.modifiers["Subdivision"].levels = 2
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_monkey_add(location=(y,x,z))
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].render_levels = 2
    bpy.context.object.modifiers["Subdivision"].levels = 2
    bpy.ops.object.shade_smooth()
