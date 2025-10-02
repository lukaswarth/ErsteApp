[app]
android.build_tools_version = 30.0.3
title = Monbachtal Kasino
package.name = kasino
package.domain = gsog.kasino

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,db
source.include_patterns = Audios/*,Bilder/*

version = 0.1
requirements = python3,kivy

#icon.filename = %(source.dir)s/Bilder/icon.png
#presplash.filename = %(source.dir)s/Bilder/icon.png

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = release-2022.12.20

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
