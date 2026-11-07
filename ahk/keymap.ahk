; ワンショットモディファイヤ -----------------------------------------------------------------
; 変換キー（右）の修飾キー化
$vk1C::
{
	startTime := A_TickCount
	KeyWait("vk1C", "T0.5")
	keyPressDuration := A_TickCount - startTime
	; 変換を押している間に他のホットキーが発動した場合は入力しない
	; 変換を長押ししていた場合も入力しない
	If (A_ThisHotkey == "$vk1C" and keyPressDuration < 200) {
        SendInput "{Blind}{vk1C}"
		imeOn()
	}
    SendInput "{vk1C Up}"
	Return
}

; 無変換キー（左）の修飾キー化
$vk1D::
{
	startTime := A_TickCount
	KeyWait("vk1D", "T0.5")
	keyPressDuration := A_TickCount - startTime
	; 無変換を押している間に他のホットキーが発動した場合は入力しない
	; 無変換を長押ししていた場合も入力しない
	If (A_ThisHotkey == "$vk1D" and keyPressDuration < 200) {
        SendInput "{Blind}{vk1D}"
		imeOff()
	}
    SendInput "{vk1D Up}"
	Return
}

; 変換（右）同時押しのキーマップ ----------------------------------------------------------------------------
~vk1C & a:: SendInput "{Blind}{@}" ; atmark
~vk1C & b:: SendInput "{Blind}{``}" ; back quote
~vk1C & c:: SendInput "{Blind}{^}" ; caret
~vk1C & d:: SendInput "{Blind}{$}" ; dollar
~vk1C & e:: SendInput "{Blind}{&}" ; et
~vk1C & f:: SendInput "{Blind}{(}" ; left
~vk1C & h:: SendInput "{Blind}{#}" ; hash
~vk1C & i:: SendInput "{Blind}{!}" ; 似てる
~vk1C & j:: SendInput "{Blind}{)}" ; right
~vk1C & l:: SendInput "{Blind}{|}" ; 似てる
~vk1C & m:: SendInput "{Blind}{+}" ; more
~vk1C & p:: SendInput "{Blind}{`%}" ; percentage
~vk1C & q:: SendInput "{Blind}{?}" ; question
~vk1C & s:: SendInput "{Blind}{'}" ; single quote
~vk1C & t:: SendInput "{Blind}{~}" ; tilde
~vk1C & u:: SendInput "{Blind}{_}" ; underscore
~vk1C & w:: SendInput '{Blind}{"}' ; double quote
~vk1C & x:: SendInput "{Blind}{*}" ; multiple

; 無変換（左）同時押しのキーマップ -----------------------------------------------------------------------------
~vk1D & H:: SendInput "{Blind}{Left}"
~vk1D & J:: SendInput "{Blind}{Down}"
~vk1D & K:: SendInput "{Blind}{Up}"
~vk1D & L:: SendInput "{Blind}{Right}"

~vk1D & w:: SendInput "{Blind}{Up}"
~vk1D & a:: SendInput "{Blind}{Left}"
~vk1D & s:: SendInput "{Blind}{Down}"
~vk1D & d:: SendInput "{Blind}{Right}"

; リマップ ----------------------------------------------------------------------------------------------------
VkF3:: SendInput "{Backspace}" ; imeToggle::Backspace
VkF4:: SendInput "{Backspace}" ; imeToggle::Backspace
+vkF3:: SendInput "{Delete}" ; imeToggle::Delete
+vkF4:: SendInput "{Delete}" ; imeToggle::Delete
^vkF3:: SendInput "{Delete}" ; imeToggle::Delete
^vkF4:: SendInput "{Delete}" ; imeToggle::Delete

VkF0:: SendInput "{Enter}" ; Caps::Enter
Vk14:: SendInput "{Enter}" ; Caps::Enter
^vkF0:: SendInput "^{Enter}" ; C-Caps::C-Enter
^vk14:: SendInput "^{Enter}" ; C-Caps::C-Enter
+vkF0:: SendInput "+{Enter}" ; S-Caps::S-Enter
+vk14:: SendInput "+{Enter}" ; S-Caps::S-Enter
!vkF0:: SendInput "!{Enter}" ; A-Caps::A-Enter
!vk14:: SendInput "!{Enter}" ; A-Caps::A-Enter

@:: SendInput "{Backspace}" ; Atmark::Backspace
^@:: SendInput "{Delete}" ; C-Atmark::Delete
+@:: SendInput "{Delete}" ; S-Atmark::Backspace

vkBA:: SendInput "{Enter}" ; Colon(Raw-keyboard)::Enter
^vkBA:: SendInput "^{Enter}" ; C-Colon(Raw-keyboard)::C-Enter
+vkBA:: SendInput "+{Enter}" ; S-Colon(Raw-keyboard)::S-Enter
!vkBA:: SendInput "!{Enter}" ; A-Colon(Raw-keyboard)::A-Enter
^+vkBA:: SendInput "^+{Enter}" ; C-S-Colon(Raw-keyboard)::C-S-Enter

vkBB:: SendInput "{vkBA}" ; Semicolon(raw-keyboard)::Colon
^vkBB:: SendInput "^{vkBA}" ; C-Semicolon(raw-keyboard)::C-Colon
+vkBB:: SendInput "{vkBB}" ; S-Semicolon(raw-keyboard)::Semicolon
!vkBB:: SendInput "!{vkBB}" ; S-Semicolon(raw-keyboard)::Semicolon
^+vkBB:: SendInput "^+{vkBA}" ; C-S-Semicolon(raw-keyboard)::C-S-Colon

+/:: SendInput "{\}" ; S-Slash::Backslash

; alt-tabでタスク切換えしてるときのキーバインドをvim likeに
#HotIf WinActive("ahk_exe explorer.exe")
!h:: SendInput "{Blind}{Left}"
!j:: SendInput "{Blind}{Down}"
!k:: SendInput "{Blind}{Up}"
!l:: SendInput "{Blind}{Right}"
#HotIf

; ---------------------------------------------------------------------------------------
; エスケープ
^j:: {
	imestate := IMEGetstate()
	if (imestate = 1) {
		SendInput "{vkF3}"
	}
	SendInput "{Esc}"
}

; alt scrollで水平移動、ただし入力速度が速いと暴発する
!WheelDown:: SendInput "{WheelRight}"
!WheelUp:: SendInput "{WheelLeft}"
