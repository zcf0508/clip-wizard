import { createRouter, createWebHashHistory  } from "vue-router";

export const routes = [
  {
    path: "/",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        path: "/home",
        component: () => import("@/views/Home.vue"),
      },
      {
        path: "/about",
        component: () => import("@/views/About.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
