import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"

const routes: RouteRecordRaw[] = [
    { path: "/", meta: { title: "Home" }, component: () => import('@/views/HomeView.vue') },
    { path: "/new", meta: { title: "New" }, component: () => import('@/views/CreateView.vue') },
    { path: "/search", meta: { title: "Search" }, component: () => import('@/views/SearchView.vue') },
    { path: "/view/:id", meta: { title: "Note" }, component: () => import('@/views/DetailsView.vue'), props: true },
    { path: "/view/:id/edit", meta: { title: "Edit" }, component: () => import('@/views/EditView.vue'), props: true },
    { path: "/:pathMatch(.*)*", meta: { title: "Not Found" }, component: () => import('@/views/NotFound.vue') },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.afterEach((to) => {
    document.title = to.meta.title as string ? `${to.meta.title} | Dunote` : "Dunote"
})

export default router