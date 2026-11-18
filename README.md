# Luludex

Luludex is a personal finance web app (Italian UI) that installs on your phone like a normal app and syncs across devices through your own free Firebase project.

Modules: work vs personal tracking on every transaction (with a Tutto / Lavoro / Personale switch), clients with PT and Coaching packages (lessons done, payments in instalments, amount still due), accounts (also in foreign currencies), transactions, transfers, tax set-asides (accantonamenti), CSV and Excel import/export, monthly and annual budget, net worth and investments, savings goals, recurring items, full JSON backup.

## Current status: local mode (no database)

Luludex is **not connected to any database yet**. `config.js` is empty (`window.LULUDEX_FIREBASE = null`), so the app starts directly without sign-in and keeps all data in the browser's `localStorage` (key `luludex.data`) on that device only. Use *Impostazioni → Backup completo* to save a copy.
The Firebase code is kept intact: connecting a dedicated Luludex Firebase project later only requires filling `config.js` (see setup below).

## How it works

- Static files hosted on GitHub Pages: `index.html`, `sw.js`, `manifest.webmanifest`, `vendor/` (Firebase SDK), `icons/`.
- Data lives in Cloud Firestore under `users/{your uid}/…`. The rules in `firebase/firestore.rules` let only your signed-in account read or write it.
- Firestore keeps a copy on each device: the app opens instantly, works offline and syncs in real time between phone and computer.

## Setup (one time, about 15 minutes)

### 1. Create the Firebase project
1. Go to https://console.firebase.google.com and sign in with your Google account.
2. **Create a project** (e.g. `luludex`). Google Analytics is not needed.
3. **Build → Firestore Database → Create database**: choose **production mode** and an EU location (e.g. `eur3` or `europe-west`).
4. In **Firestore → Rules**, replace everything with the contents of `firebase/firestore.rules` and click **Publish**.
5. **Build → Authentication → Get started → Sign-in method**: enable **Google** (and, if you want, **Email/Password**).
6. **Authentication → Settings → Authorized domains**: add `hyf0515.github.io`.
7. **Project settings (gear) → General → Your apps → Web (</>)**: register an app (e.g. `luludex-web`, no hosting) and copy the `firebaseConfig` block.

### 2. Connect the app
Open https://hyf0515.github.io/Luludex/, paste the `firebaseConfig` block and sign in with Google.
To avoid pasting it on every device, put the same values in `config.js` (these values are designed to be public; your data is protected by the security rules).

### 3. Install on your phone
- **iPhone (Safari):** Share → **Add to Home Screen**.
- **Android (Chrome):** menu ⋮ → **Install app**.

## Updating the app
Edit the files and push. Installed apps pick up the new version the next time they are opened online. If you change the list of files in `sw.js`, also bump `CACHE`.

## Backups
**Impostazioni → Backup completo** (JSON) or **Esporta in Excel (.xlsx)**.
