bl_info = {
    "name": "Add_Face_Copy_Addon",
    "author": "Noizirom",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Add > Mesh > Face Copy Object",
    "description": "Adds a New Object from Selected Faces",
    "warning": "",
    "wiki_url": "https://github.com/Noizirom/Add_Face_Copy_Addon",
    "category": "Add Mesh",
    }


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import numpy as np
from copy import deepcopy as dc



def get_sel():
    vt = bpy.context.object.data.vertices
    ed = bpy.context.object.data.edges
    fa = bpy.context.object.data.polygons
    bpy.ops.object.mode_set(mode='OBJECT')
    countv = len(vt)
    selv = np.empty(countv, dtype=np.bool)
    vt.foreach_get('select', selv)
    co = np.empty(countv * 3, dtype=np.float32)
    vt.foreach_get('co', co)
    co.shape = (countv, 3)
    vidx = np.empty(countv, dtype=np.int32)
    vt.foreach_get('index', vidx)
    countf = len(fa)
    selfa = np.empty(countf, dtype=np.bool)
    fa.foreach_get('select', selfa)
    fidx = np.empty(countf, dtype=np.int32)
    fa.foreach_get('index', fidx)
    fac = np.array([i.vertices[:] for i in fa])
    v_count = len(vidx[selv])
    f_count = len(fidx[selfa])
    new_idx = [i for i in range(v_count)]
    nv_Dict = {o: n for n, o in enumerate(vidx[selv].tolist())}
    new_f = [[nv_Dict[i] for i in nest] for nest in fac[selfa]]
    return [co[selv], new_f]

def obj_mesh(co, faces):
    cur = bpy.context.object
    mesh = bpy.data.meshes.new("Obj")
    mesh.from_pydata(co, [], faces)
    mesh.validate()
    mesh.update(calc_edges = True)
    Object = bpy.data.objects.new("Obj", mesh)
    Object.data = mesh
    bpy.context.scene.objects.link(Object)
    bpy.context.scene.objects.active = Object#
    cur.select = False
    Object.select = True

def obj_new(Name, co, faces):
    obj_mesh(co, faces)
    bpy.data.objects["Obj"].name = Name
    bpy.data.meshes[bpy.data.objects[Name].data.name].name = Name

def add_object(self, context):
    gs = get_sel()
    obj_new(self.name, gs[0], gs[1])


class OBJECT_OT_add_face_copy(Operator, AddObjectHelper):
    """Create a new Object from selected faces"""
    bl_idname = "mesh.add_face_copy"
    bl_label = "Add Face Copy"
    bl_options = {'REGISTER', 'UNDO'}

    name = StringProperty(
            name="name",
            default="Object",
            description="Object_name",
            )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration

def add_face_copy_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_face_copy.bl_idname,
        text="Add Face Copy",
        icon='PLUGIN')

def draw(self, context):
    col = self.layout.column(align = True)
    col.prop(context.scene, "name")


# This allows you to right click on a button and link to the manual
def add_face_copy_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "editors/3dview/object"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_face_copy)
    bpy.utils.register_manual_map(add_face_copy_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_face_copy_button)
    


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_face_copy)
    bpy.utils.unregister_manual_map(add_face_copy_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_face_copy_button)


if __name__ == "__main__":
    register()
