from fbxclass import *

channels = {"X", "Y", "Z"}

def optimize_animation(fbxFile:FbxClass):
    anima_stack:FbxAnimStack = fbxFile.scene.GetCurrentAnimationStack()
    if anima_stack == None:
        print("Fbx file is None!")
        return

    layer_count = anima_stack.GetMemberCount()

    for i in range(layer_count):
        anim_layer:FbxAnimLayer = anima_stack.GetMember(i)
        anim_curve_count = anim_layer.GetMemberCount(FbxCriteria.ObjectType(FbxAnimCurveNode.ClassId))
        print("fbxFile:" + fbxFile.filename + ",curve:" + str(anim_curve_count))

        # 遍历所有节点，修改曲线
        node_count = fbxFile.scene.GetNodeCount()
        for j in range(node_count):
            node:FbxNode = fbxFile.scene.GetNode(j)

            if node is None:
                continue

            #先进行精度优化
            for lcl_type in range(3):
                for channel in channels:
                    curve = get_curve(node, anim_layer, lcl_type, channel)
                    if curve is not None:
                        set_curve(curve)
            #检查scale曲线
            del_scale_curve(node, anim_layer)

    fbxFile.save()


def get_curve(node, anima_layer, lcl_type, channel):
    curve = None
    if lcl_type == 0:
        curve = node.LclTranslation.GetCurve(anima_layer, channel)
    if lcl_type == 1:
        curve = node.LclRotation.GetCurve(anima_layer, channel)
    if lcl_type == 2:
        curve = node.LclScaling.GetCurve(anima_layer, channel)
    return curve

#精度优化
def set_curve(curve:FbxAnimCurve):
    key_count = curve.KeyGetCount()
    for i in range(key_count):
        curve.KeyModifyBegin()
        curve.KeySetValue(i, round(curve.KeyGetValue(i), 1))
        curve.KeyModifyEnd()

#删除scale曲线
def del_scale_curve(node:FbxNode, anim_layer):
    scale_curve = node.LclScaling

    for channel in channels:
        anim_curve: FbxAnimCurve = scale_curve.GetCurve(anim_layer, channel)
        if anim_curve is None:
            continue
        key_count = anim_curve.KeyGetCount()
        # # 检查一下scale所有通道，没有用到才删除
        # for i in range(key_count):
        #     keyValue = anim_curve.KeyGetValue(i)
        #     if keyValue != 1:
        #         return

    anim_layer.DisconnectSrcProperty(node.LclScaling)

