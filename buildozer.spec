[app]

# (str) Title of your application
title = Kitchen App

# (str) Package name
package.name = kitchenapp

# (str) Package domain
package.domain = org.kaden

# (str) Source code location
source.dir = .

# (list) Source files to include
source.include_exts = py,kv,png,jpg,kv,db,json

# (str) Application version
version = 1.0.0

# (list) Application requirements

requirements = python3,kivy==2.3.1,requests,pillow,certifi,urllib3,idna,charset-normalizer,pygments,docutils,filetype,kivy_garden

# (str) Orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Android API levels
android.api = 33
android.minapi = 21

# (bool) Use AndroidX
android.enable_androidx = True

# (str) Architecture
android.archs = arm64-v8a, armeabi-v7a

# (bool) Log level
log_level = 2

# (bool) Show logs in terminal
log_enable = 1


#
# Python / Build settings
#

# (str) App entry point
entrypoint = main.py

# (bool) Copy site-packages
copy_libs = 0

# (bool) Warn on missing requirements
warn_on_root = 1


#
# Android packaging behavior
#

# (str) Android SDK / NDK
android.sdk = 33
android.ndk = 25b

# (bool) Preserve python optimizations
android.p4a_whitelist = libpython3.10.so


#
# (list) Exclude unwanted files
#
exclude_patterns = tests/*, *.pyc, __pycache__/*


#
# (bool) Enable debug build
#
android.debug = True