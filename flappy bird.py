import tkinter as tk
import tkinter.messagebox as messagebox
import random

class FlappyBird:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.info_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="選單", menu=self.info_menu)
        self.info_menu.add_command(label="版本", command=self.show_version)
        self.info_menu.add_command(label="說明", command=self.show_help)

        self.start_button = tk.Button(self.root, text="開始", command=self.start_game)
        self.start_button.pack()

        self.settings_button = tk.Button(self.root, text="設定", command=self.open_settings)
        self.settings_button.pack()

        self.canvas = tk.Canvas(self.root, width=400, height=600, bg='sky blue')
        self.canvas.pack()

        self.gravity = 1.5
        self.jump_speed = -10
        self.pipe_speed = -5

        self.pipe_width = 80
        self.pipe_gap = 150

        self.speed_var = tk.DoubleVar(value=self.pipe_speed)
        self.gravity_var = tk.DoubleVar(value=self.gravity)
        self.restart_button = None
        self.settings_window = None

        self.canvas.bind('<Button-1>', self.flap)
        self.root.bind('<space>', self.flap)

        self.game_running = False
        self.pipe_interval = 2500  # 增加管子生成間隔時間（毫秒）

    def start_game(self):
        if self.restart_button:
            self.restart_button.destroy()

        self.canvas.delete("all")
        self.bird = self.canvas.create_oval(50, 50, 90, 90, fill='yellow')
        self.bird_speed = 0
        self.score = 0
        self.pipes = []

        self.score_text = self.canvas.create_text(200, 50, text=f"Score: {self.score}", font=('Helvetica', 24), fill='white')
        self.is_flapping = False
        self.game_running = True

        self.create_pipe()
        self.update()

    def open_settings(self):
        if self.settings_window:
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("設定")

        tk.Label(self.settings_window, text="移動速度:").pack()
        tk.Scale(self.settings_window, from_=-10, to=0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.speed_var).pack()
        tk.Label(self.settings_window, text="重力:").pack()
        tk.Scale(self.settings_window, from_=0, to=5, resolution=0.1, orient=tk.HORIZONTAL, variable=self.gravity_var).pack()

        tk.Button(self.settings_window, text="保存", command=self.save_settings).pack()
        tk.Button(self.settings_window, text="關閉", command=self.settings_window.destroy).pack()

        self.settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_close)

    def on_settings_close(self):
        self.settings_window.destroy()
        self.settings_window = None

    def save_settings(self):
        self.pipe_speed = self.speed_var.get()
        self.gravity = self.gravity_var.get()
        self.on_settings_close()

    def flap(self, event=None):
        self.bird_speed = self.jump_speed

    def update(self):
        if not self.game_running:
            return

        self.bird_speed += self.gravity
        self.canvas.move(self.bird, 0, self.bird_speed)

        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] < 0 or bird_coords[3] > 600:
            self.game_over()
            return

        pipes_to_remove = []
        for upper_pipe, lower_pipe in self.pipes:
            self.canvas.move(upper_pipe, self.pipe_speed, 0)
            self.canvas.move(lower_pipe, self.pipe_speed, 0)

            upper_pipe_coords = self.canvas.coords(upper_pipe)
            lower_pipe_coords = self.canvas.coords(lower_pipe)

            if upper_pipe_coords[2] < 0:
                pipes_to_remove.append((upper_pipe, lower_pipe))
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

            if (bird_coords[2] > upper_pipe_coords[0] and bird_coords[0] < upper_pipe_coords[2]) and (
                    bird_coords[3] > lower_pipe_coords[1] or bird_coords[1] < upper_pipe_coords[3]):
                self.game_over()
                return

        for upper_pipe, lower_pipe in pipes_to_remove:
            self.canvas.delete(upper_pipe)
            self.canvas.delete(lower_pipe)
            self.pipes.remove((upper_pipe, lower_pipe))

        self.root.after(30, self.update)

    def create_pipe(self):
        if not self.game_running:
            return

        if self.pipes:
            last_pipe_coords = self.canvas.coords(self.pipes[-1][0])
            if last_pipe_coords[2] > 400 - self.pipe_width * 3:
                self.root.after(100, self.create_pipe)
                return

        pipe_height = random.randint(100, 400)
        upper_pipe = self.canvas.create_rectangle(400, 0, 400 + self.pipe_width, pipe_height, fill='green')
        lower_pipe = self.canvas.create_rectangle(400, pipe_height + self.pipe_gap, 400 + self.pipe_width, 600, fill='green')
        self.pipes.append((upper_pipe, lower_pipe))
        self.root.after(self.pipe_interval, self.create_pipe)

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(200, 300, text="Game Over", font=('Helvetica', 36), fill='red')
        self.restart_button = tk.Button(self.root, text="重生", command=self.start_game)
        self.restart_button.pack()

    def show_version(self):
        messagebox.showinfo("版本", "Flappy Bird v0.5 94bacon 開源專案")

    def show_help(self):
        messagebox.showinfo("說明", "按下畫面或空白鍵跳躍，避免撞到管子。")

root = tk.Tk()
game = FlappyBird(root)
root.mainloop()
