/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { API_BASE_URL } from "@plane/constants";
// types
import type { ICsrfTokenData } from "@plane/types";
// services
import { APIService } from "../api.service";

/**
 * Service class for handling authentication-related operations.
 * Authentication is handled via Zitadel OIDC — this service
 * provides CSRF token management and sign-out functionality.
 * @extends {APIService}
 */
export class AuthService extends APIService {
  constructor(BASE_URL?: string) {
    super(BASE_URL || API_BASE_URL);
  }

  /**
   * Requests a CSRF token for form submission security
   * @returns {Promise<ICsrfTokenData>} Object containing the CSRF token
   */
  async requestCSRFToken(): Promise<ICsrfTokenData> {
    return this.get("/auth/get-csrf-token/", { validateStatus: null })
      .then((response) => response.data)
      .catch((error) => {
        throw error;
      });
  }

  /**
   * Performs user sign out by submitting a form with CSRF token
   * @param {string} baseUrl - Base URL for the sign-out endpoint
   */
  async signOut(baseUrl: string): Promise<any> {
    await this.requestCSRFToken().then((data) => {
      const csrfToken = data?.csrf_token;

      if (!csrfToken) throw Error("CSRF token not found");

      const form = document.createElement("form");
      const element1 = document.createElement("input");

      form.method = "POST";
      form.action = `${baseUrl}/auth/sign-out/`;

      element1.value = csrfToken;
      element1.name = "csrfmiddlewaretoken";
      element1.type = "hidden";
      form.appendChild(element1);

      document.body.appendChild(form);

      form.submit();
    });
  }
}
