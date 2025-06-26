# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云 - 权限中心 (BlueKing-IAM) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    初始化租户，当租户创建后，执行此命令来初始化租户的相关数据。
    $ python manage.py init_tenant --tenant_id=<tenant_id>
    """

    def add_arguments(self, parser):
        parser.add_argument("--tenant_id", type=str, help="Tenant ID", required=True)

    def handle(self, *args, **options):
        tenant_id = options["tenant_id"]
        # TODO: 初始化超级管理空间（需判断是否已经创建过了）
        # TODO：初始化”全租户“的系统管理员空间
        # TODO：同步用户？
        self.stdout.write(f"tenant({tenant_id}) initialized successfully")
