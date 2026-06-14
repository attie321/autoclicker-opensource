"""
AutoClicker Pro - Full Edition
Multi-language: NL / EN / DE / FR / ES / TR
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.simpledialog as sd
import threading
import time
import json
import os
import sys
import random
from datetime import datetime

from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, KeyCode

mouse_ctrl = MouseController()
kb_ctrl = KeyboardController()

# ─────────────────────────────────────────────
# DATA PATHS
# ─────────────────────────────────────────────
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
PROFILES_FILE = os.path.join(BASE_DIR, "profiles.json")
MACROS_DIR    = os.path.join(BASE_DIR, "macros")
os.makedirs(MACROS_DIR, exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
LANGS = {
    "Nederlands": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "AutoClicker",
        "tab_macro": "Macro Recorder",
        "tab_playlist": "Playlist",
        "tab_settings": "Instellingen",
        "interval": "Klik-interval",
        "hours": "Uren", "minutes": "Minuten", "seconds": "Seconden", "ms": "Milliseconden",
        "jitter": "Random variatie (%)",
        "jitter_tip": "0 = exact interval, hoger = menselijker",
        "click_options": "Klik-opties",
        "mouse_button": "Muisknop",
        "left": "Links", "right": "Rechts", "middle": "Midden",
        "click_type": "Kliktype",
        "single": "Enkel", "double": "Dubbel", "triple": "Triple",
        "position": "Klikpositie",
        "current_pos": "Huidige muispositie",
        "fixed_pos": "Vaste positie:",
        "pick_pos": "Selecteer op scherm (3s)",
        "repeat": "Herhalen",
        "repeat_forever": "Oneindig herhalen",
        "max_clicks": "Aantal klikken:",
        "profiles": "Profielen",
        "profile_name": "Naam:",
        "save": "Opslaan", "load": "Laden", "delete": "Verwijderen",
        "stats": "Statistieken",
        "clicks": "Klikken:", "cps": "CPS:",
        "reset_counter": "Reset teller",
        "start": "Start", "stop": "Stop",
        "scheduler": "Geplande Start",
        "schedule_after": "Start over (sec):",
        "scheduled_start": "Gepland starten",
        "cancel": "Annuleren",
        "pixel_wait": "Start bij Pixelkleur",
        "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RGB (r,g,b):",
        "pixel_start": "Wachten & starten",
        "extra": "Extra opties",
        "always_top": "Altijd op voorgrond",
        "sound_click": "Geluid bij klik",
        "run_startup": "Starten bij Windows-opstart",
        "backup_export": "Backup exporteren",
        "backup_import": "Backup importeren",
        "macro_rec_options": "Opname-opties",
        "rec_clicks": "Muisklikken",
        "rec_moves": "Muisbewegingen",
        "rec_scroll": "Scrollen",
        "rec_keys": "Toetsenbord",
        "rec_start": "Opname starten",
        "rec_stop": "Opname stoppen",
        "macro_save_lib": "Opslaan in bibliotheek",
        "macro_name": "Macronaam:",
        "save_lib": "Opslaan",
        "macro_lib": "Macro Bibliotheek",
        "load_buf": "Laden → buffer",
        "rename": "Hernoemen",
        "import_json": "Importeren",
        "export_json": "Exporteren",
        "playback": "Afspelen",
        "speed": "Snelheid (x):",
        "repeats": "Herhalingen:",
        "repeat_infinite": "Onbeperkt herhalen",
        "play": "Afspelen",
        "recorded_events": "Opgenomen events:",
        "playlist_add": "Toevoegen",
        "playlist_remove": "Verwijder",
        "up": "Omhoog", "down": "Omlaag",
        "playlist_speed": "Snelheid (x):",
        "playlist_repeats": "Herhalingen playlist:",
        "play_playlist": "Playlist afspelen",
        "log": "Log",
        "clear_log": "Log wissen",
        "save_log": "Log opslaan",
        "theme": "Thema:",
        "language": "Taal:",
        "hotkeys_btn": "Hotkeys instellen",
        "hide_window": "Verberg venster",
        "mouse_pos": "Muis:",
        "status_ready": "Klaar.",
        "status_running": "Status: Actief",
        "status_stopped": "Status: Gestopt",
        "status_recording": "Status: OPNEMEN...",
        "status_playing": "Status: AFSPELEN...",
        "hotkey_clicker": "AutoClicker start/stop:",
        "hotkey_record": "Macro opnemen:",
        "hotkey_play": "Macro afspelen:",
        "hotkey_note": "Gebruik functietoetsen (f1–f12). Herstart app na wijziging.",
        "panic_note": "ESC stopt altijd alles onmiddellijk.",
        "no_macro": "Geen macro opgenomen of geladen.",
        "no_events": "Niets om op te slaan.",
        "select_first": "Selecteer eerst een macro.",
        "rename_prompt": "Nieuwe naam:",
        "delete_confirm": "Verwijderen?",
        "profile_req": "Geef het profiel een naam.",
        "profile_notfound": "Dit profiel bestaat niet.",
        "backup_saved": "Backup opgeslagen.",
        "backup_loaded": "Backup geladen.",
        "no_playlist": "Voeg eerst macro's toe aan de playlist.",
        "startup_win_only": "Werkt alleen op Windows.",
        "hotkeys_saved": "Hotkeys opgeslagen. Herstart de app.",
        "pixel_format_err": "Kleurformaat: R,G,B (bijv. 255,0,0)",
        "pick_wait": "Beweeg muis naar positie (3 sec)...",
        "pos_set": "Positie ingesteld op",
        "stopped_all": "PANIC: alles gestopt (ESC).",
        "log_saved": "Log opgeslagen naar",
        "macro_saved": "Macro opgeslagen:",
        "macro_loaded": "Macro geladen:",
        "macro_deleted": "Macro verwijderd:",
        "macro_imported": "Macro geïmporteerd:",
        "macro_exported": "Macro geëxporteerd:",
        "profile_saved": "Profiel opgeslagen:",
        "profile_loaded": "Profiel geladen:",
        "profile_deleted": "Profiel verwijderd:",
        "clicker_started": "AutoClicker gestart.",
        "clicker_stopped": "AutoClicker gestopt.",
        "rec_started": "Opname gestart.",
        "rec_stopped": "Opname gestopt.",
        "play_started": "Afspelen gestart.",
        "play_stopped": "Afspelen gestopt.",
        "play_done": "Afspelen voltooid.",
        "sched_starting": "AutoClicker start over",
        "sched_sec": "seconden...",
        "sched_cancelled": "Geplande start geannuleerd.",
        "pixel_waiting": "Wachten tot pixel kleur heeft",
        "pixel_triggered": "Pixelconditie! AutoClicker gestart.",
        "pixel_cancelled": "Pixel-wacht geannuleerd.",
        "playlist_started": "Playlist gestart.",
        "playlist_stopped": "Playlist gestopt.",
        "playlist_done": "Playlist voltooid.",
    },

    "English": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "AutoClicker",
        "tab_macro": "Macro Recorder",
        "tab_playlist": "Playlist",
        "tab_settings": "Settings",
        "interval": "Click Interval",
        "hours": "Hours", "minutes": "Minutes", "seconds": "Seconds", "ms": "Milliseconds",
        "jitter": "Random variation (%)",
        "jitter_tip": "0 = exact interval, higher = more human-like",
        "click_options": "Click Options",
        "mouse_button": "Mouse button",
        "left": "Left", "right": "Right", "middle": "Middle",
        "click_type": "Click type",
        "single": "Single", "double": "Double", "triple": "Triple",
        "position": "Click Position",
        "current_pos": "Current mouse position",
        "fixed_pos": "Fixed position:",
        "pick_pos": "Pick on screen (3s)",
        "repeat": "Repeat",
        "repeat_forever": "Repeat forever",
        "max_clicks": "Number of clicks:",
        "profiles": "Profiles",
        "profile_name": "Name:",
        "save": "Save", "load": "Load", "delete": "Delete",
        "stats": "Statistics",
        "clicks": "Clicks:", "cps": "CPS:",
        "reset_counter": "Reset counter",
        "start": "Start", "stop": "Stop",
        "scheduler": "Scheduled Start",
        "schedule_after": "Start after (sec):",
        "scheduled_start": "Scheduled start",
        "cancel": "Cancel",
        "pixel_wait": "Start on Pixel Color",
        "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RGB (r,g,b):",
        "pixel_start": "Wait & start",
        "extra": "Extra options",
        "always_top": "Always on top",
        "sound_click": "Sound on click",
        "run_startup": "Run on Windows startup",
        "backup_export": "Export backup",
        "backup_import": "Import backup",
        "macro_rec_options": "Recording options",
        "rec_clicks": "Mouse clicks",
        "rec_moves": "Mouse moves",
        "rec_scroll": "Scroll",
        "rec_keys": "Keyboard",
        "rec_start": "Start recording",
        "rec_stop": "Stop recording",
        "macro_save_lib": "Save to library",
        "macro_name": "Macro name:",
        "save_lib": "Save",
        "macro_lib": "Macro Library",
        "load_buf": "Load → buffer",
        "rename": "Rename",
        "import_json": "Import",
        "export_json": "Export",
        "playback": "Playback",
        "speed": "Speed (x):",
        "repeats": "Repeats:",
        "repeat_infinite": "Repeat infinitely",
        "play": "Play",
        "recorded_events": "Recorded events:",
        "playlist_add": "Add",
        "playlist_remove": "Remove",
        "up": "Up", "down": "Down",
        "playlist_speed": "Speed (x):",
        "playlist_repeats": "Playlist repeats:",
        "play_playlist": "Play playlist",
        "log": "Log",
        "clear_log": "Clear log",
        "save_log": "Save log",
        "theme": "Theme:",
        "language": "Language:",
        "hotkeys_btn": "Set hotkeys",
        "hide_window": "Hide window",
        "mouse_pos": "Mouse:",
        "status_ready": "Ready.",
        "status_running": "Status: Running",
        "status_stopped": "Status: Stopped",
        "status_recording": "Status: RECORDING...",
        "status_playing": "Status: PLAYING...",
        "hotkey_clicker": "AutoClicker start/stop:",
        "hotkey_record": "Macro record:",
        "hotkey_play": "Macro play:",
        "hotkey_note": "Use function keys (f1–f12). Restart app after change.",
        "panic_note": "ESC always stops everything immediately.",
        "no_macro": "No macro recorded or loaded.",
        "no_events": "Nothing to save.",
        "select_first": "Select a macro first.",
        "rename_prompt": "New name:",
        "delete_confirm": "Delete?",
        "profile_req": "Enter a profile name.",
        "profile_notfound": "Profile not found.",
        "backup_saved": "Backup saved.",
        "backup_loaded": "Backup loaded.",
        "no_playlist": "Add macros to the playlist first.",
        "startup_win_only": "Windows only.",
        "hotkeys_saved": "Hotkeys saved. Restart the app.",
        "pixel_format_err": "Color format: R,G,B (e.g. 255,0,0)",
        "pick_wait": "Move mouse to position (3 sec)...",
        "pos_set": "Position set to",
        "stopped_all": "PANIC: everything stopped (ESC).",
        "log_saved": "Log saved to",
        "macro_saved": "Macro saved:",
        "macro_loaded": "Macro loaded:",
        "macro_deleted": "Macro deleted:",
        "macro_imported": "Macro imported:",
        "macro_exported": "Macro exported:",
        "profile_saved": "Profile saved:",
        "profile_loaded": "Profile loaded:",
        "profile_deleted": "Profile deleted:",
        "clicker_started": "AutoClicker started.",
        "clicker_stopped": "AutoClicker stopped.",
        "rec_started": "Recording started.",
        "rec_stopped": "Recording stopped.",
        "play_started": "Playback started.",
        "play_stopped": "Playback stopped.",
        "play_done": "Playback complete.",
        "sched_starting": "AutoClicker starts in",
        "sched_sec": "seconds...",
        "sched_cancelled": "Scheduled start cancelled.",
        "pixel_waiting": "Waiting for pixel color",
        "pixel_triggered": "Pixel condition met! AutoClicker started.",
        "pixel_cancelled": "Pixel wait cancelled.",
        "playlist_started": "Playlist started.",
        "playlist_stopped": "Playlist stopped.",
        "playlist_done": "Playlist complete.",
    },

    "Deutsch": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "AutoClicker", "tab_macro": "Makro-Rekorder",
        "tab_playlist": "Wiedergabeliste", "tab_settings": "Einstellungen",
        "interval": "Klick-Intervall",
        "hours": "Stunden", "minutes": "Minuten", "seconds": "Sekunden", "ms": "Millisekunden",
        "jitter": "Zufallsvariation (%)", "jitter_tip": "0 = exakt, höher = menschlicher",
        "click_options": "Klick-Optionen", "mouse_button": "Maustaste",
        "left": "Links", "right": "Rechts", "middle": "Mitte",
        "click_type": "Klicktyp", "single": "Einfach", "double": "Doppel", "triple": "Dreifach",
        "position": "Klickposition", "current_pos": "Aktuelle Mausposition",
        "fixed_pos": "Feste Position:", "pick_pos": "Auf Bildschirm auswählen (3s)",
        "repeat": "Wiederholen", "repeat_forever": "Unbegrenzt wiederholen",
        "max_clicks": "Anzahl Klicks:", "profiles": "Profile", "profile_name": "Name:",
        "save": "Speichern", "load": "Laden", "delete": "Löschen",
        "stats": "Statistiken", "clicks": "Klicks:", "cps": "KPS:",
        "reset_counter": "Zähler zurücksetzen", "start": "Start", "stop": "Stop",
        "scheduler": "Geplanter Start", "schedule_after": "Starten nach (Sek.):",
        "scheduled_start": "Geplant starten", "cancel": "Abbrechen",
        "pixel_wait": "Start bei Pixelfarbe", "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RGB (r,g,b):", "pixel_start": "Warten & starten",
        "extra": "Weitere Optionen", "always_top": "Immer im Vordergrund",
        "sound_click": "Klickton", "run_startup": "Mit Windows starten",
        "backup_export": "Backup exportieren", "backup_import": "Backup importieren",
        "macro_rec_options": "Aufnahmeoptionen", "rec_clicks": "Mausklicks",
        "rec_moves": "Mausbewegungen", "rec_scroll": "Scrollen", "rec_keys": "Tastatur",
        "rec_start": "Aufnahme starten", "rec_stop": "Aufnahme stoppen",
        "macro_save_lib": "In Bibliothek speichern", "macro_name": "Makroname:",
        "save_lib": "Speichern", "macro_lib": "Makro-Bibliothek",
        "load_buf": "Laden → Puffer", "rename": "Umbenennen",
        "import_json": "Importieren", "export_json": "Exportieren",
        "playback": "Wiedergabe", "speed": "Geschwindigkeit (x):", "repeats": "Wiederholungen:",
        "repeat_infinite": "Unendlich wiederholen", "play": "Abspielen",
        "recorded_events": "Aufgezeichnete Ereignisse:",
        "playlist_add": "Hinzufügen", "playlist_remove": "Entfernen",
        "up": "Hoch", "down": "Runter",
        "playlist_speed": "Geschwindigkeit (x):", "playlist_repeats": "Listenwiederholungen:",
        "play_playlist": "Liste abspielen", "log": "Protokoll",
        "clear_log": "Protokoll löschen", "save_log": "Protokoll speichern",
        "theme": "Thema:", "language": "Sprache:", "hotkeys_btn": "Hotkeys einstellen",
        "hide_window": "Fenster ausblenden", "mouse_pos": "Maus:",
        "status_ready": "Bereit.", "status_running": "Status: Aktiv",
        "status_stopped": "Status: Gestoppt", "status_recording": "Status: AUFNAHME...",
        "status_playing": "Status: ABSPIELEN...",
        "hotkey_clicker": "AutoClicker Start/Stop:", "hotkey_record": "Makro aufnehmen:",
        "hotkey_play": "Makro abspielen:",
        "hotkey_note": "Funktionstasten (f1–f12). Neustart nach Änderung.",
        "panic_note": "ESC stoppt sofort alles.",
        "no_macro": "Kein Makro aufgezeichnet.", "no_events": "Nichts zu speichern.",
        "select_first": "Zuerst ein Makro auswählen.", "rename_prompt": "Neuer Name:",
        "delete_confirm": "Löschen?", "profile_req": "Profilname eingeben.",
        "profile_notfound": "Profil nicht gefunden.", "backup_saved": "Backup gespeichert.",
        "backup_loaded": "Backup geladen.", "no_playlist": "Zuerst Makros hinzufügen.",
        "startup_win_only": "Nur Windows.", "hotkeys_saved": "Hotkeys gespeichert. Neustart.",
        "pixel_format_err": "Format: R,G,B (z.B. 255,0,0)",
        "pick_wait": "Maus zur Position bewegen (3 Sek.)...",
        "pos_set": "Position gesetzt auf",
        "stopped_all": "PANIC: alles gestoppt (ESC).",
        "log_saved": "Protokoll gespeichert:",
        "macro_saved": "Makro gespeichert:", "macro_loaded": "Makro geladen:",
        "macro_deleted": "Makro gelöscht:", "macro_imported": "Makro importiert:",
        "macro_exported": "Makro exportiert:", "profile_saved": "Profil gespeichert:",
        "profile_loaded": "Profil geladen:", "profile_deleted": "Profil gelöscht:",
        "clicker_started": "AutoClicker gestartet.", "clicker_stopped": "AutoClicker gestoppt.",
        "rec_started": "Aufnahme gestartet.", "rec_stopped": "Aufnahme gestoppt.",
        "play_started": "Wiedergabe gestartet.", "play_stopped": "Wiedergabe gestoppt.",
        "play_done": "Wiedergabe abgeschlossen.",
        "sched_starting": "AutoClicker startet in", "sched_sec": "Sekunden...",
        "sched_cancelled": "Geplanter Start abgebrochen.",
        "pixel_waiting": "Warten auf Pixelfarbe",
        "pixel_triggered": "Pixel erkannt! AutoClicker gestartet.",
        "pixel_cancelled": "Pixel-Warten abgebrochen.",
        "playlist_started": "Liste gestartet.", "playlist_stopped": "Liste gestoppt.",
        "playlist_done": "Liste abgeschlossen.",
    },

    "Français": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "AutoClicker", "tab_macro": "Enregistreur Macro",
        "tab_playlist": "Liste de lecture", "tab_settings": "Paramètres",
        "interval": "Intervalle de clic",
        "hours": "Heures", "minutes": "Minutes", "seconds": "Secondes", "ms": "Millisecondes",
        "jitter": "Variation aléatoire (%)", "jitter_tip": "0 = exact, plus = naturel",
        "click_options": "Options de clic", "mouse_button": "Bouton souris",
        "left": "Gauche", "right": "Droite", "middle": "Milieu",
        "click_type": "Type de clic", "single": "Simple", "double": "Double", "triple": "Triple",
        "position": "Position de clic", "current_pos": "Position actuelle",
        "fixed_pos": "Position fixe:", "pick_pos": "Sélectionner à l'écran (3s)",
        "repeat": "Répéter", "repeat_forever": "Répéter indéfiniment",
        "max_clicks": "Nombre de clics:", "profiles": "Profils", "profile_name": "Nom:",
        "save": "Enregistrer", "load": "Charger", "delete": "Supprimer",
        "stats": "Statistiques", "clicks": "Clics:", "cps": "CPS:",
        "reset_counter": "Réinitialiser", "start": "Démarrer", "stop": "Arrêter",
        "scheduler": "Démarrage programmé", "schedule_after": "Démarrer dans (sec):",
        "scheduled_start": "Démarrage programmé", "cancel": "Annuler",
        "pixel_wait": "Démarrer sur couleur pixel", "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RVB (r,v,b):", "pixel_start": "Attendre & démarrer",
        "extra": "Options supplémentaires", "always_top": "Toujours au premier plan",
        "sound_click": "Son au clic", "run_startup": "Démarrer avec Windows",
        "backup_export": "Exporter sauvegarde", "backup_import": "Importer sauvegarde",
        "macro_rec_options": "Options d'enregistrement", "rec_clicks": "Clics souris",
        "rec_moves": "Mouvements souris", "rec_scroll": "Défilement", "rec_keys": "Clavier",
        "rec_start": "Démarrer enreg.", "rec_stop": "Arrêter enreg.",
        "macro_save_lib": "Enregistrer dans bibliothèque", "macro_name": "Nom macro:",
        "save_lib": "Enregistrer", "macro_lib": "Bibliothèque de macros",
        "load_buf": "Charger → tampon", "rename": "Renommer",
        "import_json": "Importer", "export_json": "Exporter",
        "playback": "Lecture", "speed": "Vitesse (x):", "repeats": "Répétitions:",
        "repeat_infinite": "Répéter indéfiniment", "play": "Lire",
        "recorded_events": "Événements enregistrés:",
        "playlist_add": "Ajouter", "playlist_remove": "Supprimer",
        "up": "Haut", "down": "Bas",
        "playlist_speed": "Vitesse (x):", "playlist_repeats": "Répétitions liste:",
        "play_playlist": "Lire la liste", "log": "Journal",
        "clear_log": "Effacer journal", "save_log": "Enregistrer journal",
        "theme": "Thème:", "language": "Langue:", "hotkeys_btn": "Configurer raccourcis",
        "hide_window": "Masquer fenêtre", "mouse_pos": "Souris:",
        "status_ready": "Prêt.", "status_running": "Statut: Actif",
        "status_stopped": "Statut: Arrêté", "status_recording": "Statut: ENREG...",
        "status_playing": "Statut: LECTURE...",
        "hotkey_clicker": "AutoClicker start/stop:", "hotkey_record": "Enregistrer macro:",
        "hotkey_play": "Lire macro:",
        "hotkey_note": "Touches de fonction (f1–f12). Redémarrer après modification.",
        "panic_note": "ÉCHAP arrête tout immédiatement.",
        "no_macro": "Aucune macro.", "no_events": "Rien à enregistrer.",
        "select_first": "Sélectionner une macro.", "rename_prompt": "Nouveau nom:",
        "delete_confirm": "Supprimer?", "profile_req": "Entrer un nom de profil.",
        "profile_notfound": "Profil introuvable.", "backup_saved": "Sauvegarde enregistrée.",
        "backup_loaded": "Sauvegarde chargée.", "no_playlist": "Ajouter des macros d'abord.",
        "startup_win_only": "Windows seulement.", "hotkeys_saved": "Raccourcis enregistrés.",
        "pixel_format_err": "Format: R,V,B (ex. 255,0,0)",
        "pick_wait": "Déplacer la souris (3 sec)...",
        "pos_set": "Position définie sur",
        "stopped_all": "PANIQUE: tout arrêté (ÉCHAP).",
        "log_saved": "Journal enregistré:",
        "macro_saved": "Macro enregistrée:", "macro_loaded": "Macro chargée:",
        "macro_deleted": "Macro supprimée:", "macro_imported": "Macro importée:",
        "macro_exported": "Macro exportée:", "profile_saved": "Profil enregistré:",
        "profile_loaded": "Profil chargé:", "profile_deleted": "Profil supprimé:",
        "clicker_started": "AutoClicker démarré.", "clicker_stopped": "AutoClicker arrêté.",
        "rec_started": "Enregistrement démarré.", "rec_stopped": "Enregistrement arrêté.",
        "play_started": "Lecture démarrée.", "play_stopped": "Lecture arrêtée.",
        "play_done": "Lecture terminée.",
        "sched_starting": "AutoClicker démarre dans", "sched_sec": "secondes...",
        "sched_cancelled": "Démarrage programmé annulé.",
        "pixel_waiting": "Attente couleur pixel",
        "pixel_triggered": "Pixel détecté! AutoClicker démarré.",
        "pixel_cancelled": "Attente pixel annulée.",
        "playlist_started": "Liste démarrée.", "playlist_stopped": "Liste arrêtée.",
        "playlist_done": "Liste terminée.",
    },

    "Español": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "AutoClicker", "tab_macro": "Grabadora Macro",
        "tab_playlist": "Lista de reproducción", "tab_settings": "Configuración",
        "interval": "Intervalo de clic",
        "hours": "Horas", "minutes": "Minutos", "seconds": "Segundos", "ms": "Milisegundos",
        "jitter": "Variación aleatoria (%)", "jitter_tip": "0 = exacto, mayor = más humano",
        "click_options": "Opciones de clic", "mouse_button": "Botón del ratón",
        "left": "Izquierdo", "right": "Derecho", "middle": "Medio",
        "click_type": "Tipo de clic", "single": "Simple", "double": "Doble", "triple": "Triple",
        "position": "Posición de clic", "current_pos": "Posición actual del ratón",
        "fixed_pos": "Posición fija:", "pick_pos": "Seleccionar en pantalla (3s)",
        "repeat": "Repetir", "repeat_forever": "Repetir infinitamente",
        "max_clicks": "Número de clics:", "profiles": "Perfiles", "profile_name": "Nombre:",
        "save": "Guardar", "load": "Cargar", "delete": "Eliminar",
        "stats": "Estadísticas", "clicks": "Clics:", "cps": "CPS:",
        "reset_counter": "Resetear contador", "start": "Iniciar", "stop": "Detener",
        "scheduler": "Inicio programado", "schedule_after": "Iniciar en (seg):",
        "scheduled_start": "Inicio programado", "cancel": "Cancelar",
        "pixel_wait": "Iniciar en color pixel", "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RGB (r,g,b):", "pixel_start": "Esperar e iniciar",
        "extra": "Opciones extra", "always_top": "Siempre encima",
        "sound_click": "Sonido al clic", "run_startup": "Iniciar con Windows",
        "backup_export": "Exportar copia", "backup_import": "Importar copia",
        "macro_rec_options": "Opciones de grabación", "rec_clicks": "Clics ratón",
        "rec_moves": "Movimientos ratón", "rec_scroll": "Desplazamiento", "rec_keys": "Teclado",
        "rec_start": "Iniciar grabación", "rec_stop": "Detener grabación",
        "macro_save_lib": "Guardar en biblioteca", "macro_name": "Nombre macro:",
        "save_lib": "Guardar", "macro_lib": "Biblioteca de macros",
        "load_buf": "Cargar → buffer", "rename": "Renombrar",
        "import_json": "Importar", "export_json": "Exportar",
        "playback": "Reproducción", "speed": "Velocidad (x):", "repeats": "Repeticiones:",
        "repeat_infinite": "Repetir infinitamente", "play": "Reproducir",
        "recorded_events": "Eventos grabados:",
        "playlist_add": "Añadir", "playlist_remove": "Eliminar",
        "up": "Arriba", "down": "Abajo",
        "playlist_speed": "Velocidad (x):", "playlist_repeats": "Repeticiones lista:",
        "play_playlist": "Reproducir lista", "log": "Registro",
        "clear_log": "Limpiar registro", "save_log": "Guardar registro",
        "theme": "Tema:", "language": "Idioma:", "hotkeys_btn": "Configurar atajos",
        "hide_window": "Ocultar ventana", "mouse_pos": "Ratón:",
        "status_ready": "Listo.", "status_running": "Estado: Activo",
        "status_stopped": "Estado: Detenido", "status_recording": "Estado: GRABANDO...",
        "status_playing": "Estado: REPRODUCIENDO...",
        "hotkey_clicker": "AutoClicker inicio/stop:", "hotkey_record": "Grabar macro:",
        "hotkey_play": "Reproducir macro:",
        "hotkey_note": "Teclas de función (f1–f12). Reiniciar después del cambio.",
        "panic_note": "ESC detiene todo inmediatamente.",
        "no_macro": "Sin macro grabada.", "no_events": "Nada que guardar.",
        "select_first": "Seleccionar una macro primero.", "rename_prompt": "Nuevo nombre:",
        "delete_confirm": "¿Eliminar?", "profile_req": "Introduce un nombre de perfil.",
        "profile_notfound": "Perfil no encontrado.", "backup_saved": "Copia guardada.",
        "backup_loaded": "Copia cargada.", "no_playlist": "Añade macros primero.",
        "startup_win_only": "Solo Windows.", "hotkeys_saved": "Atajos guardados. Reinicia.",
        "pixel_format_err": "Formato: R,G,B (ej. 255,0,0)",
        "pick_wait": "Mover ratón a posición (3 seg)...",
        "pos_set": "Posición establecida en",
        "stopped_all": "PÁNICO: todo detenido (ESC).",
        "log_saved": "Registro guardado en",
        "macro_saved": "Macro guardada:", "macro_loaded": "Macro cargada:",
        "macro_deleted": "Macro eliminada:", "macro_imported": "Macro importada:",
        "macro_exported": "Macro exportada:", "profile_saved": "Perfil guardado:",
        "profile_loaded": "Perfil cargado:", "profile_deleted": "Perfil eliminado:",
        "clicker_started": "AutoClicker iniciado.", "clicker_stopped": "AutoClicker detenido.",
        "rec_started": "Grabación iniciada.", "rec_stopped": "Grabación detenida.",
        "play_started": "Reproducción iniciada.", "play_stopped": "Reproducción detenida.",
        "play_done": "Reproducción completa.",
        "sched_starting": "AutoClicker inicia en", "sched_sec": "segundos...",
        "sched_cancelled": "Inicio programado cancelado.",
        "pixel_waiting": "Esperando color pixel",
        "pixel_triggered": "¡Pixel detectado! AutoClicker iniciado.",
        "pixel_cancelled": "Espera pixel cancelada.",
        "playlist_started": "Lista iniciada.", "playlist_stopped": "Lista detenida.",
        "playlist_done": "Lista completa.",
    },

    "Türkçe": {
        "app_title": "AutoClicker Pro",
        "tab_clicker": "OtomatikTıklayıcı", "tab_macro": "Makro Kaydedici",
        "tab_playlist": "Oynatma Listesi", "tab_settings": "Ayarlar",
        "interval": "Tıklama Aralığı",
        "hours": "Saat", "minutes": "Dakika", "seconds": "Saniye", "ms": "Milisaniye",
        "jitter": "Rastgele varyasyon (%)", "jitter_tip": "0 = tam, yüksek = doğal",
        "click_options": "Tıklama Seçenekleri", "mouse_button": "Fare düğmesi",
        "left": "Sol", "right": "Sağ", "middle": "Orta",
        "click_type": "Tıklama türü", "single": "Tekli", "double": "Çift", "triple": "Üçlü",
        "position": "Tıklama Konumu", "current_pos": "Mevcut fare konumu",
        "fixed_pos": "Sabit konum:", "pick_pos": "Ekrandan seç (3sn)",
        "repeat": "Tekrarla", "repeat_forever": "Sonsuz tekrarla",
        "max_clicks": "Tıklama sayısı:", "profiles": "Profiller", "profile_name": "Ad:",
        "save": "Kaydet", "load": "Yükle", "delete": "Sil",
        "stats": "İstatistikler", "clicks": "Tıklamalar:", "cps": "TPS:",
        "reset_counter": "Sayacı sıfırla", "start": "Başlat", "stop": "Durdur",
        "scheduler": "Zamanlanmış Başlatma", "schedule_after": "Sonra başlat (sn):",
        "scheduled_start": "Zamanlanmış başlatma", "cancel": "İptal",
        "pixel_wait": "Piksel Renginde Başlat", "pixel_x": "X:", "pixel_y": "Y:",
        "pixel_rgb": "RGB (r,g,b):", "pixel_start": "Bekle ve başlat",
        "extra": "Ek seçenekler", "always_top": "Her zaman üstte",
        "sound_click": "Tıklamada ses", "run_startup": "Windows'la başlat",
        "backup_export": "Yedek dışa aktar", "backup_import": "Yedek içe aktar",
        "macro_rec_options": "Kayıt seçenekleri", "rec_clicks": "Fare tıklamaları",
        "rec_moves": "Fare hareketleri", "rec_scroll": "Kaydırma", "rec_keys": "Klavye",
        "rec_start": "Kaydı başlat", "rec_stop": "Kaydı durdur",
        "macro_save_lib": "Kütüphaneye kaydet", "macro_name": "Makro adı:",
        "save_lib": "Kaydet", "macro_lib": "Makro Kütüphanesi",
        "load_buf": "Yükle → tampon", "rename": "Yeniden adlandır",
        "import_json": "İçe aktar", "export_json": "Dışa aktar",
        "playback": "Oynatma", "speed": "Hız (x):", "repeats": "Tekrar:",
        "repeat_infinite": "Sonsuz tekrarla", "play": "Oynat",
        "recorded_events": "Kaydedilen olaylar:",
        "playlist_add": "Ekle", "playlist_remove": "Kaldır",
        "up": "Yukarı", "down": "Aşağı",
        "playlist_speed": "Hız (x):", "playlist_repeats": "Liste tekrarları:",
        "play_playlist": "Listeyi oynat", "log": "Günlük",
        "clear_log": "Günlüğü temizle", "save_log": "Günlüğü kaydet",
        "theme": "Tema:", "language": "Dil:", "hotkeys_btn": "Kısayol tuşları",
        "hide_window": "Pencereyi gizle", "mouse_pos": "Fare:",
        "status_ready": "Hazır.", "status_running": "Durum: Aktif",
        "status_stopped": "Durum: Durdu", "status_recording": "Durum: KAYDEDİYOR...",
        "status_playing": "Durum: OYNATILIYOR...",
        "hotkey_clicker": "Tıklayıcı başlat/durdur:", "hotkey_record": "Makro kaydet:",
        "hotkey_play": "Makro oynat:",
        "hotkey_note": "Fonksiyon tuşları (f1–f12). Değişiklik sonrası yeniden başlatın.",
        "panic_note": "ESC her şeyi anında durdurur.",
        "no_macro": "Makro yok.", "no_events": "Kaydedecek bir şey yok.",
        "select_first": "Önce bir makro seçin.", "rename_prompt": "Yeni ad:",
        "delete_confirm": "Sil?", "profile_req": "Profil adı girin.",
        "profile_notfound": "Profil bulunamadı.", "backup_saved": "Yedek kaydedildi.",
        "backup_loaded": "Yedek yüklendi.", "no_playlist": "Önce makro ekleyin.",
        "startup_win_only": "Sadece Windows.", "hotkeys_saved": "Kısayollar kaydedildi.",
        "pixel_format_err": "Format: R,G,B (örn. 255,0,0)",
        "pick_wait": "Fareyi konuma taşıyın (3 sn)...",
        "pos_set": "Konum ayarlandı:",
        "stopped_all": "PANİK: her şey durdu (ESC).",
        "log_saved": "Günlük kaydedildi:",
        "macro_saved": "Makro kaydedildi:", "macro_loaded": "Makro yüklendi:",
        "macro_deleted": "Makro silindi:", "macro_imported": "Makro içe aktarıldı:",
        "macro_exported": "Makro dışa aktarıldı:", "profile_saved": "Profil kaydedildi:",
        "profile_loaded": "Profil yüklendi:", "profile_deleted": "Profil silindi:",
        "clicker_started": "Tıklayıcı başlatıldı.", "clicker_stopped": "Tıklayıcı durduruldu.",
        "rec_started": "Kayıt başladı.", "rec_stopped": "Kayıt durdu.",
        "play_started": "Oynatma başladı.", "play_stopped": "Oynatma durdu.",
        "play_done": "Oynatma tamamlandı.",
        "sched_starting": "Tıklayıcı başlıyor", "sched_sec": "saniye sonra...",
        "sched_cancelled": "Zamanlanmış başlatma iptal edildi.",
        "pixel_waiting": "Piksel rengi bekleniyor",
        "pixel_triggered": "Piksel algılandı! Tıklayıcı başlatıldı.",
        "pixel_cancelled": "Piksel bekleme iptal.",
        "playlist_started": "Liste başladı.", "playlist_stopped": "Liste durdu.",
        "playlist_done": "Liste tamamlandı.",
    },
}

# ─────────────────────────────────────────────
# THEMES
# ─────────────────────────────────────────────
THEMES = {
    "Light": {
        "bg": "#f5f5f5", "fg": "#1a1a1a", "entry_bg": "#ffffff",
        "accent": "#0078d7", "log_bg": "#ffffff", "log_fg": "#333333",
        "sel_bg": "#0078d7", "sel_fg": "#ffffff",
    },
    "Dark": {
        "bg": "#1e1e2e", "fg": "#cdd6f4", "entry_bg": "#313244",
        "accent": "#89b4fa", "log_bg": "#181825", "log_fg": "#a6adc8",
        "sel_bg": "#89b4fa", "sel_fg": "#1e1e2e",
    },
    "Midnight": {
        "bg": "#0d0d0d", "fg": "#e0e0e0", "entry_bg": "#1a1a1a",
        "accent": "#00ff99", "log_bg": "#050505", "log_fg": "#aaaaaa",
        "sel_bg": "#00ff99", "sel_fg": "#000000",
    },
    "Licht": {
        "bg": "#f0f0f0", "fg": "#000000", "entry_bg": "#ffffff",
        "accent": "#0078d7", "log_bg": "#ffffff", "log_fg": "#000000",
        "sel_bg": "#0078d7", "sel_fg": "#ffffff",
    },
    "Donker": {
        "bg": "#2b2b2b", "fg": "#e0e0e0", "entry_bg": "#3c3c3c",
        "accent": "#3a9eff", "log_bg": "#1e1e1e", "log_fg": "#d0d0d0",
        "sel_bg": "#3a9eff", "sel_fg": "#ffffff",
    },
}

# ─────────────────────────────────────────────
# AUTOCLICKER
# ─────────────────────────────────────────────
class AutoClicker:
    def __init__(self, on_tick=None):
        self.running = False
        self.thread = None
        self.click_count = 0
        self.on_tick = on_tick

    def start(self, interval, button, click_type, use_position, x, y, max_clicks, jitter_pct=0):
        if self.running:
            return
        self.running = True
        self.click_count = 0
        self.thread = threading.Thread(
            target=self._run,
            args=(interval, button, click_type, use_position, x, y, max_clicks, jitter_pct),
            daemon=True,
        )
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self, interval, button, click_type, use_position, x, y, max_clicks, jitter_pct):
        btn = {"Left": Button.left, "Right": Button.right, "Middle": Button.middle,
               "Links": Button.left, "Rechts": Button.right, "Midden": Button.middle,
               "Izquierdo": Button.left, "Derecho": Button.right, "Medio": Button.middle,
               "Sol": Button.left, "Sağ": Button.right, "Orta": Button.middle,
               "Links": Button.left, "Rechts": Button.right, "Mitte": Button.middle,
               "Gauche": Button.left, "Droite": Button.right, "Milieu": Button.middle,
               }.get(button, Button.left)
        clicks = {"Single": 1, "Double": 2, "Triple": 3,
                  "Enkel": 1, "Dubbel": 2,
                  "Einfach": 1, "Doppel": 2, "Dreifach": 3,
                  "Simple": 1, "Tekli": 1, "Çift": 2, "Üçlü": 3}.get(click_type, 1)

        while self.running:
            if use_position:
                mouse_ctrl.position = (x, y)
                time.sleep(0.005)
            for _ in range(clicks):
                mouse_ctrl.click(btn)
            self.click_count += 1
            if self.on_tick:
                self.on_tick(self.click_count)
            if max_clicks > 0 and self.click_count >= max_clicks:
                self.running = False
                break
            wait = interval
            if jitter_pct > 0:
                delta = interval * (jitter_pct / 100.0)
                wait = interval + random.uniform(-delta, delta)
            time.sleep(max(wait, 0.001))


# ─────────────────────────────────────────────
# MACRO RECORDER
# ─────────────────────────────────────────────
class MacroRecorder:
    def __init__(self):
        self.events = []
        self.recording = False
        self.start_time = 0
        self.mouse_listener = None
        self.keyboard_listener = None
        self.record_clicks = True
        self.record_moves = True
        self.record_scroll = True
        self.record_keys = True
        self.move_sample_interval = 0.02
        self._last_move_time = 0

    def start(self):
        if self.recording:
            return
        self.events = []
        self.recording = True
        self.start_time = time.time()
        self._last_move_time = 0
        self.mouse_listener = mouse.Listener(
            on_click=self._on_click, on_move=self._on_move, on_scroll=self._on_scroll)
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        if not self.recording:
            return
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def _t(self):
        return time.time() - self.start_time

    def _on_click(self, x, y, button, pressed):
        if not self.record_clicks:
            return
        self.events.append({"type": "click", "t": self._t(), "x": x, "y": y,
                             "button": str(button), "pressed": pressed})

    def _on_move(self, x, y):
        if not self.record_moves:
            return
        now = self._t()
        if now - self._last_move_time < self.move_sample_interval:
            return
        self._last_move_time = now
        self.events.append({"type": "move", "t": now, "x": x, "y": y})

    def _on_scroll(self, x, y, dx, dy):
        if not self.record_scroll:
            return
        self.events.append({"type": "scroll", "t": self._t(), "x": x, "y": y, "dx": dx, "dy": dy})

    def _on_press(self, key):
        if not self.record_keys:
            return
        self.events.append({"type": "key_press", "t": self._t(), "key": self._key_str(key)})

    def _on_release(self, key):
        if not self.record_keys:
            return
        self.events.append({"type": "key_release", "t": self._t(), "key": self._key_str(key)})

    @staticmethod
    def _key_str(key):
        if isinstance(key, KeyCode):
            return f"char:{key.char}"
        return f"special:{key.name}"

    @staticmethod
    def _str_to_key(s):
        if s.startswith("char:"):
            ch = s[5:]
            return KeyCode.from_char(ch) if ch else None
        name = s[8:]
        return getattr(Key, name, None)

    @staticmethod
    def _str_to_btn(s):
        if "left" in s: return Button.left
        if "right" in s: return Button.right
        if "middle" in s: return Button.middle
        return Button.left

    def play(self, events, speed=1.0, repeat=1, stop_flag=None):
        if not events:
            return
        for _ in range(repeat):
            if stop_flag and stop_flag.is_set():
                break
            last_t = 0
            for ev in events:
                if stop_flag and stop_flag.is_set():
                    return
                wait = (ev["t"] - last_t) / max(speed, 0.0001)
                if wait > 0:
                    time.sleep(wait)
                last_t = ev["t"]
                if ev["type"] == "move":
                    mouse_ctrl.position = (ev["x"], ev["y"])
                elif ev["type"] == "click":
                    mouse_ctrl.position = (ev["x"], ev["y"])
                    btn = self._str_to_btn(ev["button"])
                    (mouse_ctrl.press if ev["pressed"] else mouse_ctrl.release)(btn)
                elif ev["type"] == "scroll":
                    mouse_ctrl.position = (ev["x"], ev["y"])
                    mouse_ctrl.scroll(ev["dx"], ev["dy"])
                elif ev["type"] == "key_press":
                    k = self._str_to_key(ev["key"])
                    if k: kb_ctrl.press(k)
                elif ev["type"] == "key_release":
                    k = self._str_to_key(ev["key"])
                    if k: kb_ctrl.release(k)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        self.settings = load_json(SETTINGS_FILE, {
            "theme": "Light", "lang": "English",
            "hotkey_click": "f6", "hotkey_record": "f7", "hotkey_play": "f8",
        })
        self.profiles = load_json(PROFILES_FILE, {})

        self.lang_name = self.settings.get("lang", "English")
        self.T = LANGS.get(self.lang_name, LANGS["English"])

        self.autoclicker = AutoClicker(on_tick=self._on_click_tick)
        self.macro = MacroRecorder()
        self.play_stop_flag = threading.Event()
        self.play_thread = None
        self.playlist = []
        self._schedule_cancel = threading.Event()
        self.pixel_stop_flag = threading.Event()
        self.run_on_startup = tk.BooleanVar(value=False)
        self.always_on_top = tk.BooleanVar(value=False)
        self.sound_on_click = tk.BooleanVar(value=False)
        self._click_start_time = None

        self.style = ttk.Style()
        root.title(self.T["app_title"])
        root.geometry("620x820")
        root.minsize(560, 600)

        self._build_ui()
        self.apply_theme(self.settings.get("theme", "Light"))
        self._refresh_macro_list()
        self._refresh_profile_list()
        self._start_global_hotkeys()
        self._start_panic_listener()
        self._update_mouse_pos()
        root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─── T() shortcut ────────────────────────
    def t(self, key):
        return self.T.get(key, key)

    # ─── SCROLLABLE CONTAINER ─────────────────
    def _build_ui(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(outer, highlightthickness=0)
        vscroll = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vscroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.container = ttk.Frame(self.canvas)
        self._cwin = self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        self.container.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._cwin, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self._build_topbar()
        self._build_notebook()
        self._build_log()

        # Statusbar (outside scroll)
        self.status_var = tk.StringVar(value=self.t("status_ready"))
        ttk.Label(self.root, textvariable=self.status_var, anchor="w",
                  relief="sunken").pack(fill="x", side="bottom")

    def _build_topbar(self):
        top = ttk.Frame(self.container)
        top.pack(fill="x", padx=8, pady=6)

        # Language
        ttk.Label(top, text=self.t("language")).pack(side="left")
        self.lang_var = tk.StringVar(value=self.lang_name)
        lang_cb = ttk.Combobox(top, textvariable=self.lang_var,
                                values=list(LANGS.keys()), width=12, state="readonly")
        lang_cb.pack(side="left", padx=4)
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        # Theme
        ttk.Label(top, text=self.t("theme")).pack(side="left", padx=(8, 0))
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "Light"))
        theme_cb = ttk.Combobox(top, textvariable=self.theme_var,
                                 values=list(THEMES.keys()), width=10, state="readonly")
        theme_cb.pack(side="left", padx=4)
        theme_cb.bind("<<ComboboxSelected>>", lambda e: self.apply_theme(self.theme_var.get()))

        ttk.Button(top, text=self.t("hotkeys_btn"), command=self._open_hotkey_dialog).pack(side="left", padx=4)
        ttk.Button(top, text=self.t("hide_window"), command=self._hide_window).pack(side="right", padx=4)

        self.mouse_pos_var = tk.StringVar(value=f"{self.t('mouse_pos')} (0, 0)")
        ttk.Label(top, textvariable=self.mouse_pos_var).pack(side="right", padx=8)

    def _build_notebook(self):
        self.nb = ttk.Notebook(self.container)
        self.nb.pack(fill="x", padx=8, pady=4)

        self.tab_click    = ttk.Frame(self.nb)
        self.tab_macro    = ttk.Frame(self.nb)
        self.tab_playlist = ttk.Frame(self.nb)
        self.tab_settings = ttk.Frame(self.nb)

        self.nb.add(self.tab_click,    text=self.t("tab_clicker"))
        self.nb.add(self.tab_macro,    text=self.t("tab_macro"))
        self.nb.add(self.tab_playlist, text=self.t("tab_playlist"))
        self.nb.add(self.tab_settings, text=self.t("tab_settings"))

        self._build_click_tab()
        self._build_macro_tab()
        self._build_playlist_tab()
        self._build_settings_tab()

    def _build_log(self):
        log_frame = ttk.LabelFrame(self.container, text=self.t("log"))
        log_frame.pack(fill="both", expand=True, padx=8, pady=4)

        inner = ttk.Frame(log_frame)
        inner.pack(fill="both", expand=True, padx=4, pady=4)
        self.log_text = tk.Text(inner, height=9, state="disabled", wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(inner, command=self.log_text.yview)
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

        btns = ttk.Frame(log_frame)
        btns.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Button(btns, text=self.t("clear_log"), command=self._clear_log).pack(side="left", padx=2)
        ttk.Button(btns, text=self.t("save_log"),  command=self._save_log).pack(side="left", padx=2)

    # ─── AUTOCLICKER TAB ─────────────────────
    def _build_click_tab(self):
        f = self.tab_click
        pad = {"padx": 8, "pady": 5}

        # Interval
        g1 = ttk.LabelFrame(f, text=self.t("interval"))
        g1.pack(fill="x", **pad)
        self.hours   = tk.IntVar(value=0)
        self.minutes = tk.IntVar(value=0)
        self.seconds = tk.IntVar(value=0)
        self.millis  = tk.IntVar(value=100)
        for i, (lbl, var, mx) in enumerate([
            (self.t("hours"), self.hours, 99), (self.t("minutes"), self.minutes, 59),
            (self.t("seconds"), self.seconds, 59), (self.t("ms"), self.millis, 999)]):
            ttk.Label(g1, text=lbl).grid(row=0, column=i*2, padx=4, pady=4, sticky="w")
            ttk.Spinbox(g1, from_=0, to=mx, textvariable=var, width=6).grid(row=0, column=i*2+1, padx=4)
        self.jitter = tk.IntVar(value=0)
        ttk.Label(g1, text=self.t("jitter")).grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky="w")
        ttk.Spinbox(g1, from_=0, to=90, textvariable=self.jitter, width=6).grid(row=1, column=2, padx=4)
        ttk.Label(g1, text=self.t("jitter_tip"), foreground="gray").grid(row=1, column=3, columnspan=5, sticky="w")

        # Click options
        g2 = ttk.LabelFrame(f, text=self.t("click_options"))
        g2.pack(fill="x", **pad)
        ttk.Label(g2, text=self.t("mouse_button")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.mouse_button = tk.StringVar(value=self.t("left"))
        ttk.Combobox(g2, textvariable=self.mouse_button,
                     values=[self.t("left"), self.t("right"), self.t("middle")],
                     width=12, state="readonly").grid(row=0, column=1, padx=4)
        ttk.Label(g2, text=self.t("click_type")).grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.click_type = tk.StringVar(value=self.t("single"))
        ttk.Combobox(g2, textvariable=self.click_type,
                     values=[self.t("single"), self.t("double"), self.t("triple")],
                     width=12, state="readonly").grid(row=0, column=3, padx=4)

        # Position
        g3 = ttk.LabelFrame(f, text=self.t("position"))
        g3.pack(fill="x", **pad)
        self.use_current_pos = tk.BooleanVar(value=True)
        ttk.Radiobutton(g3, text=self.t("current_pos"), variable=self.use_current_pos, value=True
                        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=4, pady=2)
        ttk.Radiobutton(g3, text=self.t("fixed_pos"), variable=self.use_current_pos, value=False
                        ).grid(row=1, column=0, sticky="w", padx=4)
        self.pos_x = tk.IntVar(value=0)
        self.pos_y = tk.IntVar(value=0)
        ttk.Label(g3, text="X").grid(row=1, column=1, sticky="e")
        ttk.Entry(g3, textvariable=self.pos_x, width=6).grid(row=1, column=2, padx=2)
        ttk.Label(g3, text="Y").grid(row=1, column=3, sticky="e")
        ttk.Entry(g3, textvariable=self.pos_y, width=6).grid(row=1, column=4, padx=2)
        self.pick_btn = ttk.Button(g3, text=self.t("pick_pos"), command=self._pick_position)
        self.pick_btn.grid(row=2, column=0, columnspan=6, pady=4, sticky="we", padx=4)

        # Repeat
        g4 = ttk.LabelFrame(f, text=self.t("repeat"))
        g4.pack(fill="x", **pad)
        self.repeat_forever = tk.BooleanVar(value=True)
        ttk.Radiobutton(g4, text=self.t("repeat_forever"), variable=self.repeat_forever, value=True
                        ).grid(row=0, column=0, sticky="w", padx=4)
        ttk.Radiobutton(g4, text=self.t("max_clicks"), variable=self.repeat_forever, value=False
                        ).grid(row=1, column=0, sticky="w", padx=4)
        self.max_clicks = tk.IntVar(value=10)
        ttk.Entry(g4, textvariable=self.max_clicks, width=8).grid(row=1, column=1, padx=4)

        # Profiles
        g5 = ttk.LabelFrame(f, text=self.t("profiles"))
        g5.pack(fill="x", **pad)
        ttk.Label(g5, text=self.t("profile_name")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.profile_name = tk.StringVar()
        self.profile_combo = ttk.Combobox(g5, textvariable=self.profile_name, width=18)
        self.profile_combo.grid(row=0, column=1, padx=4)
        ttk.Button(g5, text=self.t("save"), command=self._save_profile).grid(row=0, column=2, padx=2)
        ttk.Button(g5, text=self.t("load"), command=self._load_profile).grid(row=0, column=3, padx=2)
        ttk.Button(g5, text=self.t("delete"), command=self._delete_profile).grid(row=0, column=4, padx=2)

        # Stats
        gs = ttk.LabelFrame(f, text=self.t("stats"))
        gs.pack(fill="x", **pad)
        self.click_count_var = tk.StringVar(value=f"{self.t('clicks')} 0")
        self.cps_var = tk.StringVar(value=f"{self.t('cps')} 0.0")
        ttk.Label(gs, textvariable=self.click_count_var, font=("Segoe UI", 9, "bold")).pack(side="left", padx=8, pady=4)
        ttk.Label(gs, textvariable=self.cps_var, font=("Segoe UI", 9, "bold")).pack(side="left", padx=8)
        ttk.Button(gs, text=self.t("reset_counter"), command=self._reset_click_counter).pack(side="left", padx=8)

        # Start/Stop
        ctrl = ttk.Frame(f)
        ctrl.pack(fill="x", **pad)
        self.click_status = tk.StringVar(value=self.t("status_stopped"))
        ttk.Label(ctrl, textvariable=self.click_status, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.toggle_click_btn = ttk.Button(
            ctrl, text=f"{self.t('start')} ({self.settings.get('hotkey_click','f6').upper()})",
            command=self.toggle_autoclicker)
        self.toggle_click_btn.pack(side="right")

        # Scheduler
        g6 = ttk.LabelFrame(f, text=self.t("scheduler"))
        g6.pack(fill="x", **pad)
        ttk.Label(g6, text=self.t("schedule_after")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.schedule_delay = tk.IntVar(value=5)
        ttk.Spinbox(g6, from_=1, to=3600, textvariable=self.schedule_delay, width=8).grid(row=0, column=1, padx=4)
        ttk.Button(g6, text=self.t("scheduled_start"), command=self._scheduled_start).grid(row=0, column=2, padx=4)
        ttk.Button(g6, text=self.t("cancel"), command=lambda: self._schedule_cancel.set()).grid(row=0, column=3, padx=4)

        # Pixel wait
        g7 = ttk.LabelFrame(f, text=self.t("pixel_wait"))
        g7.pack(fill="x", **pad)
        ttk.Label(g7, text=self.t("pixel_x")).grid(row=0, column=0, sticky="e")
        self.pixel_x = tk.IntVar(value=0)
        ttk.Entry(g7, textvariable=self.pixel_x, width=6).grid(row=0, column=1, padx=2)
        ttk.Label(g7, text=self.t("pixel_y")).grid(row=0, column=2, sticky="e")
        self.pixel_y = tk.IntVar(value=0)
        ttk.Entry(g7, textvariable=self.pixel_y, width=6).grid(row=0, column=3, padx=2)
        ttk.Label(g7, text=self.t("pixel_rgb")).grid(row=0, column=4, padx=4, sticky="e")
        self.pixel_color = tk.StringVar(value="255,255,255")
        ttk.Entry(g7, textvariable=self.pixel_color, width=12).grid(row=0, column=5, padx=2)
        ttk.Button(g7, text=self.t("pixel_start"), command=self._wait_for_pixel).grid(row=1, column=0, columnspan=3, pady=4, sticky="we", padx=4)
        ttk.Button(g7, text=self.t("cancel"), command=lambda: self.pixel_stop_flag.set()).grid(row=1, column=3, columnspan=3, pady=4, sticky="we", padx=4)

    # ─── MACRO TAB ────────────────────────────
    def _build_macro_tab(self):
        f = self.tab_macro
        pad = {"padx": 8, "pady": 5}

        opts = ttk.LabelFrame(f, text=self.t("macro_rec_options"))
        opts.pack(fill="x", **pad)
        self.rec_clicks = tk.BooleanVar(value=True)
        self.rec_moves  = tk.BooleanVar(value=True)
        self.rec_scroll = tk.BooleanVar(value=True)
        self.rec_keys   = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts, text=self.t("rec_clicks"), variable=self.rec_clicks).grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ttk.Checkbutton(opts, text=self.t("rec_moves"),  variable=self.rec_moves ).grid(row=0, column=1, sticky="w", padx=4)
        ttk.Checkbutton(opts, text=self.t("rec_scroll"), variable=self.rec_scroll).grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ttk.Checkbutton(opts, text=self.t("rec_keys"),   variable=self.rec_keys  ).grid(row=1, column=1, sticky="w", padx=4)

        rc = ttk.Frame(f)
        rc.pack(fill="x", **pad)
        self.rec_status = tk.StringVar(value=self.t("status_stopped"))
        ttk.Label(rc, textvariable=self.rec_status, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.toggle_rec_btn = ttk.Button(rc, text=self.t("rec_start"), command=self.toggle_recording)
        self.toggle_rec_btn.pack(side="right")

        sl = ttk.LabelFrame(f, text=self.t("macro_save_lib"))
        sl.pack(fill="x", **pad)
        ttk.Label(sl, text=self.t("macro_name")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.macro_name = tk.StringVar()
        ttk.Entry(sl, textvariable=self.macro_name, width=25).grid(row=0, column=1, padx=4)
        ttk.Button(sl, text=self.t("save_lib"), command=self.save_macro_to_library).grid(row=0, column=2, padx=4)

        lib = ttk.LabelFrame(f, text=self.t("macro_lib"))
        lib.pack(fill="both", expand=True, **pad)
        li = ttk.Frame(lib)
        li.pack(fill="both", expand=True, padx=4, pady=4)
        self.macro_listbox = tk.Listbox(li, height=7)
        self.macro_listbox.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(li, command=self.macro_listbox.yview)
        sb.pack(side="right", fill="y")
        self.macro_listbox.config(yscrollcommand=sb.set)

        bf = ttk.Frame(lib)
        bf.pack(fill="x", padx=4, pady=4)
        for txt, cmd in [(self.t("load_buf"), self.load_selected_macro),
                         (self.t("rename"),   self.rename_selected_macro),
                         (self.t("delete"),   self.delete_selected_macro),
                         (self.t("import_json"), self.import_macro),
                         (self.t("export_json"), self.export_macro)]:
            ttk.Button(bf, text=txt, command=cmd).pack(side="left", padx=2)

        po = ttk.LabelFrame(f, text=self.t("playback"))
        po.pack(fill="x", **pad)
        ttk.Label(po, text=self.t("speed")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.play_speed = tk.DoubleVar(value=1.0)
        ttk.Spinbox(po, from_=0.1, to=10, increment=0.1, textvariable=self.play_speed, width=6).grid(row=0, column=1, padx=4)
        ttk.Label(po, text=self.t("repeats")).grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.play_repeat = tk.IntVar(value=1)
        ttk.Spinbox(po, from_=1, to=9999, textvariable=self.play_repeat, width=6).grid(row=0, column=3, padx=4)
        self.play_forever = tk.BooleanVar(value=False)
        ttk.Checkbutton(po, text=self.t("repeat_infinite"), variable=self.play_forever).grid(row=1, column=0, columnspan=4, sticky="w", padx=4, pady=2)

        pc = ttk.Frame(f)
        pc.pack(fill="x", **pad)
        self.play_status = tk.StringVar(value=self.t("status_stopped"))
        ttk.Label(pc, textvariable=self.play_status, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.toggle_play_btn = ttk.Button(
            pc, text=f"{self.t('play')} ({self.settings.get('hotkey_play','f8').upper()})",
            command=self.toggle_playback)
        self.toggle_play_btn.pack(side="right")

        self.events_var = tk.StringVar(value=f"{self.t('recorded_events')} 0")
        ttk.Label(f, textvariable=self.events_var).pack(anchor="w", padx=8, pady=4)

    # ─── PLAYLIST TAB ─────────────────────────
    def _build_playlist_tab(self):
        f = self.tab_playlist
        pad = {"padx": 8, "pady": 5}

        af = ttk.Frame(f)
        af.pack(fill="x", **pad)
        self.playlist_add_var = tk.StringVar()
        self.playlist_add_combo = ttk.Combobox(af, textvariable=self.playlist_add_var, width=25)
        self.playlist_add_combo.pack(side="left", padx=4)
        for txt, cmd in [(self.t("playlist_add"), self._playlist_add),
                         (self.t("playlist_remove"), self._playlist_remove),
                         (self.t("up"), lambda: self._playlist_move(-1)),
                         (self.t("down"), lambda: self._playlist_move(1))]:
            ttk.Button(af, text=txt, command=cmd).pack(side="left", padx=2)

        lf = ttk.Frame(f)
        lf.pack(fill="both", expand=True, padx=8, pady=4)
        self.playlist_listbox = tk.Listbox(lf, height=8)
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(lf, command=self.playlist_listbox.yview)
        sb.pack(side="right", fill="y")
        self.playlist_listbox.config(yscrollcommand=sb.set)

        op = ttk.LabelFrame(f, text=self.t("playback"))
        op.pack(fill="x", **pad)
        ttk.Label(op, text=self.t("playlist_speed")).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.playlist_speed = tk.DoubleVar(value=1.0)
        ttk.Spinbox(op, from_=0.1, to=10, increment=0.1, textvariable=self.playlist_speed, width=6).grid(row=0, column=1, padx=4)
        ttk.Label(op, text=self.t("playlist_repeats")).grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.playlist_repeat = tk.IntVar(value=1)
        ttk.Spinbox(op, from_=1, to=9999, textvariable=self.playlist_repeat, width=6).grid(row=0, column=3, padx=4)

        ctrl = ttk.Frame(f)
        ctrl.pack(fill="x", **pad)
        self.playlist_status = tk.StringVar(value=self.t("status_stopped"))
        ttk.Label(ctrl, textvariable=self.playlist_status, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.playlist_toggle_btn = ttk.Button(ctrl, text=self.t("play_playlist"), command=self._toggle_playlist)
        self.playlist_toggle_btn.pack(side="right")

        self.playlist_play_thread = None
        self.playlist_stop_flag = threading.Event()

    # ─── SETTINGS TAB ─────────────────────────
    def _build_settings_tab(self):
        f = self.tab_settings
        pad = {"padx": 8, "pady": 5}

        ex = ttk.LabelFrame(f, text=self.t("extra"))
        ex.pack(fill="x", **pad)
        ttk.Checkbutton(ex, text=self.t("always_top"), variable=self.always_on_top,
                        command=lambda: self.root.attributes("-topmost", self.always_on_top.get())
                        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ttk.Checkbutton(ex, text=self.t("sound_click"), variable=self.sound_on_click
                        ).grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ttk.Checkbutton(ex, text=self.t("run_startup"), variable=self.run_on_startup,
                        command=self._toggle_run_on_startup
                        ).grid(row=2, column=0, sticky="w", padx=4, pady=2)

        bk = ttk.LabelFrame(f, text="Backup")
        bk.pack(fill="x", **pad)
        ttk.Button(bk, text=self.t("backup_export"), command=self._export_full_backup).grid(row=0, column=0, padx=4, pady=4, sticky="we")
        ttk.Button(bk, text=self.t("backup_import"), command=self._import_full_backup).grid(row=0, column=1, padx=4, pady=4, sticky="we")

        hn = ttk.LabelFrame(f, text="Hotkeys")
        hn.pack(fill="x", **pad)
        ttk.Button(hn, text=self.t("hotkeys_btn"), command=self._open_hotkey_dialog).pack(padx=8, pady=8)
        ttk.Label(hn, text=self.t("hotkey_note"), foreground="gray", wraplength=400, justify="left").pack(padx=8, pady=(0,4))
        ttk.Label(hn, text=self.t("panic_note"), foreground="red", font=("Segoe UI", 9, "bold")).pack(padx=8, pady=(0,8))

    # ─── LOGIC ────────────────────────────────
    def _on_click_tick(self, count):
        if self.sound_on_click.get():
            try:
                if os.name == "nt":
                    import winsound
                    winsound.MessageBeep(-1)
                else:
                    print("\a", end="", flush=True)
            except Exception:
                pass
        def upd():
            self.click_count_var.set(f"{self.t('clicks')} {count}")
            if self._click_start_time:
                elapsed = max(time.time() - self._click_start_time, 0.001)
                self.cps_var.set(f"{self.t('cps')} {count/elapsed:.1f}")
        self.root.after(0, upd)

    def toggle_autoclicker(self):
        if self.autoclicker.running:
            self.autoclicker.stop()
            self.click_status.set(self.t("status_stopped"))
            self.toggle_click_btn.config(text=f"{self.t('start')} ({self.settings.get('hotkey_click','f6').upper()})")
            self._log(self.t("clicker_stopped"))
        else:
            interval = (self.hours.get()*3600 + self.minutes.get()*60
                        + self.seconds.get() + self.millis.get()/1000.0)
            if interval <= 0: interval = 0.01
            max_cl = 0 if self.repeat_forever.get() else self.max_clicks.get()
            self._click_start_time = time.time()
            self.autoclicker.start(
                interval=interval, button=self.mouse_button.get(),
                click_type=self.click_type.get(), use_position=not self.use_current_pos.get(),
                x=self.pos_x.get(), y=self.pos_y.get(), max_clicks=max_cl,
                jitter_pct=self.jitter.get())
            self.click_status.set(self.t("status_running"))
            self.toggle_click_btn.config(text=f"{self.t('stop')} ({self.settings.get('hotkey_click','f6').upper()})")
            self._log(self.t("clicker_started"))

    def toggle_recording(self):
        if self.macro.recording:
            self.macro.stop()
            self.rec_status.set(self.t("status_stopped"))
            self.toggle_rec_btn.config(text=self.t("rec_start"))
            self.events_var.set(f"{self.t('recorded_events')} {len(self.macro.events)}")
            self._log(self.t("rec_stopped"))
        else:
            self.macro.record_clicks = self.rec_clicks.get()
            self.macro.record_moves  = self.rec_moves.get()
            self.macro.record_scroll = self.rec_scroll.get()
            self.macro.record_keys   = self.rec_keys.get()
            self.macro.start()
            self.rec_status.set(self.t("status_recording"))
            self.toggle_rec_btn.config(text=self.t("rec_stop"))
            self._log(self.t("rec_started"))

    def toggle_playback(self):
        if self.play_thread and self.play_thread.is_alive():
            self.play_stop_flag.set()
            self.play_status.set(self.t("status_stopped"))
            self.toggle_play_btn.config(text=f"{self.t('play')} ({self.settings.get('hotkey_play','f8').upper()})")
            self._log(self.t("play_stopped"))
        else:
            if not self.macro.events:
                messagebox.showinfo("", self.t("no_macro"))
                return
            self.play_stop_flag.clear()
            repeat = 999999 if self.play_forever.get() else self.play_repeat.get()
            self.play_thread = threading.Thread(
                target=lambda: self._play_worker(self.macro.events, self.play_speed.get(), repeat),
                daemon=True)
            self.play_thread.start()
            self.play_status.set(self.t("status_playing"))
            self.toggle_play_btn.config(text=f"{self.t('stop')} ({self.settings.get('hotkey_play','f8').upper()})")
            self._log(self.t("play_started"))

    def _play_worker(self, events, speed, repeat):
        self.macro.play(events, speed=speed, repeat=repeat, stop_flag=self.play_stop_flag)
        if not self.play_stop_flag.is_set():
            self.root.after(0, lambda: (
                self.play_status.set(self.t("status_stopped")),
                self.toggle_play_btn.config(text=f"{self.t('play')} ({self.settings.get('hotkey_play','f8').upper()})"),
                self._log(self.t("play_done"))))

    def _pick_position(self):
        self._log(self.t("pick_wait"))
        self.pick_btn.config(state="disabled")
        def w():
            time.sleep(3)
            x, y = mouse_ctrl.position
            self.pos_x.set(x); self.pos_y.set(y)
            self.use_current_pos.set(False)
            self._log(f"{self.t('pos_set')} ({x}, {y})")
            self.pick_btn.config(state="normal")
        threading.Thread(target=w, daemon=True).start()

    def _reset_click_counter(self):
        self.autoclicker.click_count = 0
        self._click_start_time = time.time()
        self.click_count_var.set(f"{self.t('clicks')} 0")
        self.cps_var.set(f"{self.t('cps')} 0.0")

    def _scheduled_start(self):
        delay = self.schedule_delay.get()
        self._log(f"{self.t('sched_starting')} {delay} {self.t('sched_sec')}")
        self._schedule_cancel.clear()
        def w():
            for r in range(delay, 0, -1):
                if self._schedule_cancel.is_set():
                    self.root.after(0, lambda: self._log(self.t("sched_cancelled")))
                    return
                self.root.after(0, lambda r=r: self.status_var.set(f"{self.t('sched_starting')} {r} {self.t('sched_sec')}"))
                time.sleep(1)
            if not self._schedule_cancel.is_set():
                self.root.after(0, self.toggle_autoclicker)
        threading.Thread(target=w, daemon=True).start()

    def _wait_for_pixel(self):
        try:
            import pyautogui
        except ImportError:
            messagebox.showerror("", "pip install pyautogui")
            return
        try:
            rgb = tuple(int(v.strip()) for v in self.pixel_color.get().split(","))
        except Exception:
            messagebox.showerror("", self.t("pixel_format_err"))
            return
        self._log(f"{self.t('pixel_waiting')} {rgb}")
        self.pixel_stop_flag.clear()
        def w():
            while not self.pixel_stop_flag.is_set():
                if pyautogui.pixel(self.pixel_x.get(), self.pixel_y.get())[:3] == rgb:
                    self.root.after(0, lambda: (self._log(self.t("pixel_triggered")), self.toggle_autoclicker()))
                    return
                time.sleep(0.2)
            self.root.after(0, lambda: self._log(self.t("pixel_cancelled")))
        threading.Thread(target=w, daemon=True).start()

    # ─── MACRO LIBRARY ────────────────────────
    def _macro_path(self, name):
        return os.path.join(MACROS_DIR, f"{name}.json")

    def _refresh_macro_list(self):
        self.macro_listbox.delete(0, tk.END)
        for fn in sorted(os.listdir(MACROS_DIR)):
            if fn.endswith(".json"):
                self.macro_listbox.insert(tk.END, fn[:-5])
        if hasattr(self, "playlist_add_combo"):
            self.playlist_add_combo["values"] = list(self.macro_listbox.get(0, tk.END))

    def _sel_macro(self):
        sel = self.macro_listbox.curselection()
        return self.macro_listbox.get(sel[0]) if sel else None

    def save_macro_to_library(self):
        if not self.macro.events:
            messagebox.showinfo("", self.t("no_events")); return
        name = self.macro_name.get().strip()
        if not name:
            messagebox.showinfo("", "Name required"); return
        save_json(self._macro_path(name), self.macro.events)
        self._refresh_macro_list()
        self._log(f"{self.t('macro_saved')} {name}")

    def load_selected_macro(self):
        name = self._sel_macro()
        if not name: messagebox.showinfo("", self.t("select_first")); return
        self.macro.events = load_json(self._macro_path(name), [])
        self.events_var.set(f"{self.t('recorded_events')} {len(self.macro.events)}")
        self.macro_name.set(name)
        self._log(f"{self.t('macro_loaded')} {name}")

    def rename_selected_macro(self):
        name = self._sel_macro()
        if not name: return
        new = sd.askstring("", self.t("rename_prompt"), initialvalue=name)
        if new and new != name:
            os.rename(self._macro_path(name), self._macro_path(new))
            self._refresh_macro_list()

    def delete_selected_macro(self):
        name = self._sel_macro()
        if not name: return
        if messagebox.askyesno("", f"{self.t('delete_confirm')} '{name}'"):
            os.remove(self._macro_path(name))
            self._refresh_macro_list()
            self._log(f"{self.t('macro_deleted')} {name}")

    def import_macro(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path: return
        name = os.path.splitext(os.path.basename(path))[0]
        save_json(self._macro_path(name), load_json(path, []))
        self._refresh_macro_list()
        self._log(f"{self.t('macro_imported')} {name}")

    def export_macro(self):
        name = self._sel_macro()
        if not name: messagebox.showinfo("", self.t("select_first")); return
        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=f"{name}.json",
                                             filetypes=[("JSON", "*.json")])
        if path:
            save_json(path, load_json(self._macro_path(name), []))
            self._log(f"{self.t('macro_exported')} {name}")

    # ─── PROFILES ─────────────────────────────
    def _current_profile(self):
        return {k: getattr(self, k).get() for k in [
            "hours", "minutes", "seconds", "millis", "jitter",
            "pos_x", "pos_y", "max_clicks",
            "repeat_forever", "use_current_pos"
        ]} | {
            "mouse_button": self.mouse_button.get(),
            "click_type": self.click_type.get(),
        }

    def _apply_profile(self, p):
        for k in ["hours", "minutes", "seconds", "millis", "jitter", "pos_x", "pos_y", "max_clicks"]:
            if k in p: getattr(self, k).set(p[k])
        for k in ["repeat_forever", "use_current_pos"]:
            if k in p: getattr(self, k).set(p[k])
        if "mouse_button" in p: self.mouse_button.set(p["mouse_button"])
        if "click_type" in p: self.click_type.set(p["click_type"])

    def _save_profile(self):
        name = self.profile_name.get().strip()
        if not name: messagebox.showinfo("", self.t("profile_req")); return
        self.profiles[name] = self._current_profile()
        save_json(PROFILES_FILE, self.profiles)
        self._refresh_profile_list()
        self._log(f"{self.t('profile_saved')} {name}")

    def _load_profile(self):
        name = self.profile_name.get().strip()
        if name not in self.profiles: messagebox.showinfo("", self.t("profile_notfound")); return
        self._apply_profile(self.profiles[name])
        self._log(f"{self.t('profile_loaded')} {name}")

    def _delete_profile(self):
        name = self.profile_name.get().strip()
        if name in self.profiles:
            del self.profiles[name]
            save_json(PROFILES_FILE, self.profiles)
            self._refresh_profile_list()
            self._log(f"{self.t('profile_deleted')} {name}")

    def _refresh_profile_list(self):
        self.profile_combo["values"] = list(self.profiles.keys())

    # ─── PLAYLIST ─────────────────────────────
    def _playlist_add(self):
        name = self.playlist_add_var.get().strip()
        if name and os.path.exists(self._macro_path(name)):
            self.playlist.append(name)
            self.playlist_listbox.insert(tk.END, name)

    def _playlist_remove(self):
        sel = self.playlist_listbox.curselection()
        if sel:
            self.playlist_listbox.delete(sel[0])
            del self.playlist[sel[0]]

    def _playlist_move(self, d):
        sel = self.playlist_listbox.curselection()
        if not sel: return
        i = sel[0]; ni = i + d
        if 0 <= ni < len(self.playlist):
            self.playlist[i], self.playlist[ni] = self.playlist[ni], self.playlist[i]
            t = self.playlist_listbox.get(i)
            self.playlist_listbox.delete(i)
            self.playlist_listbox.insert(ni, t)
            self.playlist_listbox.selection_set(ni)

    def _toggle_playlist(self):
        if self.playlist_play_thread and self.playlist_play_thread.is_alive():
            self.playlist_stop_flag.set()
            self.playlist_status.set(self.t("status_stopped"))
            self.playlist_toggle_btn.config(text=self.t("play_playlist"))
            self._log(self.t("playlist_stopped"))
        else:
            if not self.playlist: messagebox.showinfo("", self.t("no_playlist")); return
            self.playlist_stop_flag.clear()
            self.playlist_play_thread = threading.Thread(target=self._playlist_worker, daemon=True)
            self.playlist_play_thread.start()
            self.playlist_status.set(self.t("status_playing"))
            self.playlist_toggle_btn.config(text=self.t("stop"))
            self._log(self.t("playlist_started"))

    def _playlist_worker(self):
        for _ in range(self.playlist_repeat.get()):
            if self.playlist_stop_flag.is_set(): break
            for name in self.playlist:
                if self.playlist_stop_flag.is_set(): break
                self.macro.play(load_json(self._macro_path(name), []),
                                speed=self.playlist_speed.get(), repeat=1,
                                stop_flag=self.playlist_stop_flag)
        self.root.after(0, lambda: (
            self.playlist_status.set(self.t("status_stopped")),
            self.playlist_toggle_btn.config(text=self.t("play_playlist")),
            self._log(self.t("playlist_done"))))

    # ─── THEME / LANGUAGE ─────────────────────
    def apply_theme(self, name):
        t = THEMES.get(name, THEMES["Light"])
        self.settings["theme"] = name
        save_json(SETTINGS_FILE, self.settings)
        self.style.theme_use("clam")
        self.style.configure(".", background=t["bg"], foreground=t["fg"])
        self.style.configure("TFrame", background=t["bg"])
        self.style.configure("TLabelframe", background=t["bg"], foreground=t["fg"])
        self.style.configure("TLabelframe.Label", background=t["bg"], foreground=t["fg"])
        self.style.configure("TLabel", background=t["bg"], foreground=t["fg"])
        self.style.configure("TButton", background=t["entry_bg"], foreground=t["fg"])
        self.style.configure("TCheckbutton", background=t["bg"], foreground=t["fg"])
        self.style.configure("TRadiobutton", background=t["bg"], foreground=t["fg"])
        self.style.configure("TNotebook", background=t["bg"])
        self.style.configure("TNotebook.Tab", background=t["entry_bg"], foreground=t["fg"])
        self.style.configure("TEntry", fieldbackground=t["entry_bg"], foreground=t["fg"])
        self.style.configure("TSpinbox", fieldbackground=t["entry_bg"], foreground=t["fg"])
        self.style.configure("TCombobox", fieldbackground=t["entry_bg"], foreground=t["fg"])
        self.canvas.configure(bg=t["bg"])
        self.root.configure(bg=t["bg"])
        if hasattr(self, "log_text"):
            self.log_text.configure(bg=t["log_bg"], fg=t["log_fg"])
        if hasattr(self, "macro_listbox"):
            self.macro_listbox.configure(bg=t["entry_bg"], fg=t["fg"],
                                         selectbackground=t["sel_bg"], selectforeground=t["sel_fg"])
        if hasattr(self, "playlist_listbox"):
            self.playlist_listbox.configure(bg=t["entry_bg"], fg=t["fg"],
                                            selectbackground=t["sel_bg"], selectforeground=t["sel_fg"])

    def _on_lang_change(self, event=None):
        name = self.lang_var.get()
        self.settings["lang"] = name
        save_json(SETTINGS_FILE, self.settings)
        messagebox.showinfo("Language", f"Language set to '{name}'.\nRestart the app to apply.")

    # ─── HOTKEYS ──────────────────────────────
    def _open_hotkey_dialog(self):
        d = tk.Toplevel(self.root)
        d.title(self.t("hotkeys_btn"))
        d.geometry("320x200")
        d.resizable(False, False)
        rows = [
            (self.t("hotkey_clicker"), "hotkey_click"),
            (self.t("hotkey_record"),  "hotkey_record"),
            (self.t("hotkey_play"),    "hotkey_play"),
        ]
        vs = {}
        for i, (lbl, key) in enumerate(rows):
            ttk.Label(d, text=lbl).grid(row=i, column=0, padx=8, pady=8, sticky="w")
            v = tk.StringVar(value=self.settings.get(key, "f6"))
            vs[key] = v
            ttk.Combobox(d, textvariable=v, values=[f"f{i}" for i in range(1, 13)],
                         width=8, state="readonly").grid(row=i, column=1, padx=8)
        def apply():
            for key, v in vs.items():
                self.settings[key] = v.get()
            save_json(SETTINGS_FILE, self.settings)
            messagebox.showinfo("", self.t("hotkeys_saved"))
            d.destroy()
        ttk.Button(d, text=self.t("save"), command=apply).grid(row=3, column=0, columnspan=2, pady=12)

    def _start_global_hotkeys(self):
        ck = self.settings.get("hotkey_click", "f6")
        rk = self.settings.get("hotkey_record", "f7")
        pk = self.settings.get("hotkey_play", "f8")
        def on_press(key):
            try:
                name = key.name if hasattr(key, "name") else None
                if name == ck: self.root.after(0, self.toggle_autoclicker)
                elif name == rk: self.root.after(0, self.toggle_recording)
                elif name == pk: self.root.after(0, self.toggle_playback)
            except Exception:
                pass
        l = keyboard.Listener(on_press=on_press)
        l.daemon = True
        l.start()

    def _start_panic_listener(self):
        def on_press(key):
            if key == Key.esc:
                self.autoclicker.stop()
                self.macro.stop()
                self.play_stop_flag.set()
                if hasattr(self, "playlist_stop_flag"): self.playlist_stop_flag.set()
                self._schedule_cancel.set()
                self.pixel_stop_flag.set()
                self.root.after(0, lambda: (
                    self._log(self.t("stopped_all")),
                    self.click_status.set(self.t("status_stopped")),
                    self.toggle_click_btn.config(text=f"{self.t('start')} ({self.settings.get('hotkey_click','f6').upper()})"),
                    self.rec_status.set(self.t("status_stopped")),
                    self.toggle_rec_btn.config(text=self.t("rec_start")),
                    self.play_status.set(self.t("status_stopped")),
                    self.toggle_play_btn.config(text=f"{self.t('play')} ({self.settings.get('hotkey_play','f8').upper()})"),
                ))
        l = keyboard.Listener(on_press=on_press)
        l.daemon = True
        l.start()

    # ─── MISC ─────────────────────────────────
    def _update_mouse_pos(self):
        x, y = mouse_ctrl.position
        self.mouse_pos_var.set(f"{self.t('mouse_pos')} ({x}, {y})")
        self.root.after(150, self._update_mouse_pos)

    def _hide_window(self):
        self.root.withdraw()

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"[{ts}] {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")

    def _save_log(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log_text.get("1.0", tk.END))
            self._log(f"{self.t('log_saved')} {path}")

    def _toggle_run_on_startup(self):
        if os.name != "nt":
            messagebox.showinfo("", self.t("startup_win_only"))
            self.run_on_startup.set(False)
            return
        startup = os.path.join(os.environ.get("APPDATA",""),
                               "Microsoft","Windows","Start Menu","Programs","Startup")
        bat = os.path.join(startup, "AutoClicker_Pro.bat")
        if self.run_on_startup.get():
            exe = sys.executable if not getattr(sys,"frozen",False) else sys.executable
            path = os.path.abspath(__file__) if not getattr(sys,"frozen",False) else sys.executable
            with open(bat, "w") as f:
                if getattr(sys,"frozen",False):
                    f.write(f'start "" "{path}"\n')
                else:
                    f.write(f'start "" "{exe}" "{path}"\n')
        elif os.path.exists(bat):
            os.remove(bat)

    def _export_full_backup(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                             initialfile="autoclicker_backup.json",
                                             filetypes=[("JSON","*.json")])
        if not path: return
        backup = {"settings": self.settings, "profiles": self.profiles, "macros": {}}
        for fn in os.listdir(MACROS_DIR):
            if fn.endswith(".json"):
                backup["macros"][fn[:-5]] = load_json(os.path.join(MACROS_DIR, fn), [])
        save_json(path, backup)
        self._log(self.t("backup_saved"))

    def _import_full_backup(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path: return
        bk = load_json(path, {})
        self.settings.update(bk.get("settings",{}))
        self.profiles.update(bk.get("profiles",{}))
        save_json(SETTINGS_FILE, self.settings)
        save_json(PROFILES_FILE, self.profiles)
        for name, evs in bk.get("macros",{}).items():
            save_json(self._macro_path(name), evs)
        self._refresh_profile_list()
        self._refresh_macro_list()
        self.apply_theme(self.settings.get("theme","Light"))
        self._log(self.t("backup_loaded"))

    def _on_close(self):
        self.autoclicker.stop()
        self.macro.stop()
        self.play_stop_flag.set()
        if hasattr(self, "playlist_stop_flag"):
            self.playlist_stop_flag.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
