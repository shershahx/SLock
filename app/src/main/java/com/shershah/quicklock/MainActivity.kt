package com.shershah.quicklock

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.AccessibilityServiceInfo
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.view.accessibility.AccessibilityManager
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import android.widget.TextView

class MainActivity : AppCompatActivity() {

    private lateinit var tvServiceStatus: TextView
    private lateinit var btnAccessibilitySettings: MaterialButton
    private lateinit var btnBatterySettings: MaterialButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvServiceStatus = findViewById(R.id.tvServiceStatus)
        btnAccessibilitySettings = findViewById(R.id.btnAccessibilitySettings)
        btnBatterySettings = findViewById(R.id.btnBatterySettings)

        btnAccessibilitySettings.setOnClickListener {
            val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
        }

        btnBatterySettings.setOnClickListener {
            val intent = Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
        }
    }

    override fun onResume() {
        super.onResume()
        updateServiceStatus()
    }

    /**
     * Checks whether the ScreenLockService is currently enabled in Accessibility settings.
     * Updates the status TextView accordingly.
     */
    private fun updateServiceStatus() {
        val isActive = isAccessibilityServiceEnabled()
        if (isActive) {
            tvServiceStatus.text = getString(R.string.status_service_active)
            tvServiceStatus.setTextColor(getColor(android.R.color.holo_green_dark))
            tvServiceStatus.setBackgroundResource(R.drawable.bg_status_card_active)
        } else {
            tvServiceStatus.text = getString(R.string.status_service_inactive)
            tvServiceStatus.setTextColor(getColor(android.R.color.holo_red_dark))
            tvServiceStatus.setBackgroundResource(R.drawable.bg_status_card)
        }
    }

    /**
     * Queries the AccessibilityManager to determine if our ScreenLockService
     * is among the enabled accessibility services.
     */
    private fun isAccessibilityServiceEnabled(): Boolean {
        val am = getSystemService(ACCESSIBILITY_SERVICE) as AccessibilityManager
        val enabledServices = am.getEnabledAccessibilityServiceList(
            AccessibilityServiceInfo.FEEDBACK_ALL_MASK
        )
        val targetServiceName = "${packageName}/${ScreenLockService::class.java.canonicalName}"
        return enabledServices.any { serviceInfo ->
            serviceInfo.resolveInfo.serviceInfo.let { si ->
                "${si.packageName}/${si.name}" == targetServiceName
            }
        }
    }
}
