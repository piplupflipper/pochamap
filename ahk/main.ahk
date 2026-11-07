#Requires AutoHotkey v2.0
#SingleInstance Force

; 起動するのはこのファイルだけ。各キーマップは #Include で読み込む

; 一度に大量のキーイベントを発生させると警告ポップアップがでるやつの抑制（alt scrollで水平移動するやつのため）
A_MaxHotkeysPerInterval := 9999

; リマップの再帰を無効化
#UseHook True

; pauseキーで一時停止/再開（読み込んだすべてのホットキーが対象）
global isSuspended := false
SuspendToggle() {
    global isSuspended
    isSuspended := !isSuspended
    Suspend(isSuspended)
}
#SuspendExempt
Pause::SuspendToggle()
#SuspendExempt False

#Include %A_ScriptDir%\ime.ahk
#Include %A_ScriptDir%\keymap.ahk
