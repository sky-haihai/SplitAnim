bl_info = {
    'name' : 'SplitAnim',
    'author' : 'sky_haihai <skyhaihai2000@gmail.com>',
    'version' : (0,1),
    'blender' : (3, 1, 0),
    'category' : 'Animation',
    'location' : 'View3D > SideBar[N] > SplitAnim',
    'description' : 'An animation tool for splitting animation on a single bone to animation(s) which are evenly applied on multiple bones using contraints',
    'warning' : '',
    'doc_url' : '',
}

import bpy

class SplitAnimationProps(bpy.types.PropertyGroup):
    originArmature: bpy.props.PointerProperty(name="origin armature",type=bpy.types.Object)
    targetArmature: bpy.props.PointerProperty(name="target armature",type=bpy.types.Object)
#    selectedBoneNames: bpy.props.StringProperty(name="selected bones",default="no bone selected")
#    originBone: bpy.props.PointerProperty(name = "original bone", type = bpy.types.Object)
    #: bpy.props.BoolProperty(name = "Use Active")
    
class SplitAnimationOperator(bpy.types.Operator):
    """apply the animation split"""
    bl_idname = "pose.split_animation"
    bl_label = "Split Animation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        props=context.scene.SA_Props
        pbs=bpy.context.selected_pose_bones
        
        for i in range(len(pbs)):
            if i==0:continue
        
            cr=pbs[i].constraints.new('COPY_ROTATION')
            cr.target_space='LOCAL'
            cr.owner_space='LOCAL'
            if i==1:
                cr.target=props.originArmature
                cr.subtarget=pbs[0].name
                cr.influence=1.0 / (len(pbs)-1)
            else:
                cr.target=props.targetArmature
                cr.subtarget=pbs[1].name
                cr.influence=1.0
        
        return {'FINISHED'}

class SplitAnimationPanel(bpy.types.Panel):
    """Split animation on single bone to multiple bones"""
    bl_label = "Split Animation Tool"
    bl_idname = "Split_Animation_Panel"
    bl_space_type = 'VIEW_3D'
    bl_category = 'SplitAnim'
    bl_region_type = "UI" 

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        obj = context.active_object
        
        row=layout.row()
        row.prop(scene.SA_Props,"originArmature")
        row=layout.row()
        row.prop(scene.SA_Props,"targetArmature")
        
        #make sure in pose mode
        row = layout.row()
        if context.mode=='POSE':
            row.label(text="In Pose Mode",icon='CHECKMARK')
            
            row=layout.row()
            row.label(text="Selected Bones: ")
            
            pbs=bpy.context.selected_pose_bones
            for i in range(len(pbs)):
                row=layout.row()
                if i==0:
                    row.label(text="Original bone: "+pbs[i].name)
                else:
                    row.label(text="Target bone "+str(i)+": "+pbs[i].name)
            
            row=layout.row()
            row.operator('pose.split_animation')
        else:
            row.label(text="Switch to Pose Mode!",icon='X')
            row=layout.row()
            row.operator('object.posemode_toggle')

classes = (SplitAnimationProps,SplitAnimationOperator,SplitAnimationPanel)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.SA_Props = bpy.props.PointerProperty(type=SplitAnimationProps)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.SA_Props
        
if __name__ == "__main__":
    register()