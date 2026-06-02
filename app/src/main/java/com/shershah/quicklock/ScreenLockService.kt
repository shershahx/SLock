package com.shershah.quicklock

import android.accessibilityservice.AccessibilityService
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Build
import android.view.accessibility.AccessibilityEvent
import androidx.core.app.NotificationCompat

class ScreenLockService : AccessibilityService() {

    companion object {
        private const val CHANNEL_ID = "quicklock_channel"
        private const val NOTIFICATION_ID = 1
        const val ACTION_LOCK = "com.shershah.quicklock.ACTION_LOCK"
    }

    /**
     * BroadcastReceiver that listens for the ACTION_LOCK intent
     * (fired when the user taps the persistent notification)
     * and triggers performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN).
     */
    private val lockReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == ACTION_LOCK) {
                performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN)
            }
        }
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        createNotificationChannel()
        postPersistentNotification()
        registerLockReceiver()
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // No-op: this service does not monitor or process accessibility events.
        // It exists solely to provide the GLOBAL_ACTION_LOCK_SCREEN capability.
    }

    override fun onInterrupt() {
        // No-op: nothing to interrupt.
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            unregisterReceiver(lockReceiver)
        } catch (_: IllegalArgumentException) {
            // Receiver was not registered; safe to ignore.
        }
    }

    /**
     * Creates the notification channel required for Android O+ (API 26+).
     */
    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID,
            getString(R.string.notification_channel_name),
            NotificationManager.IMPORTANCE_LOW // Low: no sound, shows in shade
        ).apply {
            description = getString(R.string.notification_channel_description)
            setShowBadge(false)
        }

        val manager = getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(channel)
    }

    /**
     * Posts an ongoing (persistent) notification. Tapping it sends a broadcast
     * with ACTION_LOCK, which the lockReceiver picks up to lock the screen.
     */
    private fun postPersistentNotification() {
        val lockIntent = Intent(ACTION_LOCK).apply {
            setPackage(packageName)
        }

        val pendingIntent = PendingIntent.getBroadcast(
            this,
            0,
            lockIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(getString(R.string.notification_title))
            .setContentText(getString(R.string.notification_text))
            .setSmallIcon(android.R.drawable.ic_lock_lock)
            .setOngoing(true)           // Cannot be swiped away
            .setAutoCancel(false)       // Stays after tap
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .build()

        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, notification)
    }

    /**
     * Registers the BroadcastReceiver to listen for the lock action.
     * Uses RECEIVER_NOT_EXPORTED on Android 13+ (API 33+) for security.
     */
    private fun registerLockReceiver() {
        val filter = IntentFilter(ACTION_LOCK)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(lockReceiver, filter, RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(lockReceiver, filter)
        }
    }
}
