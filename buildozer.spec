[app]
# (str) Title of your application
title = Monbachtal Kasino

# (str) Package name
package.name = monbachtal_kasino

# (str) Package domain (unique reverse domain name style)
package.domain = org.example

# (str) Source code where the main.py file is located
source.dir = .

# (str) Application version
version = 1.0

# (str) Application icon (must be a 48x48 PNG file)
icon.filename = icon.png

# (list) Permissions required for your application
# For example: android.permissions = INTERNET,ACCESS_FINE_LOCATION
android.permissions = INTERNET

# (list) Add any Java/Android permissions you want to include
#android.permissions = 

# (str) Supported orientation (one of: landscape, portrait, sensor)
orientation = portrait

# (str) Path to the Python file that will be executed
entrypoint = main.py

# (list) Application requirements
requirements = python3, kivy

# (bool) Enable fullscreen mode (default is 1)
fullscreen = 1

# (str) Android architecture(s) to support (comma-separated). Defaults to armeabi-v7a.
android.archs = arm64-v8a, armeabi-v7a

# (bool) Include debug symbols in the APK (default is 0)
android.debug_symbols = 0

# (str) Android package format (apk, aab or both). Default is apk.
android.package_format = apk

# (str) presplash image file (PNG only)
# presplash.filename = 

# (str) Presplash background color (for example: #FFFFFF)
# presplash.color =

# (bool) Copy the `.spec` file to the project directory. (default is 0)
copy_to_dir = 0

# (bool) Sign the package using your keystore (recommended, set to 1).
android.release_sign = 1

# (str) Path to your keystore file (required if signing is enabled)
# android.keystore = path/to/keystore.jks

# (str) Keystore password
# android.keystore_password = password

# (str) Key alias
# android.keyalias = alias

# (str) Key password
# android.keyalias_password = password
