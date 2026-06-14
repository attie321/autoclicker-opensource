Dim dir
dir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
CreateObject("WScript.Shell").Run "pythonw """ & dir & "AutoClicker_Pro.py""", 0, False
