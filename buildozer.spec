[app]

title = Monbachtal Kasino
package.name = kasino
package.domain = gsog.kasino
icon = icon.png

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3

version = 0.1
requirements = python3,kivy

icon.filename = /path/to/your/icon.png
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.icon = /path/to/your/icon.png
p4a.branch = release-2022.12.20

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
