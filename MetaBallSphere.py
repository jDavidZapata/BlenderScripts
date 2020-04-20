# Meta Balls
import bpy
from math import pi, sin, cos, ceil
from mathutils import Vector, Quaternion
import colorsys
from random import TWOPI

#select all the objects in the scene 
bpy.ops.object.select_all(action='SELECT')

# Delete all the objects in the scene
bpy.ops.object.delete(use_global=False)


def vecrotate(angle, axis, vin, vout):
    # Assume axis is a unit vector.
    # Find squares of each axis component.
    xsq = axis.x * axis.x
    ysq = axis.y * axis.y
    zsq = axis.z * axis.z

    cosa = cos(angle)
    sina = sin(angle)

    complcos = 1.0 - cosa
    complxy = complcos * axis.x * axis.y
    complxz = complcos * axis.x * axis.z
    complyz = complcos * axis.y * axis.z

    sinx = sina * axis.x
    siny = sina * axis.y
    sinz = sina * axis.z

    # Construct the x-axis (i).
    ix = complcos * xsq + cosa
    iy = complxy + sinz
    iz = complxz - siny

    # Construct the y-axis (j).
    jx = complxy - sinz
    jy = complcos * ysq + cosa
    jz = complyz + sinx

    # Construct the z-axis (k).
    kx = complxz + siny
    ky = complyz - sinx
    kz = complcos * zsq + cosa

    vout.x = ix * vin.x + jx * vin.y + kx * vin.z
    vout.y = iy * vin.x + jy * vin.y + ky * vin.z
    vout.z = iz * vin.x + jz * vin.y + kz * vin.z
    return vout


def vecrotatex(angle, vin, vout):
    cosa = cos(angle)
    sina = sin(angle)
    vout.x = vin.x
    vout.y = cosa * vin.y - sina * vin.z
    vout.z = cosa * vin.z + sina * vin.y
    return vout


# Variables from still sphere.
diameter = 4.0
sz = 2.125 / diameter
latitude = 16
longitude = latitude * 2
invlatitude = 1.0 / (latitude - 1)
invlongitude = 1.0 / (longitude - 1)
iprc = 0.0
jprc = 0.0
phi = 0.0
theta = 0.0
alph = 1.0

# Animation variables.
currframe = 0
fcount = 10
invfcount = 1.0 / (fcount - 1)
frange = bpy.context.scene.frame_end - bpy.context.scene.frame_start
if frange == 0:
    bpy.context.scene.frame_end = 150
    bpy.context.scene.frame_start = 0
    frange = 150
fincr = ceil(frange * invfcount)

# Animate center of the sphere.
center = Vector((0.0, -4.0, 0.0))
startcenter = Vector((0.0, -4.0, 0.0))
stopcenter = Vector((0.0, 4.0, 0.0))

# Rotate cubes around the surface of the sphere.
pt = Vector((0.0, 0.0, 0.0))
rotpt = Vector((0.0, 0.0, 0.0))

# Change the axis of rotation for the point.
baseaxis = Vector((0.0, 1.0, 0.0))
axis = Vector((0.0, 0.0, 0.0))

# Slerp between two rotations for each cube.
startrot = Quaternion((0.0, 1.0, 0.0), pi)
stoprot = Quaternion((1.0, 0.0, 0.0), pi * 1.5)
currot = Quaternion()

# ...
elemtypes = ['BALL', 'CAPSULE', 'PLANE', 'ELLIPSOID', 'CUBE']

# Create metaball data, then assign it to a metaball object.
mbdata = bpy.data.metaballs.new('SphereData')
mbdata.render_resolution = 0.075
mbdata.resolution = 0.2
mbobj = bpy.data.objects.new("Sphere", mbdata)
bpy.context.collection.objects.link(mbobj)
# Add a material to the metaball.
mat = bpy.data.materials.new(name='SphereMaterial')
mat.diffuse_color = (1.0, 0.214041, 0.214041, alph)
mbobj.data.materials.append(mat)

for i in range(0, latitude, 1):
    # ...
    iprc = i * invlatitude
    phi = pi * (i + 1) * invlatitude
    
    sinphi = sin(phi)
    cosphi = cos(phi)

    rad = 0.01 + sz * abs(sinphi) * 0.99
    pt.z = cosphi * diameter
    
    for j in range(0, longitude, 1):
        # ...
        jprc = j * invlongitude
        theta = TWOPI * j / longitude

        sintheta = sin(theta)
        costheta = cos(theta)

        pt.y = center.y + sinphi * sintheta * diameter
        pt.x = center.x + sinphi * costheta * diameter
        
        # Add a metaelement to the metaball.
        # See elemtypes array above for possible shapes.
        mbelm = mbdata.elements.new(type=elemtypes[3])
        mbelm.co = pt
        mbelm.radius = 0.15 + sz * abs(sinphi) * 1.85
        # Stiffness of blob, in a range of 1 .. 10.
        mbelm.stiffness = 1.0
        
        current = bpy.context.object
        
        vecrotatex(theta, baseaxis, axis)
        currframe = bpy.context.scene.frame_start
        currot = startrot
        center = startcenter

        # Set some metaelements to have a repulsive, rather than attractive force.
        if i % 7 == j % 3:
            mbelm.use_negative = True

        for f in range(0, fcount, 1):
            # ...
            fprc = f * invfcount
            osc = abs(sin(TWOPI * fprc))
            bpy.context.scene.frame_set(currframe)
            

            # Update location.
            vecrotate(TWOPI * fprc, axis, pt, rotpt)
            mbelm.co = rotpt
            mbelm.keyframe_insert(data_path='co')

            currframe += fincr
            

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-3.2947700023651123, -51.51686096191406, -0.7010366916656494), rotation=(1.5743393898010254, 0.000106481667899061, -0.08023278415203094))
bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
bpy.context.object.data.color = (0.0, 1.0, 1.0)
bpy.context.object.data.energy = 10
bpy.ops.object.light_add(type='POINT', radius=1, location=(0, -4, 0))
bpy.context.object.data.color = (0.0645496, 0, 1)
bpy.context.object.data.energy = 1000
bpy.context.scene.render.engine = 'CYCLES'
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.132864, 0.132864, 0.132864, 1)
bpy.context.scene.render.film_transparent = True


bpy.context.object.data.color = (0.0645496, 0, 1)
