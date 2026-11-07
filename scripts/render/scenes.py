"""Original FRENUGO models. Run with Blender 4.3+: blender -b -t 6 -P scripts/render/scenes.py
All geometry is generated here. No reference-site assets are used.
"""
import bpy, math, os, sys
from mathutils import Quaternion, Vector
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
OUT=os.path.join(ROOT,'public/visuals'); TMP=os.path.join(ROOT,'.render')
os.makedirs(OUT,exist_ok=True)
def material(name,color,metal=1,rough=.22):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
GOLD=material('Polished warm gold',(.83,.43,.025));PALE=material('Gold highlights',(1,.69,.12));FACE=material('Brushed coin gold',(.78,.39,.018),1,.29);BLACK=material('Phone graphite',(.016,.017,.022),.8,.23);CHROME=material('Phone polished rim',(.28,.29,.31),1,.19)
def finish(obj,mat=GOLD,bevel=0):
 obj.data.materials.append(mat)
 if bevel:
  mod=obj.modifiers.new('Soft machined edges','BEVEL');mod.width=bevel;mod.segments=3
 for p in getattr(obj.data,'polygons',[]):p.use_smooth=True
 if obj.type=='MESH':obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return obj
def loc(x,y,d=0):return (x,-d,y)
def box(name,w,h,depth,x=0,y=0,d=0,mat=GOLD,bevel=.05):
 r=min(bevel,w/2,h/2);points=[]
 for cx,cy,a0 in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(13):
   a=math.radians(a0+i*90/12);points.append((cx+r*math.cos(a),cy+r*math.sin(a)))
 n=len(points);verts=[loc(xx,yy,dd) for dd in [-depth/2,depth/2] for xx,yy in points];faces=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]
 for i in range(n):j=(i+1)%n;faces.append((i,j,j+n,i+n))
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.uv_layers.new(name='UVMap');o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);o.location=loc(x,y,d)
 return finish(o,mat,min(.012,depth/5))

def text(text,size,x=0,y=0,d=.13,font=None,mat=GOLD,extrude=.025,bevel=.012):
 c=bpy.data.curves.new(text,'FONT');c.body=text;c.size=size;c.align_x='CENTER';c.align_y='CENTER';c.extrude=extrude;c.bevel_depth=bevel;c.bevel_resolution=4;c.resolution_u=24
 if font:c.font=bpy.data.fonts.load(font)
 o=bpy.data.objects.new(text,c);bpy.context.collection.objects.link(o);o.rotation_euler=(math.pi/2,0,0);o.location=loc(x,y,d);o.data.materials.append(mat);return o
def group(name,objects):
 e=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(e)
 for o in objects:o.parent=e
 return e
def coin():
    start = set(bpy.data.objects)
    edge = material('Deep gold alloy', (.84, .36, .019), 1, .24)
    rim = material('Polished yellow gold', (1, .59, .055), 1, .16)
    face = material('Satin struck gold', (.94, .48, .029), .98, .33)
    stamp = material('Raised gold hallmark', (1, .58, .047), .97, .23)

    bpy.ops.mesh.primitive_cylinder_add(vertices=160, radius=.94, depth=.19, rotation=(math.pi/2, 0, 0))
    finish(bpy.context.object, edge, .028)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=160, radius=.873, depth=.034,
            location=loc(0, 0, side * .089), rotation=(math.pi/2, 0, 0),
        )
        finish(bpy.context.object, face, .009)

        for radius, width, depth in [(.899, .020, .094), (.839, .006, .107)]:
            bpy.ops.mesh.primitive_torus_add(
                major_radius=radius, minor_radius=width, major_segments=160, minor_segments=12,
                location=loc(0, 0, side * depth), rotation=(math.pi/2, 0, 0),
            )
            finish(bpy.context.object, rim)

        mark = text('F', 1.17, d=side * .114, font=os.path.join(TMP, 'archivo.ttf'), mat=stamp, extrude=.017, bevel=.008)
        if side < 0:
            mark.rotation_euler.z = math.pi

    # Fine ridges cut into the circumference of the coin.
    steps = 112 * 4
    vertices = []
    for depth in [-.056, .056]:
        for i in range(steps):
            angle = i / steps * math.tau
            radius = .949 if i % 4 in (1, 2) else .940
            vertices.append(loc(radius * math.cos(angle), radius * math.sin(angle), depth))
    faces = [(i, (i+1) % steps, (i+1) % steps+steps, i+steps) for i in range(steps)]
    mesh = bpy.data.meshes.new('Reeded gold edge')
    mesh.from_pydata(vertices, [], faces)
    reed = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.collection.objects.link(reed)
    reed.data.materials.append(edge)

    return group('FRENUGO struck gold coin', set(bpy.data.objects)-start)
