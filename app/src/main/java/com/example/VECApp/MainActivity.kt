package com.example.VECApp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_menu.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_menu)
        supportActionBar?.hide()

        btnClassification.setOnClickListener {
            startActivity(Intent(this,Classification::class.java))
        }

        btnAbout.setOnClickListener {
            startActivity(Intent(this,AboutActivity::class.java))
        }
    }
}