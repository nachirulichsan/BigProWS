package com.example.VECApp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class AboutActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)
        val actionbar = supportActionBar
        actionbar!!.title = "Tentang Aplikasi"
        actionbar.setDisplayHomeAsUpEnabled(true)

    }
    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}