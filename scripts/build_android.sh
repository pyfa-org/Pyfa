#!/usr/bin/env bash
# =============================================================================
# PYFA Mobile — Android build automation
# =============================================================================
#
# Prerequisites:
#   - Android Studio + NDK installed
#   - ANDROID_HOME set (e.g. ~/Android/Sdk)
#   - Java 17 in PATH
#   - Node.js 18+ and npm/yarn in PATH
#   - expo-cli installed: npm install -g expo-cli eas-cli
#
# Usage:
#   ./scripts/build_android.sh [--release]
#
# With --release: builds a release APK/AAB (requires signing config)
# Without:        builds a debug APK for sideloading / emulator testing
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MOBILE_DIR="$REPO_ROOT/mobile"
BUILD_MODE="debug"

for arg in "$@"; do
  case $arg in
    --release) BUILD_MODE="release" ;;
  esac
done

echo "============================================="
echo "  PYFA Mobile — Android Build ($BUILD_MODE)"
echo "============================================="

# ---------------------------------------------------------------------------
# 1. Verify required tools
# ---------------------------------------------------------------------------
echo ""
echo "[1/6] Checking prerequisites..."

command -v node    >/dev/null 2>&1 || { echo "ERROR: node not found";  exit 1; }
command -v java    >/dev/null 2>&1 || { echo "ERROR: java not found";  exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found"; exit 1; }

if [ -z "${ANDROID_HOME:-}" ]; then
  echo "ERROR: ANDROID_HOME is not set. Set it to your Android SDK directory."
  exit 1
fi

echo "  node   : $(node --version)"
echo "  java   : $(java -version 2>&1 | head -1)"
echo "  python : $(python3 --version)"
echo "  SDK    : $ANDROID_HOME"

# ---------------------------------------------------------------------------
# 2. Trim the SDE (if not already done)
# ---------------------------------------------------------------------------
echo ""
echo "[2/6] Checking SDE..."

SDE_OUTPUT="$REPO_ROOT/backend/data/eve.db"

if [ ! -f "$SDE_OUTPUT" ]; then
  if [ -f "$REPO_ROOT/eve.db" ]; then
    echo "  Trimming SDE from $REPO_ROOT/eve.db ..."
    python3 "$SCRIPT_DIR/trim_sde.py" \
      --input  "$REPO_ROOT/eve.db" \
      --output "$SDE_OUTPUT"
  else
    echo "WARNING: No eve.db found at repo root and no trimmed SDE exists."
    echo "         Download the EVE SDE and run:"
    echo "         python3 scripts/trim_sde.py --input <path/to/eve.db>"
    echo "         Continuing without eve.db — the app will fail at runtime."
  fi
else
  SIZE_MB=$(du -sm "$SDE_OUTPUT" | cut -f1)
  echo "  Found trimmed SDE: $SDE_OUTPUT (${SIZE_MB} MB)"
fi

# ---------------------------------------------------------------------------
# 3. Install JS dependencies
# ---------------------------------------------------------------------------
echo ""
echo "[3/6] Installing JS dependencies..."

cd "$MOBILE_DIR"
if [ -f "package-lock.json" ]; then
  npm ci --legacy-peer-deps
elif [ -f "yarn.lock" ]; then
  yarn install --frozen-lockfile
else
  npm install --legacy-peer-deps
fi

# ---------------------------------------------------------------------------
# 4. Run Expo prebuild (generates native android/ directory)
# ---------------------------------------------------------------------------
echo ""
echo "[4/6] Running Expo prebuild..."

npx expo prebuild --platform android --clean

# ---------------------------------------------------------------------------
# 5. Copy backend data into Android assets
# ---------------------------------------------------------------------------
echo ""
echo "[5/6] Copying backend data into Android assets..."

ASSETS_DIR="$MOBILE_DIR/android/app/src/main/assets/pyfa_backend"
mkdir -p "$ASSETS_DIR"

if [ -f "$SDE_OUTPUT" ]; then
  cp "$SDE_OUTPUT" "$ASSETS_DIR/eve.db"
  echo "  Copied eve.db → $ASSETS_DIR/eve.db"
fi

# Copy the backend Python source so Chaquopy can bundle it
BACKEND_ASSET_DIR="$MOBILE_DIR/android/app/src/main/python"
mkdir -p "$BACKEND_ASSET_DIR"

rsync -av --exclude='__pycache__' --exclude='*.pyc' \
  "$REPO_ROOT/backend/"       "$BACKEND_ASSET_DIR/backend/" \
  "$REPO_ROOT/eos/"           "$BACKEND_ASSET_DIR/eos/" \
  "$REPO_ROOT/graphs/"        "$BACKEND_ASSET_DIR/graphs/" \
  "$REPO_ROOT/service/"       "$BACKEND_ASSET_DIR/service_orig/" \
  "$REPO_ROOT/utils/"         "$BACKEND_ASSET_DIR/utils/" \
  2>/dev/null || true

echo "  Copied Python backend source."

# ---------------------------------------------------------------------------
# 6. Build the APK / AAB
# ---------------------------------------------------------------------------
echo ""
echo "[6/6] Building Android ($BUILD_MODE)..."

cd "$MOBILE_DIR/android"

if [ "$BUILD_MODE" = "release" ]; then
  ./gradlew bundleRelease
  echo ""
  echo "Release AAB: $MOBILE_DIR/android/app/build/outputs/bundle/release/app-release.aab"
else
  ./gradlew assembleDebug
  echo ""
  echo "Debug APK: $MOBILE_DIR/android/app/build/outputs/apk/debug/app-debug.apk"
fi

echo ""
echo "Build complete!"
