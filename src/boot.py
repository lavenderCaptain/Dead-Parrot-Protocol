import board
import digitalio
import storage
import usb_cdc
import usb_midi
import usb_hid
import supervisor

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.UP)

if button.value:
    # 1. Hide the Drive and Serial Console
    storage.disable_usb_drive()
    usb_cdc.disable()

    # 2. Kill MIDI
    usb_midi.disable()

    # 3. Kill Audio (Wrap in try/except as some firmware versions lack this module)
    try:
        import usb_audio

        usb_audio.disable()
    except ImportError:
        pass

    # 4. Spoof Logitech Receiver
    supervisor.set_usb_identification(
        vid=0x046D,
        pid=0xC52B,
        manufacturer="Logitech",
        product="USB Receiver"
    )
