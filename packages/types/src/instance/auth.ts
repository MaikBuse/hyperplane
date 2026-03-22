/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

export type TCoreInstanceAuthenticationModeKeys = "zitadel";

export type TInstanceAuthenticationModeKeys = TCoreInstanceAuthenticationModeKeys;

export type TInstanceAuthenticationModes = {
  key: TInstanceAuthenticationModeKeys;
  name: string;
  description: string;
  icon: React.ReactNode;
  config: React.ReactNode;
  enabledConfigKey: TInstanceAuthenticationMethodKeys;
  unavailable?: boolean;
};

export type TInstanceAuthenticationMethodKeys = "ENABLE_SIGNUP" | "IS_ZITADEL_ENABLED";

export type TInstanceZitadelAuthenticationConfigurationKeys =
  | "ZITADEL_ISSUER_URL"
  | "ZITADEL_CLIENT_ID"
  | "ZITADEL_CLIENT_SECRET";

export type TInstanceAuthenticationConfigurationKeys = TInstanceZitadelAuthenticationConfigurationKeys;

export type TInstanceAuthenticationKeys = TInstanceAuthenticationMethodKeys | TInstanceAuthenticationConfigurationKeys;

export type TGetBaseAuthenticationModeProps = {
  disabled: boolean;
  updateConfig: (key: TInstanceAuthenticationMethodKeys, value: string) => void;
  resolvedTheme: string | undefined;
};

export type TOAuthOption = {
  id: string;
  text: string;
  icon: React.ReactNode;
  onClick: () => void;
  enabled?: boolean;
};

export type TOAuthConfigs = {
  isOAuthEnabled: boolean;
  oAuthOptions: TOAuthOption[];
};

export type TCoreLoginMediums = "zitadel";
