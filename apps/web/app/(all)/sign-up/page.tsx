/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { redirect } from "next/navigation";

// Sign-up is handled by Zitadel — redirect to main page
export default function SignUpPage() {
  redirect("/");
}
