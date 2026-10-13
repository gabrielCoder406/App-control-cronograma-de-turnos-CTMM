package ar.ctmm.turnos;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Mantiene la app dentro de sus archivos; cualquier enlace externo se abre en el navegador. */
public class LinkClient extends WebViewClient {
    private final Activity activity;

    public LinkClient(Activity activity) {
        this.activity = activity;
    }

    @Override
    public boolean shouldOverrideUrlLoading(WebView v, String url) {
        if (url.startsWith("file:///android_asset/")) return false;
        try {
            activity.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception ignored) {
        }
        return true;
    }
}
