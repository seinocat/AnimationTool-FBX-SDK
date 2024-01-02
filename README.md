# AnimationTool-Python-FBX-SDK
动画文件(.Fbx)压缩工具，Animation, FBX-Python-SDK, Python3.7

#### 1.Unity C#
Unity资源导入后处理，无法直接读写FBX文件，后处理脚本添加之前的FBX或Animation文件需要重新导入才能生效

#### 2.Python
使用FBX-Python-SDK，直接对FBX文件读写(因此会污染源FBX文件)，但scale曲线无法删除，只能对关键帧精度进行缩减