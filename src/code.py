import time
import board
import digitalio
import analogio
import pwmio
import usb_hid
import random
import math
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

COMMON_ANODE = True

# --- Hardware Setup ---
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

potentiometer = analogio.AnalogIn(board.GP26)
button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.UP)
sound_btn = digitalio.DigitalInOut(board.GP14)
sound_btn.switch_to_input(pull=digitalio.Pull.UP)

sound_led = digitalio.DigitalInOut(board.GP13)
sound_led.switch_to_output()
active_buzzer = digitalio.DigitalInOut(board.GP9)
active_buzzer.switch_to_output()
passive_buzzer = pwmio.PWMOut(board.GP16, variable_frequency=True)

led_r = pwmio.PWMOut(board.GP18, frequency=5000)
led_g = pwmio.PWMOut(board.GP19, frequency=5000)
led_b = pwmio.PWMOut(board.GP20, frequency=5000)

bar_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
            board.GP5, board.GP6, board.GP7, board.GP8, board.GP10]
bar_leds = [digitalio.DigitalInOut(pin) for pin in bar_pins]
for led in bar_leds: led.switch_to_output()

# --- State Engines ---
rgb_state = "off"
current_color = [0.0, 0.0, 0.0]
target_color = [0.0, 0.0, 0.0]
cylon_phase = 0.0
last_cylon_time = time.monotonic()


class Brain:
    def __init__(self):
        self.history = []
        self.current_subject = None
        self.sentences_in_topic = 0

        self.subjects = [
            "the CI/CD pipeline", "that DEC RM03P disk pack", "the corporate EDR heuristics",
            "the Shinkansen schedule", "that 35mm prime lens", "the new fish tank stand",
            "agile methodologies", "the Z80 instruction set", "the risk compliance mandate",
            "the legacy mainframe integration", "a proper dovetail joint", "surface mount soldering",
            "recovering partition tables from a dead drive", "the firmware payload",
            "the route to Halifax", "the insurance sector's tech debt",
            "the wood glue curing time", "the ISO performance on that sensor",
            "the Tokyo subway map", "the 8-bit bus architecture", "the Q3 delivery targets", "Peter the parrot", "FileNet"
        ]

        self.verbs = [
            "is fundamentally incompatible with", "somehow relates to",
            "needs to be refactored for", "completely disrupts", "reminds me of",
            "completely bottlenecks", "is an absolute nightmare for",
            "fundamentally shifts the paradigm of", "creates unnecessary friction with",
            "somehow bypasses", "requires a complete teardown of", "makes you rethink",
            "is basically the exact same thing as", "adds way too much latency to",
            "completely nullifies the point of", "could really optimize"
        ]

        self.objects = [
            "legacy banking mainframes", "the software delivery lifecycle",
            "a proper depth of field", "the next trip to Kyoto",
            "vintage hardware restoration", "the constraints of 8-bit memory",
            "the structural integrity of the stand", "the Kansai region transit pass",
            "the entire deployment pipeline", "the data recovery process",
            "the compliance audit", "a long exposure shot",
            "the East Coast road trip itinerary", "the production environment",
            "the replacement capacitors", "the reverse-engineering process"
        ]

        self.tangents = [
            "Need to check the exchange rate again.",
            "Wonder if I have enough fabric to reupholster that chair.",
            "Maybe a road trip to Halifax is the answer.",
            "Coffee is basically keeping this whole thing running.",
            "Wonder if I have the right router bit for this.",
            "Need to order more flux and solder wick.",
            "Could really go for some BBQ ribs right now.",
            "That Halifax drive was brutal but absolutely worth it.",
            "Need to practice my Kanji reading.",
            "I should probably back up the NAS tonight.",
            "Can't decide between the 35mm or the 50mm lens.",
            "Honestly, the kids are growing up too fast.",
            "Still need to figure out that seating upholstery.",
            "Hoping those replacement capacitors arrive soon.",
            "I really need to clear off my workbench."
        ]

        self.fragments = [
            "Typical.", "Fascinating.", "Absolute disaster.", "Whatever works.",
            "Classic.", "Unbelievable.", "So it goes.", "Agile, right?",
            "Needs more flux.", "RTFM.", "Just reboot it.", "Scope creep.",
            "Dead on arrival.", "Management.", "Perfect."
        ]

    def get_unique(self, word_list):
        for _ in range(5):
            w = random.choice(word_list)
            if w not in self.history:
                self.history.append(w)
                if len(self.history) > 15: self.history.pop(0)
                return w
        return random.choice(word_list)

    def generate_paragraph(self):
        sentences = []
        num_sentences = random.randint(2, 4)

        for i in range(num_sentences):
            # Tangents
            if random.random() < 0.12:
                sentences.append(f"(Side note: {self.get_unique(self.tangents)})")
                continue

            # Fragments
            if random.random() < 0.15:
                sentences.append(self.get_unique(self.fragments))
                continue

            # Core Sentences
            if self.current_subject is None or self.sentences_in_topic > random.randint(1, 3):
                self.current_subject = self.get_unique(self.subjects)
                self.sentences_in_topic = 1

                # Notice the trailing spaces are removed from these strings now
                intros = ["Thinking about how", "Reviewing the specs,", "I was just analyzing why", "Honestly,"]
                intro = random.choice(intros)

                sentences.append(
                    f"{intro} {self.current_subject} {self.get_unique(self.verbs)} {self.get_unique(self.objects)}.")
            else:
                self.sentences_in_topic += 1
                pronoun = "It" if not self.current_subject.endswith('s') else "They"
                verb = self.get_unique(self.verbs)
                obj = self.get_unique(self.objects)

                if random.random() < 0.5:
                    sentences.append(f"In a way, {pronoun.lower()} {verb} {obj}.")
                else:
                    sentences.append(f"{pronoun} just {verb} {obj}.")

        # 1. Join all the sentences perfectly with a single space
        paragraph_text = " ".join(sentences)

        # 2. Add the 20% chance of a Tab indent at the very beginning
        if random.random() < 0.2:
            paragraph_text = "\t" + paragraph_text

        # 3. Return the fully formatted block with the double Enter
        return paragraph_text + "\n\n"


