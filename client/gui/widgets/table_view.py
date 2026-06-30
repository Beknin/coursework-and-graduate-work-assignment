import tkinter as tk
from tkinter import ttk

class TableView(ttk.Frame):
    def __init__(self, parent, columns: list, column_names: dict = None):
        super().__init__(parent)
        self.columns = columns
        self.column_names = column_names or {col: col for col in columns}

        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(search_frame, text="🔍").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=self.column_names[col], command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=100, minwidth=50)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self._all_data = []
        self._sort_column = None
        self._sort_reverse = False

    def set_data(self, data: list[dict]):
        self._all_data = data
        self._refresh()

    def get_selected(self) -> dict | None:
        selection = self.tree.selection()
        if selection:
            return self._all_data[self.tree.index(selection[0])]
        return None

    def _on_search(self, *args):
        self._refresh()

    def _refresh(self):
        query = self.search_var.get().lower()
        filtered = [row for row in self._all_data
                    if any(query in str(row.get(col, "")).lower() for col in self.columns)]
        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            values = [str(row.get(col, "")) for col in self.columns]
            self.tree.insert("", "end", values=values)

    def _sort_by(self, col):
        if self._sort_column == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = col
            self._sort_reverse = False
        self._all_data.sort(key=lambda r: str(r.get(col, "")), reverse=self._sort_reverse)
        self._refresh()