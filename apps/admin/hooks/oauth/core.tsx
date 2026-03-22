/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { KeyRound } from "lucide-react";
// types
import type {
  TCoreInstanceAuthenticationModeKeys,
  TGetBaseAuthenticationModeProps,
  TInstanceAuthenticationModes,
} from "@plane/types";

// Authentication methods
export const getCoreAuthenticationModesMap: (
  props: TGetBaseAuthenticationModeProps
) => Partial<Record<TCoreInstanceAuthenticationModeKeys, TInstanceAuthenticationModes>> = ({
  disabled: _disabled,
  updateConfig: _updateConfig,
  resolvedTheme: _resolvedTheme,
}) => ({
  zitadel: {
    key: "zitadel",
    name: "Zitadel OIDC",
    description:
      "Authentication is managed by Zitadel. Configure your Zitadel instance settings via environment variables.",
    icon: <KeyRound className="h-6 w-6 p-0.5 text-tertiary" />,
    config: (
      <div className="text-sm text-tertiary">
        Zitadel OIDC is configured via environment variables (ZITADEL_ISSUER_URL, ZITADEL_CLIENT_ID,
        ZITADEL_CLIENT_SECRET).
      </div>
    ),
    enabledConfigKey: "IS_ZITADEL_ENABLED",
  },
});