brain = Brain()
typo_map = {'a': 's', 's': 'd', 'd': 'f', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
            'n': 'm', 'm': ','}


# --- Hardware Animation Functions ---
def update_rgb(t):
    global current_color, target_color
    if rgb_state == "rainbow":
        target_color = [(math.sin(t) + 1.0) / 2.0, (math.sin(t + 2.094) + 1.0) / 2.0, (math.sin(t + 4.188) + 1.0) / 2.0]
    elif rgb_state == "armed":
        target_color = [1.0, 0.0, 0.0]
    elif rgb_state == "typing":
        target_color = [0.0, 1.0, 0.0]
    elif rgb_state == "thinking":
        target_color = [0.0, 0.0, 1.0]
    else:
        target_color = [0.0, 0.0, 0.0]

    for i in range(3): current_color[i] += (target_color[i] - current_color[i]) * 0.08
    intensity = (math.sin(t * 4) + 1.2) / 2.2 if rgb_state in ["armed", "typing", "thinking"] else 1.0

    r_val = int(current_color[0] * intensity * 65535)
    g_val = int(current_color[1] * intensity * 65535)
    b_val = int(current_color[2] * intensity * 65535)

    if COMMON_ANODE:
        led_r.duty_cycle, led_g.duty_cycle, led_b.duty_cycle = 65535 - r_val, 65535 - g_val, 65535 - b_val
    else:
        led_r.duty_cycle, led_g.duty_cycle, led_b.duty_cycle = r_val, g_val, b_val


def clear_bar():
    for led in bar_leds: led.value = False


def anim_cylon(t):
    global cylon_phase, last_cylon_time
    dt = t - last_cylon_time
    last_cylon_time = t
    if dt > 0.1: dt = 0.02

    clear_bar()
    pot_factor = potentiometer.value / 65535.0
    speed = 1.0 + (pot_factor * 11.0)
    cylon_phase += speed * dt

    pos = max(0, min(9, int((math.sin(cylon_phase) + 1.0) / 2.0 * 9.0)))
    bar_leds[pos].value = True
    if pos > 0: bar_leds[pos - 1].value = True
    if pos < 9: bar_leds[pos + 1].value = True


def anim_typing():
    for led in bar_leds: led.value = random.random() > 0.7


def anim_countdown(start_t, duration, current_t):
    clear_bar()
    for i in range(min(int(((current_t - start_t) / duration) * 10), 10)): bar_leds[i].value = True


def click_key():
    if sound_mode:
        active_buzzer.value = True
        time.sleep(0.005)
        active_buzzer.value = False


def active_delay(duration, mode="cylon"):
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        t = time.monotonic()
        update_rgb(t)
        if mode == "cylon":
            anim_cylon(t)
        elif mode == "typing":
            anim_typing()
        elif mode == "thinking":
            anim_countdown(start_time, duration, t)
            if random.random() < 0.02: mouse.move(x=random.randint(-3, 3), y=random.randint(-3, 3))
        if not button.value: return False
        time.sleep(0.02)
    return True


def move_mouse_arc(dx, dy, steps=40):
    current_x, current_y = 0.0, 0.0
    dist = max(1, math.sqrt(dx * dx + dy * dy))
    curve_amp = random.uniform(-0.4, 0.4) * dist
    perp_x, perp_y = -dy / dist, dx / dist

    for i in range(1, steps + 1):
        t = i / steps
        arc_factor = 4 * t * (1 - t) * curve_amp
        ideal_x = (dx * t) + (perp_x * arc_factor)
        ideal_y = (dy * t) + (perp_y * arc_factor)

        move_x, move_y = int(ideal_x - current_x), int(ideal_y - current_y)
        if move_x != 0 or move_y != 0:
            move_x, move_y = max(-127, min(127, move_x)), max(-127, min(127, move_y))
            mouse.move(x=move_x, y=move_y)
            current_x += move_x
            current_y += move_y

        update_rgb(time.monotonic())
        anim_cylon(time.monotonic())
        time.sleep(random.uniform(0.008, 0.025))


