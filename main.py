class Row:
    def __init__(self, row_id, values, table=None, default_value=None):
        self.row_id = row_id
        self.values = values
        self.table = table
        self.column_ids = table.column_ids # add capability to have no row on its own.
        self.as_dict = dict(zip(self.column_ids, self.values))
        self.default_value = default_value

    # _update_value is needed so the Column class can update
    # this class without this class trying to update the Column
    # class when it gets updated
    def _update_value(self, column_id, new_value):
        self.as_dict[column_id] = new_value
        self.values = list(self.as_dict.values())

    def __getitem__(self, key):
        if key in self.column_ids:
            return self.as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.column_ids:
            self._update_value(key, value)
            self.table.columns[key]._update_value(self.row_id, value)
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return f"Row({self.values})"

class Column:
    def __init__(self, column_id, values, table, default_value=None):
        self.column_id = column_id
        self.values = values
        self.table = table
        self.row_ids = table.row_ids
        self.as_dict = dict(zip(self.row_ids, self.values))
        self.default_value = default_value

    def _update_value(self, row_id, new_value):
        self.as_dict[row_id] = new_value
        self.values = list(self.as_dict.values())

    def __getitem__(self, key):
        if key in self.row_ids:
            return self.as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.row_ids:
            self._update_value(key, value)
            self.table.rows[key]._update_value(self.column_id, value)
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return f"Column({self.values})"

    def __add__(self, other):
        if isinstance(other, Column):
            column_ids = [self.column_id, other.column_id]
            row_ids = self.row_ids
            for row_id in other.row_ids:
                if row_id not in self.row_ids:
                    row_ids.append(row_id)
            data = list()
            for row_id in row_ids:
                data.append([
                    self[row_id] if row_id in self.row_ids else self.default_value,
                    other[row_id] if row_id in other.row_ids else other.default_value
                ])
            return Table(column_ids, row_ids, data)
        elif isinstance(other, Table):
            




class Table:
    def __init__(self, column_ids: list, row_ids: list, data):
        if len(row_ids) != len(data):
            raise ValueError("row ids do not have the same length as data")
        elif len(column_ids) != len(data[0]):  # assume data has values in it
            raise ValueError("number of columns in data should match column ids")
        self.column_ids = column_ids
        self.row_ids = row_ids
        self.data = data

        self.columns = dict()
        for i, col_id in enumerate(column_ids):
            values = [row[i] for row in data]
            self.columns[col_id] = Column(col_id, values, self)
        self.rows = dict()
        for row_number, row_id in enumerate(row_ids):
            self.rows[row_id] = Row(row_id, data[row_number], self)

    def __getitem__(self, key):
        if key in self.column_ids:
            return self.columns[key]
        elif key in self.row_ids:
            return self.rows[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.column_ids:
            self.columns[key] = Column(key, value, self)
        elif key in self.row_ids:
            self.rows[key] = Row(key, value, self)
        else:
            raise KeyError(f"The key '{key}' does not exist")



def test():
    bc = ["Date", "1 Mo", "1.5 Mo", "2 Mo"]
    br = ["a", "b", "c"]
    bt = [[111, 222, 333, 444],
          [555, 666, 777, 888],
          [999, 1010, 1111, 1212]]
    t = Table(bc, br, bt)
    t["c"]["2 Mo"] = 199
    t["Date"]["a"] = 0
    print(t["c"])
    print(t["2 Mo"])
    for i in t["1.5 Mo"]:
        print(i)
    for i in t["1.5 Mo"]:
        print(i)
    print(t["a"])