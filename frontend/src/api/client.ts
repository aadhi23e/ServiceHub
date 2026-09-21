import { useAuthStore } from "../stores/auth";
import { pinia } from "../app/pinia";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured.",
  );
}

export interface ApiValidationError {
  loc?: Array<string | number>;
  msg: string;
  type?: string;
}

export interface ApiErrorBody {
  detail?:
    | string
    | ApiValidationError[]
    | unknown;

  code?: string;
  message?: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string | null;
  readonly body: unknown;

  constructor(
    message: string,
    status: number,
    code: string | null = null,
    body: unknown = null,
  ) {
    super(message);

    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.body = body;
  }

  get isNetworkError(): boolean {
    return this.status === 0;
  }

  get isUnauthorized(): boolean {
    return this.status === 401;
  }

  get isForbidden(): boolean {
    return this.status === 403;
  }

  get isValidationError(): boolean {
    return this.status === 422;
  }

  get isConflict(): boolean {
    return this.status === 409;
  }

  get isServerError(): boolean {
    return this.status >= 500;
  }
}

export interface ApiRequestOptions
  extends RequestInit {
  skipAuth?: boolean;
}

/*
 * Only ONE refresh operation can run at a time.
 *
 * If five requests receive 401 at the same time,
 * requests 2-5 reuse this same Promise instead
 * of creating four additional refresh requests.
 */
let refreshPromise:
  | Promise<string | null>
  | null = null;

async function parseResponseBody(
  response: Response,
): Promise<unknown> {
  const contentType =
    response.headers.get("content-type");

  if (
    contentType?.includes("application/json")
  ) {
    try {
      return await response.json();
    } catch {
      return null;
    }
  }

  const text = await response.text();

  return text || null;
}

function extractApiErrorCode(
  body: unknown,
): string | null {
  if (
    body &&
    typeof body === "object" &&
    "code" in body
  ) {
    const code = (
      body as { code?: unknown }
    ).code;

    if (typeof code === "string") {
      return code;
    }
  }

  return null;
}

function extractApiErrorMessage(
  status: number,
  body: unknown,
): string {
  if (
    body &&
    typeof body === "object" &&
    "detail" in body
  ) {
    const detail = (
      body as ApiErrorBody
    ).detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return "Please check the information you entered.";
    }
  }

  if (
    body &&
    typeof body === "object" &&
    "message" in body
  ) {
    const message = (
      body as { message?: unknown }
    ).message;

    if (typeof message === "string") {
      return message;
    }
  }

  switch (status) {
    case 400:
      return "The request could not be processed.";

    case 401:
      return "Your session has expired. Please sign in again.";

    case 403:
      return "You do not have permission to perform this action.";

    case 404:
      return "The requested resource was not found.";

    case 409:
      return "This information already exists.";

    case 422:
      return "Please check the information you entered.";

    case 429:
      return "Too many requests. Please try again later.";

    default:
      if (status >= 500) {
        return "Something went wrong on the server.";
      }

      return "The request could not be completed.";
  }
}

/**
 * Refresh the access token.
 *
 * This function talks directly to /auth/refresh rather
 * than using apiRequest(), otherwise a 401 from the
 * refresh endpoint could recursively trigger another
 * refresh.
 */
async function refreshAccessToken(): Promise<string | null> {
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = (async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/refresh`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        },
      );

      const body =
        await parseResponseBody(response);

      if (!response.ok) {
        throw new ApiError(
          extractApiErrorMessage(
            response.status,
            body,
          ),
          response.status,
          extractApiErrorCode(body),
          body,
        );
      }

      if (
        !body ||
        typeof body !== "object" ||
        !("access_token" in body)
      ) {
        throw new ApiError(
          "The server returned an invalid authentication response.",
          500,
          "INVALID_AUTH_RESPONSE",
          body,
        );
      }

      const accessToken = (
        body as {
          access_token?: unknown;
        }
      ).access_token;

      if (
        typeof accessToken !== "string" ||
        accessToken.length === 0
      ) {
        throw new ApiError(
          "The server returned an invalid access token.",
          500,
          "INVALID_ACCESS_TOKEN",
          body,
        );
      }

      const authStore = useAuthStore(pinia);

      authStore.setAccessToken(
        accessToken,
      );

      return accessToken;
    } catch {
      const authStore = useAuthStore(pinia);

      authStore.clearSession();

      return null;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

async function redirectToLogin(): Promise<void> {
  /*
   * Dynamic import avoids creating a static module cycle:
   *
   * router -> auth store -> api -> router
   */
  const { default: router } =
    await import("../router");

  if (
    router.currentRoute.value.name !==
    "login"
  ) {
    await router.replace({
      name: "login",
    });
  }
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const {
    skipAuth = false,
    headers,
    ...requestInit
  } = options;

  const authStore = useAuthStore(pinia);

  /*
   * Keep a copy of the original request configuration.
   *
   * Request bodies such as JSON strings can be reused,
   * unlike a consumed Request object.
   */
  const requestHeaders = new Headers(
    headers,
  );

  if (
    requestInit.body &&
    !requestHeaders.has("Content-Type")
  ) {
    requestHeaders.set(
      "Content-Type",
      "application/json",
    );
  }

  async function executeRequest(
    token: string | null,
  ): Promise<Response> {
    const currentHeaders =
      new Headers(requestHeaders);

    if (
      !skipAuth &&
      token
    ) {
      currentHeaders.set(
        "Authorization",
        `Bearer ${token}`,
      );
    } else {
      currentHeaders.delete(
        "Authorization",
      );
    }

    return fetch(
      `${API_BASE_URL}${path}`,
      {
        ...requestInit,
        headers: currentHeaders,
        credentials: "include",
      },
    );
  }

  let response: Response;

  try {
    response = await executeRequest(
      authStore.accessToken,
    );
  } catch {
    throw new ApiError(
      "Unable to connect to ServiceHub. Please check your connection and try again.",
      0,
      "NETWORK_ERROR",
    );
  }

  /*
   * Only authenticated normal API requests should
   * trigger automatic refresh.
   *
   * Login/register/refresh/logout requests use skipAuth.
   */
  if (
    response.status === 401 &&
    !skipAuth
  ) {
    const newAccessToken =
      await refreshAccessToken();

    /*
     * Refresh token is invalid/expired/revoked.
     *
     * The user's authenticated session is over.
     */
    if (!newAccessToken) {
      await redirectToLogin();

      throw new ApiError(
        "Your session has expired. Please sign in again.",
        401,
        "SESSION_EXPIRED",
      );
    }

    /*
     * Retry the original request exactly once.
     */
    try {
      response = await executeRequest(
        newAccessToken,
      );
    } catch {
      throw new ApiError(
        "Unable to connect to ServiceHub. Please check your connection and try again.",
        0,
        "NETWORK_ERROR",
      );
    }
  }

  const body =
    await parseResponseBody(response);

  if (!response.ok) {
    throw new ApiError(
      extractApiErrorMessage(
        response.status,
        body,
      ),
      response.status,
      extractApiErrorCode(body),
      body,
    );
  }

  return body as T;
}