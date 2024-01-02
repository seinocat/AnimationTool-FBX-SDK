using UnityEditor;
using UnityEngine;

public class AnimationOptimize : AssetPostprocessor
{
    private void OnPostprocessAnimation(GameObject root, AnimationClip clip)
    {
        var bindings = AnimationUtility.GetCurveBindings(clip);
        foreach (var binding in bindings)
        {
            var curve = AnimationUtility.GetEditorCurve(clip, binding);
            Keyframe[] keyframes = curve.keys;
            for (int i = 0; i < keyframes.Length; i++)
            {
                keyframes[i].value = (int)(keyframes[i].value * 1000) / 1000f;
            }
            curve.keys = keyframes;
            AnimationUtility.SetEditorCurve(clip, binding, curve);
                
            var name = binding.propertyName.ToLower();
            if (name.Contains("scale"))
            {
                AnimationUtility.SetEditorCurve(clip, binding, null);
            }
        }
    }
}