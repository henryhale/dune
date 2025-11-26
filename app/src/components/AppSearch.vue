<script setup lang="ts">
import { InputGroup, InputGroupInput, InputGroupAddon } from "@/components/ui/input-group"
import { SearchIcon } from "lucide-vue-next";
import { onMounted } from "vue";
import { useUrlSearchParams } from '@vueuse/core';
import { useRouter } from "vue-router";
import { useTodoStore } from "@/stores/todo";

const router = useRouter()
const store = useTodoStore()
const params = useUrlSearchParams("history")

onMounted(() => {
    if (params.k !== store.searchQuery) {
        store.searchQuery = params.k as string
    }
})

const find = () => {
    router.push(`/search?k=${encodeURI(store.searchQuery)}`)
}
</script>

<template>
    <div>
        <InputGroup>
            <InputGroupInput @keyup.enter.prevent="find" v-model.trim="store.searchQuery" placeholder="Search..." />
            <InputGroupAddon>
                <SearchIcon />
            </InputGroupAddon>
            <InputGroupAddon v-if="router.currentRoute.value.path === '/search'" align="inline-end">
                {{ store.filteredTodos.length }} results
            </InputGroupAddon>
        </InputGroup>
    </div>
</template>