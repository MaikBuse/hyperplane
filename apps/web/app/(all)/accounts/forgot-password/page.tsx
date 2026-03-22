/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { redirect } from "react-router";

// Passwords are managed by Zitadel
export const clientLoader = () => {
  throw redirect("/");
};

export default function ForgotPasswordPage() {
  return null;
}
