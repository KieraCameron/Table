class _Row:
    def __init__(self, row_id, data, column_ids=None, table=None, default_value=None):
        self.row_id = row_id
        self.data = data
        self.table = table
        if table is not None and column_ids is not None:
            raise Exception("column ids are ambiguous. Both column_ids and table parameters are assigned.")
        elif table is not None:
            self.column_ids = table.column_ids
        elif column_ids is not None:
            self.column_ids = column_ids
        else:
            self.column_ids = list(range(len(self.data)))
        self._as_dict = dict(zip(self.column_ids, self.data))
        self.default_value = default_value

    # _update_value is needed so the Column class can update
    # this class without this class trying to update the Column
    # class when it gets updated
    def _update_value(self, column_id, new_value):
        self[column_id] = new_value
        self.data = list(self._as_dict.values())

    def _get_column_index(self, column_id):
        """gets index of column, returns None if None"""
        if column_id in self.column_ids:
            return self.column_ids.index(column_id)
        elif column_id is None:
            return None
        else:
            raise KeyError(f"The key '{column_id}' does not exist")

    def get_slice_section(self, slice_obj):
        start_index = self._get_column_index(slice_obj.start)
        stop_index = self._get_column_index(slice_obj.stop)
        step = slice_obj.step
        if not isinstance(step, int) and step is not None:
            raise TypeError("step must be None or of type 'int'")
        return slice(start_index, stop_index, step)

    def __getitem__(self, key):
        if isinstance(key, slice):
            section = self.get_slice_section(key)
            column_ids = self.column_ids[section]
            data = self.data[section]
            return _Row(self.row_id, data, column_ids, None, self.default_value)
        elif key in self.column_ids:
            return self._as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            section = self.get_slice_section(key)
            if len(value) != (section.stop - section.start):
                raise KeyError("mismatching length between slice range and value")
            for column_id, v in zip(self.column_ids[section], value):
                self[column_id] = v
        if key in self.column_ids:
            self._update_value(key, value)
            if self.table is not None:
                self.table.columns[key]._update_value(self.row_id, value)
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"Row({self.data})"

    def _merge_column_ids(self, other):
        merged_column_ids = self.column_ids
        for column_id in other.column_ids:
            if column_id not in self.column_ids:
                merged_column_ids.append(column_id)
        return merged_column_ids

    def _merge_data(self, other, merged_column_ids):
        new_row = [self[column_id] if column_id in self.column_ids else self.default_value\
                        for column_id in merged_column_ids]
        other_data = other.data
        # continue here after capability of adding colums is created

    def __add__(self, other):
        if isinstance(other, _Row):
            pass

class _Column:
    def __init__(self, column_id, data, row_ids=None, table=None, default_value=None):
        self.column_id = column_id
        self.data = data
        if table is not None and row_ids is not None:
            raise Exception("row ids are ambiguous. Both row_ids and table parameters are assigned.")
        elif table is not None:
            self.row_ids = table.row_ids
        elif row_ids is not None:
            self.row_ids = row_ids
        else:
            self.row_ids = list(range(len(self.data)))
        self.table = table
        self._as_dict = dict(zip(self.row_ids, self.data))
        self.default_value = default_value

    def _update_value(self, row_id, new_value):
        self[row_id] = new_value
        self.data = list(self._as_dict.values())

    def _get_row_index(self, row_id):
        """gets index of row, returns None if None"""
        if row_id in self.row_ids:
            return self.row_ids.index(row_id)
        elif row_id is None:
            return None
        else:
            raise KeyError(f"The key '{row_id}' does not exist")

    def get_slice_section(self, slice_obj):
        start_index = self._get_row_index(slice_obj.start)
        stop_index = self._get_row_index(slice_obj.stop)
        step = slice_obj.step
        if not isinstance(step, int) and step is not None:
            raise TypeError("step must be None or of type 'int'")
        return slice(start_index, stop_index, step)

    def __getitem__(self, key):
        if isinstance(key, slice):
            section = self.get_slice_section(key)
            row_ids = self.row_ids[section]
            data = self.data[section]
            return _Column(self.column_id, data, row_ids, None, self.default_value)
        elif key in self.row_ids:
            return self._as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            section = self.get_slice_section(key)
            if len(value) != (section.stop - section.start):
                raise KeyError("mismatching length between slice range and value")
            for row_id, v in zip(self.row_ids[section], value):
                self[row_id] = v
        elif key in self.row_ids:
            self._update_value(key, value)
            if self.table is not None:
                self.table.rows[key]._update_value(self.column_id, value)
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"Column({self.data})"

    def _merge_row_ids(self, other):
        merged_row_ids = self.row_ids
        for row_id in other.row_ids:
            if row_id not in self.row_ids:
                merged_row_ids.append(row_id)
        return merged_row_ids

    def _merge_data(self, other, merged_row_ids):
        data = list()
        for row_id in merged_row_ids:
            data.append([
                self[row_id] if row_id in self.row_ids else self.default_value,
                other[row_id] if row_id in other.row_ids else other.default_value
            ])
        return data

    # add capability in Table to reposition columns
    def __add__(self, other):
        if isinstance(other, _Column):
            column_ids = [self.column_id, other.column_id]
            merged_row_ids = self._merge_row_ids(other)
            data = self._merge_data(other, merged_row_ids)
        elif isinstance(other, Table):
            column_ids = [self.column_id] + other.column_ids
            merged_row_ids = self._merge_row_ids(other)
            data = self._merge_data(other, merged_row_ids)
        else:
            raise TypeError(f"can not add types '_Column' and {type(other).__name__}")
        return Table(column_ids, merged_row_ids, data)

    def __radd__(self, other):
        return other + self



