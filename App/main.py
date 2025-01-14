import flet
import keyboard
import ctypes,asyncio
import win32clipboard
import chatapi
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)  # 0: screen width
screen_height = user32.GetSystemMetrics(1)  # 1: screen height

example_text = """
Dastur ishlamoqda
"""
QUERY = None
def get_clipboard_text():
    try:
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

class AnswerField(flet.Text):
    def __init__(self):
        super().__init__()
        self.value=example_text
        self.size=12
        self.color='#00bfa3'
        self.bgcolor = 'transparent'
        
    def did_mount(self):
        self.running = True
        self.page.run_task(self.server_updater)

    def will_unmount(self):
        self.running = False

    def ask_question(self,text):
        global QUERY
        query_id = chatapi.Create_Question(text)
        QUERY = query_id
        self.value = "Javob Kutilmoqda..."
        self.update()
         
    async def server_updater(self):
        global QUERY
        while self.running:
            await asyncio.sleep(3)
            if QUERY!=None:
                res = chatapi.Get_Answer(QUERY)
                if res != 'wait' and res != 'error':
                    self.value = res
                    QUERY = None
                    for i in range(5):
                        self.color = 'white'
                        self.bgcolor = 'red'
                        self.update()
                        await asyncio.sleep(0.3)
                        self.color='#00bfa3'
                        self.bgcolor = 'transparent'
                        self.update()
                        await asyncio.sleep(0.3)

body = flet.Container(
   AnswerField()
   ,expand=True,bgcolor='transparent'
)
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 70
DISPLAY_SIZE = (screen_width,screen_height)

def main(page:flet.Page):
    page.window.width = WINDOW_WIDTH
    page.window.height=WINDOW_HEIGHT
    page.bgcolor='transparent'
    page.window.bgcolor = 'transparent'
    page.window.maximizable = False
    page.window.max_width = WINDOW_WIDTH
    page.window.max_height = WINDOW_HEIGHT
    page.window.frameless = True
    page.window.opacity=0.5
    page.window.title_bar_hidden = True
    page.window.always_on_top = True
    page.window.left = DISPLAY_SIZE[0]-WINDOW_WIDTH
    page.window.top = 0
    page.padding = 0
    page.add(
        body
    )

def on_key_event(e):
    if e.event_type == 'up' and e.name == 'down':
        if body.page.window.minimized:
            body.page.window.minimized=False
        else:
            body.page.window.minimized=True
        body.page.update()
    elif e.event_type == 'up' and e.name == 'right':
        body.content.ask_question(get_clipboard_text())
        body.page.update()

keyboard.hook(on_key_event)
flet.app(main)