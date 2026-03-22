/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import type { TInstanceAuthenticationModes } from "@plane/types";
import { getCoreAuthenticationModesMap } from "./core";
import type { TGetAuthenticationModeProps } from "./types";

export const useAuthenticationModes = (props: TGetAuthenticationModeProps): TInstanceAuthenticationModes[] => {
  const authenticationModes = getCoreAuthenticationModesMap(props);

  return Object.values(authenticationModes).filter((v): v is TInstanceAuthenticationModes => v !== undefined);
};
