"""
Module containing all sql objects
"""
from dataclasses import InitVar, dataclass
from typing import Any, Callable, ClassVar, Dict, List, Set

import ibis
from ibis.expr.types import AnyColumn, NumericScalar
from ibis.expr.window import Window as IbisWindow

from sql_to_ibis.sql.sql_clause_objects import (
    ColumnExpression,
    FrameExpression,
    OrderByExpression,
    PartitionByExpression,
)
from sql_to_ibis.sql.sql_value_objects import Table


class AliasRegistry:
    def __init__(self):
        self._registry = {}

    def add_to_registry(self, alias: str, table: Table):
        assert alias not in self._registry
        self._registry[alias] = table

    def get_registry_entry(self, item: str):
        return self._registry[item]

    def __contains__(self, item):
        return item in self._registry

    def __repr__(self):
        return f"Registry:\n{self._registry}"


class AmbiguousColumn:
    """
    Class for identifying ambiguous table names
    """

    def __init__(self, tables: Set[str]) -> None:
        assert tables != set()
        self._tables = tables

    def __repr__(self) -> str:
        return f"AmbiguousColumn({', '.join(self.tables)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AmbiguousColumn) and self.tables == other.tables

    def add_table(self, table):
        self._tables.add(table)

    def remove_table(self, table: str):
        if len(self._tables) <= 1:
            raise Exception("Ambiguous column table set cannot be empty!")
        self._tables.remove(table)

    @property
    def tables(self):
        return self._tables


@dataclass
class Window:
    window_part_list: InitVar[List[ColumnExpression]]
    aggregation: NumericScalar
    window_function_map: ClassVar[Dict[str, Callable]] = {
        "range": ibis.range_window,
        "rows": ibis.window,
    }

    def __post_init__(self, window_part_list):
        self.partition: List[AnyColumn] = [
            clause.column_value
            for clause in window_part_list
            if isinstance(clause, PartitionByExpression)
        ]
        self.order_by: List[AnyColumn] = [
            clause.column_value
            for clause in window_part_list
            if isinstance(clause, OrderByExpression)
        ]
        self.frame_expression: FrameExpression = self.__get_frame_expression(
            window_part_list
        )

    def __get_frame_expression(self, window_part_list: list) -> FrameExpression:
        filtered_expressions = [
            clause for clause in window_part_list if isinstance(clause, FrameExpression)
        ]
        if not filtered_expressions:
            return FrameExpression()
        return filtered_expressions[0]

    def apply_ibis_window_function(self) -> IbisWindow:
        return self.aggregation.over(
            self.window_function_map[self.frame_expression.frame_type](
                group_by=self.partition,
                order_by=self.order_by,
                preceding=self.frame_expression.preceding.extent,
                following=self.frame_expression.following.extent,
            )
        )