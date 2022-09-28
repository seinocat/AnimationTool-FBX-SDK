from decimal import Decimal
from FBXClass import *


def doAnimOptimize(fbxFile:FBX_Class):

    rAnimStack:FbxAnimStack = fbxFile.scene.GetCurrentAnimationStack()
    nLayerCount = rAnimStack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))

    for j in range(nLayerCount):
        rAnimLayer = rAnimStack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), j)

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
    FbxAnimCurveNode = None
    if type == 0:
        FbxAnimCurveNode = node.LclTranslation
    if type == 1:
        FbxAnimCurveNode = node.LclRotation
    if type == 2:
        FbxAnimCurveNode = node.LclScaling

    rAnimCurve: FbxAnimCurve = FbxAnimCurveNode.GetCurve(animaLayer, channel)
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
        print(curve.KeyGetValue(i))
    return 0

