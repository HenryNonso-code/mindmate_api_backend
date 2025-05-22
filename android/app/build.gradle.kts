android {
    namespace = "com.nonsoapps.mindmate_app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.nonsoapps.mindmate_app"
        minSdk = 21
        targetSdk = 34
        versionCode = 2
        versionName = "1.0.1"
    }

    signingConfigs {
        create("release") {
            storeFile = file("mindmate-key.jks")
            storePassword = "Jmindmate2025"
            keyAlias = "mindmate"
            keyPassword = "Jmindmate2025"
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = false
            isShrinkResources = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = "11"
    }
}
