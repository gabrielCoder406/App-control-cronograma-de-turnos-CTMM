#!/usr/bin/env bash
# Compila el APK de Turnos CTMM sin Gradle: aapt2 + javac + d8 + zipalign + apksigner.
#
# Requisitos: JDK 17+, Android SDK con build-tools y platforms/android-34, Python 3.
# Variables:
#   ANDROID_SDK   ruta del SDK (por defecto /opt/android-sdk o $ANDROID_HOME)
#   VCODE, VNAME  versión (por defecto 2 / 1.1). Subí VCODE en cada actualización.
#   KEYSTORE      clave de firma (por defecto ./keystore.jks). NO se sube al repositorio.
#   KS_PASS       contraseña del keystore (obligatoria si el keystore ya existe).
#
# Para que una versión nueva se instale encima de la anterior sin perder los datos,
# hay que firmarla SIEMPRE con el mismo keystore.
set -euo pipefail
cd "$(dirname "$0")"
SDK=${ANDROID_SDK:-${ANDROID_HOME:-/opt/android-sdk}}
BT=${BUILD_TOOLS:-$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)}
AJ=${ANDROID_JAR:-$SDK/platforms/android-34/android.jar}
VCODE=${VCODE:-2}; VNAME=${VNAME:-1.1}
KEYSTORE=${KEYSTORE:-keystore.jks}

python3 tools/build_pages.py

B=build/apk; rm -rf "$B"; mkdir -p "$B"/res "$B"/gen "$B"/classes "$B"/dex
"$BT"/aapt2 compile --dir android/res -o "$B"/res/
"$BT"/aapt2 link -o "$B"/base.apk -I "$AJ" --manifest android/AndroidManifest.xml -A android/assets \
  --java "$B"/gen --min-sdk-version 24 --target-sdk-version 34 \
  --version-code "$VCODE" --version-name "$VNAME" "$B"/res/*.flat
# Nota: sin clases anónimas ni genéricos con métodos puente en el código Java;
# el d8 de build-tools 34 falla con esos casos cuando se compila con JDK 21.
javac -nowarn -Xlint:-options --release 8 -classpath "$AJ" -d "$B"/classes \
  $(find android/src "$B"/gen -name '*.java')
"$BT"/d8 --release --min-api 24 --lib "$AJ" --output "$B"/dex $(find "$B"/classes -name '*.class')
cp "$B"/base.apk "$B"/unsigned.apk
(cd "$B"/dex && zip -q -X ../unsigned.apk classes.dex)
"$BT"/zipalign -f -p 4 "$B"/unsigned.apk "$B"/aligned.apk

if [ ! -f "$KEYSTORE" ]; then
  : "${KS_PASS:?No existe $KEYSTORE. Definí KS_PASS para crear una clave nueva (o apuntá KEYSTORE a la tuya).}"
  echo "Creando clave de firma nueva en $KEYSTORE (guardala: sin ella no se puede actualizar la app)"
  keytool -genkeypair -keystore "$KEYSTORE" -alias turnos -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" -dname "CN=Turnos CTMM, L=Rio Cuarto, C=AR" >/dev/null 2>&1
fi
: "${KS_PASS:?Definí KS_PASS con la contraseña de $KEYSTORE}"
OUT=build/TurnosCTMM-v$VNAME.apk
"$BT"/apksigner sign --ks "$KEYSTORE" --ks-key-alias turnos --ks-pass env:KS_PASS --key-pass env:KS_PASS \
  --out "$OUT" "$B"/aligned.apk
"$BT"/apksigner verify "$OUT" && echo "APK listo: $OUT"
