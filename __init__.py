import bpy
bl_info = {
    'name': 'SplitAnim',
    'author': 'sky_haihai <skyhaihai2000@gmail.com>',
    'version': (0, 1),
    'blender': (3, 1, 0),
    'category': 'Animation',
    'location': 'View3D > SideBar[N] > SplitAnim',
    'description': 'An animation tool for splitting animation on a single bone to animation(s) which are evenly applied on multiple bones using contraints',
    'warning': '',
    'doc_url': 'https://github.com/sky-haihai/SplitAnim',
}


def getParentObjectList():
    pbs = bpy.context.selected_pose_bones

    objs = []
    for obj in bpy.data.objects:
        pose = obj.pose
        if pose is not None:
            for bone in pose.bones:  # each bone
                for s in pbs:  # each selected bone
                    if s == bone:
                        objs.append(obj)

    return objs


def isObjectsConsistentFromSecond(objs):
    if objs is None or len(objs) <= 1:
        return False

    second = objs[1]
    for i in range(len(objs)):
        if i == 0:
            continue

        if objs[i] == second:
            continue
        else:
            return False

    return True


class SplitAnimationOperator(bpy.types.Operator):
    """apply the animation split"""
    bl_idname = "pose.split_animation"
    bl_label = "Apply Constraints to Target bones"

    parents = []

    @classmethod
    def poll(cls, context):
        cls.parents = getParentObjectList()
        if cls.parents is None or len(cls.parents) <= 1:
            return False

        if not isObjectsConsistentFromSecond(cls.parents):
            return False

        return context.active_object is not None

    def execute(self, context):
        pbs = bpy.context.selected_pose_bones

        o = self.parents[0]
        t = self.parents[1]

        for i in range(len(pbs)):
            if i == 0:
                continue

            cr = pbs[i].constraints.get("SplitAnim_CR")
            if cr is not None:
                pbs[i].constraints.remove(cr)

            cr = pbs[i].constraints.new('COPY_ROTATION')
            cr.name = "SplitAnim_CR"
            cr.target_space = 'LOCAL'
            cr.owner_space = 'LOCAL'
            if i == 1:
                cr.target = o
                cr.subtarget = pbs[0].name
                cr.influence = 1.0 / (len(pbs)-1)
            else:
                cr.target = t
                cr.subtarget = pbs[1].name
                cr.influence = 1.0

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

    # Condition check
        isTwoArmature = True
        isPoseMode = False
        isBoneEnough = False
        isParentsCorrect = False

        parents = []

        # isTwoArmature
        if len(bpy.context.selected_objects) == 2:
            for obj in bpy.context.selected_objects:
                if obj.pose is None:
                    isTwoArmature = False
        else:
            isTwoArmature = False

        # isPoseMode
        if context.mode == 'POSE':
            isPoseMode = True
        else:
            isPoseMode = False

        # isBoneEnough
        if isPoseMode:
            parents = getParentObjectList()
            if len(parents) > 1:
                isBoneEnough = True
            else:
                isBoneEnough = False
        else:
            isBoneEnough = False

        # isParentsCorrect
        if isPoseMode:
            if isObjectsConsistentFromSecond(parents):
                isParentsCorrect = True
            else:
                isParentsCorrect = False

    # drawing panel

        # draw isTwoArmature label
        row = layout.row()
        if isTwoArmature:
            row.label(text="Select two Armatures", icon='CHECKMARK')
        else:
            row.label(text="Select two Armatures", icon='X')

        # draw isPoseMode label
        row = layout.row()
        if isPoseMode:
            row.label(text="In Pose Mode", icon='CHECKMARK')
        else:
            row.label(text="In Pose Mode", icon='X')

        # draw isBoneEnough label
        if isPoseMode:
            row = layout.row()
            if isBoneEnough:
                row.label(text=str(len(parents)) +
                          " Bone selected", icon='CHECKMARK')
            else:
                row.label(text=str(len(parents)) + " Bone selected", icon='X')

        # draw posemode label
        if isPoseMode:
            row = layout.row()
            if isParentsCorrect:
                row.label(text="Same Armature for all Target bones",
                          icon='CHECKMARK')
            else:
                row.label(text="Same Armature for all Target bones", icon='X')

    # draw props

        # debug selected bones
        if isPoseMode:
            row = layout.row()
            row = layout.row()
            row.label(text="Selected Bones: ")

            spb = bpy.context.selected_pose_bones

            for i in range(len(spb)):
                row = layout.row(align=True)
                if i == 0:
                    row.label(text="Original bone")
                    row.label(text=parents[i].name+" > "+spb[i].name)
                else:
                    row.label(text="Target bone "+str(i))
                    row.label(text=parents[i].name+" > "+spb[i].name)

            row = layout.row()
            row.operator('pose.split_animation')


classes = (SplitAnimationOperator, SplitAnimationPanel)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
