# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from .common import CSRFTokenEndpoint

from .app.zitadel import ZitadelOIDCInitiateEndpoint, ZitadelOIDCCallbackEndpoint
from .app.signout import SignOutAuthEndpoint

from .space.zitadel import ZitadelOIDCInitiateSpaceEndpoint, ZitadelOIDCCallbackSpaceEndpoint
from .space.signout import SignOutAuthSpaceEndpoint
