import { useAuthStore } from "../stores/auth";
import { pinia } from "../app/pinia";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

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
      return "Your email or password is incorrect.";

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

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const {
    skipAuth = false,
    headers,
    ...requestInit
  } = options;

  const requestHeaders = new Headers(headers);

  if (
    requestInit.body &&
    !requestHeaders.has("Content-Type")
  ) {
    requestHeaders.set(
      "Content-Type",
      "application/json",
    );
  }

  const authStore = useAuthStore(pinia);

  if (
    !skipAuth &&
    authStore.accessToken
  ) {
    requestHeaders.set(
      "Authorization",
      `Bearer ${authStore.accessToken}`,
    );
  }

  let response: Response;

  try {
    response = await fetch(
      `${API_BASE_URL}${path}`,
      {
        ...requestInit,
        headers: requestHeaders,

        // Required for the HttpOnly refresh cookie.
        credentials: "include",
      },
    );
  } catch {
    throw new ApiError(
      "Unable to connect to ServiceHub. Please check your connection and try again.",
      0,
      "NETWORK_ERROR",
    );
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