; IME の状態を読み書きする関数と、Esc で IME をオフにする処理
; 関数は keymap.ahk からも使う

IMEGetState() {
	hwnd := WinExist("A")
	imeHwnd := DllCall("imm32.dll\ImmGetDefaultIMEWnd", "Ptr", hwnd, "Ptr")
	imestate := DllCall("user32.dll\SendMessageA", "Ptr", imeHwnd, "UInt", 0x0283, "Int", 0x0005, "Int", 0, "Int")
	return imestate
}

IMESetState(state) {
	hwnd := WinExist("A")
	imeHwnd := DllCall("imm32.dll\ImmGetDefaultIMEWnd", "Ptr", hwnd, "Ptr")
	DllCall("user32.dll\SendMessageA", "Ptr", imeHwnd, "UInt", 0x0283, "Int", 0x0006, "Int", state ? 1 : 0)
}

imeOn() {
	if (IMEGetState() = 0) {
		IMESetState(1)
	}
}

imeOff() {
	if (IMEGetState() = 1) {
		IMESetState(0)
	}
}

; esc押下時にimeオフにする
esc:: {
    imeOff()
    SendInput "{esc}"
}
