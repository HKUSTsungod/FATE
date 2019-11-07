#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from federatedml.feature.feature_selection.selection_params import SelectionParams
import random
import operator


class BaseFilterMethod(object):
    """
    Use for filter columns

    Attributes
    ----------
    cols: list of int
        Col index to do selection

    left_cols: dict,
        k is col_index, value is bool that indicate whether it is left or not.

    feature_values: dict
        k is col_name, v is the value that used to judge whether left or not.
    """

    def __init__(self, filter_param):
        self.selection_param = SelectionParams()
        self._parse_filter_param(filter_param)

    @property
    def feature_values(self):
        return self.selection_param.feature_values

    def fit(self, data_instances):
        """
        Filter data_instances for the specified columns

        Parameters
        ----------
        data_instances : DTable,
            Input data

        Returns
        -------
        A list of index of columns left.

        """
        pass

    def _parse_filter_param(self, filter_param):
        raise NotImplementedError("Should not call this function directly")

    def set_selection_param(self, selection_param):
        self.selection_param = selection_param

    def _keep_one_feature(self, pick_high=True):
        """
        Make sure at least one feature can be left after filtering.

        Parameters
        ----------
        pick_high: bool
            Set when none of value left, choose the highest one or lowest one. True means highest one while
            False means lowest one.
        """
        if len(self.selection_param.left_col_indexes) > 0:
            return

        # random pick one
        if len(self.feature_values) == 0:
            left_col_name = random.choice(self.selection_param.select_col_names)
        else:
            result = sorted(self.feature_values.items(), key=operator.itemgetter(1), reverse=pick_high)
            left_col_name = result[0][0]
        self.selection_param.add_left_col_name(left_col_name)
