package ar.ctmm.turnos;

import android.app.Activity;
import android.content.Intent;

/** Abre el menú Compartir de Android (WhatsApp, mail, Drive…). */
public class ShareTask implements Runnable {
    private final Activity activity;
    private final String text;
    private final String title;

    public ShareTask(Activity activity, String text, String title) {
        this.activity = activity;
        this.text = text;
        this.title = title;
    }

    @Override
    public void run() {
        Intent i = new Intent(Intent.ACTION_SEND);
        i.setType("text/plain");
        i.putExtra(Intent.EXTRA_SUBJECT, title);
        i.putExtra(Intent.EXTRA_TEXT, text);
        activity.startActivity(Intent.createChooser(i, title));
    }
}
