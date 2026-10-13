package ar.ctmm.turnos;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;

/** Contenedor nativo: muestra la app web (assets/index.html) y guarda los datos en el teléfono. */
@SuppressWarnings({"rawtypes", "unchecked"})
public class MainActivity extends Activity implements ValueCallback {
    private WebView web;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        SharedPreferences prefs = getSharedPreferences("turnos", Context.MODE_PRIVATE);
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#08111F"));
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setTextZoom(100);
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new LinkClient(this));
        web.addJavascriptInterface(new Bridge(this, prefs), "AndroidBridge");
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
    }

    /** Botón atrás: primero cierra hojas/pestañas dentro de la app. */
    @Override
    public void onBackPressed() {
        web.evaluateJavascript("(window.onAndroidBack&&window.onAndroidBack())?'1':'0'", this);
    }

    @Override
    public void onReceiveValue(Object v) {
        // Sin genéricos a propósito: evita el método puente que el d8 de build-tools 34 no procesa con JDK 21.
        if (!"\"1\"".equals(v)) finish();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onPause() {
        if (web != null) web.onPause();
        super.onPause();
    }
}
