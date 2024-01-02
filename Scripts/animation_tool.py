from fbxclass import *

def animation_optimize(fbxFile:FbxClass):
    anima_stack:FbxAnimStack = fbxFile.scene.GetCurrentAnimationStack()
    if anima_stack == None:
        print("Fbx file is None!")
        return

    print(anima_stack.GetName())
    doc:FbxDocument = anima_stack.GetDocument()
    doc.RemoveAnimStack(anima_stack.GetName())

    layer_count = anima_stack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))

    for i in range(layer_count):
        anim_layer = anima_stack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), i)
        anim_curve_count = anim_layer.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimCurveNode.ClassId))
        print(anim_curve_count)

        # 遍历所有节点，修改曲线
        for k in range(fbxFile.scene.GetNodeCount()):
            node:FbxNode = fbxFile.scene.GetNode(k)

            for node_type in range(3):
                curve_x = get_curve(node, anim_layer, node_type, "X")
                curve_y = get_curve(node, anim_layer, node_type, "Y")
                curve_z = get_curve(node, anim_layer, node_type, "Z")
                if curve_x is not None:
                    set_curve(curve_x)
                if curve_y is not None:
                    set_curve(curve_y)
                if curve_z is not None:
                    set_curve(curve_z)

    fbxFile.save()


def get_curve(node, animaLayer, node_type, channel):
    curve = None
    if node_type == 0:
        curve = node.LclTranslation
    if node_type == 1:
        curve = node.LclRotation
    if node_type == 2:
        curve = node.LclScaling

    anim_curve: FbxAnimCurve = curve.GetCurve(animaLayer, channel)



    return anim_curve


def set_curve(curve:FbxAnimCurve):
    for i in range(curve.KeyGetCount()):
        curve.KeyModifyBegin()
        keyValue = curve.KeyGetValue(i)
        newValue = round(keyValue, 3)
        if abs(newValue) == 0:
            newValue = 0
        curve.KeySetValue(i, newValue)
        curve.KeyModifyEnd()
    return 0

def del_scale_curve(node:FbxNode):

    node.LclScaling

    return 0