def area(name,pos,power,size,color=(1,1,1),size_y=None):
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='RECTANGLE' if size_y else 'DISK';o.data.size=size
 if size_y:o.data.size_y=size_y
 o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
def setup(width,height,scale):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=384;s.cycles.use_denoising=False;s.render.resolution_x=width;s.render.resolution_y=height;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True;s.world.color=(.1,.1,.1);s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.35
 area('Large white softbox',(-3,-4,4),400,3,(1,.88,.55));area('Right warm strip',(4,-2,1),700,3,(1,.83,.49),.55);area('Upper edge',(-1,2,4),1400,3,(1,.95,.76),1);area('Front fill',(0,-5,-2),55,3)
 bpy.ops.object.camera_add(location=(0,-10,0));c=bpy.context.object;c.rotation_euler=(Vector((0,0,0))-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=scale;s.camera=c;return s
def render(name):
 s=bpy.context.scene;s.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
def phone(stats=False):
 box('Metal rim',2.34,4.85,.22,mat=CHROME,bevel=.24);box('Black glass',2.29,4.79,.23,d=.04,mat=BLACK,bevel=.23)
 # Authored screen texture, applied to a real glass-fronted 3D phone.
 m=bpy.data.materials.new('Original FRENUGO display');m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(os.path.join(TMP,'phone-'+('stats' if stats else 'welcome')+'.png'));m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);em.inputs['Strength'].default_value=.8;m.node_tree.links.new(em.outputs[0],out.inputs[0])
 # A beveled rectangle keeps the physical screen corners rounded.
 o=box('Screen',2.18,4.61,.025,d=.168,mat=m,bevel=.19)
 # Cube UVs need front mapping rather than six packed faces.
 for polygon in o.data.polygons:
  for i in polygon.loop_indices:
   co=o.data.vertices[o.data.loops[i].vertex_index].co;o.data.uv_layers.active.data[i].uv=(co.x/2.18+.5,co.z/4.61+.5)
 box('Notch',.92,.19,.03,y=2.21,d=.195,mat=BLACK,bevel=.08)
 for yy in [.8,1.35]:box('Side button',.05,.3,.08,x=-1.18,y=yy,mat=CHROME,bevel=.015)
 for o in [x for x in bpy.context.scene.objects if x.type in ['MESH','FONT']]:o.location.z-=.45
def bank(x,y,scale,angle):
 start=set(bpy.data.objects)
 box('Bank lower step',2.2,.15,1.1,y=-1,bevel=.035);box('Bank plinth',2,.2,.9,y=-.83,bevel=.03)
 for xx in [-.66,.66]:
  for dd in [-.28,.28]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.12,depth=1.45,location=loc(xx,0,dd));finish(bpy.context.object,GOLD,.025)
   for yy in [-.71,.71]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.18,depth=.13,location=loc(xx,yy,dd));finish(bpy.context.object,PALE,.025)
 verts=[(-1.1,-.45,.77),(1.1,-.45,.77),(0,-.45,1.36),(-1.1,.45,.77),(1.1,.45,.77),(0,.45,1.36)];faces=[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)];m=bpy.data.meshes.new('Triangular classical roof');m.from_pydata(verts,[],faces);o=bpy.data.objects.new('Pediment',m);bpy.context.collection.objects.link(o);finish(o,GOLD,.045);box('Cornice',2.25,.11,1,y=.76,bevel=.035)
 g=group('Original miniature bank',set(bpy.data.objects)-start);g.scale=(scale,)*3;g.location=loc(x,y,.5);g.rotation_euler=(.12,0,angle)
