# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-权限中心(BlueKing-IAM) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from django_filters import rest_framework as filters

from backend.apps.application.models import Application
from backend.common.filters import InitialFilterSet
from backend.common.time import get_period_start_end
from backend.util.time import string_to_datetime


class ApplicationFilter(InitialFilterSet):
    start_time = filters.CharFilter(method="start_time_filter", label="开始时间")
    end_time = filters.CharFilter(method="end_time_filter", label="结束时间")
    period = filters.NumberFilter(method="period_filter", label="区间")
    hidden = filters.BooleanFilter(method="hidden_filter", initial=True)
    source_system_id = filters.CharFilter()

    class Meta:
        model = Application
        fields = ["start_time", "end_time", "period", "hidden", "source_system_id"]

    def period_filter(self, queryset, name, value):
        start_time, end_time = get_period_start_end(int(value))
        return queryset.filter(created_time__range=(start_time, end_time))

    def end_time_filter(self, queryset, name, value):
        end_time = string_to_datetime(value)
        return queryset.filter(created_time__lte=end_time)

    def start_time_filter(self, queryset, name, value):
        start_time = string_to_datetime(value)
        return queryset.filter(created_time__gte=start_time)

    def hidden_filter(self, queryset, name, value):
        if value:
            return queryset.filter(hidden=False)
        return queryset
