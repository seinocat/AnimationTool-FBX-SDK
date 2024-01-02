using System;
using UnityEditor;
using UnityEngine;

/// <summary>
/// 优化Animation精度和删除scale
/// 脚本添加之前导入的Animation和Fbx需要重新导入
/// </summary>
public class AnimationOptimize : AssetPostprocessor
{
    private void OnPostprocessAnimation(GameObject root, AnimationClip clip)
    {
        var bindings = AnimationUtility.GetCurveBindings(clip);
        bool delete = true;
        foreach (var binding in bindings)
        {
            var curve = AnimationUtility.GetEditorCurve(clip, binding);
            Keyframe[] keyframes = curve.keys;
            
            //保留三位小数点
            for (int i = 0; i < keyframes.Length; i++)
            {
                keyframes[i].value = (int)(keyframes[i].value * 1000) / 1000f;
            }
            curve.keys = keyframes;
            AnimationUtility.SetEditorCurve(clip, binding, curve);
            
            //第一次遍历检查一下scale是否在使用
            var name = binding.propertyName.ToLower();
            if (name.Contains("scale"))
            {
                foreach (var keyframe in keyframes)
                {
                    if (Math.Abs(keyframe.value - 1.0) > 0.001)
                        delete = false;
                }
            }
        }

        //根据检查结果判断是否执行删除操作
        if (delete)
        {
            foreach (var binding in bindings)
            {
                var name = binding.propertyName.ToLower();
                if (name.Contains("scale"))
                {
                    AnimationUtility.SetEditorCurve(clip, binding, null);
                }
            }
        }
        
    }
}