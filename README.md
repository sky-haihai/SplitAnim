# SplitAnim
## Supported Blender Version  
Only tested on 3.1.0  
## What it does
Split the rotation on a original bone evenly to target bones using constraints
## Why useful
Most humanoid retargeting tool consider leg as thigh > shin > foot.  
  
However when thicc thighs are involved(if you know what I'm talking about), you propbably want something like thigh > knee > shin > foot or even thigh > knee > knee.001 > shin > foot.  
  
In that case, you can use this addon to setup a connection between your custom armature(thigh > knee > shin > foot) and your intermidiate armature(thigh > shin > foot), so that a standard humanoid animation will be "converted" from a standard armature(your intermidiate armature) to your custom armature.
## How to use  
Note: in v0.2 armatures no longer have to be chose manually  
[![Tutorial](https://img.youtube.com/vi/58BqEQTv2ZY/0.jpg)](https://www.youtube.com/watch?v=58BqEQTv2ZY)  
