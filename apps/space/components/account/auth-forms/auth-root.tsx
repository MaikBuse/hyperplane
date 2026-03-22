/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect, useState } from "react";
import { observer } from "mobx-react";
import { useSearchParams } from "next/navigation";
// plane imports
import { API_BASE_URL } from "@plane/constants";
import { Button } from "@plane/ui";
// helpers
import type { TAuthErrorInfo } from "@/helpers/authentication.helper";
import { EErrorAlertType, authErrorHandler, EAuthenticationErrorCodes } from "@/helpers/authentication.helper";
// local imports
import { AuthBanner } from "./auth-banner";
import { AuthHeader } from "./auth-header";

export const AuthRoot = observer(function AuthRoot() {
  const searchParams = useSearchParams();
  const error_code = searchParams.get("error_code") || undefined;
  const nextPath = searchParams.get("next_path") || undefined;
  const [errorInfo, setErrorInfo] = useState<TAuthErrorInfo | undefined>(undefined);

  useEffect(() => {
    if (error_code) {
      const errorhandler = authErrorHandler(error_code?.toString() as EAuthenticationErrorCodes);
      if (errorhandler) {
        setErrorInfo(errorhandler);
      }
    }
  }, [error_code]);

  const handleSignIn = () => {
    const url = `${API_BASE_URL}/auth/spaces/zitadel/${nextPath ? `?next_path=${nextPath}` : ""}`;
    window.location.assign(url);
  };

  return (
    <div className="mt-10 flex w-full flex-grow flex-col items-center justify-center py-6">
      <div className="relative flex w-full max-w-[22.5rem] flex-col gap-6">
        {errorInfo && errorInfo?.type === EErrorAlertType.BANNER_ALERT && (
          <AuthBanner bannerData={errorInfo} handleBannerData={(value) => setErrorInfo(value)} />
        )}
        <AuthHeader />
        <Button size="xl" className="w-full" onClick={handleSignIn}>
          Sign in
        </Button>
      </div>
    </div>
  );
});
