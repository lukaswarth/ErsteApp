[app]

title = Monbachtal Kasino
package.name = kasino
package.domain = gsog.kasino

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3

version = 0.1
requirements = python3,kivy,sqlite3,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = master

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
