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

import random

from django.core.management.base import BaseCommand

from backend.apps.organization.models import User
from backend.biz.role import RoleBiz
from backend.component import iam


class Command(BaseCommand):
    """
    授权超级管理员空间权限
    $ python manage.py grant_super_manager --tenant_id <tenant_id> --bk_username <bk_username>
    """

    def add_arguments(self, parser):
        parser.add_argument("--tenant_id", type=str, help="Tenant ID", required=True)
        parser.add_argument("--bk_username", type=str, help="BK Username", required=True)

    def handle(self, *args, **options):
        tenant_id = options["tenant_id"]
        bk_username = options["bk_username"]

        # 单一用户同步
        # FIXME(nan): 这里应该调用用户管理接口查询 bk_username 相关信息
        _, created = User.objects.get_or_create(
            username=bk_username,
            defaults={
                "id": random.randint(10**4, 10**8),
                "display_name": bk_username,
                "category_id": 0,
            },
        )
        # 后台创建用户
        if created:
            iam.create_subjects_by_auto_paging([{"type": "user", "id": bk_username, "name": bk_username}])

        # 授权超级管理员空间权限
        RoleBiz().add_super_manager_member(bk_username, True)

        self.stdout.write(f"grant super manager for {bk_username} in tenant {tenant_id} successfully")
