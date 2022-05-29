import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import NProgress from "nprogress";
import { Amplify, Auth, Hub } from "aws-amplify";
import awsconfig from "../aws-exports";

Amplify.configure(awsconfig);

let user;
getUser().then((user: any) => {
  if (user) {
    console.log(user);
    router.push({ path: "/" });
  }
});

function getUser() {
  return Auth.currentAuthenticatedUser()
    .then((data: any) => {
      if (data && data.signInUserSession) {
        return data;
      }
    })
    .catch(() => {
      return null;
    });
}

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("~/views/login/index.vue"),
  },
  {
    path: "/",
    name: "Home",
    component: () => import("~/views/home/index.vue"),
    redirect: "/search",
    children: [
      {
        path: "/search",
        name: "Search",
        component: () => import("~/views/search/index.vue"),
      },
      {
        path: "/upload",
        name: "Upload",
        component: () => import("~/views/upload/index.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeResolve(async (to, from, next) => {
//   if (to.matched.some((record) => record.meta.requiresAuth)) {
//     user = await getUser();
//     if (!user) {
//       return next({
//         path: "/login",
//       });
//     }
//     return next();
//   }
//   return next();
// });

Hub.listen("auth", async (data: any) => {
  if (data.payload.event === "signOut") {
    user = null;
    router.push({ path: "/login" });
  } else if (data.payload.event === "signIn") {
    user = await getUser();
    sessionStorage.setItem("user", JSON.stringify(user));
    router.push({ path: "/" });
  }
});

router.beforeEach(async (to, from, next) => {
  const auth = sessionStorage.getItem("user");
  if (!NProgress.isStarted()) {
    NProgress.start();
  }
  if (!auth && to.name !== "Login") {
    Auth.signOut();
    next({ name: "Login" });
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  NProgress.done();
});

export default router;