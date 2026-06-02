# QuickLock

QuickLock is a simple, lightweight Android application that allows you to instantly lock your phone screen by tapping a persistent notification. 

It is designed to be minimal and secure, specifically catering to devices like Huawei/EMUI by offering direct battery optimization instructions to prevent the background service from being killed.

## Features
- **One-Tap Screen Lock**: A persistent notification stays in your notification shade, allowing you to lock the screen instantly with one tap.
- **Accessibility Service-based**: Uses Android's built-in Accessibility Service `GLOBAL_ACTION_LOCK_SCREEN` capability.
- **Privacy-First**: The app explicitly sets `canRetrieveWindowContent="false"` and does not monitor any of your screen content or personal data.
- **No Malicious Permissions**: Does not request the `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` permission, which is often flagged by heuristic malware scanners for sideloaded accessibility apps.
- **Adaptive Icons**: Fully supports modern Android adaptive icons.

## Requirements
- Android 10 (API Level 29) or higher.

## Setup Instructions

Once installed, you need to configure two main things for QuickLock to work reliably:

1. **Enable Accessibility Service:**
   - Open the app and tap **Open Accessibility Settings**.
   - Find **QuickLock** in the list of installed services and enable it.
   - You will see a persistent notification appear in your notification shade.

2. **Disable Battery Optimization (especially for Huawei / EMUI devices):**
   - Background services are often aggressively killed by battery managers.
   - Tap **Open Battery Optimization Settings** in the app.
   - Find QuickLock and set it to **Don't optimize** (or Allow).
   - *For EMUI:* Go to Settings → Battery → App launch. Toggle OFF "Manage automatically" for QuickLock and ensure "Run in background" and "Auto-launch" are enabled.

## Build Instructions

To build this project locally, you will need Android Studio and the Android SDK (API 34).

1. Clone or download the repository.
2. Open the project in Android Studio.
3. Build the APK using Gradle:
   ```bash
   # Debug build
   ./gradlew assembleDebug

   # Release build
   ./gradlew assembleRelease
   ```

To generate the launcher icons from `app_logo.png`, this project includes a Python script `generate_icons.py`. Run it with:
```bash
python generate_icons.py
```
*(Requires Python 3 and the Pillow library).*

## License
[MIT License](LICENSE)
