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
# Generated by Django 2.2.24 on 2021-11-30 03:37

from django.db import migrations

from backend.api.constants import ALLOW_ANY


def init_allow_list(apps, schema_editor):
    """初始化授权API白名单"""
    ManagementAPIAllowListConfig = apps.get_model("management", "ManagementAPIAllowListConfig")

    # 查询已存在白名单，避免重复
    all_allow_list = ManagementAPIAllowListConfig.objects.all()
    allow_set = set([(a.system_id, a.api) for a in all_allow_list])

    # 白名单列表
    system_id_allow_apis = {
        "bk_nocode": [ALLOW_ANY],
    }

    # 组装成Model对象
    mgmt_api_allow_list_config = []
    for system_id, apis in system_id_allow_apis.items():
        for api in apis:
            # 已存在，则直接忽略
            if (system_id, api) in allow_set:
                continue
            mgmt_api_allow_list_config.append(ManagementAPIAllowListConfig(system_id=system_id, api=api))
    # 批量创建
    if len(mgmt_api_allow_list_config) != 0:
        ManagementAPIAllowListConfig.objects.bulk_create(mgmt_api_allow_list_config)


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0003_systemallowauthsystem"),
    ]

    operations = [migrations.RunPython(init_allow_list)]
