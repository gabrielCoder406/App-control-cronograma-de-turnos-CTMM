package ar.ctmm.turnos;

import android.app.Activity;
import android.content.SharedPreferences;
import android.webkit.JavascriptInterface;

/** Puente JavaScript ↔ Android: guarda los datos en el teléfono y abre el menú Compartir. */
public class Bridge {
    private final Activity activity;
    private final SharedPreferences prefs;

    public Bridge(Activity activity, SharedPreferences prefs) {
        this.activity = activity;
        this.prefs = prefs;
    }

    @JavascriptInterface
    public String load() {
        return prefs.getString("state", "");
    }

    @JavascriptInterface
    public void save(String data) {
        prefs.edit().putString("state", data).apply();
    }

    @JavascriptInterface
    public void share(final String text, final String title) {
        activity.runOnUiThread(new ShareTask(activity, text, title));
    }
}
