import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import { useAuthStore } from "../stores/auth";
import type { UserRole } from "../types/router";

const isDevelopment = import.meta.env.DEV;

const routes: RouteRecordRaw[] = [
  // ─────────────────────────────────────────────
  // Public routes
  // ─────────────────────────────────────────────

  {
    path: "/",
    component: () => import("../layouts/AuthLayout.vue"),
    children: [
      {
        path: "",
        redirect: "/login",
      },

      {
        path: "login",
        name: "login",
        component: () => import("../pages/auth/LoginPage.vue"),
        meta: {
          requiresGuest: true,
        },
      },

      {
        path: "register",
        name: "register",
        component: () => import("../pages/auth/RegisterPage.vue"),
        meta: {
          requiresGuest: true,
        },
      },
    ],
  },

  // ─────────────────────────────────────────────
  // Customer
  // ─────────────────────────────────────────────

  {
    path: "/customer",
    component: () => import("../layouts/DashboardLayout.vue"),
    meta: {
      requiresAuth: true,
      role: "CUSTOMER",
    },
    children: [
      {
        path: "",
        name: "customer",
        component: () => import("../pages/customer/CustomerDashboard.vue"),
        meta: {
          title: "Customer Dashboard",
          description: "Manage your services and bookings.",
        },
      },

      // Customer Bookings
      {
        path: "bookings",
        name: "customer-bookings",
        component: () => import("../pages/bookings/BookingsView.vue"),
        meta: {
          title: "My Bookings",
          description: "View and manage your bookings.",
        },
      },

      // Create Booking
      {
        path: "bookings/new",
        name: "customer-booking-create",
        component: () => import("../pages/bookings/BookingCreateView.vue"),
        meta: {
          roles: ["CUSTOMER"],
          title: "Create Booking",
          description: "Create a new service booking.",
        },
      },

      // Booking Detail
      {
        path: "bookings/:bookingId",
        name: "customer-booking-detail",
        component: () => import("../pages/bookings/BookingDetailView.vue"),
        meta: {
          title: "Booking Details",
        },
      },
    ],
  },

  // ─────────────────────────────────────────────
  // Provider
  // ─────────────────────────────────────────────

  {
    path: "/provider",
    component: () => import("../layouts/DashboardLayout.vue"),
    meta: {
      requiresAuth: true,
      role: "PROVIDER",
    },
    children: [
      {
        path: "",
        name: "provider",
        component: () => import("../pages/provider/ProviderDashboard.vue"),
        meta: {
          title: "Provider Dashboard",
          description: "Manage your services, availability, and bookings.",
        },
      },

      // Provider Bookings
      {
        path: "bookings",
        name: "provider-bookings",
        component: () => import("../pages/bookings/BookingsView.vue"),
        meta: {
          title: "Bookings",
          description: "Manage your customer bookings.",
        },
      },

      // Provider Booking Detail
      {
        path: "bookings/:bookingId",
        name: "provider-booking-detail",
        component: () => import("../pages/bookings/BookingDetailView.vue"),
        meta: {
          title: "Booking Details",
        },
      },
    ],
  },

  // ─────────────────────────────────────────────
  // Admin
  // ─────────────────────────────────────────────

  {
    path: "/admin",
    component: () => import("../layouts/DashboardLayout.vue"),
    meta: {
      requiresAuth: true,
      role: "ADMIN",
    },
    children: [
      {
        path: "",
        name: "admin",
        component: () => import("../pages/admin/AdminDashboard.vue"),
        meta: {
          title: "Admin Dashboard",
          description: "Manage ServiceHub users, providers, and activity.",
        },
      },

      // Admin Bookings
      {
        path: "bookings",
        name: "admin-bookings",
        component: () => import("../pages/bookings/BookingsView.vue"),
        meta: {
          title: "All Bookings",
          description: "Manage all ServiceHub bookings.",
        },
      },

      // Admin Booking Detail
      {
        path: "bookings/:bookingId",
        name: "admin-booking-detail",
        component: () => import("../pages/bookings/BookingDetailView.vue"),
        meta: {
          title: "Booking Details",
        },
      },
    ],
  },

  // ─────────────────────────────────────────────
  // Fallback
  // ─────────────────────────────────────────────

  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

function getDashboardRoute(role: UserRole | null) {
  switch (role) {
    case "CUSTOMER":
      return { name: "customer" };

    case "PROVIDER":
      return { name: "provider" };

    case "ADMIN":
      return { name: "admin" };

    default:
      return { name: "login" };
  }
}

// ─────────────────────────────────────────────
// Navigation guard
// ─────────────────────────────────────────────

router.beforeEach((to) => {
  const authStore = useAuthStore();

  const requiresAuth = to.meta.requiresAuth === true;

  const requiresGuest = to.meta.requiresGuest === true;

  const requiredRole = to.meta.role as UserRole | undefined;

  const requiredRoles = to.meta.roles as UserRole[] | undefined;

  if (requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" };
  }

  if (requiresGuest && authStore.isAuthenticated) {
    return getDashboardRoute(authStore.role);
  }

  if (requiresAuth && requiredRole && authStore.role !== requiredRole) {
    return getDashboardRoute(authStore.role);
  }

  if (
    requiresAuth &&
    requiredRoles &&
    !requiredRoles.includes(authStore.role as UserRole)
  ) {
    return getDashboardRoute(authStore.role);
  }

  return true;
});

export default router;