class Table:
    def __init__(self, column_ids: list, row_ids: list, data, default_value=None):
        if len(row_ids) != len(data):
            raise ValueError("row ids do not have the same length as data")
        elif len(column_ids) != len(data[0]):  # assume data has values in it
            raise ValueError("number of columns in data should match column ids")
        self.column_ids = column_ids
        self.row_ids = row_ids
        self.data = data # a 2D matrix
        self.default_value = default_value

        self.columns = dict()
        for i, col_id in enumerate(column_ids):
            values = [row[i] for row in data]
            self.columns[col_id] = _Column(col_id, values, self)
        self.rows = dict()
        for row_number, row_id in enumerate(row_ids):
            self.rows[row_id] = _Row(row_id, data[row_number], self)

    def get_slice_section(self, slice_obj):
        start_index = self._get_key_index(slice_obj.start)
        stop_index = self._get_key_index(slice_obj.stop)
        step = slice_obj.step
        if not isinstance(step, int) and step is not None:
            raise TypeError("step must be None or of type 'int'")
        return slice(start_index, stop_index, step)

    def _get_key_index(self, key):
        if key in self.column_ids:
            return self.column_ids.index(key)
        elif key in self.row_ids:
            return self.row_ids.index(key)
        elif key is None:
            return None
        else:
            raise KeyError(f"the key {key} does not exist")

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start in self.column_ids and key.stop in self.row_ids or \
                key.start in self.row_ids and key.stop in self.column_ids:
                raise KeyError("start and stop slices must be both row ids or column ids")
            section = self.get_slice_section(key)
            if key.start in self.column_ids or key.stop in self.column_ids:
                data = list()
                for row in self.data:
                    data.append(row[section])
                column_ids = self.column_ids[section]
                return Table(column_ids, self.row_ids, data, self.default_value)
            elif key.start in self.row_ids or key.stop in self.row_ids:
                data = self.data[section]
                row_ids = self.row_ids[section]
                return Table(self.column_ids, row_ids, data, self.default_value)
            elif isinstance(key.step, int):
                raise KeyError("step is defined without targetting rows or columns")
            elif key.start is None and key.stop is None and key.step is None:
                return Table(self.column_ids, self.row_ids, self.data, self.default_value)
            assert False, "slice start, stop, and step not accounted for"
        elif key in self.column_ids:
            return self.columns[key]
        elif key in self.row_ids:
            return self.rows[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.column_ids:
            self.columns[key] = _Column(key, value, table=self, default_value=self.default_value)
            index = self.column_ids.index(key)
            for row_number, row in enumerate(self.data):
                self.data[row_number][index] =
                #_Clumn values are lists, not lists of lists. im pretty sure i assumed the latter somewhere above.
        elif key in self.row_ids:
            self.rows[key] = _Row(key, value, table=self)
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def transpose(self):
        data = list()
        for column_number, column_id in enumerate(self.column_ids):
            data.append([])
            for row in self.data:
                data[column_number].append(row[column_number])
        return Table(self.row_ids, self.column_ids, data, self.default_value)

    def _split_row_ids(self, other):
        other_only_row_ids = list()
        matching_row_ids = list()
        for row_id in other.row_ids:
            if row_id in self.row_ids:
                matching_row_ids.append(row_id)
            else:
                other_only_row_ids.append(row_id)
        return other_only_row_ids, matching_row_ids

    def _has_conflicting_data(self, other, matching_column_ids, matching_row_ids):
        if matching_column_ids == [] or matching_row_ids == []:
            return False, None, None
        else:
            for row_id, column_id in zip(matching_row_ids, matching_column_ids):
                if self[row_id][column_id] != other[row_id][column_id]:
                    return True, row_id, column_id
            return False, None, None

    def _split_column_ids(self, other):
        other_only_column_ids = list()
        matching_column_ids = list()
        for column_id in other.column_ids:
            if column_id in self.column_ids:
                matching_column_ids.append(column_id)
            else:
                other_only_column_ids.append(column_id)
        return other_only_column_ids, matching_column_ids

    def _merge_data(self, other):
        other_only_column_ids, matching_column_ids = self._split_column_ids(other)
        other_only_row_ids, matching_row_ids = self._split_row_ids(other)
        has_conflicts, row_id, column_id = self._has_conflicting_data(other, matching_column_ids, matching_row_ids)
        if has_conflicts:
            raise ValueError(f"can not add tables with conflicting values at {row_id} and {column_id}")

        merged_data = self.data
        for row_id, column_id in zip(matching_row_ids, matching_column_ids):
            pass

    def __add__(self, other):
        if not (isinstance(other, Table) or isinstance(other, _Row) or isinstance(other, _Column)):
            raise TypeError(f"can not add types 'Table' and {type(other).__name__}")
        if self.default_value != other.default_value:
            raise ValueError("can not merge tables with mismatched default values")


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