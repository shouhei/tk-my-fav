import tkinter as tk
from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk
from urllib import request
from typing import List
from webbrowser import open_new_tab
from lib.datasource.twitter import Twitter
from config.twitter import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from lib.datasource.hatena import Hatena
from config.hatena import USER_NAME
from lib.data_source_manager import DataSourceManager
from lib.cell_data import CellData


class LabelListManager(object):
    """
    List[CellData]をtk.Labelでリスト表示するクラス
    """
    def __init__(self, frame: tk.Frame, data: List[CellData]=None, initial_row: int=2):
        """
        :param tk.Frame frame: tkのフレーム
        :param List[CellData] data: CellDataの入ったリスト
        :param int initial_row: データをリスト表示する際の初期位置
        """
        self.__frame = frame
        self.__initial_row = initial_row
        if data:
            self.update(data)

    def update(self, data):
        """
        :param List[CellData] data:
        """
        row_num = self.__initial_row
        for row in data:
            BindLabel.text(self.__frame, row, row_num)
            # 以下URLから取得した画像を表示するラベル
            if row.image:
                BindLabel.image(self.__frame, row, row_num)
            row_num += 1


class BindLabel(object):
    """
    tk.Frameとデータを受けてLabelを作成するクラス
    """
    TEXT_COLUMN_NUMBER = 1
    IMAGE_COLUMN_NUMBER = 2

    @staticmethod
    def text(frame: tk.Frame, data: CellData, row_number: int, column_number: int=TEXT_COLUMN_NUMBER):
        """
        CellDataのテキストを利用し、フレームにLabelを表示する

        :param tk.Frame frame: tkのフレームオブジェクト
        :param CellData data:  CellData
        :param int row_number: 何行目に表示するか
        :param column_number:
        """
        label = tk.Label(frame, text=data.text, anchor=tk.W, justify=tk.LEFT, wraplength=300)
        label.grid(row=row_number, column=1, sticky=tk.W)
        if data.url:
            label.bind("<Button-1>", lambda e, url=data.url: open_new_tab(url))

    @staticmethod
    def image(frame: tk.Frame, data: CellData, row_number: int, column_number: int=IMAGE_COLUMN_NUMBER):
        """
        CellDataのimageを利用し、フレームにLabelを表示する

        :param tk.Frame frame: tkのフレームオブジェクト
        :param CellData data:  CellData
        :param int row_number: 何行目に表示するか
        :param column_number:
        """
        tmp_image, header = request.urlretrieve(data.image)
        img = PILImage.open(tmp_image)
        # 200 = x * image.width
        rate = 200 / img.width
        resize_height = int(img.height * rate)
        # rezizeのタプルは 幅 * 高さ
        photo_img = PILImageTk.PhotoImage(img.resize((200, resize_height)))
        img_label = tk.Label(frame, image=photo_img, width=200, height=resize_height)
        # 2度挿入しないと駄目？
        img_label.image = photo_img
        img_label.grid(row=row_number, column=column_number, sticky=tk.W)


class TkMyFav(tk.Frame):
    def __init__(self, root: tk.Tk, data_source: DataSourceManager):
        self.__data_source = data_source
        tk.Frame.__init__(self, root)
        self.__canvas = tk.Canvas(root, borderwidth=0, width=500, height=500)
        self.__frame = tk.Frame(self.__canvas)
        self.__vsb = tk.Scrollbar(root, orient="vertical", command=self.__canvas.yview)
        self.__canvas.bind('<MouseWheel>', lambda e: self.__canvas.yview_scroll(-1*(1 if e.delta > 0 else -1), tk.UNITS))
        self.__canvas.configure(yscrollcommand=self.__vsb.set)
        self.__vsb.pack(side="right", fill="y")
        self.__canvas.pack(side="left", fill="both", expand=True)
        self.__canvas.create_window((4, 4), window=self.__frame, anchor="nw", tags="self.frame")
        self.__frame.bind("<Configure>", self.on_frame_configure)
        btn = tk.Button(self.__frame, text='update')
        btn.grid(row=1, column=1)
        self.__label_list_manager = LabelListManager(self.__frame, self.__data_source.get(), initial_row=2)
        btn.bind("<Button-1>", lambda e: self.update())
        self.update()

    def update(self):
        self.__data_source.update()
        self.__label_list_manager.update(self.__data_source.get())

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))


if __name__ == "__main__":
    d = DataSourceManager(order_by='date')
    d.register(Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET))
    d.register(Hatena(USER_NAME))
    #d.register(Dummy())
    root = tk.Tk()
    TkMyFav(root, d).pack(side="top", fill="both", expand=True)
    root.mainloop()
