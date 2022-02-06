"""Template for a new Godot project file."""
project_file = """
; Engine configuration file.
; It's best edited using the editor UI and not directly,
; since the parameters that go here are not all obvious.
;
; Format:
;   [section] ; section goes between []
;   param=value ; assign values to parameters

config_version=5

[application]

config/name="{name}"
config/icon="res://icon.png"
config/features=PackedStringArray("4.0", "Vulkan Clustered")
"""
