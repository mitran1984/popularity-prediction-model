import tkinter as tk
from tkinter import ttk, messagebox
from model import predict_popularity

class GamePredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Popularity Predictor")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create chat container
        self.chat_frame = ttk.Frame(root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable chat area
        self.canvas = tk.Canvas(self.chat_frame, bg="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Input fields as chat messages
        self.fields = [
            ("Game Name", "Enter the name of the game"),
            ("Year of Release", "Enter the release year"),
            ("Developer", "Enter the developer name"),
            ("Genre", "Enter the game genre"),
            ("YouTube Likes", "Enter number of YouTube likes"),
            ("Twitter Followers", "Enter number of Twitter followers")
        ]
        
        self.entries = {}
        self.current_field = 0
        
        # Add bot message style
        style = ttk.Style()
        style.configure("Bot.TLabel", background="#e3e3e3", padding=10, borderwidth=1, relief="solid")
        
        # Show first question
        self.show_next_field()
        
        # Create input area
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_entry = ttk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.handle_input)
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind enter key to send
        self.input_entry.bind("<Return>", lambda e: self.handle_input())

    def show_next_field(self):
        if self.current_field < len(self.fields):
            label = ttk.Label(
                self.scrollable_frame,
                text=f"{self.fields[self.current_field][1]}",
                style="Bot.TLabel",
                wraplength=300
            )
            label.pack(anchor="w", padx=5, pady=5)
            self.update_scroll()

    def add_user_message(self, message):
        label = ttk.Label(
            self.scrollable_frame,
            text=message,
            background="#DCF8C6",
            padding=10,
            wraplength=300
        )
        label.pack(anchor="e", padx=5, pady=5)
        self.update_scroll()

    def update_scroll(self):
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def handle_input(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
            
        self.add_user_message(user_input)
        self.entries[self.fields[self.current_field][0]] = user_input
        self.input_entry.delete(0, tk.END)
        
        self.current_field += 1
        
        if self.current_field < len(self.fields):
            self.show_next_field()
        else:
            self.make_prediction()

    def make_prediction(self):
        try:
            result = predict_popularity(
                self.entries["Game Name"],
                int(self.entries["Year of Release"]),
                self.entries["Developer"],
                self.entries["Genre"],
                int(self.entries["YouTube Likes"]),
                int(self.entries["Twitter Followers"])
            )
            
            # Show prediction as bot message
            prediction_label = ttk.Label(
                self.scrollable_frame,
                text=f"Prediction: {result}",
                style="Bot.TLabel",
                wraplength=300
            )
            prediction_label.pack(anchor="w", padx=5, pady=5)
            self.update_scroll()
            
            # Disable input after prediction
            self.input_entry.configure(state="disabled")
            self.send_button.configure(state="disabled")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = GamePredictionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

