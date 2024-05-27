import ttkbootstrap as tb
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ttkbootstrap.dialogs import Messagebox
from utils.config import project_config as pjcf
from core import logic_handler, ui_handler

controller = logic_handler.Model_Controller(
    pjcf.MODEL_PATH1, pjcf.MODEL_PATH2, pjcf.MODEL_PATH3
)
saver = logic_handler.Saver()
root = tb.Window(themename="darkly")
root.eval("tk::PlaceWindow . center")
root.title("Pneumonoia Detection")
root.iconbitmap(pjcf.MAIN_ICON_PATH)
root.geometry(pjcf.SIZE_MAIN)
root.resizable(False, False)
ui_handler.center_window(root)

# Setup frame
name_frame = tb.Frame(root)
name_frame.pack(side=TOP, padx=20, pady=5, ipadx=5, ipady=5)

buttons_frame = tb.Frame(root)
buttons_frame.pack(side=RIGHT, padx=20, pady=5, ipadx=5, ipady=5)

img_frame = tb.Frame(root)
img_frame.pack(side=LEFT, padx=20, pady=5, ipadx=5, ipady=5)


#########FRAME BUTTON
## Info button
def open_info():
    ui_handler.PDFViewer(root)


info_btn = tb.Button(
    buttons_frame, text="INFO", bootstyle=(INFO, OUTLINE), width=30, command=open_info
)
info_btn.pack(pady=15, ipadx=20, ipady=10)


## Upload button
def open_image():
    file_path = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        saver.refresh_saver()
        saver.img = Image.open(file_path)
        saver.original_img = cv2.imread(file_path)
        saver.img = saver.img.resize((900, 640), Image.LANCZOS)
        img_label.image = ImageTk.PhotoImage(saver.img)
        img_label.config(image=img_label.image)


upload_btn = tb.Button(
    buttons_frame,
    text="UPLOAD",
    bootstyle=(WARNING, OUTLINE),
    width=30,
    command=open_image,
)
upload_btn.pack(pady=15, ipadx=20, ipady=10)


# Menu button
model_menu_btn = tb.Menubutton(
    buttons_frame,
    text="                     MODEL : NONE",
    bootstyle=(SUCCESS, OUTLINE),
    width=26,
)
model_menu_btn.pack(pady=15, ipadx=20, ipady=10)

model_menu = tb.Menu()
item_var = tb.StringVar()


def change_model(model):
    model_menu_btn.config(text="               MODEL : " + model)
    saver.model_name = model


for x in ["CNN", "CNN_LSTM", "CNN_RNN"]:
    model_menu.add_radiobutton(
        label=x, variable=item_var, command=lambda model=x: change_model(model)
    )

# Associate the menu with the menu button
model_menu_btn.config(menu=model_menu)


## Predict button
def predict():
    if saver.img is None:
        Messagebox.show_error("No image to predict!\nUpload image first.", "Error")
    elif saver.model_name is None:
        Messagebox.show_error("Please select a model.", "Error")
    else:
        result = controller.predict(saver.model_name, saver.original_img)
        saver.predict_img = saver.img.convert("RGB")
        draw = ImageDraw.Draw(saver.predict_img)
        font = ImageFont.truetype("arial.ttf", 20)
        text = None
        if result == 0:
            text = "MODEL : " + saver.model_name + "\nPREDICTION: PNEUMONIA"
            draw.text((15, 15), text, fill=pjcf.RED, font=font, bold=True)
        elif result == 1:
            text = "MODEL : " + saver.model_name + "\nPREDICTION: NORMAL"
            draw.text((15, 15), text, fill=pjcf.GREEN, font=font, bold=True)

        img_label.image = ImageTk.PhotoImage(saver.predict_img)
        img_label.config(image=img_label.image)


predict_btn = tb.Button(
    buttons_frame,
    text="PREDICT",
    bootstyle=(WARNING, OUTLINE),
    width=30,
    command=predict,
)
predict_btn.pack(pady=15, ipadx=20, ipady=10)


## Save result
def save_image():
    if saver.img is None:
        Messagebox.show_error("No image to save!\nUpload image first.", "Error")
    elif saver.predict_img is None:
        Messagebox.show_warning("Not predict yet.", "Warning")
    else:
        file_path = asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            resized_img = saver.predict_img.resize(saver.original_img.shape[:2][::-1])
            resized_img.save(file_path, format="png")
            Messagebox.ok(
                "Save predicted image successfully!", "Save successfully", True
            )


save_btn = tb.Button(
    buttons_frame,
    text="SAVE RESULT",
    bootstyle=(SUCCESS, OUTLINE),
    width=30,
    command=save_image,
)
save_btn.pack(pady=15, ipadx=20, ipady=10)
##Exit btn
exit_btn = tb.Button(
    buttons_frame,
    text="EXIT",
    bootstyle=(DANGER, OUTLINE),
    command=root.destroy,
    width=30,
)
exit_btn.pack(pady=15, ipadx=20, ipady=10)

#########FRAME IMG
img_label = tb.Label(img_frame, justify=CENTER, text="None")
img_label.pack()
#########FRAME NAME
var = tb.StringVar()
label = tb.Label(name_frame, textvariable=var, font=(None, 25), justify=CENTER)
var.set("PNEUMONIA DETECTION USING DEEP LEARNING")
label.pack()

root.mainloop()
