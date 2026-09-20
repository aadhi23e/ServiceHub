export type UserRole =
  | "CUSTOMER"
  | "PROVIDER"
  | "ADMIN";

export interface RouteMeta {
  requiresAuth?: boolean;
  requiresGuest?: boolean;
  role?: UserRole;
}