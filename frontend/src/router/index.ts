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
            component: () =>
                import("../pages/customer/CustomerDashboard.vue"),
            meta: {
                requiresAuth: true,
                role: "CUSTOMER",
                title: "Customer Dashboard",
                description: "Manage your services and bookings.",
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
            component: () =>
                import("../pages/provider/ProviderDashboard.vue"),
            meta: {
                requiresAuth: true,
                role: "PROVIDER",
                title: "Provider Dashboard",
               description: "Manage your services, availability, and bookings.",
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
          component: () =>
            import("../pages/admin/AdminDashboard.vue"),
          meta: {
              requiresAuth: true,
              role: "ADMIN",
              title: "Admin Dashboard",
              description: "Manage ServiceHub users, providers, and activity.",
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

function getDashboardRoute(
  role: UserRole | null,
) {
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

  const requiresAuth =
    to.meta.requiresAuth === true;

  const requiresGuest =
    to.meta.requiresGuest === true;

  const requiredRole =
    to.meta.role as UserRole | undefined;

  if (
    requiresAuth &&
    !authStore.isAuthenticated
  ) {
    return { name: "login" };
  }

  if (
    requiresGuest &&
    authStore.isAuthenticated
  ) {
    return getDashboardRoute(
      authStore.role,
    );
  }

  if (
    requiresAuth &&
    requiredRole &&
    authStore.role !== requiredRole
  ) {
    return getDashboardRoute(
      authStore.role,
    );
  }

  return true;
});
export default router;