def play_mario():
    notes = [(659, 0.15), (0, 0.05), (659, 0.15), (0, 0.15), (659, 0.15), (0, 0.15), (523, 0.15), (659, 0.15),
             (0, 0.15), (784, 0.3), (0, 0.3), (392, 0.3)]
    for freq, duration in notes:
        update_rgb(time.monotonic())
        if freq == 0:
            passive_buzzer.duty_cycle = 0
        else:
            passive_buzzer.frequency, passive_buzzer.duty_cycle = freq, 32768
        time.sleep(duration)
    passive_buzzer.duty_cycle = 0


# --- Main Loop ---
typing_mode = False
sound_mode = False
last_button_state = True
last_sound_btn_state = True
last_jiggle_time = time.monotonic()

while True:
    current_time = time.monotonic()
    pot_val = potentiometer.value
    update_rgb(current_time)

    current_sound_btn = sound_btn.value
    if last_sound_btn_state and not current_sound_btn:
        sound_mode = not sound_mode
        sound_led.value = sound_mode
        time.sleep(0.2)
    last_sound_btn_state = current_sound_btn

    current_button_state = button.value
    if last_button_state and not current_button_state:
        typing_mode = not typing_mode
        clear_bar()
        if typing_mode:
            rgb_state = "armed"
            play_mario()
        time.sleep(0.3)
    last_button_state = current_button_state

    if typing_mode:
        paragraph = brain.generate_paragraph()
        rgb_state = "typing"

        i = 0
        while i < len(paragraph):
            if not typing_mode: break
            char = paragraph[i]

            # --- Formatting Delays ---
            # Pauses slightly longer after hitting Enter or Tab, like a real human hand
            if char == '\n' or char == '\t':
                layout.write(char);
                click_key()
                if not active_delay(random.uniform(0.3, 0.8), mode="typing"): break
                i += 1
                continue

            # --- The "Fat Finger Enter" Simulator ---
            # 1% chance to accidentally hit Enter instead of a quote or bracket
            if random.random() < 0.01 and char in ["'", '"', "]", "[", "\\"]:
                keyboard.send(Keycode.ENTER);
                click_key()
                if not active_delay(random.uniform(0.4, 0.9), mode="typing"): break  # Stare at the screen
                keyboard.send(Keycode.BACKSPACE);
                click_key()  # Delete the accidental new line
                if not active_delay(0.2, mode="typing"): break

            # --- Mid-Sentence Pause Simulator ---
            if char == ' ' and random.random() < 0.05:
                rgb_state = "thinking"
                if not active_delay(random.uniform(1.0, 3.5), mode="thinking"): break
                rgb_state = "typing"

            # --- Advanced Transposition Typo ---
            if random.random() < 0.015 and i < len(paragraph) - 1 and paragraph[i].isalpha() and paragraph[
                i + 1].isalpha():
                layout.write(paragraph[i + 1]);
                click_key()
                layout.write(paragraph[i]);
                click_key()
                if not active_delay(0.5, mode="typing"): break
                keyboard.send(Keycode.BACKSPACE);
                click_key();
                active_delay(0.1, mode="typing")
                keyboard.send(Keycode.BACKSPACE);
                click_key();
                active_delay(0.1, mode="typing")
                layout.write(paragraph[i]);
                click_key()
                layout.write(paragraph[i + 1]);
                click_key()
                i += 2
                continue

            # --- Standard Adjacent Key Typo ---
            char_lower = char.lower()
            if char_lower in typo_map and random.random() < 0.02:
                layout.write(typo_map[char_lower]);
                click_key()
                if not active_delay(0.3, mode="typing"): break
                keyboard.send(Keycode.BACKSPACE);
                click_key()
                if not active_delay(0.1, mode="typing"): break

            layout.write(char)
            click_key()
            if not active_delay(random.uniform(0.03, 0.12), mode="typing"): typing_mode = False
            i += 1

        if typing_mode:
            rgb_state = "thinking"
            if not active_delay(random.uniform(3.0, 10.0), mode="thinking"): typing_mode = False

        if not typing_mode:
            clear_bar()
            rgb_state = "rainbow" if pot_val > 5000 else "off"

    else:
        if pot_val > 5000:
            rgb_state = "rainbow"
            anim_cylon(current_time)
            interval = 5 + ((65535 - pot_val) / 60535) * 25

            if current_time - last_jiggle_time > interval:
                target_x, target_y = random.randint(-500, 500), random.randint(-300, 300)
                move_mouse_arc(target_x, target_y, steps=random.randint(30, 60))
                last_jiggle_time = current_time
        else:
            rgb_state = "off"
            clear_bar()
            time.sleep(0.1)
