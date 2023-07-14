import tkinter as tk
import json
from itertools import product

# 读取汉字拼音数据
with open('simplified_py2hz.json', 'r', encoding='utf-8') as f:
    py2hz = json.load(f)


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('拼音域名常用字工具')

        # 创建拼音输入框和汉字显示框
        self.pinyins = []
        self.hanzis = []
        for i in range(4):
            tk.Label(self.master, text='拼音%d:' % (i + 1), font=("微软雅黑", 12)).grid(row=i, column=0)
            pinyin_entry = tk.Entry(self.master)
            pinyin_entry.grid(row=i, column=1)
            pinyin_entry.bind('<Return>', lambda event, index=i: self.show_hanzis(event, index))
            self.pinyins.append(pinyin_entry)

            tk.Label(self.master, text='汉字%d:' % (i + 1), font=("微软雅黑", 12)).grid(row=i, column=2)
            hz_text = tk.Text(self.master, height=1, wrap='char', font=("微软雅黑", 12))
            hz_text.grid(row=i, column=3)
            self.hanzis.append(hz_text)

        # 创建汉字组合框和滚动条
        tk.Label(self.master, text='汉字组合:', font=("微软雅黑", 12)).grid(row=4, column=0)
        self.combination_text = tk.Text(self.master, height=10, wrap='word', font=("微软雅黑", 12))
        self.combination_text.grid(row=4, column=1, columnspan=3, sticky='we')
        self.scrollbar = tk.Scrollbar(self.master, orient='vertical', command=self.combination_text.yview)
        self.scrollbar.grid(row=4, column=4, sticky='ns')
        self.combination_text['yscrollcommand'] = self.scrollbar.set

        tk.Button(self.master, text='执行组合', command=self.show_combinations, font=("微软雅黑", 12), borderwidth=4).grid(row=5, column=1, columnspan=2)
        tk.Button(self.master, text='清空所有', command=self.clear_inputs, font=("微软雅黑", 12), borderwidth=4).grid(row=5, column=3, columnspan=2)

    def show_hanzis(self, event, index):
        pinyin = self.pinyins[index].get()
        if not pinyin:
            return
        hanzis = py2hz.get(pinyin, [])
        self.hanzis[index].delete('1.0', 'end')
        self.hanzis[index].insert('1.0', '、'.join(hanzis))
        self.hanzis[index]['height'] = len(hanzis) / 20 + 1

        if index < 3:
            self.pinyins[index + 1].focus_set()

    def show_combinations(self):
        pinyins = [pinyin.get() for pinyin in self.pinyins if pinyin.get()]
        if len(pinyins) < 2:
            return
        hanzis_list = [py2hz.get(pinyin, []) for pinyin in pinyins]
        combinations = [''.join(comb) for comb in product(*hanzis_list)]
        self.combination_text.delete('1.0', 'end')
        self.combination_text.insert('1.0', '、'.join(combinations))
        # self.combination_text['height'] = len(combinations) / 25 + 1

    def clear_inputs(self):
        for pinyin, hz in zip(self.pinyins, self.hanzis):
            pinyin.delete(0, 'end')
            hz.delete('1.0', 'end')
            hz['height'] = 1
        self.combination_text.delete('1.0', 'end')
        self.combination_text['height'] = 10


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
