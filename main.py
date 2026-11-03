import machine
import utime
import urandom
from ssd1306 import SSD1306_I2C

# ==========================================
# 1. HARDWARE SETUP
# ==========================================
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

btn_start_end = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
btn_home      = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
btn_add       = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
btn_sub       = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

# ==========================================
# 2. VARIABLES & STATES
# ==========================================
state = "HOME"
daily_total_sec = 0
target_sec = 25 * 60
time_left = 0
elapsed_sec = 0
MAX_TIME = 10800  # 3 hours max

b4_presses = 0
b4_last_time = 0

# ==========================================
# 3. GRAPHICS & HELPER FUNCTIONS
# ==========================================
def format_hours(seconds):
    return round(seconds / 3600, 2)

def format_mm_ss(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def draw_tree(stage):
    """Draws a geometric tree on the left side of the screen based on the stage."""
    oled.hline(0, 55, 60, 1) # Draw the ground
    
    if stage == 0:
        # Seed
        oled.fill_rect(28, 53, 4, 2, 1)
    elif stage == 1:
        # Sprout
        oled.vline(30, 45, 10, 1)
        oled.hline(28, 45, 5, 1)
    elif stage == 2:
        # Sapling
        oled.fill_rect(29, 35, 3, 20, 1) # Trunk
        oled.fill_rect(22, 25, 17, 10, 1) # Leaves
    elif stage == 3:
        # Full Tree
        oled.fill_rect(28, 25, 5, 30, 1) # Thick Trunk
        oled.fill_rect(15, 10, 30, 20, 1) # Big Canopy

def draw_withered_tree():
    """Draws a dead, bent tree."""
    oled.hline(0, 55, 60, 1) # Ground
    oled.line(30, 55, 25, 40, 1) # Bent trunk
    oled.line(25, 40, 15, 35, 1) # Broken branch
    oled.line(25, 40, 35, 30, 1) # Broken branch

def draw_confetti():
    """Draws 30 random pixels across the screen."""
    for _ in range(30):
        x = urandom.getrandbits(7) % 128
        y = urandom.getrandbits(6) % 64
        oled.pixel(x, y, 1)

def update_display():
    oled.fill(0)
    
    if state == "HOME":
        oled.text(f"Today: {format_hours(daily_total_sec)}h", 0, 0)
        oled.text("Set Time:", 0, 20)
        oled.text(f"{target_sec // 60} Mins", 35, 35)
        oled.text("Press B1 ->", 0, 55)
        
    elif state == "RUNNING":
        # Calculate growth stage (0 to 3) based on time elapsed
        progress = elapsed_sec / target_sec
        if progress < 0.25:
            stage = 0
        elif progress < 0.60:
            stage = 1
        elif progress < 0.90:
            stage = 2
        else:
            stage = 3
            
        draw_tree(stage)
        
        # Draw text on the right side
        oled.text("LOCK IN", 65, 20)
        oled.text(format_mm_ss(time_left), 65, 35)
        
    elif state == "FINISHED":
        draw_confetti()
        draw_tree(3) # Show fully grown tree
        oled.text("YAY!", 65, 10)
        oled.text("You did", 60, 30)
        oled.text(f"{format_hours(target_sec)}h", 65, 45)
        
    elif state == "FAILED":
        draw_withered_tree()
        # 16 char max per line on 128x64 display
        oled.text("You", 60, 10)
        oled.text("withered", 60, 20)
        oled.text("a tree,", 60, 30)
        oled.text("monster!", 60, 40)
        
    oled.show()

def debounce():
    utime.sleep_ms(200)

update_display()
last_timer_tick = utime.ticks_ms()

# ==========================================
# 4. MAIN LOOP
# ==========================================
while True:
    current_time = utime.ticks_ms()
    
    # BUTTON 1: START / END
    if not btn_start_end.value():
        if state == "HOME":
            state = "RUNNING"
            time_left = target_sec
            elapsed_sec = 0
            last_timer_tick = utime.ticks_ms()
            
        elif state == "RUNNING":
            if elapsed_sec < 600: 
                state = "FAILED"
            else: 
                daily_total_sec += elapsed_sec
                target_sec = elapsed_sec 
                state = "FINISHED"
                
        update_display()
        debounce()

    # BUTTON 2: HOME SCREEN
    if not btn_home.value():
        if state in ["RUNNING", "FINISHED", "FAILED"]:
            state = "HOME"
            update_display()
        debounce()

    # BUTTON 3: ADD 10 MINS (MAX 3 HOURS)
    if not btn_add.value():
        if state == "HOME":
            if target_sec < MAX_TIME:
                target_sec += 600 
            update_display()
        debounce()

    # BUTTON 4: SUB 10 MINS & LOG DATA
    if not btn_sub.value():
        if utime.ticks_diff(current_time, b4_last_time) < 1500:
            b4_presses += 1
        else:
            b4_presses = 1 
            
        b4_last_time = current_time

        if b4_presses == 3:
            print(f"Today's Study Hours: {format_hours(daily_total_sec)} hours")
            oled.fill(0)
            oled.text("DATA LOGGED!", 15, 30)
            oled.show()
            utime.sleep(1.5)
            b4_presses = 0 
            update_display()
        else:
            if state == "HOME":
                if target_sec >= 600:
                    target_sec -= 600
                update_display()
        debounce()

    # TIMER COUNTDOWN
    if state == "RUNNING":
        if utime.ticks_diff(current_time, last_timer_tick) >= 1000:
            time_left -= 1
            elapsed_sec += 1
            last_timer_tick = current_time
            
            # Animate Confetti natively during countdown if you want, but sticking to tree for now
            update_display()
            
            if time_left <= 0:
                daily_total_sec += target_sec
                state = "FINISHED"
                update_display()