def card():
 start=set(bpy.data.objects);box('Brushed gold card',3.45,2.1,.07,mat=FACE,bevel=.13);box('Card chip',.43,.34,.025,x=-1.08,y=-.24,d=.07,mat=PALE,bevel=.05);text('F',.5,x=1.12,y=.53,d=.08,font=os.path.join(TMP,'archivo.ttf'),extrude=.005,bevel=.005)
 g=group('FRENUGO gold card',set(bpy.data.objects)-start);g.location.z=-.25;g.rotation_euler=(.12,-.23,-.12);bank(-1.65,1.6,.69,-.3);bank(1.7,-1.65,.65,.32)
def note():
 verts=[];faces=[];nx=70;ny=30
 def wave(x,y):return math.sin(x*2.7)*.18+math.sin(y*1.4+x*2)*.06
 for j in range(ny+1):
  y=-.85+1.7*j/ny
  for i in range(nx+1):
   x=-1.45+2.9*i/nx;verts.append(loc(x,y,wave(x,y)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
 m=bpy.data.meshes.new('Curved banknote');m.from_pydata(verts,[],faces);o=bpy.data.objects.new('Original flowing gold note',m);bpy.context.collection.objects.link(o);finish(o,GOLD);sol=o.modifiers.new('Thin metal thickness','SOLIDIFY');sol.thickness=.022
 def tube(name,pts,r):
  c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=4;s=c.splines.new('POLY');s.points.add(len(pts)-1)
  for p,co in zip(s.points,pts):p.co=(*co,1)
  o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(PALE)
 for yy in [-.77,.77]:tube('Embossed note border',[loc(-1.37+2.74*i/80,yy,wave(-1.37+2.74*i/80,yy)+.028) for i in range(81)],.018)
 tube('Embossed note oval',[loc(.35*math.cos(a),.59*math.sin(a),wave(.35*math.cos(a),.59*math.sin(a))+.025) for a in [i*math.pi*2/100 for i in range(101)]],.025)
 for xx in [-1,1]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.1,location=loc(xx,0,wave(xx,0)+.025));o=bpy.context.object;o.scale.y=.25;finish(o,PALE)
 group('Gold banknote', [o for o in bpy.context.scene.objects if o.type in ['MESH','CURVE']]).rotation_euler=(.1,-.16,-.15)

mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'all'
if mode in ['all', 'coin']:
    s = setup(400, 400, 2.55)
    s.world.use_nodes = True
    background = s.world.node_tree.nodes.get('Background')
    background.inputs['Color'].default_value = (.48, .38, .24, 1)
    background.inputs['Strength'].default_value = .9
    for light in [obj for obj in s.objects if obj.type == 'LIGHT']:
        bpy.data.objects.remove(light, do_unlink=True)
    s.view_settings.exposure = -.35
    area('Main gold softbox', (-2.1, -4, 3), 315, 3.4, (1, .92, .73), 2.3)
    area('Right gold strip', (3.2, -2, 1.5), 420, 3.1, (1, .86, .58), .65)
    area('Upper edge', (-1, 2, 4), 1250, 3, (1, .95, .76), 1)
    area('Low warm strip', (1, -3.5, -2.8), 95, 3, (1, .88, .65), 1.15)
    s.cycles.samples = 24
    s.cycles.use_denoising = False
    s.cycles.sample_clamp_indirect = 2
    s.cycles.max_bounces = 4
    c = coin()
    # Both faces are identical. A half turn loops into the same physical pose.
    tilt = Quaternion((0, 1, 0), -.14) @ Quaternion((1, 0, 0), .10)
    c.rotation_mode = 'QUATERNION'
    frames = 120
    for i in range(frames):
        c.rotation_quaternion = tilt @ Quaternion((0, 0, 1), -.12 + math.pi * i / frames)
        s.render.filepath = os.path.join(TMP, f'coin-turn-{i:03}.png')
        bpy.ops.render.render(write_still=True)
if mode in ['all','static']:
 setup(500,625,6.3);phone();render('phone-welcome')
 setup(500,625,6.3);phone(True);render('phone-stats')
 setup(500,625,6.3);card();render('card')
 setup(420,420,3.65);note();render('banknote')
 setup(1000,400,9.5);o=text('Green',3.1,y=-.15,d=0,font=os.path.join(ROOT,'public/fonts/allura.ttf'),extrude=.1,bevel=.085);o.rotation_euler.x+=.08;render('green')
