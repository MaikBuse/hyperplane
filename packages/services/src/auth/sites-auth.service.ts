/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { API_BASE_URL } from "@plane/constants";
// services
import { APIService } from "../api.service";

/**
 * Service class for handling authentication-related operations for Plane space application.
 * Authentication is handled via Zitadel OIDC.
 * @extends {APIService}
 */
export class SitesAuthService extends APIService {
  constructor(BASE_URL?: string) {
    super(BASE_URL || API_BASE_URL);
  }
}
