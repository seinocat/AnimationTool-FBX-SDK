from fbxclass import *

def optimize_animation(fbxFile:FbxClass):
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
        for j in range(fbxFile.scene.GetNodeCount()):
            node:FbxNode = fbxFile.scene.GetNode(j)

            channels = {"X", "Y", "Z"}
            #先进行精度优化
            for channel in channels:
                curve = get_curve(node, anim_layer, channel)
                if curve is not None:
                    set_curve(channel)

            #检查scale曲线
            del_scale_curve(node, anim_layer)

    fbxFile.save()


def get_curve(node, anima_layer, channel):
    curve = None
    if channel == "X":
        curve = node.LclTranslation
    if channel == "Y":
        curve = node.LclRotation
    if channel == "Z":
        curve = node.LclScaling
    anim_curve: FbxAnimCurve = curve.GetCurve(anima_layer, channel)
    return anim_curve

#精度优化，默认保留三位小数点
def set_curve(curve:FbxAnimCurve, decimal_places: int = 3):
    key_count = curve.KeyGetCount()
    for i in range(key_count):
        curve.KeyModifyBegin()
        keyValue = curve.KeyGetValue(i)
        newValue = round(keyValue, decimal_places)
        if abs(newValue) == 0:
            newValue = 0
        curve.KeySetValue(i, newValue)
        curve.KeyModifyEnd()

#删除scale曲线
def del_scale_curve(node:FbxNode, anim_layer):
    scale_curve = node.LclScaling
    key_count = scale_curve.KeyGetCount()

    #检查一下scale曲线，没有用到才删除
    for i in range(key_count):
        keyValue = scale_curve.KeyGetValue(i)
        if keyValue != 1:
            return

    node.LclScaling.SetCurve(anim_layer, None)

