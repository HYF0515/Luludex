# Luludex

Luludex is a personal finance web app (Italian UI) that installs on your phone like a normal app and syncs across devices through your own free Firebase project.

Modules: work vs personal tracking on every transaction (with a Tutto / Lavoro / Personale switch), clients with PT and Coaching packages (lessons done, payments in instalments, amount still due), accounts (also in foreign currencies), transactions, transfers, tax set-asides (accantonamenti), CSV and Excel import/export, monthly and annual budget, net worth and investments, savings goals, recurring items, full JSON backup.

## Status

Until `config.js` is filled, Luludex runs in **local mode**: no sign-in, data only in this browser (`localStorage`, key `luludex.data`).
Once `config.js` contains the Luludex Firebase project, the app asks for sign-in and keeps everything in Firestore.

Runs entirely on the **free Firebase plan (Spark)**: no Firebase Storage and no credit card.
Invoice and diet files are saved in Firestore too (`users/{uid}/files/{key}`, split into parts of max 1 MB), up to 5 MB per file.

### Still to do
- **Google Calendar sync (one-way, Luludex → Google):** enable the Google Calendar API in the same Google project and request the calendar permission at sign-in; Luludex creates, updates and deletes the appointments in a dedicated calendar (e.g. "Luludex – Clienti"). On the iPhone, adding the Google account in Settings → Calendar shows them in the iPhone Calendar too.

## How it works

- Static files hosted on GitHub Pages (branch `main`, address https://hyf0515.github.io/Luludex/): `index.html`, `sw.js`, `manifest.webmanifest`, `vendor/` (Firebase SDK), `icons/`.
- Data lives in Cloud Firestore under `users/{your uid}/…`. The rules in `firebase/firestore.rules` let only your signed-in account read or write it.
- Firestore keeps a copy on each device: the app opens instantly, works offline and syncs in real time between phone and computer.

## Setup (one time, about 15 minutes)

### 1. Create the Firebase project
1. Go to https://console.firebase.google.com and sign in with your Google account.
2. **Create a project** (e.g. `luludex`). Google Analytics is not needed. Stay on the free **Spark** plan: Storage is not used.
3. **Build → Firestore Database → Create database**: choose **production mode** and an EU location (e.g. `eur3` or `europe-west`).
4. In **Firestore → Rules**, replace everything with the contents of `firebase/firestore.rules` and click **Publish**.
5. **Build → Authentication → Get started → Sign-in method**: enable **Google** (and, if you want, **Email/Password**).
6. **Authentication → Settings → Authorized domains**: add `hyf0515.github.io`.
7. **Project settings (gear) → General → Your apps → Web (</>)**: register an app (e.g. `luludex-web`, no hosting) and copy the `firebaseConfig` block.

### 2. Connect the app
Put the `firebaseConfig` values in `config.js` (`window.LULUDEX_FIREBASE = {...}`) and push to `main`. These values are designed to be public: your data is protected by the security rules.
Then open https://hyf0515.github.io/Luludex/ and sign in with Google.

### 3. Move the existing data
In the old version (local mode / artifact): *Impostazioni → Scarica backup*. In the connected app, after signing in: *Impostazioni → Ripristina da backup*. Files of invoices and diets travel inside the backup and are uploaded to Firestore.

### 4. Install on your phone
- **iPhone (Safari):** Share → **Add to Home Screen**.
- **Android (Chrome):** menu ⋮ → **Install app**.

## Updating the app
Edit the files and push. Installed apps pick up the new version the next time they are opened online. If you change the list of files in `sw.js`, also bump `CACHE`.

## Backups
**Impostazioni → Backup completo** (JSON) or **Esporta in Excel (.xlsx)**.
