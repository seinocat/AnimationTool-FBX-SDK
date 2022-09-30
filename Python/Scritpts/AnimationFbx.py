from FBXClass import *

def doAnimOptimize(fbxFile:FBX_Class):

    rAnimStack:FbxAnimStack = fbxFile.scene.GetCurrentAnimationStack()
    print(rAnimStack.GetName())
    Docu:FbxDocument = rAnimStack.GetDocument()
    Docu.RemoveAnimStack(rAnimStack.GetName())

    nLayerCount = rAnimStack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))

    for i in range(nLayerCount):
        rAnimLayer = rAnimStack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), i)
        animCurveNodeCount = rAnimLayer.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimCurveNode.ClassId))
        print(animCurveNodeCount)


        for j in range(animCurveNodeCount):
            animCurveNode = rAnimLayer.GetSrcObject(FbxCriteria.ObjectType(FbxAnimCurveNode.ClassId), j)
            douc:FbxDocument = animCurveNode.GetDocument()
            # print(douc.RemoveAnimStack())
            # print(animCurveNode.GetSrcObjectCount(FbxCriteria.ObjectType())

        # 遍历所有节点，修改曲线
        for k in range(fbxFile.scene.GetNodeCount()):
            rNode:FbxNode = fbxFile.scene.GetNode(k)

            for type in range(3):
                curveX = GetCurve(rNode, rAnimLayer, type, "X")
                curveY = GetCurve(rNode, rAnimLayer, type, "Y")
                curveZ = GetCurve(rNode, rAnimLayer, type, "Z")
                if curveX is not None:
                    # print(rNode.GetName(), "X", curveX.KeyGetValue(0))
                    SetCurve(curveX)
                if curveY is not None:
                    # print(rNode.GetName(), "Y", curveY.KeyGetValue(0))
                    SetCurve(curveY)
                if curveZ is not None:
                    # print(rNode.GetName(), "Z", curveZ.KeyGetValue(0))
                    SetCurve(curveZ)

    fbxFile.save()


def GetCurve(node, animaLayer, type, channel):
    TempFbxAnimCurveNode = None
    if type == 0:
        TempFbxAnimCurveNode = node.LclTranslation
    if type == 1:
        TempFbxAnimCurveNode = node.LclRotation
    if type == 2:
        TempFbxAnimCurveNode = node.LclScaling

    rAnimCurve: FbxAnimCurve = TempFbxAnimCurveNode.GetCurve(animaLayer, channel)



    return rAnimCurve


def SetCurve(curve:FbxAnimCurve):
    for i in range(curve.KeyGetCount()):
        curve.KeyModifyBegin()
        keyValue = curve.KeyGetValue(i)
        newValue = round(keyValue, 3)
        if abs(newValue) == 0:
            newValue = 0
        curve.KeySetValue(i, newValue)
        curve.KeyModifyEnd()
    return 0

def DelScaleCurve(node:FbxNode):

    node.LclScaling

    return 0

